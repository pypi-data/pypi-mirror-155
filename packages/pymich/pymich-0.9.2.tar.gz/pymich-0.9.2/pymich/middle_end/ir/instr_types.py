import ast
from dataclasses import dataclass
from copy import deepcopy
from typing import Optional, List
import pymich.utils.exceptions as E


class Type:
    def __init__(self, annotation: Optional[str] = None):
        self.annotation = annotation
        pass

    def __eq__(self, o):
        return type(self) == type(o)

    def python_name(self):
        return self.__str__()

class Unknown(Type):
    def __str__(self):
        return "unknown"

class TypeVar(Type):
    def __init__(self, name="T", annotation: Optional[str] = None):
        super().__init__(annotation)
        self.name = name

    def __str__(self):
        return self.name

class Option(Type):
    def __init__(self, option_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.option_type = option_type

    def __str__(self):
        return f"{self.option_type} option"

    def __eq__(self, o):
        return type(self) == type(o) and self.option_type == o.option_type


class Or(Type):
    def __init__(self, left_type: Type, right_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.left_type = left_type
        self.right_type = right_type

    def __str__(self):
        return f"or {self.left_type} {self.right_type}"


class Union:
    """Not a michelson type. Used to signal in errors that multiple types are allowed.

    Indeed, in Michelson, `Or` is a type itself and thus `Int` or `Nat` will not be
    a acceptable types if is the expected type `Or(Int, Nat)`.
    """
    def __init__(self, allowed_types: List[Type]):
        self.allowed_types = allowed_types

    def __str__(self):
        if not len(self.allowed_types):
            return "()"

        type_as_string = "("
        for allowed_type in self.allowed_types:
            type_as_string += str(allowed_type) + " | "
        return type_as_string[:-3] + ")"


class Unit(Type):
    def __str__(self):
        return "unit"


class Bytes(Type):
    def __str__(self):
        return "bytes"

class PythonInt(Type):
    def __str__(self):
        return "python_int"

class Int(Type):
    def __str__(self):
        return "int"

    def __eq__(self, o):
        return type(self) == type(o)

class Datetime(Type):
    def __str__(self):
        return "timestamp"


class Nat(Type):
    def __str__(self):
        return "nat"


class Mutez(Type):
    def __str__(self):
        return "mutez"

class PythonString(Type):
    def __str__(self):
        return "python_string"

class String(Type):
    def __str__(self):
        return "string"


class Bool(Type):
    def __str__(self):
        return "bool"


class Address(Type):
    def __str__(self):
        return "address"

    def python_name(self):
        return "Address"


class Universal(Type):
    def __str__(self):
        return "universal"

    def __eq__(self, o: Type):
        return True


class Operation(Type):
    def __str__(self):
        return "operation"


class Pair(Type):
    """
    car: first element
    cdr: second element
    """
    def __init__(self, car: Type, cdr: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.car = car
        self.cdr = cdr

    def __eq__(self, o):
        if isinstance(o, Record):
            return self == o.get_type()
        return type(self) == type(o) and self.car == o.car and self.cdr == o.cdr

    def __str__(self):
        if isinstance(self.car, Pair) and isinstance(self.cdr, Pair):
            return f"pair({self.car.car}, {self.car.cdr}, {self.cdr.car}, {self.cdr.cdr})"
        if isinstance(self.car, Pair):
            return f"pair({self.car.car}, {self.car.cdr}, {self.cdr})"
        if isinstance(self.cdr, Pair):
            return f"pair({self.car}, {self.cdr.car}, {self.cdr.cdr})"
        else:
            return f"pair({self.car}, {self.cdr})"

    @staticmethod
    def pair_n(args: List[Type]) -> "Pair":
        args.reverse()
        right_comb = Pair(args[1], args[0])

        for i in range(2, len(args)):
            car = args[i]
            right_comb = Pair(car, right_comb)

        return right_comb

    def get_n(self, n: int) -> Type:
        if n == 0:
            return self

        acc = self
        for i in range(1, n + 1):
            if i != n:
                if i % 2:
                    if isinstance(acc, Pair):
                        acc = acc.cdr
                    else:
                        raise E.InvalidMichelsonException(f"GET {n} requires a right comb of minimum length {n - 1}")
            else:
                if (n % 2) == 0:
                    return acc
                else:
                    if isinstance(acc, Pair):
                        return acc.car
                    else:
                        raise E.InvalidMichelsonException(f"GET {n} requires a right comb of minimum length {n}")

        return acc

    def update_n(self, el: Type, n: int) -> Type:
        if n == 0:
            return el

        acc = deepcopy(self)
        prev_acc = acc
        new_pair = acc
        for i in range(1, n + 1):
            if i != n:
                if i % 2:
                    if isinstance(acc, Pair):
                        prev_acc = acc
                        acc = acc.cdr
                    else:
                        raise E.InvalidMichelsonException(f"UPDATE {n} requires a right comb of minimum length {n - 1}")
            else:
                if (n % 2) == 0:
                    pass
                else:
                    if isinstance(acc, Pair):
                        acc.car = el
                        return new_pair
                    else:
                        raise E.InvalidMichelsonException(f"UPDATE {n} requires a right comb of minimum length {n}")

        if isinstance(prev_acc, Pair):
            prev_acc.cdr = el
        else:
            raise E.InvalidMichelsonException(f"UPDATE {n} requires a right comb of minimum length {n - 1}")

        return new_pair


class Record(Type):
    def __init__(self, name: str, attribute_names: List[str], attribute_types: List[Type], annotation: Optional[str] = None):
        super().__init__(annotation)
        self.name = name
        self.attribute_names = attribute_names
        self.attribute_types = attribute_types

    def __eq__(self, o):
        if isinstance(o, Pair):
            return self.get_type() == o
        return type(self) == type(o) and self.attribute_names == o.attribute_names and self.attribute_types == o.attribute_types

    def __str__(self):
        return str(self.get_type())

    def make_node(self, left, right):
        return Pair(car=left, cdr=right)

    def get_type(self, i=0, acc=None):
        attribute_type = self.attribute_types[i]
        if acc == None:
            acc = self.make_node(None, None)

        if i == 0:
            return self.make_node(attribute_type, self.get_type(i+1))

        elif i == len(self.attribute_types) - 1:
            return attribute_type

        else:
            return self.make_node(attribute_type, self.get_type(i+1))

    def get_attribute_type(self, attribute_name: str):
        attribute_index = self.attribute_names.index(attribute_name)
        return self.attribute_types[attribute_index]


class List(Type):
    def __init__(self, element_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.element_type = element_type

    def __eq__(self, o):
        if isinstance(o, Operations):
            return self.element_type == o.element_type
        return type(self) == type(o) and self.element_type == o.element_type

    def __str__(self):
        return f"{self.element_type} list"

class Operations(Type):
    def __init__(self, annotation: Optional[str] = None):
        self.element_type = Operation()
        super().__init__(annotation)

    def __str__(self):
        return f"operation list"

    def __eq__(self, o):
        if isinstance(o, List):
            return self.element_type == o.element_type
        return type(self) == type(o) and self.element_type == o.element_type

class Set(Type):
    def __init__(self, element_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.element_type = element_type

    def __eq__(self, o):
        return type(self) == type(o) and self.element_type == o.element_type

    def __str__(self):
        return f"{self.element_type} set"

class Spread(Type):
    def __init__(self, element_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.element_type = element_type

    def __eq__(self, o):
        return type(self) == type(o) and self.element_type == o.element_type


class Dict(Type):
    def __init__(self, key_type: Type, value_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.key_type = key_type
        self.value_type = value_type

    def __eq__(self, o):
        return type(self) == type(o) and self.key_type == o.key_type and self.value_type == o.value_type

    def __str__(self):
        return f"({self.key_type}, {self.value_type}) map"


class BigMap(Type):
    def __init__(self, key_type: Type, value_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.key_type = key_type
        self.value_type = value_type

    def __eq__(self, o):
        return type(self) == type(o) and self.key_type == o.key_type and self.value_type == o.value_type

    def __str__(self):
        return f"({self.key_type}, {self.value_type}) big_map"


class Callable(Type):
    def __init__(self, param_type: Type, return_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.param_type = param_type
        self.return_type = return_type
        self.applied_arg_types = []

    def __eq__(self, o):
        return type(self) == type(o) and self.param_type == o.param_type and self.return_type == o.return_type


#from pymich.compiler_stdlib import StdlibFunctionSpec

class StdlibVariable:
    def __init__(self, type_: Type, compile_callback):
        self.type = type_
        self.compile_callback = compile_callback


@dataclass
class FunctionPrototype:
    arg_type: Type
    return_type: Type

class StdlibFunctionSpec:
    def __init__(self, compile_callback, get_prototype: FunctionPrototype):
        self.compile_callback = compile_callback
        self.get_prototype = get_prototype


class StdLibClassSpec:
    def __init__(self):
        self.methods = {}
        self.attributes = {}
        self.static_methods = []
        self.constructor = None

    def create_constructor(self, constructor_spec: StdlibFunctionSpec):
        self.constructor = constructor_spec
        return self

    def create_method(self, name: str, method_spec: StdlibFunctionSpec, is_static=False):
        self.methods[name] = method_spec
        if is_static:
            self.static_methods.append(name)
        return self

    def create_attribute(self, name: str, attribute_spec: StdlibVariable):
        self.attributes[name] = attribute_spec
        return self


class StdlibMethodInstance(Type):
    """
    eg. To retrieve `my_dict.add`, retreive `my_dict` and apply its `add` method
    """
    def __init__(
        self,
        var_name: str,
        signature: StdlibFunctionSpec,
        compile_callback: Callable,
        annotation: Optional[str] = None,
    ):
        super().__init__(annotation)
        self.var_name = var_name
        self.signature = signature
        self.compile_callback = compile_callback

    def __eq__(self, o):
        return self.var_name == o.var_name and self.signature == o.signature and self.compile_callback == o.compile_callback


class StdlibStaticMethodInstance(Type):
    """
    eg. To retrieve `Timestamp.now`
    """
    def __init__(
        self,
        signature: StdlibFunctionSpec,
        compile_callback: Callable,
        annotation: Optional[str] = None,
    ):
        super().__init__(annotation)
        self.signature = signature
        self.compile_callback = compile_callback

    def __eq__(self, o):
        return self.signature == o.signature and self.compile_callback == o.compile_callback



class Contract(Type):
    def __init__(self, param_type: Type, annotation: Optional[str] = None):
        super().__init__(annotation)
        self.param_type = param_type

    def __eq__(self, o):
        return type(self) == type(o) and self.param_type == o.param_type

    def __str__(self):
        return f"{self.param_type} contract"



base_types = [
    "Unit",
    "Nat",
    "Int",
    "str",
    "Address",
    "bool",
    "unit",
    "Mutez",
    "bytes",
    "datetime",
]

polymorphic_types = [
    "Dict",
    "List",
    "Set",
    "Callable",
    "Contract",
]

record_types = [
    "Records"
]

class TypeParser:
    def __init__(self):
        pass

    def parse_name(self, name: ast.Name, e, annotation: Optional[str] = None, lineno = 0) -> Type:
        if name.id == 'Int':
            return Int(annotation)
        if name.id == 'Nat':
            return Nat(annotation)
        if name.id == 'String':
            return String(annotation)
        if name.id == 'Address':
            return Address(annotation)
        if name.id == 'bool':
            return Bool(annotation)
        if name.id == 'unit' or name.id == 'Unit':
            return Unit(annotation)
        if name.id == 'Mutez':
            return Mutez(annotation)
        if name.id == 'Bytes':
            return Bytes(annotation)
        if name.id == 'datetime':
            return Datetime(annotation)
        if name.id == 'Timestamp':
            return Datetime(annotation)
        if name.id == 'Operations':
            return Operations()
        if name.id in e.types.keys():
            return e.types[name.id]

        allowed_annotations = base_types + record_types
        raise E.TypeAnnotationDoesNotExistException(name.id, allowed_annotations, lineno)

    def parse_dict(self, dictionary: ast.Subscript, e, annotation: Optional[str] = None):
        key_type = self.parse(dictionary.slice.elts[0], e)
        value_type = self.parse(dictionary.slice.elts[1], e)
        return Dict(key_type, value_type, annotation)

    def parse_big_map(self, big_map: ast.Subscript, e, annotation: Optional[str] = None):
        key_type = self.parse(big_map.slice.elts[0], e)
        value_type = self.parse(big_map.slice.elts[1], e)
        return BigMap(key_type, value_type, annotation)

    def parse_callable(self, dictionary: ast.Subscript, e, annotation: Optional[str] = None):
        key_type = self.parse(dictionary.slice.elts[0].elts[0], e)
        value_type = self.parse(dictionary.slice.elts[1], e)
        return Callable(key_type, value_type, annotation)

    def parse_contract(self, contract: ast.Subscript, e, annotation):
        param_type = self.parse(contract.slice, e)
        return Contract(param_type)

    def parse_list(self, list_: ast.Subscript, e, annotation):
        param_type = self.parse(list_.slice, e)
        return List(param_type, annotation)

    def parse_set(self, set_: ast.Subscript, e, annotation):
        param_type = self.parse(set_.slice, e)
        return Set(param_type, annotation)

    def parse_subscript(self, subscript: ast.Subscript, e, annotation: Optional[str] = None, lineno = 0):
        if subscript.value.id == "Dict":
            return self.parse_dict(subscript, e, annotation)
        if subscript.value.id == "BigMap":
            return self.parse_big_map(subscript, e, annotation)
        if subscript.value.id == "Map":
            return self.parse_dict(subscript, e, annotation)
        if subscript.value.id == "Callable":
            return self.parse_callable(subscript, e, annotation)
        if subscript.value.id == "Contract":
            return self.parse_contract(subscript, e, annotation)
        if subscript.value.id == "List":
            return self.parse_list(subscript, e, annotation)
        if subscript.value.id == "Set":
            return self.parse_set(subscript, e, annotation)
        else:
            allowed_annotations = f"only polymorphic types ({polymorphic_types}) are subscriptable"
            raise E.TypeAnnotationDoesNotExistException(subscript.value.id, allowed_annotations, lineno)

    def parse(self, type_ast, e, annotation: Optional[str] = None, lineno = 0) -> Type:
        if type(type_ast) == ast.Name:
            return self.parse_name(type_ast, e, annotation, lineno)
        if type(type_ast) == ast.Subscript:
           return self.parse_subscript(type_ast, e, annotation, lineno)
        if type(type_ast) == ast.Tuple:
            attribute_names = []
            attribute_types = []
            for i, elt in enumerate(type_ast.elts):
                attribute_names.append(str(i))
                attribute_types.append(self.parse(elt, e, annotation, lineno))
            return Record("_", attribute_names, attribute_types)
        if type_ast == None:
            return Unit()
        raise E.TypeAnnotationDoesNotExistException(
            ast.dump(type_ast),
            f"expected a base type ({base_types}) or an polymorphic type ({polymorphic_types})",
            type_ast.lineno
            )
        raise NotImplementedError

