import ast

from pymich.backend.micheline_emitter import CompilerBackend
from pymich.backend.michelson_typechecker import MichelsonTypeChecker
from pymich.frontend.compiler import python_to_ir

from pymich.utils.environment import Env

from pymich.backend.compiler import Compiler as BackendCompiler

import pymich.utils.exceptions as E


class Compiler:
    def __init__(self, src: str = "", isDebug=False):
        self.ast = ast.parse(src)
        self.isDebug = isDebug
        self.ir_to_michelson = BackendCompiler(src, isDebug)
        self._compile = self.ir_to_michelson._compile
        self._compile_attribute = self.ir_to_michelson._compile_attribute
        self.compile_assign_record = self.ir_to_michelson.compile_assign_record
        self.type_checker = self.ir_to_michelson.type_checker

    def expose_internals(self):
        self.env = self.ir_to_michelson.env
        self.std_lib = self.ir_to_michelson.std_lib
        self.type_checker = self.ir_to_michelson.type_checker

    def compile_expression(self, e: Env = None):
        self.ast = python_to_ir(self.ast, self.ir_to_michelson.std_lib)
        instructions = self.ir_to_michelson._compile(self.ast, e)
        self.expose_internals()
        return CompilerBackend().compile_instructions(instructions)

    def compile_expression_object(self, e: Env = None):
        self.ast = python_to_ir(self.ast, self.ir_to_michelson.std_lib)
        instructions = self.ir_to_michelson._compile(self.ast, e)
        return instructions

    def compile_contract(self):
        self.ast = python_to_ir(self.ast, self.ir_to_michelson.std_lib)
        self.ir_to_michelson.ast = self.ast
        try:
            self.ir_to_michelson.compile()
        except (E.CompilerException, E.TypeException, AttributeError) as e:
            print(ast.unparse(self.ast))
            raise e
        self.expose_internals()

        typechecker = MichelsonTypeChecker()
        typechecker.typecheck_contract(self.ir_to_michelson.contract)

        return CompilerBackend().compile_contract(self.ir_to_michelson.contract)

    def compile_contract_object(self):
        self.ast = python_to_ir(self.ast, self.ir_to_michelson.std_lib)
        self.ir_to_michelson.ast = self.ast
        self.ir_to_michelson.compile()
        self.expose_internals()
        return self.ir_to_michelson.contract

    @staticmethod
    def print_instructions(instructions):
        print("\n".join([f"{i.name} {i.args} {i.kwargs}" for i in instructions]))


