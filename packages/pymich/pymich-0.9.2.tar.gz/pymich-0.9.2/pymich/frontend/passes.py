import ast
from typing import Any, List, Union
from dataclasses import dataclass

import unittest

import pymich.utils.exceptions as E



def _is_view(node) -> bool:
    """A contract method is considered a view if has a return type annotation
    and does not start with an underscore (_)"""
    if type(node) == ast.FunctionDef and node.name[0] != "_" and node.returns is not None:
        for body_el in node.body:
            if type(body_el) == ast.Return:
                return True

    return False


def make_dataclass(name, arguments_spec):
    return ast.ClassDef(
        name=name,
        bases=[],
        keywords=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id=argument_name, ctx=ast.Store()),
                annotation=argument_type[0],
                value=None,
                simple=1,
                lineno=argument_type[1],
            )
            for argument_name, argument_type in arguments_spec.items()
        ],
        decorator_list=[ast.Name(id='dataclass', ctx=ast.Load())]
    )


class RewriteViews(ast.NodeTransformer):
    """
    Input
    -----

    def myView(self, arg1: type1, ..., argN: typeN) -> return_type:
        return expr(arg1, ..., argN)

    Output
    -----

    def myView(self, arg1: type1, ..., argN: typeN, __callback__: Contract[return_type]):
        transaction(__callback__, Mutez(0), self.total_supply)

    """
    def _transform_return(self, node: ast.Return) -> ast.Call:
        return ast.Call(
            func=ast.Name(id='transaction', ctx=ast.Load()),
            args=[
                ast.Name(id='__callback__', ctx=ast.Load()),
                ast.Call(
                    func=ast.Name(id='Mutez', ctx=ast.Load()),
                    args=[ast.Constant(value=0, kind=None)],
                    keywords=[]
                ),
                node.value
            ],
            keywords=[]
        )

    def _transform_block(self, nodes) -> List[Any]:
        new_nodes = []
        for node in nodes:
            if type(node) == ast.Return:
                new_nodes.append(self._transform_return(node))
            else:
                new_nodes.append(node)

        return new_nodes

    def _expand_view(self, node: ast.FunctionDef) -> Any:
        # add `contract_callback: Contract[return_type]` to method parameter
        callback_annotation = ast.Subscript(
            value=ast.Name(id='Contract', ctx=ast.Load()),
            slice=ast.Index(
                value=node.returns
            ),
            ctx=ast.Load()
        )
        callback_argument = ast.arg(arg="__callback__", annotation=callback_annotation)
        node.args.args.append(callback_argument)

        # remove the return type annotation
        node.returns = None

        # transform all return expressions into `transaction` function call
        node.body = self._transform_block(node.body)


        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        new_body = []
        for body_el in node.body:
            if _is_view(body_el):
                new_body.append(self._expand_view(body_el))
            else:
                new_body.append(body_el)

        node.body = new_body

        return node


