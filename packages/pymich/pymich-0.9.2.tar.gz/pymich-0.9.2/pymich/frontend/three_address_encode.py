import ast
from typing import List, Tuple, Callable
from pymich.utils.compiler_stdlib import StdLib


class Helpers:
    """Some helpers to manipulate ASTs"""

    def __init__(self, tmp_var_prefix):
        self.counter = -1
        self.prefix = tmp_var_prefix
        self.std_lib = StdLib()

    def make_tmp_var_name(self, counter: int) -> str:
        return self.prefix + str(counter)

    def get_tmp_var_name(self) -> str:
        self.counter += 1
        return self.make_tmp_var_name(self.counter)

    def refactor_into_variable(self, node: ast.stmt) -> Tuple[ast.Assign, ast.Name, str]:
        tmp_var_name = self.get_tmp_var_name()
        assign_ast = ast.Assign(
            targets=[ast.Name(id=tmp_var_name, ctx=ast.Store())],
            value=node,
        )
        fetch_ast = ast.Name(id=tmp_var_name, ctx=ast.Load())
        return assign_ast, fetch_ast, tmp_var_name

    def is_base_type(self, node: ast.stmt) -> bool:
        if isinstance(node, (ast.Name, ast.Constant)):
            return True
        if isinstance(node, ast.Call):
            is_std_lib_constructor = (
                isinstance(node.func, ast.Name)
                and node.func.id in self.std_lib.constants_mapping
                and node.func.id != "Bytes"
            )
            if is_std_lib_constructor:
                return True
        if isinstance(node, ast.Subscript):
            is_std_lib_type_constructor = (
                isinstance(node.value, ast.Name)
                and node.value.id in self.std_lib.constants_mapping
            )
            if is_std_lib_type_constructor:
                return True
        # handle `-1`
        if (
                isinstance(node, ast.UnaryOp)
                and isinstance(node.op, ast.USub)
                and isinstance(node.operand, ast.Constant)
            ):
            return True

        return False

    def assign_last_statement(self, stmts: List[ast.stmt]):
        """
        takes a list of statements, assigns its last statement to a new temp
        variable, and return an AST node to retrieve that variable
        """
        if len(stmts):
            assign_ast, fetch_ast, _ = self.refactor_into_variable(stmts[-1])
            stmts[-1] = assign_ast
            return fetch_ast


def get_empty_list(x: ast.stmt) -> List[ast.stmt]:
    return []


