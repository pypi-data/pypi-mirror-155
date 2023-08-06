import logging
from copy import deepcopy
from pymich.middle_end.ir.vm_types import Instr, Contract
import pymich.middle_end.ir.instr_types as t
from pymich.middle_end.ir import vm_types
from typing import List, Optional, Type, Callable
from pymich.middle_end.ir.typechecker import TypeChecker

from pymich.utils.exceptions import InvalidMichelsonException, MichelsonTypecheckerException, StackLengthException, StackTopTypeException, TypeException
import pymich.utils.exceptions as E



def simplify_type(el_type):
    if isinstance(el_type, (t.FunctionPrototype, vm_types.FunctionPrototype)):
        return t.Callable(simplify_type(el_type.arg_type), simplify_type(el_type.return_type))
    if isinstance(el_type, t.Record):
        return simplify_type(el_type.get_type())
    if isinstance(el_type, t.Pair):
        return t.Pair(simplify_type(el_type.car), simplify_type(el_type.cdr))
    else:
        return el_type


class StackType:
    def __init__(self, stack_type: Optional[List[t.Type]] = None):
        if not stack_type:
            self._stack_type = []
        else:
            self._stack_type = stack_type

    def replace_stack(self, new_stack: "StackType"):
        self._stack_type = new_stack._stack_type

    def protect_stack_top(self, depth: int):
        if depth > 0:
            self._protected_stack_top = self._stack_type[-depth:]
            self._stack_type = self._stack_type[:-depth]
        else:
            self._protected_stack_top = []

    def restore_stack_top(self):
        self._stack_type = self._stack_type + self._protected_stack_top

    def reset(self):
        self._stack_type = []

    def push_type(self, element_type: t.Type):
        self._stack_type.append(element_type)

    def pop(self):
        if not len(self._stack_type):
            raise StackLengthException(f"Cannot pop an empty stack.")

        el = self._stack_type[-1]
        del self._stack_type[-1]
        return el

    def del_at_depth(self, depth: int):
        del self._stack_type[-depth - 1]

    def get_at_depth(self, depth: int):
        stack_length = len(self._stack_type)
        if stack_length < depth:
            raise StackLengthException(
                f"Stack too short ({stack_length}) to get element at depth {depth}."
            )

        return self._stack_type[-depth - 1]

    def insert_at_depth(self, element: Type, depth: int):
        stack_length = len(self._stack_type)
        if stack_length < depth:
            raise StackLengthException(
                f"Stack too short ({stack_length}) to get element at depth {depth}."
            )

        self._stack_type.insert(-depth, element)

    @property
    def stack_type(self):
        return self._stack_type

    def __len__(self):
        return len(self._stack_type)

    def __eq__(self, other: "StackType"):
        is_universal = lambda s: len(s) and s.get_at_depth(0) == t.Universal()
        if is_universal(self) or is_universal(other):
            return True
        return self._stack_type == other._stack_type

    def __str__(self):
        acc = "\n=== STACK ===\n"
        for i, el_type in enumerate(reversed(self._stack_type)):
            acc += str(i) + " -- " + str(el_type) + "\n"
        return str(acc)[:-1]

    def __repr__(self):
        return str(self._stack_type)

    def assert_min_length(self, min_stack_length: int, error_message=""):
        if len(self.stack_type) < min_stack_length:
            raise StackLengthException(error_message)

    def assert_length_greater_than(self, stack_length: int, error_message=""):
        if len(self.stack_type) < stack_length:
            raise StackLengthException(error_message)

    def assert_length(self, stack_length: int, error_message=""):
        if len(self.stack_type) != stack_length:
            raise StackLengthException(error_message)

    def assert_top_type(self, stack_top_type: List[t.Type], error_message=""):
        self.assert_min_length(len(stack_top_type), error_message)
        for i, element_type in enumerate(stack_top_type):
            if self._stack_type[-(i + 1)] != element_type:
                raise E.StackTopTypeException(
                    "",
                    stack_top_type,
                    self._stack_type[:-len(stack_top_type)],
                    error_message,
                )


def default_prepare_stack_for_branch(is_true_branch: bool, temp_stack: StackType) -> StackType:
    temp_stack.pop()
    return temp_stack

def generic_if(
        instruction_name: str,
        instruction: Instr,
        operand_type: Type[t.Type],
        stack: StackType,
        prepare_stack_for_branch: Optional[Callable[[bool, StackType], StackType]] = None,
    ):
    stack.assert_min_length(1, f"Cannot call {instruction_name} on an empty stack.")
    if isinstance(stack.get_at_depth(0), operand_type):
        if (
            len(instruction.args) == 2
            and isinstance(instruction.args[0], list)
            and isinstance(instruction.args[1], list)
        ):
            branch_true = instruction.args[0]
            branch_false = instruction.args[1]

            prepare_stack = prepare_stack_for_branch if prepare_stack_for_branch else default_prepare_stack_for_branch

            typechecker = MichelsonTypeChecker()

            # True branch
            temp_stack = deepcopy(stack)
            temp_stack = prepare_stack(True, temp_stack)
            typechecker.typecheck(init_stack_type=deepcopy(temp_stack), instructions=branch_true)
            stack_branch_true = typechecker.stack

            # False branch
            temp_stack = deepcopy(stack)
            temp_stack = prepare_stack(False, temp_stack)
            typechecker.typecheck(init_stack_type=deepcopy(temp_stack), instructions=branch_false)
            stack_branch_false = typechecker.stack

            if len(stack_branch_true) and isinstance(stack_branch_true.get_at_depth(0), t.Universal):
                stack_branch_true.replace_stack(stack_branch_false)

            if len(stack_branch_false) and isinstance(stack_branch_false.get_at_depth(0), t.Universal):
                stack_branch_false.replace_stack(stack_branch_true)

            if stack_branch_true != stack_branch_false:
                raise E.ConditionBranchesTypeMismatch(
                    stack_branch_false,
                    stack_branch_true,
                )
            else:
                stack.replace_stack(stack_branch_true)
        else:
            raise InvalidMichelsonException(
                f"{instruction_name} only accepts 2 code sequences are arguments."
            )
    else:
        raise E.StackTopTypeException(
            instruction_name,
            operand_type,
            stack.get_at_depth(0),
        )


class TypeChecker:
    def __init__(
        self,
        stack: Optional[StackType] = None,
        instructions: Optional[List[Instr]] = None,
    ):
        if instructions is None:
            self.instructions = []
        else:
            self.instructions = instructions

        if stack is None:
            self.stack = StackType()
        else:
            self.stack = stack

    def assert_valid_michelson(self, cond: bool, message = ""):
        if not cond:
            raise InvalidMichelsonException(message)

    def assert_el_has_constructor_type(self, el: Type, constructor_type: Type[t.Type], message = ""):
        if not isinstance(el, constructor_type):
            raise TypeException(el, constructor_type, 0)

    def assert_type(self, el: Type, should_be: Type, message = ""):
        if el != should_be:
            raise TypeException(el, should_be, 0)


class ConstantsTypeChecker(TypeChecker):
    def typecheck_unit(self):
        self.stack.push_type(t.Unit())

    def typecheck_self_address(self):
        self.stack.push_type(t.Address())

    def typecheck_sender(self):
        self.stack.push_type(t.Address())

    def typecheck_source(self):
        self.stack.push_type(t.Address())

    def typecheck_amount(self):
        self.stack.push_type(t.Mutez())

    def typecheck_balance(self):
        self.stack.push_type(t.Mutez())


class ComparaisonOperatorTypeChecker(TypeChecker):
    def typecheck_operator(self):
        self.stack.assert_min_length(1, "GT requires a minimum stack depth of 1.")
        number = self.stack.pop()
        if number == t.Int():
            self.stack.push_type(t.Bool())
        else:
            raise E.StackTopTypeException(
                "(LT|LE|EQ|GE|GT)",
                [t.Int()],
                [number],
            )



