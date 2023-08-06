from typing import Callable, Optional
from dataclasses import dataclass
import pymich.middle_end.ir.instr_types as t
from pymich.middle_end.ir.instr_types import StdlibVariable, StdlibFunctionSpec, StdLibClassSpec
from pymich.middle_end.ir.vm_types import FunctionPrototype, MultiArgFunctionPrototype


identity = lambda x: x


@dataclass
class StdLibCompileCallbacks:
    sender: Callable = identity
    self_address: Callable = identity
    source: Callable = identity
    amount: Callable = identity
    balance: Callable = identity
    unit: Callable = identity
    datetime: Callable = identity
    dict_safe: Callable = identity
    abs: Callable = identity
    blake2b: Callable = identity
    pack: Callable = identity
    unpack: Callable = identity
    datetime_now: Callable = identity
    datetime_from_timestamp: Callable = identity
    timedelta: Callable = identity
    transaction: Callable = identity
    contract: Callable = identity
    mutez: Callable = identity
    nat: Callable = identity
    to_int: Callable = identity
    int: Callable = identity
    is_nat: Callable = identity
    string: Callable = identity
    address: Callable = identity
    list: Callable = identity
    list_prepend: Callable = identity
    map: Callable = identity
    map_set: Callable = identity
    big_map: Callable = identity
    set: Callable = identity
    set_add: Callable = identity
    set_remove: Callable = identity
    push_operation: Callable = identity
    compile_option: Callable = identity
    compile_option_get: Callable = identity
    compile_option_get_with_default: Callable = identity
    compile_breakpoint: Callable = identity