class ThreeAddressCodePass1:
    """Three address code assignment LHS"""
    def __init__(self, helpers: Helpers):
        self.helpers = helpers

    def _get_set_nested_expr_spec(self, node, spec = None):
        if spec is None:
            spec = []

        def var_spec(var_name):
            return {
                "type": "FETCH",
                "value": var_name.id,
                "lineno": var_name.lineno
            }

        def attr_spec(attr_name, lineno):
            return {
                "type": "ATTR",
                "value": {
                    "key": attr_name
                },
                "lineno": lineno
            }

        def subscript_spec(subscript_ast: ast.expr):
            return {
                "type": "SUBSCRIPT",
                "value": subscript_ast,
                "lineno": subscript_ast.lineno
            }

        if type(node) == ast.Name:
            spec.append(var_spec(node))
        elif type(node) == ast.Attribute:
            spec += self._get_set_nested_expr_spec(node.value)
            record_key = node.attr
            spec.append(attr_spec(record_key, node.lineno))
        elif type(node) == ast.Subscript:
            spec += self._get_set_nested_expr_spec(node.value)
            spec.append(subscript_spec(node.slice))

        return spec

    def compile_assign(self, node: ast.Assign) -> List[ast.stmt]:
        if not isinstance(node.targets[0], (ast.Attribute, ast.Subscript)):
            return [node]

        spec = self._get_set_nested_expr_spec(node.targets[0])

        # do not rewrite un-nested record/subscript assignments
        if len(spec) <= 2:
            return [node]

        code = []
        # decompose forward
        if spec[1]["type"] == "ATTR":
            root = ast.Attribute(
                value=ast.Name(id=spec[0]["value"], ctx=ast.Load()),
                attr=spec[1]["value"]["key"],
                ctx=ast.Load(),
            )
        else:
            root = ast.Subscript(
                value=ast.Name(id=spec[0]["value"], ctx=ast.Load()),
                slice=spec[1]["value"],
                ctx=ast.Load(),
            )
        code.append(root)
        fetch_var = self.helpers.assign_last_statement(code)
        for i, spec_element in enumerate(spec[2:-1]):
            if spec_element["type"] == "ATTR":
                attribute = ast.Attribute(
                    value=fetch_var,
                    attr=spec_element["value"]["key"],
                    ctx=ast.Load(),

                )
                code.append(attribute)
                fetch_var = self.helpers.assign_last_statement(code)
            elif spec_element["type"] == "SUBSCRIPT":
                subscript = ast.Subscript(
                    value=fetch_var,
                    slice=spec_element["value"],
                    ctx=ast.Load(),
                )
                code.append(subscript)
                fetch_var = self.helpers.assign_last_statement(code)

        # assign value
        if spec[-1]["type"] == "ATTR":
            target = ast.Attribute(
                value=fetch_var,
                attr=spec[-1]["value"]["key"],
                ctx=ast.Store(),
            )
        else:
            target = ast.Subscript(
                value=fetch_var,
                slice=spec[-1]["value"],
                ctx=ast.Store(),
            )
        value_assign = ast.Assign(
            targets=[target],
            value=node.value
        )
        code.append(value_assign)

        # decompose backwards
        sub_spec = spec[2:-1]
        last_counter = self.helpers.counter
        counter = last_counter
        for i, spec_element in enumerate(reversed(sub_spec)):
            counter = last_counter - i - 1
            tmp_var_name_assign = self.helpers.make_tmp_var_name(counter)
            tmp_var_name_value = self.helpers.make_tmp_var_name(counter + 1)
            if spec_element["type"] == "ATTR":
                target = ast.Attribute(
                    value=ast.Name(tmp_var_name_assign, ctx=ast.Load()),
                    attr=spec_element["value"]["key"],
                    ctx=ast.Store(),
                )
                assign_ast = ast.Assign(
                    targets=[target],
                    value=ast.Name(tmp_var_name_value, ctx=ast.Load()),
                )
                code.append(assign_ast)
            elif spec_element["type"] == "SUBSCRIPT":
                target= ast.Subscript(
                    value=ast.Name(tmp_var_name_assign, ctx=ast.Load()),
                    slice=spec_element["value"],
                )
                assign_ast = ast.Assign(
                    targets=[target],
                    value=ast.Name(tmp_var_name_value, ctx=ast.Load()),
                )
                code.append(assign_ast)

        # assign back to original record
        if spec[1]["type"] == "ATTR":
            target = ast.Attribute(
                value=ast.Name(id=spec[0]["value"], ctx=ast.Load()),
                attr=spec[1]["value"]["key"],
                ctx=ast.Load(),
            )
        else:
            target = ast.Subscript(
                value=ast.Name(id=spec[0]["value"], ctx=ast.Load()),
                slice=spec[1]["value"],
            )
        tmp_var_name = self.helpers.make_tmp_var_name(counter)
        assign = ast.Assign(
            targets=[target],
            value=ast.Name(tmp_var_name, ctx=ast.Load())
        )
        code.append(assign)

        return code

    def compile_function_def(self, node: ast.FunctionDef) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return [node]

    def compile_class_def(self, node: ast.Module) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return [node]

    def compile_if(self, node: ast.Module) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        new_orelse = []
        for stmt in node.orelse:
            new_orelse += self.compile(stmt)

        node.orelse = new_orelse

        return [node]

    def compile_for(self, node: ast.For) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return [node]

    def compile_module(self, module: ast.Module) -> ast.Module:
        new_body = []

        for stmt in module.body:
            new_body += self.compile(stmt)

        module.body = new_body

        return module

    def compile(
        self,
        stmt: ast.stmt,
    ) -> List[ast.stmt]:
        if isinstance(stmt, ast.Assign):
            return self.compile_assign(stmt)
        elif isinstance(stmt, ast.FunctionDef):
            return self.compile_function_def(stmt)
        elif isinstance(stmt, ast.ClassDef):
            return self.compile_class_def(stmt)
        elif isinstance(stmt, ast.If):
            return self.compile_if(stmt)
        elif isinstance(stmt, ast.For):
            return self.compile_for(stmt)

        return [stmt]