class BooleanTypeChecker(TypeChecker):
    def typecheck_or(self):
        self.stack.assert_min_length(2, "OR requires a minimum stack depth of 2.")
        first_operand = self.stack.pop()
        second_operand = self.stack.pop()
        if first_operand == t.Bool() and second_operand == t.Bool():
            self.stack.push_type(t.Bool())
        else:
            raise E.OperandException(
                "OR",
                [t.Bool()],
                [first_operand, second_operand],
            )

    def typecheck_not(self):
        self.stack.assert_min_length(1, "NOT requires a minimum stack depth of 1.")
        operand = self.stack.pop()
        if operand == t.Bool():
            self.stack.push_type(t.Bool())
        else:
            raise E.OperandException(
                "NOT",
                [t.Bool()],
                [operand],
            )

    def typecheck_and(self):
        self.stack.assert_min_length(2, "AND requires a minimum stack depth of 2.")
        first_operand = self.stack.pop()
        second_operand = self.stack.pop()
        if first_operand == t.Bool() and second_operand == t.Bool():
            self.stack.push_type(t.Bool())
        else:
            raise E.OperandException(
                "AND",
                [t.Bool()],
                [first_operand, second_operand],
            )


    def typecheck_xor(self):
        self.stack.assert_min_length(2, "XOR requires a minimum stack depth of 2.")
        first_operand = self.stack.pop()
        second_operand = self.stack.pop()
        if first_operand == t.Bool() and second_operand == t.Bool():
            self.stack.push_type(t.Bool())
        else:
            raise E.OperandException(
                "XOR",
                [t.Bool()],
                [first_operand, second_operand],
            )




class IntOrNatTypeChecker(TypeChecker):
    def typecheck_neg(self):
        self.stack.assert_min_length(1, "ADD requires a minimum stack depth of 2.")
        number = self.stack.get_at_depth(0)
        if number == t.Int() or number == t.Nat():
            self.stack.pop()
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "ABS",
                [t.Union([t.Int(), t.Nat()])],
                [number],
            )


    def typecheck_abs(self):
        self.stack.assert_min_length(1, "You cannot call ABS on an empty stack.")
        number = self.stack.get_at_depth(0)
        if number == t.Int():
            self.stack.pop()
            self.stack.push_type(t.Nat())
        else:
            raise E.StackTopTypeException(
                "ABS",
                [t.Int()],
                [number],
            )


    def typecheck_is_nat(self):
        self.stack.assert_min_length(1, "You cannot call IS_NAT on an empty stack.")
        number = self.stack.get_at_depth(0)
        if number == t.Int():
            self.stack.pop()
            self.stack.push_type(t.Option(t.Nat()))
        else:
            raise E.StackTopTypeException(
                "IS_NAT",
                [t.Int()],
                [number],
            )


    def typecheck_int(self):
        self.stack.assert_min_length(1, "You cannot call INT on an empty stack.")
        number = self.stack.get_at_depth(0)
        if number == t.Nat():
            self.stack.pop()
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "INT",
                [t.Int()],
                [number],
            )


    def typecheck_add(self):
        self.stack.assert_min_length(2, "ADD requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Int() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "ADD",
                [t.Nat(), t.Int()],
                [first_operand, second_operand],
            )

    def typecheck_sub(self):
        self.stack.assert_min_length(2, "SUB requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Int() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        else:
            raise E.OperandException(
                "SUB",
                [t.Nat(), t.Int()],
                [first_operand, second_operand],
            )

    def typecheck_mul(self):
        self.stack.assert_min_length(2, "MUL requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Int() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "MUL",
                [t.Nat(), t.Int()],
                [first_operand, second_operand],
            )

    def typecheck_ediv(self):
        self.stack.assert_min_length(2, "EDIV requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Int() and second_operand == t.Int():
            self.stack.push_type(t.Option(t.Pair(t.Int(), t.Nat())))
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Option(t.Pair(t.Int(), t.Nat())))
        elif first_operand == t.Nat() and second_operand == t.Int():
            self.stack.push_type(t.Option(t.Pair(t.Int(), t.Nat())))
        elif first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Option(t.Pair(t.Nat(), t.Nat())))
        else:
            raise E.OperandException(
                "EDIV",
                [t.Nat(), t.Int()],
                [first_operand, second_operand],
            )

    def typecheck_or(self):
        self.stack.assert_min_length(2, "OR requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "EDIV",
                t.Nat(),
                [first_operand, second_operand],
            )

    def typecheck_and(self):
        self.stack.assert_min_length(2, "AND requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "AND",
                t.Nat(),
                [first_operand, second_operand],
                "also available when the top operand is signed",
            )

    def typecheck_xor(self):
        self.stack.assert_min_length(2, "XOR requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "XOR",
                t.Nat(),
                [first_operand, second_operand],
            )

    def typecheck_not(self):
        self.stack.assert_min_length(2, "NOT requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Nat() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Int() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        else:
            raise E.OperandException(
                "NOT",
                [t.Int(), t.Nat()],
                [first_operand, second_operand],
            )

    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Int() and second_operand == t.Int():
            self.stack.push_type(t.Int())
        elif first_operand == t.Nat() and second_operand == t.Nat():
            self.stack.push_type(t.Int())
        else:
            raise E.OperandException(
                "COMPARE",
                [t.Int(), t.Nat()],
                [first_operand, second_operand],
            )


class UnionTypeChecker(TypeChecker):
    def typecheck_left(self, instruction: Instr):
        self.stack.assert_min_length(1, "LEFT requires a non empty stack.")
        instruction.assert_n_args(1, "LEFT requires a type as unique argument.")
        instruction.assert_arg_type(0, t.Type, "LEFT requires a type as unique argument.")

        left_type = self.stack.get_at_depth(0)
        right_type = instruction.args[0]
        self.stack.pop()
        self.stack.push_type(t.Or(left_type, right_type))

    def typecheck_right(self, instruction: Instr):
        self.stack.assert_min_length(1, "RIGHT requires a non empty stack.")
        instruction.assert_n_args(1, "RIGHT requires a type as unique argument.")
        instruction.assert_arg_type(0, t.Type, "RIGHT requires a type as unique argument.")

        right_type = self.stack.get_at_depth(0)
        left_type = instruction.args[0]
        self.stack.pop()
        self.stack.push_type(t.Or(left_type, right_type))

    def typecheck_if_left(self, instruction):
        def prepare_stack(is_true_branch: bool, temp_stack: StackType) -> StackType:
            union = temp_stack.get_at_depth(0)
            temp_stack.pop()
            if is_true_branch:
                temp_stack.push_type(union.left_type)
            else:
                temp_stack.push_type(union.right_type)

            return temp_stack
        generic_if("IF_LEFT", instruction, t.Or, self.stack, prepare_stack)


class DatetimeTypeChecker(TypeChecker):
    def typecheck_now(self):
        self.stack.push_type(t.Datetime())

    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        datetime_a = self.stack.get_at_depth(0)
        datetime_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if isinstance(datetime_a, t.Datetime) and isinstance(datetime_b, t.Datetime):
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.Datetime(), t.Datetime()],
                [datetime_b, datetime_a],
            )

    def typecheck_sub(self):
        self.stack.assert_min_length(2, "SUB requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Datetime() and second_operand == t.Datetime():
            self.stack.push_type(t.Int())
        else:
            raise E.OperandException(
                "SUB",
                [t.Datetime(), t.Datetime()],
                [first_operand, second_operand],
            )


class OptionTypeChecker(TypeChecker):
    def typecheck_some(self):
        self.stack.assert_min_length(1, "SOME requires a non empty stack.")
        el = self.stack.get_at_depth(0)
        self.stack.pop()
        self.stack.push_type(t.Option(el))

    def typecheck_none(self, instruction: Instr):
        instruction.assert_n_args(1, "NONE requires a type as unique argument.")
        instruction.assert_arg_type(0, t.Type, "NONE requires a type as unique argument.")
        self.stack.push_type(t.Option(instruction.args[0]))

    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        option_a = self.stack.get_at_depth(0)
        option_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if isinstance(option_a, t.Option) and isinstance(option_b, t.Option):
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.Option(t.Universal()), t.Option(t.Universal())],
                [option_b, option_a],
            )

    def typecheck_if_none(self, instruction):
        def prepare_stack(is_true_branch: bool, temp_stack: StackType) -> StackType:
            optional = temp_stack.pop()
            if is_true_branch:
                pass
            else:
                temp_stack.push_type(optional.option_type)

            return temp_stack
        generic_if("IF_NONE", instruction, t.Option, self.stack, prepare_stack)

