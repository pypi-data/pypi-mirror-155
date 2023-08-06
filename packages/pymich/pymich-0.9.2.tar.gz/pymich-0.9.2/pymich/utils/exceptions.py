class CompilerException(Exception):
    """Raised when the compiler fails

    Attributes:
        message -- error message
    """

    def __init__(self, message, lineno):
        self.message = message + f" at line {lineno}"

class NotAnIterableException(CompilerException):
    def __init__(self, actual_type):
        self.message = f"{actual_type} is not an iterable"

class MalformedAnnotationException(CompilerException):
    def __init__(self, message):
        self.message = message

class TypeException(CompilerException):
    def __init__(self, expected_type, actual_type, lineno):
        self.message = f"Unexpected type: expected {expected_type}, got {actual_type} at line {lineno}"

class OperandException(CompilerException):
    def __init__(self, instr_name, allowed_types, actual_types, extra_msg="", lineno=0):
        self.message = f"""{instr_name} operand type error:
  - allowed operand types: {allowed_types}
  - actual types: {actual_types}
        """

        if extra_msg:
            self.message += f"\n\n N.B. {extra_msg}"

class AttributeException(TypeException):
    def __init__(self, record_type, attribute_name, lineno):
        self.message = f"{record_type} Record has no attribute {attribute_name} at line {lineno}"

class NameException(TypeException):
    def __init__(self, token_name, lineno):
        self.message = f"Variable '{token_name}' does not exist at line {lineno}"

class FunctionNameException(TypeException):
    def __init__(self, function_name, lineno):
        self.message = f"Function '{function_name}' does not exist at line {lineno}"

class FunctionParameterTypeException(TypeException):
    def __init__(self, function_name, expected_type, actual_type, lineno):
        self.message = f"Function '{function_name}' expected a parameter of type {expected_type} but got {actual_type} at line {lineno}"

class TypeAnnotationDoesNotExistException(TypeException):
    def __init__(self, annotation_name, expected_type_annotations, lineno):
        self.message = f"Type annotation '{annotation_name}' does not exist, expected {expected_type_annotations} at line {lineno}"


class ConditionBranchesTypeMismatch(CompilerException):
    def __init__(self, false_branch_type, true_branch_type, lineno=0):
        self.message = f"""Condition branches type mismatch:
  - left branch {false_branch_type}
  - right branch {true_branch_type}
        """


class MichelsonTypecheckerException(Exception):
    """Raised when the emitted Michelson fails to typecheck

    Attributes:
        message -- error message
    """

    def __init__(self, message, lineno=0):
        self.message = message + f" at line {lineno}"

class StackTopTypeException(MichelsonTypecheckerException):
    def __init__(self, instr_name, expected_type, actual_type, extra_msg="", lineno=0):
        self.message = f"""Top stack type mismatch when calling {instr_name}:
  - expected top stack: {expected_type}
  - actual top stack: {actual_type}

N.B. {extra_msg}

Hint: stack grows this way: [stack_bottom, ..., stack_top] ---->
        """

class SetElementTypeException(MichelsonTypecheckerException):
    def __init__(self, el_type, set_type, lineno=0):
        self.message = f"""Element type incompatible with set type:
  - el type: {el_type}
  - set type: {set_type}
        """

class MapKeyTypeException(MichelsonTypecheckerException):
    def __init__(self, key_type, map_type, lineno=0):
        self.message = f"""Key type incompatible with map type on GET instruction:
  - key type: {key_type}
  - map type: {map_type}
        """

class MapValueTypeException(MichelsonTypecheckerException):
    def __init__(self, value_type, map_type, extra_msg="", lineno=0):
        self.message = f"""Value type incompatible with map type on GET instruction:
  - value type: {value_type}
  - map type: {map_type}
        """

        if extra_msg:
            self.message += f"\n\nN.B. {extra_msg}"


class ContractReturnTypeException(MichelsonTypecheckerException):
    def __init__(self, actual_return_type, expected_return_type, lineno=0):
        self.message = f"""The contract is not returning an (operation list, storage_type) pair:
  - actual return type: {actual_return_type}
  - expected return type: {expected_return_type}
        """

class PushTypeException(MichelsonTypecheckerException):
    def __init__(self, lineno=0):
        self.message = "Can only PUSH one of [int, nat, string, mutez, timestamp, address]"


class LambdaArgumentTypeException(MichelsonTypecheckerException):
    def __init__(self, argument_type, expected_argument_type, lineno=0):
        self.message = f"""LAMBDA argument type mismatch when calling EXEC:
  - actual argument type: {argument_type},
  - expected argument type: {expected_argument_type}
        """

class StackLengthException(MichelsonTypecheckerException):
    pass


class InvalidMichelsonException(MichelsonTypecheckerException):
    pass