class ThreeAddressCodePass2:
    """Three address code everything else"""
    def __init__(self, helpers: Helpers):
        self.helpers = helpers

    def compile_subscript(self, subscript: ast.Subscript) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(subscript.value):
            code += self.compile(subscript.value)
            fetch_ast = self.helpers.assign_last_statement(code)
            subscript.value = fetch_ast

        if not self.helpers.is_base_type(subscript.slice):
            code += self.compile(subscript.slice)
            fetch_ast = self.helpers.assign_last_statement(code)
            subscript.slice = fetch_ast

        return code + [subscript]

    def compile_call(self, call: ast.Call) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(call.func):
            code += self.compile(call.func)
            fetch_ast = self.helpers.assign_last_statement(code)
            call.func = fetch_ast

        for i, arg_ast in enumerate(call.args):
            if not self.helpers.is_base_type(arg_ast):
                code += self.compile(arg_ast)
                fetch_ast = self.helpers.assign_last_statement(code)
                call.args[i] = fetch_ast

        code.append(call)

        return code

    def compile_expression(self, node: ast.Expr) -> List[ast.stmt]:
        code = self.compile(node.value)
        code[-1] = ast.Expr(value=code[-1])
        return code

    def compile_assign(self, assign: ast.Assign) -> List[ast.stmt]:
        code = []

        value_code = self.compile(assign.value)
        if value_code != [assign.value]:
            assign.value = value_code[-1]
            code += value_code[:-1]

        targets_code = self.compile(assign.targets[0])
        if targets_code != assign.targets:
            assign.targets = [targets_code[-1]]
            code += targets_code[:-1]

        if code:
            code.append(assign)
        else:
            code = [assign]

        return code

    def compile_boolop(self, node: ast.BoolOp) -> List[ast.stmt]:
        code = []

        for i, value in enumerate(node.values):
            if not self.helpers.is_base_type(node.values):
                values_code = self.compile(value)
                fetch_ast = self.helpers.assign_last_statement(values_code)
                code += values_code
                node.values[i] = fetch_ast

        return code + [node]

    def compile_compare(self, node: ast.Compare) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(node.left):
            left_code = self.compile(node.left)
            fetch_ast = self.helpers.assign_last_statement(left_code)
            code += left_code
            node.left = fetch_ast

        for i, (_, comparator) in enumerate(zip(node.ops, node.comparators)):
            if not self.helpers.is_base_type(comparator):
                comparators_code = self.compile(comparator)
                fetch_ast = self.helpers.assign_last_statement(comparators_code)
                code += comparators_code
                node.comparators[i] = fetch_ast

        return code + [node]

    def compile_binop(self, node: ast.BinOp) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(node.left):
            left_code = self.compile(node.left)
            fetch_ast = self.helpers.assign_last_statement(left_code)
            code += left_code
            node.left = fetch_ast

        if not self.helpers.is_base_type(node.right):
            right_code = self.compile(node.right)
            fetch_ast = self.helpers.assign_last_statement(right_code)
            code += right_code
            node.right = fetch_ast

        return code + [node]

    def compile_unaryop(self, node: ast.BinOp) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(node.operand):
            operand_code = self.compile(node.operand)
            fetch_ast = self.helpers.assign_last_statement(operand_code)
            code += operand_code
            node.operand = fetch_ast

        return code + [node]

    def compile_function_def(self, node: ast.FunctionDef) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return [node]

    def compile_return(self, node: ast.Return) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(node.value):
            code += self.compile(node.value)
            fetch_ast = self.helpers.assign_last_statement(code)
            node.value = fetch_ast

        return code + [node]

    def compile_attribute(self, node: ast.Attribute) -> List[ast.stmt]:
        code = []

        if not self.helpers.is_base_type(node.value):
            code += self.compile(node.value)
            fetch_ast = self.helpers.assign_last_statement(code)
            node.value = fetch_ast

        return code + [node]

    def compile_class_def(self, node: ast.Module) -> List[ast.stmt]:
        new_body = []

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return [node]

    def compile_if(self, node: ast.Module) -> List[ast.stmt]:
        code = []
        new_body = []

        if not self.helpers.is_base_type(node.test):
            code += self.compile(node.test)
            fetch_ast = self.helpers.assign_last_statement(code)
            node.test = fetch_ast

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        new_orelse = []
        for stmt in node.orelse:
            new_orelse += self.compile(stmt)

        node.orelse = new_orelse

        return code + [node]

    def compile_for(self, node: ast.For) -> List[ast.stmt]:
        code = []
        new_body = []

        if not self.helpers.is_base_type(node.iter):
            code += self.compile(node.iter)
            fetch_ast = self.helpers.assign_last_statement(code)
            node.iter = fetch_ast

        for stmt in node.body:
            new_body += self.compile(stmt)

        node.body = new_body

        return code + [node]

    def compile_module(self, module: ast.Module) -> ast.Module:
        new_body = []

        for stmt in module.body:
            new_body += self.compile(stmt)

        module.body = new_body

        return module

    def compile(
        self,
        stmt: ast.stmt,
    ) -> List[ast.stmt]:
        if isinstance(stmt, ast.Expr):
            return self.compile_expression(stmt)
        elif isinstance(stmt, ast.UnaryOp):
            return self.compile_unaryop(stmt)
        elif isinstance(stmt, ast.BinOp):
            return self.compile_binop(stmt)
        elif isinstance(stmt, ast.BoolOp):
            return self.compile_boolop(stmt)
        elif isinstance(stmt, ast.Assign):
            return self.compile_assign(stmt)
        elif isinstance(stmt, ast.Subscript):
            return self.compile_subscript(stmt)
        elif isinstance(stmt, ast.Call):
            return self.compile_call(stmt)
        elif isinstance(stmt, ast.Attribute):
            return self.compile_attribute(stmt)
        elif isinstance(stmt, ast.FunctionDef):
            return self.compile_function_def(stmt)
        elif isinstance(stmt, ast.Return):
            return self.compile_return(stmt)
        elif isinstance(stmt, ast.ClassDef):
            return self.compile_class_def(stmt)
        elif isinstance(stmt, ast.If):
            return self.compile_if(stmt)
        elif isinstance(stmt, ast.For):
            return self.compile_for(stmt)
        elif isinstance(stmt, ast.Compare):
            return self.compile_compare(stmt)

        return [stmt]


class ThreeAddressEncode:
    def __init__(self, tmp_var_prefix = "tmp_var_"):
        self.helpers = Helpers(tmp_var_prefix)
        self.tac_pass_1 = ThreeAddressCodePass1(self.helpers)
        self.tac_pass_2 = ThreeAddressCodePass2(self.helpers)

    def compile_module(self, module: ast.Module) -> ast.Module:
        passes = [
            self.tac_pass_1.compile_module,
            self.tac_pass_2.compile_module,
        ]
        for compiler_pass in passes:
            module = compiler_pass(module)

        module = ast.fix_missing_locations(module)
        return module

    def visit(self, module: ast.Module) -> ast.Module:
        return self.compile_module(module)