class StringTypeChecker(TypeChecker):
    def typecheck_concat(self):
        self.stack.assert_min_length(2, "CONCAT requires a minimum stack depth of 2.")
        first_string = self.stack.get_at_depth(0)
        second_string = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_string == t.String() and second_string == t.String():
            self.stack.push_type(t.String())
        else:
            raise E.OperandException(
                "CONCAT",
                t.String(),
                [second_string, second_string],
            )

    def typecheck_size(self):
        self.stack.assert_min_length(1, "SIZE cannot be called on an empty stack.")
        string = self.stack.get_at_depth(0)
        self.stack.pop()
        if string == t.String():
            self.stack.push_type(t.Nat())
        else:
            raise E.OperandException(
                "SIZE",
                t.String(),
                string,
            )

    def typecheck_slice(self):
        self.stack.assert_min_length(3, "SLICE requires a stack of minimum length 3.")
        offset_a = self.stack.get_at_depth(0)
        offset_b = self.stack.get_at_depth(1)
        string = self.stack.get_at_depth(2)
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        if offset_a == t.Nat() and offset_b == t.Nat() and string == t.String():
            self.stack.push_type(t.Option(t.String()))
        else:
            raise E.OperandException(
                "SLICE",
                [t.String(), t.Nat(), t.Nat()],
                [string, offset_a, offset_b],
            )

    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        string_a = self.stack.get_at_depth(0)
        string_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if string_a == t.String() and string_b == t.String():
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.String(), t.String()],
                [string_b, string_a],
            )


class AddressTypeChecker(TypeChecker):
    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        address_a = self.stack.get_at_depth(0)
        address_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if address_a == t.Address() and address_b == t.Address():
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.Address(), t.Address()],
                [address_b, address_a],
            )