class TuplifyFunctionArguments(ast.NodeTransformer):
    """
    Input
    -----

    def my_function(arg1: type1, arg2: type2):
        return arg1 + arg2

    Result
    ------

    @dataclass
    Arg:
        arg1: type1
        arg2: type2

    def my_function(param: Arg):
        arg1 = param.arg1
        arg2 = param.arg2
        return arg1 + arg2

    """

    def __init__(self, std_lib, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = {}  # key: fun_nam, val: param_dataclass_name
        self.dataclasses = []
        self.defined_class_names = []
        self.std_lib = std_lib

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.defined_class_names.append(node.name)
        node.body = [self.visit(body_element) for body_element in node.body]
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        prologue_body_instructions = []
        arguments = node.args.args

        # skip class instantiations and functions of 1 argument
        if len(arguments) > 1:
            ### generate argument dataclass
            arguments_spec = {
                argument_node.arg: (argument_node.annotation, node.lineno)
                for argument_node in arguments
            }
            param_dataclass_name = node.name + "Param"
            self.dataclasses.append(make_dataclass(param_dataclass_name, arguments_spec))

            # tuplify arguments
            param_name = node.name + "__param"

            self.env[node.name] = param_dataclass_name

            node.args.args = [ast.arg(arg=param_name, annotation=ast.Name(id=param_dataclass_name, ctx=ast.Load()))]

            # destructure tuplified arguments
            prologue_body_instructions = [
                ast.Assign(
                    targets=[ast.Name(id=attr_name, ctx=ast.Store())],
                    value=ast.Attribute(
                        value=ast.Name(id=param_name, ctx=ast.Load()),
                        attr=attr_name,
                        ctx=ast.Load()
                    ),
                    type_comment=None)
                for attr_name in arguments_spec.keys()
            ]

        new_body = [self.visit(body_node) for body_node in node.body]

        node.body = prologue_body_instructions + new_body

        return node

    def check_if_stdlib_method(self, node: ast.Call) -> bool:
        if type(node.func) != ast.Attribute:
            return False

        stdlib_method_names = []
        for stdlib_el in self.std_lib.values():
            if hasattr(stdlib_el, "methods"):
                stdlib_method_names += list(stdlib_el.methods.keys())

        return node.func.attr in stdlib_method_names

    def check_if_stdlib_function(self, node: ast.Call) -> bool:
        if type(node.func) != ast.Name:
            return False

        stdlib_function_names = []
        for stdlib_function_name, stdlib_el in self.std_lib.items():
            if not hasattr(stdlib_el, "methods"):
                stdlib_function_names.append(stdlib_function_name)

        return node.func.id in stdlib_function_names

    def check_if_stdlib_constructor(self, node: ast.Call) -> bool:
        stdlib_constructor_names = []
        for stdlib_constructor_name, stdlib_el in self.std_lib.items():
            if hasattr(stdlib_el, "constructor"):
                stdlib_constructor_names.append(stdlib_constructor_name)

        # Check if constructor
        if type(node.func) == ast.Name:
            return node.func.id in stdlib_constructor_names

        # Check if casted constructor
        if type(node.func) == ast.Subscript:
            if type(node.func.value) == ast.Name:
                return node.func.value.id in stdlib_constructor_names

        return False


    def visit_Call(self, node: ast.Call) -> Any:
        if self.check_if_stdlib_method(node):
            return node

        if self.check_if_stdlib_function(node) or self.check_if_stdlib_constructor(node):
            return node

        try:
            if node.func.value.id == "Contract":
                return node
        except AttributeError:
            pass

        if type(node.func) == ast.Attribute:
            return node

        fun_name = node.func.id

        if len(node.args) > 1 and fun_name not in self.defined_class_names and fun_name != "transaction":
            #if fun_name not in self.env:
            #    raise E.FunctionNameException(fun_name, node.lineno)
            try:
                node.args = [
                    ast.Call(
                        func=ast.Name(id=self.env[fun_name], ctx=ast.Load()),
                        args=[self.visit(arg) for arg in node.args],
                        keywords=[])
                ]
            except:
                pass
        return node


class AssignAllFunctionCalls(ast.NodeTransformer):
    """
    Input
    -----

    foo(*args)

    Result
    ------

    _ = foo(*args)
    """

    def visit_Expr(self, node: ast.Expr) -> Any:
        """Funcalls which's return value are not assigned are wrapped in an ast.Expr"""
        if type(node.value) == ast.Call:
            if type(node.value.func) == ast.Name and node.value.func.id == "transaction":
                pass
            else:
                call_node = node.value
                return ast.Assign(
                    targets=[ast.Name(id='__placeholder__', ctx=ast.Store())],
                    value=call_node,
                    type_comment=None)

        return node


class RemoveSelfArgFromMethods(ast.NodeTransformer):
    """
    Input
    -----

    class C:
        def f(self, x: t1, y: t2) -> t3:

    Result
    ------

    class C:
        def f(x: t1, y: t2) -> t3:
    """

    def remove_first_untyped_arg(self, node: ast.FunctionDef) -> Any:
        if len(node.args.args) and node.args.args[0].annotation == None:
            del node.args.args[0]

        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        new_body = []
        for body_node in node.body:
            if type(body_node) == ast.FunctionDef:
                new_body.append(self.remove_first_untyped_arg(body_node))
            else:
                new_body.append(body_node)

        return node


class ExpandStorageInEntrypoints(ast.NodeTransformer):
    def visit_Attribute(self, node: ast.Attribute) -> Union[ast.Name, ast.Attribute]:
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "self"
        ):
            node.value.id = '__STORAGE__'
            return node
        else:
            return ast.Attribute(value=self.visit(node.value), attr=node.attr)


def is_contract_class_def(node: ast.ClassDef) -> bool:
    if type(node) == ast.ClassDef and node.name == "Contract":
        return True
    elif type(node) == ast.ClassDef and len(node.bases) and (node.bases[0].id == "Contract" or node.bases[0].id == "BaseContract"):
        return True
    return False