class StdLib:
    def __init__(
            self,
            compile_callbacks: Optional[StdLibCompileCallbacks] = None
    ):
        if not compile_callbacks:
            compile_callbacks = StdLibCompileCallbacks()

        self.compile_callbacks = compile_callbacks
        dict_object = self.dict_get()
        datetime_object = self.datetime()
        timestamp_object = self.timestamp()
        bytes_object = self.bytes()
        list_object = self.list()
        map_object = self.map()
        set_object = self.set()
        big_map_object = self.big_map()
        nat_object = self.nat()
        int_object = self.int()
        option_object = self.option()
        tezos_object = self.tezos()
        self.constants_mapping = {
            "SENDER": self.sender(),
            "SELF_ADDRESS": self.self_address(),
            "SOURCE": self.source(),
            "AMOUNT": self.amount(),
            "BALANCE": self.balance(),
            "Unit": self.unit(),
            "dic_get": dict_object,
            "abs": self.abs(),
            "datetime": datetime_object,
            "timedelta": self.timedelta(),
            "breakpoint": self.breakpoint(),
            "transaction": self.transaction(),
            "Contract": self.contract(),
            "Bytes": bytes_object,
            "String": self.string(),
            "Mutez": self.mutez(),
            "Nat": self.nat(),
            "Int": int_object,
            "Address": self.address(),
            "Timestamp": timestamp_object,
            "List": list_object,
            "Map": map_object,
            "Set": set_object,
            "BigMap": big_map_object,
            "Option": option_object,
            "Tezos": tezos_object,
        }
        self.types_mapping = {
            t.Set: set_object,
            t.Dict: map_object,
            t.BigMap: big_map_object,
            t.Datetime: timestamp_object,
            t.Bytes: bytes_object,
            t.List: list_object,
            t.Nat: nat_object,
            t.Int: int_object,
            t.Operations: self.operations(),
            t.Option: self.option(),
        }

    def option(self):
        option_constructor = StdlibFunctionSpec(
            self.compile_callbacks.compile_option,
            lambda element_types: FunctionPrototype(
                element_types[0],
                t.Option(element_types[0]),
            )
        )
        option_get = StdlibFunctionSpec(
            self.compile_callbacks.compile_option_get,
            lambda el_type: FunctionPrototype(
                t.PythonString(),
                el_type.option_type,
            )
        )
        option_get_with_default = StdlibFunctionSpec(
            self.compile_callbacks.compile_option_get_with_default,
            lambda el_type: FunctionPrototype(
                el_type.option_type,
                el_type.option_type,
            )
        )
        option_object = StdLibClassSpec()
        option_object.create_constructor(option_constructor)
        option_object.create_method("get", option_get)
        option_object.create_method("get_with_default", option_get_with_default)

        return option_object

    def list(self):
        list_constructor = StdlibFunctionSpec(
            self.compile_callbacks.list,
            lambda element_types: FunctionPrototype(
                t.Spread(element_types[0]),
                t.List(element_types[0]),
            )
        )
        list_prepend = StdlibFunctionSpec(
            self.compile_callbacks.list_prepend,
            lambda el_type: FunctionPrototype(
                el_type,
                t.List(el_type),
            )
        )
        list_object = StdLibClassSpec()
        list_object.create_constructor(list_constructor)
        list_object.create_method("prepend", list_prepend, False)

        return list_object

    def big_map(self):
        def big_map_constructor_cb(element_types):
            return FunctionPrototype(
                t.Unit(),
                t.BigMap(element_types[0].get_attribute_type("0"), element_types[0].get_attribute_type("1")),
            )
        big_map_constructor = StdlibFunctionSpec(
            self.compile_callbacks.big_map,
            big_map_constructor_cb,
        )
        big_map_set = StdlibFunctionSpec(
            self.compile_callbacks.map_set,
            lambda el_type: FunctionPrototype(
                el_type,
                t.BigMap(el_type.key_type, el_type.value_type),
            )
        )
        big_map_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda big_map_type: FunctionPrototype(
                big_map_type.key_type,
                big_map_type.value_type,
            )
        )
        big_map_object = StdLibClassSpec()
        big_map_object.create_constructor(big_map_constructor)
        big_map_object.create_method("get", big_map_get)
        big_map_object.create_method("add", big_map_set, False)

        return big_map_object

    def set(self):
        set_constructor = StdlibFunctionSpec(
            self.compile_callbacks.set,
            lambda element_types: FunctionPrototype(
                t.Spread(element_types[0]),
                t.Set(element_types[0]),
            )
        )
        set_add = StdlibFunctionSpec(
            self.compile_callbacks.set_add,
            lambda el_type: FunctionPrototype(
                el_type,
                t.Set(el_type),
            )
        )
        set_remove = StdlibFunctionSpec(
            self.compile_callbacks.set_remove,
            lambda el_type: FunctionPrototype(
                el_type,
                t.Set(el_type),
            )
        )
        set_object = StdLibClassSpec()
        set_object.create_constructor(set_constructor)
        set_object.create_method("add", set_add, False)
        set_object.create_method("remove", set_remove, False)

        return set_object

    def map(self):
        map_constructor = StdlibFunctionSpec(
            self.compile_callbacks.map,
            lambda element_types: FunctionPrototype(
                t.Unit(),
                t.Dict(element_types[0].get_attribute_type("0"), element_types[0].get_attribute_type("1")),
            )
        )
        map_set = StdlibFunctionSpec(
            self.compile_callbacks.map_set,
            lambda el_type: FunctionPrototype(
                el_type,
                t.Dict(el_type.key_type, el_type.value_type),
            )
        )
        map_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda map_type: FunctionPrototype(
                map_type.key_type,
                map_type.value_type,
            )
        )
        map_object = StdLibClassSpec()
        map_object.create_constructor(map_constructor)
        map_object.create_method("get", map_get)
        map_object.create_method("add", map_set, False)

        return map_object

    def tezos(self):
        amount = StdlibVariable(t.Mutez(), self.compile_callbacks.amount)
        sender = StdlibVariable(t.Address(), self.compile_callbacks.sender)
        source = StdlibVariable(t.Address(), self.compile_callbacks.source)
        self_address = StdlibVariable(t.Address(), self.compile_callbacks.self_address)
        balance = StdlibVariable(t.Mutez(), self.compile_callbacks.balance)
        tezos_object = StdLibClassSpec()
        tezos_object.create_attribute("amount", amount)
        tezos_object.create_attribute("sender", sender)
        tezos_object.create_attribute("source", source)
        tezos_object.create_attribute("self_address", self_address)
        tezos_object.create_attribute("balance", balance)

        return tezos_object

    def sender(self):
        return StdlibVariable(t.Address(), self.compile_callbacks.sender)

    def self_address(self):
        return StdlibVariable(t.Address(), self.compile_callbacks.self_address)

    def source(self):
        return StdlibVariable(t.Address(), self.compile_callbacks.source)

    def amount(self):
        return StdlibVariable(t.Mutez(), self.compile_callbacks.amount)

    def balance(self):
        return StdlibVariable(t.Mutez(), self.compile_callbacks.balance)

    def unit(self):
        return StdlibVariable(t.Unit(), self.compile_callbacks.unit)

    def unit(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.unit,
            lambda _: MultiArgFunctionPrototype(
                _,
                t.Unit()
            )
        )

    def breakpoint(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.compile_breakpoint,
            lambda: FunctionPrototype(
                t.Unit(),
                t.Unit()
            )
        )


    def timestamp(self):
        timestamp_constructor = StdlibFunctionSpec(
            self.compile_callbacks.datetime_from_timestamp,
            lambda _: FunctionPrototype(
                t.PythonInt(),
                t.Datetime()
            )
        )
        timestamp_now = StdlibFunctionSpec(
            self.compile_callbacks.datetime_now,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Datetime()
            )
        )
        timestamp_object = StdLibClassSpec()
        timestamp_object.create_constructor(timestamp_constructor)
        timestamp_object.create_method("now", timestamp_now, True)

        return timestamp_object

    def datetime(self):
        """Obselete"""
        datetime_constructor = StdlibFunctionSpec(
            self.compile_callbacks.datetime,
            lambda _: MultiArgFunctionPrototype(
                [t.PythonInt(), t.PythonInt(), t.PythonInt(), t.PythonInt(), t.PythonInt()],
                t.Datetime()
            )
        )
        datetime_now = StdlibFunctionSpec(
            self.compile_callbacks.datetime_now,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Datetime()
            ),
        )
        datetime_object = StdLibClassSpec()
        datetime_object.create_constructor(datetime_constructor)
        datetime_object.create_method("now", datetime_now, True)

        return datetime_object

    def dict_get(self):
        dict_get = StdlibFunctionSpec(
            self.compile_callbacks.dict_safe,
            lambda dict_type: FunctionPrototype(
                t.Unit(),
                dict_type.value_type,
            )
        )
        dict_object = StdLibClassSpec()
        dict_object.create_method("get", dict_get)
        return dict_object

    def abs(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.abs,
            lambda: FunctionPrototype(
                t.Int(),
                t.Nat()
            )
        )

    def bytes(self):
        bytes_constructor = StdlibFunctionSpec(
            self.compile_callbacks.pack,
            lambda _: FunctionPrototype(
                t.Unknown(),
                t.Bytes()
            )
        )
        bytes_unpack = StdlibFunctionSpec(
            self.compile_callbacks.unpack,
            lambda ty: FunctionPrototype(
                ty,
                ty
            )
        )
        bytes_blake2b = StdlibFunctionSpec(
            self.compile_callbacks.blake2b,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Bytes()
            )
        )

        bytes_object = StdLibClassSpec()
        bytes_object.create_constructor(bytes_constructor)
        bytes_object.create_method("unpack", bytes_unpack, False)
        bytes_object.create_method("blake2b", bytes_blake2b, False)

        return bytes_object

    def timedelta(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.timedelta,
            lambda: MultiArgFunctionPrototype(
                [t.Int(), t.Int(), t.Int(), t.Int(), t.Int()],
                t.Int()
            )
        )

    def transaction(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.transaction,
            lambda contract_type: MultiArgFunctionPrototype(
                [t.Contract([contract_type]), t.Mutez(), contract_type],
                t.Operation()
            )
        )

    def operations(self):
        push = StdlibFunctionSpec(
            self.compile_callbacks.push_operation,
            lambda contract_type: MultiArgFunctionPrototype(
                [t.Contract(contract_type), t.Mutez(), contract_type],
                t.Operations(),
            )
        )

        operations_object = StdLibClassSpec()
        operations_object.create_method("push", push, False)

        return operations_object

    def contract(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.contract,
            lambda contract_type: FunctionPrototype(
                [t.Address()],
                t.Contract(contract_type)
            )
        )

    def mutez(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.mutez,
            lambda: FunctionPrototype(t.PythonInt(), t.Mutez())
        )

    def nat(self):
        nat_constructor = StdlibFunctionSpec(
            self.compile_callbacks.nat,
            lambda _: FunctionPrototype(
                t.PythonInt(),
                t.Nat()
            )
        )
        to_int = StdlibFunctionSpec(
            self.compile_callbacks.to_int,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Int(),
            )
        )

        nat_object = StdLibClassSpec()
        nat_object.create_constructor(nat_constructor)
        nat_object.create_method("to_int", to_int, False)

        return nat_object

    def int(self):
        int_constructor = StdlibFunctionSpec(
            self.compile_callbacks.int,
            lambda _: FunctionPrototype(
                t.PythonInt(),
                t.Int()
            )
        )
        is_nat = StdlibFunctionSpec(
            self.compile_callbacks.is_nat,
            lambda _: FunctionPrototype(
                t.Unit(),
                t.Option(t.Nat()),
            )
        )

        int_object = StdLibClassSpec()
        int_object.create_constructor(int_constructor)
        int_object.create_method("is_nat", is_nat, False)

        return int_object

    def string(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.string,
            lambda: FunctionPrototype(t.PythonString(), t.String())
        )

    def address(self):
        return StdlibFunctionSpec(
            self.compile_callbacks.address,
            lambda: FunctionPrototype(t.PythonString(), t.Address())
        )