class MutezTypeChecker(TypeChecker):
    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        mutez_a = self.stack.get_at_depth(0)
        mutez_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if mutez_a == t.Mutez() and mutez_b == t.Mutez():
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.Mutez(), t.Mutez()],
                [mutez_b, mutez_a],
            )

    def typecheck_ediv(self):
        self.stack.assert_min_length(2, "EDIV requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Mutez() and second_operand == t.Mutez():
            self.stack.push_type(t.Option(t.Pair(t.Nat(), t.Mutez())))
        elif first_operand == t.Mutez() and second_operand == t.Nat():
            self.stack.push_type(t.Option(t.Pair(t.Mutez(), t.Mutez())))
        else:
            raise E.OperandException(
                "EDIV",
                [t.Mutez(), t.Mutez()],
                [first_operand, second_operand],
            )

    def typecheck_mul(self):
        self.stack.assert_min_length(2, "MUL requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Mutez() and second_operand == t.Nat():
            self.stack.push_type(t.Mutez())
        elif first_operand == t.Nat() and second_operand == t.Mutez():
            self.stack.push_type(t.Mutez())
        else:
            raise E.OperandException(
                "MUL",
                [t.Mutez(), t.Nat()],
                [first_operand, second_operand],
            )

    def typecheck_add(self):
        self.stack.assert_min_length(2, "ADD requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Mutez() and second_operand == t.Mutez():
            self.stack.push_type(t.Mutez())
        else:
            raise E.OperandException(
                "ADD",
                [t.Mutez(), t.Mutez()],
                [first_operand, second_operand],
            )

    def typecheck_sub_mutez(self):
        self.stack.assert_min_length(2, "SUB requires a minimum stack depth of 2.")
        first_operand = self.stack.get_at_depth(0)
        second_operand = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if first_operand == t.Mutez() and second_operand == t.Mutez():
            self.stack.push_type(t.Option(t.Mutez()))
        else:
            raise E.OperandException(
                "SUB",
                [t.Mutez(), t.Mutez()],
                [first_operand, second_operand],
            )


class PairTypeChecker(TypeChecker):
    def typecheck_pair(self):
        self.stack.assert_min_length(2, "PAIR requires a stack of minimum length 2.")
        car = self.stack.get_at_depth(0)
        cdr = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        self.stack.push_type(t.Pair(car, cdr))

    def typecheck_unpair(self):
        self.stack.assert_min_length(1, "UNPAIR requires a stack of minimum length 1.")
        pair = self.stack.pop()
        self.assert_el_has_constructor_type(pair, t.Pair)
        self.stack.push_type(pair.cdr)
        self.stack.push_type(pair.car)

    def typecheck_pair_n(self, n: int):
        self.assert_valid_michelson(n >= 2, "PAIR n requires `n` to be strictly geater than 1.")
        self.stack.assert_min_length(n, "PAIR n requires a stack of minimum length n.")

        args = []
        for i in range(n):
            args.append(self.stack.get_at_depth(i))
        right_comb = t.Pair.pair_n(args)

        for _ in range(n):
            self.stack.pop()

        self.stack.push_type(right_comb)

    def typecheck_car(self):
        self.stack.assert_min_length(1, "CAR requires a non empty stack.")
        pair = self.stack.get_at_depth(0)
        if isinstance(pair, t.Pair):
            self.stack.pop()
            self.stack.push_type(pair.car)
        else:
            raise E.StackTopTypeException(
                "CAR",
                [t.Pair(t.Universal(), t.Universal())],
                [pair],
            )

    def typecheck_cdr(self):
        self.stack.assert_min_length(1, "CDR requires a non empty stack.")
        pair = self.stack.get_at_depth(0)
        if isinstance(pair, t.Pair):
            self.stack.pop()
            self.stack.push_type(pair.cdr)
        else:
            raise E.StackTopTypeException(
                "CDR",
                [t.Pair(t.Universal(), t.Universal())],
                [pair],
            )

    def typecheck_get_n(self, n: int):
        self.stack.assert_min_length(1, "GET n requires a non empty stack.")
        pair = self.stack.get_at_depth(0)
        if isinstance(pair, t.Pair):
            self.stack.pop()
            self.stack.push_type(pair.get_n(n))
        else:
            raise E.StackTopTypeException(
                "GET",
                [t.Pair(t.Universal(), t.Universal())],
                [pair],
            )

    def typecheck_update_n(self, n: int):
        self.stack.assert_min_length(2, "UPDATE n requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        pair = self.stack.get_at_depth(1)
        if isinstance(pair, t.Pair):
            self.stack.pop()
            self.stack.pop()
            self.stack.push_type(pair.update_n(element, n))
        else:
            raise E.StackTopTypeException(
                "UPDATE n",
                [t.Pair(t.Universal(), t.Universal())],
                [pair],
            )


class BytesTypeChecker(TypeChecker):
    def typecheck_pack(self):
        self.stack.assert_min_length(1, "PACK requires a non empty stack.")
        self.stack.pop()
        self.stack.push_type(t.Bytes())

    def typecheck_unpack(self, instruction: Instr):
        self.stack.assert_min_length(1, "UNPACK requires a non empty stack.")

        instruction.assert_n_args(1, "UNPACK requires a type as unique argument.")
        instruction.assert_arg_type(0, t.Type, "UNPACK requires a type as unique argument.")
        unpack_type = t.Option(instruction.args[0])

        self.stack.pop()
        self.stack.push_type(unpack_type)

    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of minimum length 2.")
        bytes_a = self.stack.get_at_depth(0)
        bytes_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if bytes_a == t.Bytes() and bytes_b == t.Bytes():
            self.stack.push_type(t.Int())
        else:
            raise E.StackTopTypeException(
                "COMPARE",
                [t.Bytes(), t.Bytes()],
                [bytes_b, bytes_a],
            )

    def typecheck_concat(self):
        self.stack.assert_min_length(2, "CONCAT requires a stack of minimum length 2.")
        bytes_a = self.stack.get_at_depth(0)
        bytes_b = self.stack.get_at_depth(1)
        self.stack.pop()
        self.stack.pop()
        if bytes_a == t.Bytes() and bytes_b == t.Bytes():
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "CONCAT",
                [t.Bytes(), t.Bytes()],
                [bytes_b, bytes_a],
            )

    def typecheck_size(self):
        self.stack.assert_min_length(1, "SIZE cannot be called on an empty stack.")
        bytes_type = self.stack.get_at_depth(0)
        self.stack.pop()
        if bytes_type == t.Bytes():
            self.stack.push_type(t.Nat())
        else:
            raise E.StackTopTypeException(
                "SIZE",
                [t.Bytes()],
                [bytes_type],
            )

    def typecheck_slice(self):
        self.stack.assert_min_length(3, "SLICE requires a stack of minimum length 3.")
        offset_a = self.stack.get_at_depth(0)
        offset_b = self.stack.get_at_depth(1)
        string = self.stack.get_at_depth(2)
        self.stack.pop()
        self.stack.pop()
        self.stack.pop()
        if offset_a == t.Nat() and offset_b == t.Nat() and string == t.Bytes():
            self.stack.push_type(t.Option(t.Bytes()))
        else:
            raise E.StackTopTypeException(
                "SLICE",
                [t.Bytes(), t.Nat(), t.Nat()],
                [string, offset_b, offset_a],
            )


class CryptographicPrimitivesTypeChecker(TypeChecker):
    def typecheck_blake2b(self):
        self.stack.assert_min_length(1, "BLAKE2B requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        if element == t.Bytes():
            self.stack.pop()
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "BLAKE2B",
                [t.Bytes()],
                [element],
            )

    def typecheck_keccak(self):
        self.stack.assert_min_length(1, "KECCAK requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        if element == t.Bytes():
            self.stack.pop()
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "KECCAK",
                [t.Bytes()],
                [element],
            )

    def typecheck_sha256(self):
        self.stack.assert_min_length(1, "SHA256 requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        if element == t.Bytes():
            self.stack.pop()
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "SHA256",
                [t.Bytes()],
                [element],
            )

    def typecheck_sha512(self):
        self.stack.assert_min_length(1, "SHA512 requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        if element == t.Bytes():
            self.stack.pop()
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "SHA512",
                [t.Bytes()],
                [element],
            )

    def typecheck_sha3(self):
        self.stack.assert_min_length(1, "SHA3 requires a non empty stack.")
        element = self.stack.get_at_depth(0)
        if element == t.Bytes():
            self.stack.pop()
            self.stack.push_type(t.Bytes())
        else:
            raise E.StackTopTypeException(
                "SHA3",
                [t.Bytes()],
                [element],
            )

class SetTypeChecker(TypeChecker):
    def typecheck_empty_set(self, instruction: Instr):
        if len(instruction.args) != 1:
            raise InvalidMichelsonException("EMPTY_SET requires a type as only argument")

        for type_ in instruction.args:
            if not isinstance(type_, t.Type):
                raise InvalidMichelsonException(
                    "EMPTY_SET requires that the arguments are the element type."
                )

        self.stack.push_type(t.Set(instruction.args[0]))

    def typecheck_mem_set(self):
        self.stack.assert_min_length(
            2, "Cannot call MEM on a stack of length less than 2."
        )

        el_type = self.stack.get_at_depth(0)
        set_type = self.stack.get_at_depth(1)
        if isinstance(set_type, t.Set):
            if el_type != set_type.element_type:
                raise E.SetElementTypeException(
                    el_type,
                    set_type,
                )
            return_type = t.Bool()
            self.stack.pop()
            self.stack.pop()
            self.stack.push_type(return_type)
        else:
            raise E.StackTopTypeException(
                "MEM",
                [t.Set(t.Universal())],
                [set_type],
            )

    def typecheck_update_set(self):
        self.stack.assert_min_length(
            3, "Cannot call UPDATE on a stack of length less than 2."
        )

        el_type = self.stack.get_at_depth(0)
        direction_type = self.stack.get_at_depth(1)
        set_type = self.stack.get_at_depth(2)
        if isinstance(set_type, t.Set):
            wrong_stack_type = (
                not isinstance(direction_type, t.Bool)
                or el_type != set_type.element_type
            )
            if wrong_stack_type:
                raise E.StackTopTypeException(
                    "UPDATE",
                    [t.TypeVar(), t.Bool(), t.Set(t.TypeVar())],
                    [el_type, direction_type, set_type],
                )
            self.stack.pop()
            self.stack.pop()
        else:
            raise E.StackTopTypeException(
                "UPDATE",
                [t.TypeVar(), t.Bool(), t.Set(t.TypeVar())],
                [el_type, direction_type, set_type],
            )



class ListTypeChecker(TypeChecker):
    def typecheck_empty_list(self, instruction: Instr):
        if len(instruction.args) != 1:
            raise InvalidMichelsonException("NIL requires a type as only argument")

        for type_ in instruction.args:
            if not isinstance(type_, t.Type):
                raise InvalidMichelsonException(
                    "NIL requires that the arguments are the element type."
                )

        self.stack.push_type(t.List(instruction.args[0]))

    def typecheck_cons(self):
        self.stack.assert_min_length(2, "CONS requires a stack of minimum length 2.")

        element_type = self.stack.pop()
        list_type = self.stack.pop()
        if isinstance(list_type, (t.List, t.Operations)):
            if element_type != list_type.element_type:
                raise E.StackTopTypeException(
                    "CONS",
                    [list_type.element_type],
                    [element_type],
                )
            else:
                self.stack.push_type(list_type)
        else:
            raise E.StackTopTypeException(
                "CONS",
                [t.List(t.Universal())],
                [list_type],
            )

    def typecheck_size(self):
        self.stack.assert_min_length(1, "Cannot call SIZE on an empty stack.")

        list_type = self.stack.get_at_depth(0)
        if isinstance(list_type, t.List):
            self.stack.pop()
            self.stack.push_type(t.Nat())
        else:
            raise E.StackTopTypeException(
                "SIZE",
                [t.List(t.Universal())],
                [list_type],
            )

    def typecheck_iter(self, instruction: Instr):
        self.stack.assert_min_length(1, "Cannot call ITER on an empty stack.")

        self.assert_valid_michelson(
            len(instruction.args) == 1 and isinstance(instruction.args[0], list),
            "ITER must have a single argument that is a list of instructions."
        )
        iter_instructions = instruction.args[0]

        list_type = self.stack.pop()
        if isinstance(list_type, t.List):
            typechecker = MichelsonTypeChecker()
            old_length = len(self.stack)
            self.stack.push_type(list_type.element_type)
            typechecker.typecheck(self.stack, iter_instructions)

            self.stack.assert_length(old_length, "The body of an ITER must not change the stack length.")
        else:
            raise E.StackTopTypeException(
                "ITER",
                [t.List(t.Universal())],
                [list_type],
            )


class MapTypeChecker(TypeChecker):
    def typecheck_empty_map(self, instruction: Instr):
        if len(instruction.args) != 2:
            raise InvalidMichelsonException("EMPTY_MAP requires two arguments")

        for type_ in instruction.args:
            if not isinstance(type_, t.Type):
                raise InvalidMichelsonException(
                    "EMPTY_MAP requires that the arguments are the key and value types."
                )

        self.stack.push_type(t.Dict(instruction.args[0], instruction.args[1]))

    def typecheck_empty_big_map(self, instruction: Instr):
        if len(instruction.args) != 2:
            raise InvalidMichelsonException("EMPTY_MAP requires two arguments")

        for type_ in instruction.args:
            if not isinstance(type_, t.Type):
                raise InvalidMichelsonException(
                    "EMPTY_MAP requires that the arguments are the key and value types."
                )

        self.stack.push_type(t.BigMap(instruction.args[0], instruction.args[1]))

    def typecheck_get_map(self):
        self.stack.assert_min_length(
            2, "Cannot call GET on a stack of length less than 2."
        )

        key_type = self.stack.get_at_depth(0)
        map_type = self.stack.get_at_depth(1)
        if isinstance(map_type, (t.Dict, t.BigMap)):
            if key_type != map_type.key_type:
                raise E.MapKeyTypeException(
                    key_type,
                    map_type,
                )
            return_type = t.Option(map_type.value_type)
            self.stack.pop()
            self.stack.pop()
            self.stack.push_type(return_type)
        else:
            raise E.StackTopTypeException(
                "GET",
                [t.Dict(t.Universal(), t.Universal())],
                [map_type],
            )

    def typecheck_mem_map(self):
        self.stack.assert_min_length(
            2, "Cannot call MEM on a stack of length less than 2."
        )

        key_type = self.stack.get_at_depth(0)
        map_type = self.stack.get_at_depth(1)
        if isinstance(map_type, (t.Dict, t.BigMap)):
            if key_type != map_type.key_type:
                raise E.MapKeyTypeException(
                    key_type,
                    map_type,
                )
            return_type = t.Bool()
            self.stack.pop()
            self.stack.pop()
            self.stack.push_type(return_type)
        else:
            raise E.StackTopTypeException(
                "MEM",
                [t.Dict(t.Universal(), t.Universal())],
                [map_type],
            )


    def typecheck_update_map(self):
        self.stack.assert_min_length(
            3, "Cannot call UPDATE on a stack of length less than 2."
        )

        key_type = self.stack.get_at_depth(0)
        value_type = self.stack.get_at_depth(1)
        map_type = self.stack.get_at_depth(2)
        if isinstance(map_type, (t.Dict, t.BigMap)):
            if not isinstance(value_type, t.Option):
                raise E.MapValueTypeException(
                    f"{value_type}",
                    f"{t.Option(map_type.value_type)}",
                    f"Trying to update a `{map_type}` with a non optional of type `{value_type}`."
                )
            if key_type != map_type.key_type:
                raise E.MapKeyTypeException(
                    key_type,
                    map_type,
                )
            if value_type.option_type != map_type.value_type:
                raise E.MapValueTypeException(
                    key_type.option_type,
                    map_type,
                )
            self.stack.pop()
            self.stack.pop()
        else:
            raise E.StackTopTypeException(
                "UPDATE",
                [t.Dict(t.Universal(), t.Universal())],
                [map_type],
            )

    def typecheck_size(self):
        self.stack.assert_min_length(1, "Cannot call SIZE on an empty stack.")

        map_type = self.stack.get_at_depth(0)
        if isinstance(map_type, t.Dict):
            self.stack.pop()
            self.stack.push_type(t.Nat())
        else:
            raise E.StackTopTypeException(
                "SIZE",
                [t.Dict(t.Universal(), t.Universal())],
                [map_type],
            )


class TransactionTypeChecker(TypeChecker):
    def typecheck_contract(self, instruction: Instr):
        self.assert_valid_michelson(
            len(instruction.args) == 1
            and isinstance(instruction.args[0], t.Type),
            "CONTRACT takes the contract type as single argument"
        )
        cast_type = instruction.args[0]
        self.stack.assert_min_length(1, "CONTRACT requires a minimum stack length of 1.")
        address = self.stack.pop()
        if address != t.Address():
            raise E.StackTopTypeException(
                "CONTRACT",
                [t.Address()],
                [address],
            )
        self.stack.push_type(t.Option(t.Contract(cast_type)))

    def typecheck_transfer_tokens(self):
        self.stack.assert_min_length(3, "TRANSFER_TOKENS requires a minimum stack length of 3.")
        arg_type = self.stack.pop()
        mutez = self.stack.pop()
        contract = self.stack.pop()

        if not isinstance(contract, t.Contract):
            raise E.StackTopTypeException(
                "TRANSFER_TOKENS",
                [t.Contract(t.TypeVar()), t.Mutez(), t.TypeVar()],
                [contract, mutez, arg_type],
            )

        if arg_type != contract.param_type:
            raise E.StackTopTypeException(
                "TRANSFER_TOKENS",
                [t.Contract(t.TypeVar()), t.Mutez(), t.TypeVar()],
                [contract, mutez, arg_type],
            )

        self.assert_type(mutez, t.Mutez(), "Type of second topmost stack element when calling TRANSFER_TOKENS should be mutez.")

        self.stack.push_type(t.Operation())


class StackManipulationTypeChecker(TypeChecker):
    def typecheck_lambda(self, instruction: Instr):
        arg_type = instruction.args[0]
        return_type = instruction.args[1]
        function_body = instruction.args[2]

        typechecker = MichelsonTypeChecker(function_body)
        function_stack = StackType([arg_type])
        typechecker.typecheck(function_stack, function_body)

        function_stack.assert_length(1, "The body of a LAMBDA must return a stack of 1 element")
        function_stack.assert_top_type([return_type], "LAMBDA body does not return type matching its signature.")

        self.stack.push_type(t.Callable(arg_type, return_type, function_body))

    def typecheck_dig(self, instruction: Instr):
        if not len(instruction.args):
            raise InvalidMichelsonException("DIG takes an argument")
        if isinstance(instruction.args[0], int) and instruction.args[0] >= 0:
            depth = instruction.args[0]
            if not depth:
                return
            stack_length = len(self.stack)
            self.stack.assert_min_length(
                depth, f"Cannot call DIG {depth} on a stack of length {stack_length}."
            )
            element = self.stack.get_at_depth(depth)
            self.stack.del_at_depth(depth)
            self.stack.push_type(element)
        else:
            raise InvalidMichelsonException(
                "DIG only accepts a single integer greater than or equal to 0 as argument"
            )

    def typecheck_dug(self, instruction: Instr):
        if not len(instruction.args):
            raise InvalidMichelsonException("DUG takes an argument")
        if len(instruction.args) and isinstance(instruction.args[0], int) and instruction.args[0] >= 0:
            depth = instruction.args[0]
            if not depth:
                return
            stack_length = len(self.stack)
            self.stack.assert_min_length(
                depth, f"Cannot call DUG {depth} on a stack of length {stack_length}."
            )
            element = self.stack.pop()
            element = self.stack.insert_at_depth(element, depth)
        else:
            raise InvalidMichelsonException(
                "DUG only accepts a single integer greater than or equal to 0 as argument"
            )

    def typecheck_push(self, instruction: Instr):
        instruction.assert_n_args(2, "PUSH requires 2 arguments.")
        arg_type = instruction.args[0]
        arg_value = instruction.args[1]
        update_stack = lambda: self.stack.push_type(instruction.args[0])
        if arg_type == t.Int() and isinstance(arg_value, int):
            update_stack()
        elif arg_type == t.Nat() and isinstance(arg_value, int):
            update_stack()
        elif arg_type == t.String() and isinstance(arg_value, str):
            update_stack()
        elif arg_type == t.Mutez() and isinstance(arg_value, int):
            update_stack()
        elif arg_type == t.Address() and isinstance(arg_value, str):
            update_stack()
        elif arg_type == t.Bool() and isinstance(arg_value, bool):
            update_stack()
        else:
            raise E.PushTypeException()

    def typecheck_drop(self):
        self.stack.assert_min_length(1, "Cannot call DROP on an empty stack")
        self.stack.pop()

    def typecheck_dup(self, instruction: Instr):
        self.stack.assert_min_length(1, "Cannot call DUP on an empty stack")

        if len(instruction.args) == 0:
            self.stack.push_type(self.stack.get_at_depth(0))
        elif (
            len(instruction.args) == 1
            and isinstance(instruction.args[0], int)
            and instruction.args[0] > 0
        ):
            depth = instruction.args[0] - 1
            stack_length = len(self.stack)

            self.stack.assert_min_length(
                depth + 1,
                f"Cannot call DUP {depth} on a stack of length {stack_length}.",
            )
            self.stack.push_type(self.stack.get_at_depth(depth))
        else:
            raise InvalidMichelsonException(
                "DUP only accepts a single integer greater than 0 as argument"
            )


class ControlStructuresTypeChecker(TypeChecker):
    def typecheck_dip(self, instruction: Instr, typecheck):
        if (
            len(instruction.args) == 2
            and isinstance(instruction.args[0], int)
            and instruction.args[0] >= 0
        ):
            depth = instruction.args[0]
            instructions = instruction.args[1]

            self.stack.assert_min_length(depth, "Cannot call DIP n on a stack smaller than n")

            self.stack.protect_stack_top(depth)
            typecheck(init_stack_type=self.stack, instructions=instructions)
            self.stack.restore_stack_top()
        else:
            raise InvalidMichelsonException(
                "DIP only accepts a single integer greater or equal 0 as argument"
            )

    def typecheck_if(self, instruction: Instr):
        generic_if("IF", instruction, t.Bool, self.stack)

    def typecheck_exec(self, instruction: Instr):
        self.stack.assert_min_length(2, "LAMBDA requires a stack of minimum length 2.")
        arg_type = simplify_type(self.stack.pop())
        lambda_type = simplify_type(self.stack.pop())
        param_type = simplify_type(simplify_type(lambda_type).param_type)
        if arg_type != param_type:
            raise E.LambdaArgumentTypeException(arg_type, param_type)
        self.stack.push_type(lambda_type.return_type)

    def typecheck_apply(self):
        self.stack.assert_min_length(2, "EXEC requires a stack of minimum length 2.")

        partial_arg_type = simplify_type(self.stack.pop())
        lambda_type = simplify_type(self.stack.pop())

        stack_exception = E.StackTopTypeException(
            "APPLY",
            [t.Contract(t.TypeVar()), t.Mutez(), t.TypeVar()],
            [t.TypeVar("T"), t.Callable(t.Pair(t.TypeVar("T"), t.TypeVar("U")), t.TypeVar("V"))],
            [partial_arg_type, lambda_type],
        )
        if not isinstance(lambda_type, t.Callable) or not isinstance(lambda_type.param_type, t.Record):
            raise stack_exception

        arg_type = lambda_type.param_type.get_type()
        appliable_arg_type = simplify_type(arg_type.car)

        if appliable_arg_type != partial_arg_type:
            raise stack_exception
        else:
            lambda_type.param_type = arg_type.cdr
            lambda_type.applied_arg_types.append(partial_arg_type)
            self.stack.push_type(lambda_type)


class MichelsonTypeChecker(TypeChecker):
    def typecheck_mem(self):
        self.stack.assert_min_length(2, "MEM requires a stack of minimum length 2.")
        if isinstance(self.stack.get_at_depth(1), (t.Dict, t.BigMap)):
            MapTypeChecker(self.stack).typecheck_mem_map()
        elif isinstance(self.stack.get_at_depth(1), t.Set):
            SetTypeChecker(self.stack).typecheck_mem_set()
        else:
            raise E.StackTopTypeException(
                "MEM",
                [t.Union([t.Set(t.TypeVar()), t.Dict(t.TypeVar(), t.Universal()), t.BigMap(t.TypeVar(), t.Universal())]), t.TypeVar()],
                [self.stack.get_at_depth(1), self.stack.get_at_depth(0)],
            )

    def typecheck_get(self, instruction: Instr):
        if len(self.stack) >= 2 and isinstance(self.stack.get_at_depth(1), t.Dict) and not len(instruction.args):
            self.stack.assert_min_length(2, "Get applied to a map requires a stack of minimum length 2.")
            MapTypeChecker(self.stack).typecheck_get_map()
        elif len(self.stack) >= 2 and isinstance(self.stack.get_at_depth(1), t.BigMap) and not len(instruction.args):
            self.stack.assert_min_length(2, "Get applied to a map requires a stack of minimum length 2.")
            MapTypeChecker(self.stack).typecheck_get_map()
        elif len(self.stack) >= 1 and isinstance(self.stack.get_at_depth(0), t.Pair):
            self.stack.assert_min_length(1, "Get applied to a pair requires a stack of minimum length 1.")
            instruction.assert_n_args(1, "GET applied to a Pair requires an integer argument.")
            instruction.assert_arg_type(0, int, "GET applied to a Pair requires an integer argument.")
            PairTypeChecker(self.stack).typecheck_get_n(instruction.args[0])
        elif len(self.stack) >= 1 and isinstance(self.stack.get_at_depth(0), t.Record):
            self.stack.assert_min_length(1, "Get applied to a pair requires a stack of minimum length 1.")
            instruction.assert_n_args(1, "GET applied to a Pair requires an integer argument.")
            instruction.assert_arg_type(0, int, "GET applied to a Pair requires an integer argument.")
            record = self.stack.pop()
            self.stack.push_type(record.get_type())
            PairTypeChecker(self.stack).typecheck_get_n(instruction.args[0])
        else:
            get_on_iterable_allowed_stacks = [t.Union([t.List(t.TypeVar()), t.Dict(t.TypeVar(), t.Universal()), t.BigMap(t.TypeVar(), t.Universal())]), t.TypeVar()]
            get_on_pair_allowed_stacks = [t.Pair(t.Universal(), t.Universal())]
            allowed_stacks = t.Union([get_on_iterable_allowed_stacks, get_on_pair_allowed_stacks])
            raise E.StackTopTypeException(
                "GET",
                allowed_stacks,
                [self.stack.get_at_depth(1), self.stack.get_at_depth(0)],
            )

    def typecheck_update(self, instruction: Instr):
        if len(self.stack) >= 3 and isinstance(self.stack.get_at_depth(2), t.Dict) and not len(instruction.args):
            self.stack.assert_min_length(3, "UPDATE applied to a map requires a stack of minimum length 3.")
            MapTypeChecker(self.stack).typecheck_update_map()
        elif len(self.stack) >= 3 and isinstance(self.stack.get_at_depth(2), t.BigMap) and not len(instruction.args):
            self.stack.assert_min_length(3, "UPDATE applied to a map requires a stack of minimum length 3.")
            MapTypeChecker(self.stack).typecheck_update_map()
        elif len(self.stack) >= 3 and isinstance(self.stack.get_at_depth(2), t.Set) and not len(instruction.args):
            self.stack.assert_min_length(3, "UPDATE applied to a set requires a stack of minimum length 3.")
            SetTypeChecker(self.stack).typecheck_update_set()
        elif len(self.stack) >= 2 and isinstance(self.stack.get_at_depth(1), t.Pair) and len(self.stack) >= 2 and len(instruction.args) == 1:
            self.stack.assert_min_length(1, "UPDATE applied to a pair requires a stack of minimum length 2.")
            instruction.assert_n_args(1, "UPDATE applied to a Pair requires an integer argument.")
            instruction.assert_arg_type(0, int, "UPDATE applied to a Pair requires an integer argument.")
            PairTypeChecker(self.stack).typecheck_update_n(instruction.args[0])
        elif len(self.stack) >= 2 and isinstance(self.stack.get_at_depth(1), t.Record) and len(instruction.args) == 1:
            self.stack.assert_min_length(1, "UPDATE applied to a pair requires a stack of minimum length 2.")
            instruction.assert_n_args(1, "UPDATE applied to a Pair requires an integer argument.")
            instruction.assert_arg_type(0, int, "UPDATE applied to a Pair requires an integer argument.")
            argument = self.stack.pop()
            record = self.stack.pop()
            self.stack.push_type(record.get_type())
            self.stack.push_type(argument)
            PairTypeChecker(self.stack).typecheck_update_n(instruction.args[0])
        else:
            get_on_iterable_allowed_stacks = [
                t.Union([
                    t.Dict(t.TypeVar("T"), t.Universal("U")),
                    t.BigMap(t.TypeVar("T"), t.Universal("U"))
                ]),
                t.TypeVar("T"),
                t.TypeVar("U"),
            ]
            get_on_pair_allowed_stacks = [t.Pair(t.Universal(), t.Universal())]
            allowed_stacks = t.Union([get_on_iterable_allowed_stacks, get_on_pair_allowed_stacks])
            raise E.StackTopTypeException(
                "UPDATE",
                allowed_stacks,
                [self.stack.get_at_depth(1), self.stack.get_at_depth(0)],
            )

    def typecheck_size(self):
        self.stack.assert_min_length(1, "Cannot call SIZE on an empty stack.")
        if isinstance(self.stack.get_at_depth(0), t.Dict):
            MapTypeChecker(self.stack).typecheck_size()
        elif isinstance(self.stack.get_at_depth(0), t.String):
            StringTypeChecker(self.stack).typecheck_size()
        elif isinstance(self.stack.get_at_depth(0), t.Bytes):
            BytesTypeChecker(self.stack).typecheck_size()
        elif isinstance(self.stack.get_at_depth(0), t.List):
            ListTypeChecker(self.stack).typecheck_size()
        else:
            raise E.StackTopTypeException(
                "SIZE",
                [t.Union([t.List(t.Universal()), t.Set(t.Universal()), t.Dict(t.Universal(), t.Universal()), t.Dict(t.Universal(), t.Universal())])],
                [self.stack.get_at_depth(0)],
            )

    def typecheck_concat(self):
        self.stack.assert_min_length(2, "CONCAT requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.String) and isinstance(operand_b, t.String):
            StringTypeChecker(self.stack).typecheck_concat()
        elif isinstance(operand_a, t.Bytes) and isinstance(operand_b, t.Bytes):
            BytesTypeChecker(self.stack).typecheck_concat()
        else:
            raise E.OperandException(
                "CONCAT",
                [t.String(), t.Bytes()],
                [operand_a, operand_b],
            )


    def typecheck_slice(self):
        self.stack.assert_min_length(2, "SLICE requires a stack of length at least 2.")
        offset = self.stack.get_at_depth(0)
        length = self.stack.get_at_depth(1)
        element_type = self.stack.get_at_depth(2)
        if length == t.Nat() and offset == t.Nat() and element_type == t.String():
            StringTypeChecker(self.stack).typecheck_slice()
        elif length == t.Nat() and offset == t.Nat() and element_type == t.Bytes():
            BytesTypeChecker(self.stack).typecheck_slice()
        else:
            raise E.StackTopTypeException(
                "SLICE",
                [t.Union([t.String(), t.Bytes()]), t.Nat(), t.Nat()],
                [element_type, length, offset],
            )


    def typecheck_compare(self):
        self.stack.assert_min_length(2, "COMPARE requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.String) and isinstance(operand_b, t.String):
            StringTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Int) and isinstance(operand_b, t.Int):
            IntOrNatTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Nat) and isinstance(operand_b, t.Nat):
            IntOrNatTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Address) and isinstance(operand_b, t.Address):
            AddressTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Mutez) and isinstance(operand_b, t.Mutez):
            MutezTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Option) and isinstance(operand_b, t.Option):
            OptionTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Bytes) and isinstance(operand_b, t.Bytes):
            BytesTypeChecker(self.stack).typecheck_compare()
        elif isinstance(operand_a, t.Datetime) and isinstance(operand_b, t.Datetime):
            DatetimeTypeChecker(self.stack).typecheck_compare()
        else:
            raise E.OperandException(
                "COMPARE",
                [t.Int(), t.Nat(), t.String(), t.Mutez(), t.Bytes(), t.Address(), t.Datetime()],
                [operand_b, operand_a],
            )


    def typecheck_pair(self, instruction: Instr):
        if len(instruction.args) and isinstance(instruction.args[0], int):
            PairTypeChecker(self.stack).typecheck_pair_n(instruction.args[0])
        else:
            PairTypeChecker(self.stack).typecheck_pair()


    def typecheck_contract(self, contract: Contract):
        parameter_type = contract.get_parameter_type()
        storage_type = contract.get_storage_type()
        body_instructions = contract.instructions + [
            contract.get_contract_body()
        ]

        init_stack = StackType([t.Pair(car=parameter_type, cdr=storage_type)])
        self.typecheck(init_stack, body_instructions)
        self.stack.assert_length(1, "The contract must return a stack of length 1.")
        if isinstance(storage_type, t.Record):
            storage_type = storage_type.get_type()
        if self.stack != StackType([t.Pair(car=t.List(t.Operation()), cdr=storage_type)]):
            raise E.ContractReturnTypeException(
                self.stack,
                StackType([t.Pair(car=t.List(t.Operation()), cdr=storage_type)])
            )

    def typecheck_mul(self):
        self.stack.assert_min_length(2, "MUL requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Mutez) or isinstance(operand_b, t.Mutez):
            MutezTypeChecker(self.stack).typecheck_mul()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_mul()

    def typecheck_ediv(self):
        self.stack.assert_min_length(2, "EDIV requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        if isinstance(operand_a, t.Mutez):
            MutezTypeChecker(self.stack).typecheck_ediv()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_ediv()


    def typecheck_add(self):
        self.stack.assert_min_length(2, "ADD requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Mutez) and isinstance(operand_b, t.Mutez):
            MutezTypeChecker(self.stack).typecheck_add()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_add()


    def typecheck_sub(self):
        self.stack.assert_min_length(2, "SUB requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Datetime) and isinstance(operand_b, t.Datetime):
            DatetimeTypeChecker(self.stack).typecheck_sub()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_sub()

    def typecheck_or(self):
        self.stack.assert_min_length(2, "OR requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Bool) and isinstance(operand_b, t.Bool):
            BooleanTypeChecker(self.stack).typecheck_or()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_or()

    def typecheck_and(self):
        self.stack.assert_min_length(2, "AND requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Bool) and isinstance(operand_b, t.Bool):
            BooleanTypeChecker(self.stack).typecheck_and()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_and()

    def typecheck_xor(self):
        self.stack.assert_min_length(2, "XOR requires a stack of length at least 2.")
        operand_a = self.stack.get_at_depth(0)
        operand_b = self.stack.get_at_depth(1)
        if isinstance(operand_a, t.Bool) and isinstance(operand_b, t.Bool):
            BooleanTypeChecker(self.stack).typecheck_xor()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_xor()

    def typecheck_not(self):
        self.stack.assert_min_length(2, "NOT requires a stack of length at least 1.")
        operand = self.stack.get_at_depth(0)
        if isinstance(operand, t.Bool):
            BooleanTypeChecker(self.stack).typecheck_not()
        else:
            IntOrNatTypeChecker(self.stack).typecheck_not()


    def typecheck(
            self,
            init_stack_type: Optional[StackType] = None,
            instructions: Optional[List[Instr]] = None,
    ):
        if init_stack_type is None:
            self.stack.reset()
        else:
            self.stack = init_stack_type

        if not instructions:
            instructions = self.instructions

        for instruction in instructions:
            if not isinstance(instruction, Instr):
                raise InvalidMichelsonException("Cannot typecheck: not a Michelson instruction")
            elif instruction.name == "FAILWITH":
                self.stack = StackType([t.Universal()])
                return
            elif instruction.name == "CDR":
                PairTypeChecker(self.stack).typecheck_cdr()
            elif instruction.name == "CAR":
                PairTypeChecker(self.stack).typecheck_car()
            elif instruction.name == "PUSH":
                StackManipulationTypeChecker(self.stack).typecheck_push(instruction)
            elif instruction.name == "DROP":
                StackManipulationTypeChecker(self.stack).typecheck_drop()
            elif instruction.name == "DUP":
                StackManipulationTypeChecker(self.stack).typecheck_dup(instruction)
            elif instruction.name == "DIG":
                StackManipulationTypeChecker(self.stack).typecheck_dig(instruction)
            elif instruction.name == "DUG":
                StackManipulationTypeChecker(self.stack).typecheck_dug(instruction)
            elif instruction.name == "EXEC":
                ControlStructuresTypeChecker(self.stack).typecheck_exec(instruction)
            elif instruction.name == "APPLY":
                ControlStructuresTypeChecker(self.stack).typecheck_apply()
            elif instruction.name == "DIP":
                ControlStructuresTypeChecker(self.stack).typecheck_dip(instruction, self.typecheck)
            elif instruction.name == "IF":
                ControlStructuresTypeChecker(self.stack).typecheck_if(instruction)
            elif instruction.name == "LAMBDA":
                StackManipulationTypeChecker(self.stack).typecheck_lambda(instruction)
            elif instruction.name == "IF_NONE":
                OptionTypeChecker(self.stack).typecheck_if_none(instruction)
            elif instruction.name == "IF_LEFT":
                UnionTypeChecker(self.stack).typecheck_if_left(instruction)
            elif instruction.name == "EMPTY_MAP":
                MapTypeChecker(self.stack).typecheck_empty_map(instruction)
            elif instruction.name == "EMPTY_BIG_MAP":
                MapTypeChecker(self.stack).typecheck_empty_big_map(instruction)
            elif instruction.name == "GET":
                self.typecheck_get(instruction)
            elif instruction.name == "UPDATE":
                self.typecheck_update(instruction)
            elif instruction.name == "SIZE":
                self.typecheck_size()
            elif instruction.name == "MEM":
                self.typecheck_mem()
            elif instruction.name == "ABS":
                IntOrNatTypeChecker(self.stack).typecheck_abs()
            elif instruction.name == "NEG":
                IntOrNatTypeChecker(self.stack).typecheck_neg()
            elif instruction.name == "ISNAT":
                IntOrNatTypeChecker(self.stack).typecheck_is_nat()
            elif instruction.name == "INT":
                IntOrNatTypeChecker(self.stack).typecheck_int()
            elif instruction.name == "ADD":
                self.typecheck_add()
            elif instruction.name == "SUB":
                self.typecheck_sub()
            elif instruction.name == "SUB_MUTEZ":
                MutezTypeChecker(self.stack).typecheck_sub_mutez()
            elif instruction.name == "MUL":
                self.typecheck_mul()
            elif instruction.name == "EDIV":
                self.typecheck_ediv()
            elif instruction.name == "OR":
                self.typecheck_or()
            elif instruction.name == "AND":
                self.typecheck_and()
            elif instruction.name == "XOR":
                self.typecheck_xor()
            elif instruction.name == "NOT":
                self.typecheck_not()
            elif instruction.name == "COMPARE":
                self.typecheck_compare()
            elif instruction.name == "CONCAT":
                self.typecheck_concat()
            elif instruction.name == "SLICE":
                self.typecheck_slice()
            elif instruction.name == "PAIR":
                self.typecheck_pair(instruction)
            elif instruction.name == "UNPAIR":
                PairTypeChecker(self.stack).typecheck_unpair()
            elif instruction.name == "SOME":
                OptionTypeChecker(self.stack).typecheck_some()
            elif instruction.name == "NONE":
                OptionTypeChecker(self.stack).typecheck_none(instruction)
            elif instruction.name == "PACK":
                BytesTypeChecker(self.stack).typecheck_pack()
            elif instruction.name == "UNPACK":
                BytesTypeChecker(self.stack).typecheck_unpack(instruction)
            elif instruction.name == "BLAKE2B":
                CryptographicPrimitivesTypeChecker(self.stack).typecheck_blake2b()
            elif instruction.name == "KECCAK":
                CryptographicPrimitivesTypeChecker(self.stack).typecheck_keccak()
            elif instruction.name == "SHA256":
                CryptographicPrimitivesTypeChecker(self.stack).typecheck_sha256()
            elif instruction.name == "SHA512":
                CryptographicPrimitivesTypeChecker(self.stack).typecheck_sha512()
            elif instruction.name == "SHA3":
                CryptographicPrimitivesTypeChecker(self.stack).typecheck_sha3()
            elif instruction.name == "EMPTY_SET":
                SetTypeChecker(self.stack).typecheck_empty_set(instruction)
            elif instruction.name == "NIL":
                ListTypeChecker(self.stack).typecheck_empty_list(instruction)
            elif instruction.name == "CONS":
                ListTypeChecker(self.stack).typecheck_cons()
            elif instruction.name == "ITER":
                ListTypeChecker(self.stack).typecheck_iter(instruction)
            elif instruction.name == "UNIT":
                ConstantsTypeChecker(self.stack).typecheck_unit()
            elif instruction.name == "NOW":
                DatetimeTypeChecker(self.stack).typecheck_now()
            elif instruction.name == "SELF_ADDRESS":
                ConstantsTypeChecker(self.stack).typecheck_self_address()
            elif instruction.name == "SENDER":
                ConstantsTypeChecker(self.stack).typecheck_sender()
            elif instruction.name == "BALANCE":
                ConstantsTypeChecker(self.stack).typecheck_balance()
            elif instruction.name == "SOURCE":
                ConstantsTypeChecker(self.stack).typecheck_source()
            elif instruction.name == "AMOUNT":
                ConstantsTypeChecker(self.stack).typecheck_amount()
            elif instruction.name == "EQ":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "NEQ":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "LT":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "GT":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "LE":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "GE":
                ComparaisonOperatorTypeChecker(self.stack).typecheck_operator()
            elif instruction.name == "CONTRACT":
                TransactionTypeChecker(self.stack).typecheck_contract(instruction)
            elif instruction.name == "TRANSFER_TOKENS":
                TransactionTypeChecker(self.stack).typecheck_transfer_tokens()
            elif instruction.name == "COMMENT":
                pass
            else:
                breakpoint()
                raise NotImplementedError()

            logging.debug("\n\n" + str(instruction).ljust(12) + "\n" + str(self.stack) + "\n")

