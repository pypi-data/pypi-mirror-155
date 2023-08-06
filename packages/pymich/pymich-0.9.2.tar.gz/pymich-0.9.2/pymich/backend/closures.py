import ast
from typing import Tuple, Union
from pymich.utils.environment import Env
import pymich.utils.exceptions as E
from pymich.middle_end.ir.instr_types import Record


class ClosureEnv:
    def __init__(self, parent_env: Env):
        self.closure = []
        self.parent_env = parent_env
        self.function_env = Env({}, 0, {}, {})

    def reset(self):
        self.closure = []

    def add_to_closure(self, var_name: str):
        if var_name not in self.closure:
            self.closure.append(var_name)

    def is_in_closure(self, var_name: str) -> bool:
        return self.parent_env.is_var_defined(var_name) and not self.function_env.is_var_defined(var_name)



class ClosureAnalyzer:
    def __init__(self):
        pass

    def get_closure(self, stmt_ast: ast.stmt, e: Env):
        return self.check_closure(stmt_ast, ClosureEnv(e))

    def get_closure_type(self, stmt_ast: ast.stmt, e: Env):
        c = self.check_closure(stmt_ast, ClosureEnv(e))
        if len(c.closure) == 1:
            return c.parent_env.types[c.closure[0]]
        else:
            return Record(
                name="closure_wrapper",
                attribute_names=c.closure,
                attribute_types=[c.parent_env.types[var_name] for var_name in c.closure],
            )

    def check_return(self, return_ast: ast.Return, c: ClosureEnv) -> ClosureEnv:
        if return_ast.value:
            return self.check_closure(return_ast.value, c)
        else:
            return c

    def check_name(self, name_ast: ast.Name, c: ClosureEnv) -> ClosureEnv:
        var_name = name_ast.id
        if c.is_in_closure(var_name):
            c.add_to_closure(var_name)

        return c

    def check_binop(self, binop_ast: ast.BinOp, c: ClosureEnv) -> ClosureEnv:
        c = self.check_closure(binop_ast.left, c)
        c = self.check_closure(binop_ast.right, c)
        return c

    def check_expr(self, expr_ast: ast.Expr, c: ClosureEnv) -> ClosureEnv:
        return self.check_closure(expr_ast.value, c)

    def check_assign(self, assign_ast: ast.Assign, c: ClosureEnv) -> ClosureEnv:
        if len(assign_ast.targets) != 1:
            raise E.CompilerException("Only assignment with 1 target are supported", f.lineno)

        c = self.check_closure(assign_ast.value, c)

        if isinstance(assign_ast.targets[0], ast.Name):
            c.function_env.add_var(assign_ast.targets[0].id, 0)

        return c

    def check_call(self, call_ast: ast.Expr, c: ClosureEnv) -> ClosureEnv:
        c = self.check_closure(call_ast.func, c)
        for arg_ast in call_ast.args:
            c = self.check_closure(arg_ast, c)

        return c

    def check_attribute(self, attribute_ast: ast.Expr, c: ClosureEnv) -> ClosureEnv:
        return self.check_closure(attribute_ast.value, c)

    def check_subscript(self, subscript_ast: ast.Subscript, c: ClosureEnv) -> ClosureEnv:
        return self.check_closure(subscript_ast.value, c)

    def check_if(self, if_ast: ast.If, c: ClosureEnv) -> ClosureEnv:
        c = self.check_closure(if_ast.test, c)

        for stmt in if_ast.body:
            c = self.check_closure(stmt, c)

        for stmt in if_ast.orelse:
            c = self.check_closure(stmt, c)

        return c

    def check_constant(self, constant_ast: ast.Constant, c: ClosureEnv) -> ClosureEnv:
        return c

    def check_unary_op(self, unary_op_ast: ast.UnaryOp, c: ClosureEnv) -> ClosureEnv:
        return self.check_closure(unary_op_ast.operand, c)

    def check_compare(self, compare_ast: ast.Compare, c: ClosureEnv) -> ClosureEnv:
        c = self.check_closure(compare_ast.left, c)

        for comparator in compare_ast.comparators:
            c = self.check_closure(comparator, c)

        return c

    def check_for(self, for_ast: ast.For, c: ClosureEnv) -> ClosureEnv:
        c = self.check_closure(for_ast.target, c)

        c = self.check_closure(for_ast.iter, c)

        for stmt in for_ast.body:
            c = self.check_closure(stmt, c)

        for stmt in for_ast.orelse:
            c = self.check_closure(stmt, c)

        return c

    def check_tuple(self, tuple_ast: ast.Expr, c: ClosureEnv) -> ClosureEnv:
        for el in tuple_ast.elts:
            c = self.check_closure(el, c)

        return c

    def check_function_def(self, function_def_ast: ast.FunctionDef, c: ClosureEnv) -> ClosureEnv:
        for arg in function_def_ast.args.args:
            c.function_env.add_var(arg.arg, 0)

        for stmt in function_def_ast.body:
            c = self.check_closure(stmt, c)

        return c

    def check_module(self, module_ast: ast.Module, c: ClosureEnv) -> ClosureEnv:
        for stmt in module_ast.body:
            c = self.check_closure(stmt, c)
        return c

    def check_raise(self, raise_ast: ast.Raise, c: ClosureEnv) -> ClosureEnv:
        return c

    def check_list(self, list_ast: ast.List, c: ClosureEnv) -> ClosureEnv:
        for el in list_ast.elts:
            c = self.check_closure(el, c)
        return c

    def check_template(self, _ast: ast.Expr, c: ClosureEnv) -> ClosureEnv:
        return c

    def check_closure(self, node_ast: Union[ast.expr, ast.stmt], c: ClosureEnv) -> ClosureEnv:
        if isinstance(node_ast, ast.Return):
            c = self.check_return(node_ast, c)
        elif isinstance(node_ast, ast.Name):
            c = self.check_name(node_ast, c)
        elif isinstance(node_ast, ast.BinOp):
            c = self.check_binop(node_ast, c)
        elif isinstance(node_ast, ast.Expr):
            c = self.check_expr(node_ast, c)
        elif isinstance(node_ast, ast.Assign):
            c = self.check_assign(node_ast, c)
        elif isinstance(node_ast, ast.Call):
            c = self.check_call(node_ast, c)
        elif isinstance(node_ast, ast.Attribute):
            c = self.check_attribute(node_ast, c)
        elif isinstance(node_ast, ast.Subscript):
            c = self.check_subscript(node_ast, c)
        elif isinstance(node_ast, ast.If):
            c = self.check_if(node_ast, c)
        elif isinstance(node_ast, ast.Constant):
            c = self.check_constant(node_ast, c)
        elif isinstance(node_ast, ast.UnaryOp):
            c = self.check_unary_op(node_ast, c)
        elif isinstance(node_ast, ast.Compare):
            c = self.check_compare(node_ast, c)
        elif isinstance(node_ast, ast.For):
            c = self.check_for(node_ast, c)
        elif isinstance(node_ast, ast.Tuple):
            c = self.check_tuple(node_ast, c)
        elif isinstance(node_ast, ast.FunctionDef):
            c = self.check_function_def(node_ast, c)
        elif isinstance(node_ast, ast.Module):
            c = self.check_module(node_ast, c)
        elif isinstance(node_ast, ast.Raise):
            c = self.check_raise(node_ast, c)
        elif isinstance(node_ast, ast.List):
            c = self.check_list(node_ast, c)
        else:
            breakpoint()
            raise NotImplementedError()

        return c
