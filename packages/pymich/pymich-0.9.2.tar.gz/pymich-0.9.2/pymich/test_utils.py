import pprint
import unittest
from contextlib import contextmanager
from typing import List, Tuple

from pytezos.context.impl import ExecutionContext
from pytezos.michelson.repl import InterpreterResult
from pytezos.michelson.sections import CodeSection
from pytezos import ContractInterface
from pytezos.michelson.stack import MichelsonStack
from pytezos.michelson.micheline import MichelsonRuntimeError
from pytezos.crypto.key import Key
from pytezos.contract.call import ContractCall
from pytezos.michelson.sections.storage import StorageSection
from pytezos.michelson.repl import Interpreter
from pytezos.logging import logger
from pytezos.michelson.types.map import MapType
from pytezos.michelson.types.base import MichelsonType

from pymich.compiler import Compiler


def callback_view(self, storage=None):
    """ Get return value of an on-chain callback method

    :storage: current storage
    :returns: Decoded parameters of a callback
    """
    if self.address:
        initial_storage = self.shell.blocks[self.context.block_id].context.contracts[self.address].storage()
    elif storage is not None:
        storage_ty = StorageSection.match(self.context.storage_expr)
        initial_storage = storage_ty.from_python_object(storage).to_micheline_value(lazy_diff=True)
    else:
        storage_ty = StorageSection.match(self.context.storage_expr)
        initial_storage = storage_ty.dummy(self.context).to_micheline_value(lazy_diff=True)

    operations, _, stdout, error = Interpreter.run_callback(
        parameter=self.parameters['value'],
        entrypoint=self.parameters['entrypoint'],
        storage=initial_storage,
        context=self.context
    )
    if not len(operations) == 1:
        raise Exception('Multiple internal operations, not sure which one to pick')
    if error:
        logger.debug('\n'.join(stdout))
        raise error
    return operations[0]

ContractCall.callback_view = callback_view


@classmethod
def check_constraints(cls, items: List[Tuple[MichelsonType, MichelsonType]] = None):
    keys = list(map(lambda x: x[0], items))
    assert len(set(keys)) == len(keys), f'duplicate keys found'

MapType.check_constraints = check_constraints


class VM:
    def __init__(
            self,
            sender = "tz3M4KAnKF2dCSjqfa1LdweNxBGQRqzvPL88",
            self_address = "KT1RAAQNZbqtJvMYc9ZRg2WXhK8vRsGJZ11z"
        ):
        self.reset_stack()
        self.context = ExecutionContext()
        self.set_sender(sender)
        self.set_self_address(self_address)

    def execute(self, micheline):
        self.result = InterpreterResult(stdout=[])
        code_section = CodeSection.match(micheline)
        try:
            code_section.args[0].execute(self.stack, self.result.stdout, self.context)
        except Exception as e:
            pprint.pprint(self.result.stdout)
            raise e

        return self

    def load_contract(self, micheline):
        self.contract = ContractInterface.from_micheline(micheline)
        return self

    def reset_stack(self):
        self.stack = MichelsonStack()
        return self

    def set_sender(self, sender):
        self.context.sender = sender
        return self

    def set_self_address(self, self_address):
        self.context.address = self_address
        return self

    def stdout(self):
        print("\n".join(self.result.stdout))
        return self


class TestContract(unittest.TestCase):
    contract_path = ""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        with open(self.contract_path) as f:
            source = f.read()

        self.compiler = Compiler(source)
        self.micheline = self.compiler.compile_contract()
        self.vm = VM()
        self.vm.load_contract(self.micheline)
        self.contract = self.vm.contract

    def tearDown(self):
        pass

    @contextmanager
    def raisesMichelsonError(self, error_message):
        with self.assertRaises(MichelsonRuntimeError) as r:
            yield r

        error_msg = r.exception.format_stdout()
        if "FAILWITH" in error_msg:
            self.assertEqual(f"FAILWITH: '{error_message}'", r.exception.format_stdout())
        else:
            self.assertEqual(f"'{error_message}': ", r.exception.format_stdout())

    def make_test_account(self):
        key = Key.generate(export=False)
        return key.public_key_hash()

    def make_n_test_accounts(self, n):
        return (self.make_test_account() for _ in range(n))
