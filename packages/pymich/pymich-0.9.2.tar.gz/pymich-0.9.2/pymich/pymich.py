import cli2
import json
import sys

from pymich.utils.exceptions import CompilerException

from enum import Enum
from pymich.compiler import Compiler
from pymich.test_utils import VM
from pymich.frontend.compiler import python_to_ir

from pygments import highlight
from pygments.lexers import PythonLexer, lisp
from pygments.formatters import Terminal256Formatter


MICHELSON = "michelson"
MICHELINE = "micheline"
IR = "ir"


def dump_ir(input_path: str, syntax_highlight: bool):
    """
    Compiles a Python file to Pymich IR.

    :param input_path: path to the Python file to compile to IR
    :param syntax_highlight: pass `True` to highlight the output code
    """
    with open(input_path) as f:
        source = f.read()

    try:
        import ast
        source_ast = ast.parse(source)
        compiler = Compiler(source)
        compiler.compile_contract()
        ir = compiler.ast
        ir_code = ast.unparse(ir)
        if syntax_highlight:
            print(highlight(ir_code, PythonLexer(), Terminal256Formatter()))
        else:
            print(ir_code)
    except CompilerException as e:
        print(e.message, file=sys.stderr)



def compile(input_path: str, output_format: str = MICHELSON, syntax_highlight: bool = False):
    """
    Compiles a Python file and outputs the result to stdout.

    :param input_path: path to the Python file to compile
    :param output_format: output format for the contract, one of "michelson", "micheline" or "ir"
    :param syntax_highlight: pass `True` to highlight the output code
    """
    with open(input_path) as f:
        source = f.read()

    try:
        micheline = Compiler(source).compile_contract()

        if output_format == MICHELINE:
            micheline_code = json.dumps(micheline, indent=4)
            if syntax_highlight:
                print(highlight(micheline_code, PythonLexer(), Terminal256Formatter()))
            else:
                print(micheline_code)
        elif output_format == MICHELSON:
            vm = VM()
            vm.load_contract(micheline)
            michelson = vm.contract.to_michelson()

            if syntax_highlight:
                print(highlight(michelson, lisp.CPSALexer(), Terminal256Formatter()))
            else:
                print(michelson)
        elif output_format == IR:
            dump_ir(input_path, syntax_highlight)
        else:
            print(f"Only 'michelson' and 'micheline' parameters are supported", file=sys.stderr)
    except CompilerException as e:
        print(e.message, file=sys.stderr)


cli = cli2.Group()
cli.add(compile)

if __name__ == '__main__':
    cli.entry_point()
