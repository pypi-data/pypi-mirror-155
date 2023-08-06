import ast
from pymich.frontend.three_address_encode import ThreeAddressEncode
from pymich.frontend.passes import *


def python_to_ir(source_ast, std_lib):
    factor_out_storage = FactorOutStorage()
    tuplify_function_arguments = TuplifyFunctionArguments(std_lib)

    frontend_passes = [
        RewriteOperations(),
        RewriteViews(),
        factor_out_storage,
        RemoveSelfArgFromMethods(),
        AssignAllFunctionCalls(),
        HandleNoArgEntrypoints(),
        ThreeAddressEncode(),
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