class FactorOutStorage(ast.NodeTransformer):
    """
    Input
    -----

    @dataclass
    class MyContract(Contract):
        counter: int
        admin: address

        def update_counter(self, new_counter: int):
            self.counter = 1

    Output
    ------

    @dataclass
    class Storage
        counter: int
        admin: address

    class Contract:
        def deploy():
            return Storage()

        def update_counter(self, new_counter: int):
            self.storage.counter = 1

            return self.storage
    """
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        # only expand contract methods
        if is_contract_class_def(node):
            node.name = "Contract"
            node.bases = []

            # TODO remove: if there is a `deploy` method, do nothing
            for body_node in node.body:
                if type(body_node) == ast.FunctionDef:
                    if body_node.name == "deploy":
                        return node

            # Factor body ast.AnnAssign into dataclass
            storage_keys_spec = {}
            new_node_body = []
            for i, body_node in enumerate(node.body):
                if type(body_node) == ast.AnnAssign:
                    lineno = body_node.lineno
                    storage_keys_spec[body_node.target.id] = (body_node.annotation, lineno)
                else:
                    new_node_body.append(body_node)
            node.body = new_node_body

            self.storage_dataclass = make_dataclass('Storage', storage_keys_spec)

            # For all methods, update `self.<storage_key>` into `self.storage.<key>`
            # and add return `self.storage`
            new_body = []
            for body_node in node.body:
                new_body_node = ExpandStorageInEntrypoints().visit(body_node)
                if type(body_node) == ast.FunctionDef:
                    returns_none = isinstance(body_node.returns, ast.Constant) and body_node.returns.value == None
                    if not body_node.returns or returns_none:
                        body_node.returns = ast.Name(id='Storage', ctx=ast.Load())
                    return_storage_node = ast.Return(
                        value=ast.Name(id='__STORAGE__', ctx=ast.Load()),
                    )
                    new_body_node.body.append(return_storage_node)
                new_body.append(new_body_node)
            node.body = new_body

            # Create deploy function
            deploy_function_node = ast.FunctionDef(
                name='deploy',
                args=ast.arguments(posonlyargs=[], args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
                body=[ast.Return(value=ast.Call(func=ast.Name(id='Storage', ctx=ast.Load()), args=[], keywords=[]))],
                decorator_list=[],
                returns=None,
                type_comment=None,
            )
            node.body = [deploy_function_node] + node.body

            return node
        else:
            return node


class HandleNoArgEntrypoints(ast.NodeTransformer):
    """
    Input
    -----

    class Contract:
        def my_function(self):
            return 0

    Result
    ------

    class Contract:
        def my_function(self, p: unit):
            return 0

    """

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if not len(node.args.args) and node.name != "deploy":
            node.args.args.append(ast.arg(arg='p', annotation=ast.Name(id='unit', ctx=ast.Load())))

        return node


class RewriteOperations(ast.NodeTransformer):
    """
    Input
    -----

    class Contract:
        def my_function(self):
            self.ops = self.ops.push(Contract[Unit](SENDER), AMOUNT, Unit)

    Result
    ------

    class Contract:
        def my_function(self, p: unit):
            __OPERATIONS__ = __OPERATIONS__(Contract[Unit](SENDER), AMOUNT, Unit)

    """

    def visit_Attribute(self, node: ast.Attribute) -> Union[ast.Name, ast.Attribute]:
        if (
            isinstance(node.value, ast.Name)
            and node.value.id == "self"
            and node.attr == "ops"
        ):
            return ast.Name(id="__OPERATIONS__", ctx=node.ctx)
        elif (
            isinstance(node.value, ast.Attribute)
        ):
            return ast.Attribute(value=self.visit(node.value), attr=node.attr)
        else:
            return node



class PlaceBackStorageDataclass(ast.NodeTransformer):
    def __init__(self, storage_dataclass: ast.ClassDef):
        super().__init__()
        self.storage_dataclass = storage_dataclass

    def visit_Module(self, node: ast.Module) -> Any:
        el_number = 0
        for i, el in enumerate(node.body):
            if is_contract_class_def(el):
                el_number = i

        node.body.insert(el_number, self.storage_dataclass)
        return node


def macro_expander(source_ast, std_lib):
    factor_out_storage = FactorOutStorage()
    tuplify_function_arguments = TuplifyFunctionArguments(std_lib)

    frontend_passes = [
        RewriteOperations(),
        RewriteViews(),
        factor_out_storage,
        RemoveSelfArgFromMethods(),
        AssignAllFunctionCalls(),
        HandleNoArgEntrypoints(),
        FrontendCompiler(),
        tuplify_function_arguments,
    ]

    new_ast = source_ast
    for frontend_pass in frontend_passes:
        new_ast = frontend_pass.visit(new_ast)
        new_ast = ast.fix_missing_locations(new_ast)

    new_ast.body = tuplify_function_arguments.dataclasses + new_ast.body
    if hasattr(factor_out_storage, 'storage_dataclass'):
        new_ast = PlaceBackStorageDataclass(factor_out_storage.storage_dataclass).visit(new_ast)

    new_ast = ast.fix_missing_locations(new_ast)
    return new_ast

