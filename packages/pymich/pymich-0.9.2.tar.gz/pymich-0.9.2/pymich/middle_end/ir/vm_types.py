import unittest
import copy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, NewType, Tuple, Optional

import pymich.middle_end.ir.instr_types as t
from pymich.utils.helpers import Tree
import pymich.utils.exceptions as E


@dataclass
class Array:
    """Michelson list. Called array not to conflict with `typing.List`
    used in type annotations.

    Parameters
    ----------
    els: python list representing the Michelson list"""

    els: List[Any]


@dataclass
class Pair:
    """Michelson pair.

    Parameters
    ----------
    car: first element
    cdr: second element"""

    car: Any
    cdr: Any
    annotation: Optional[str] = None


@dataclass
class Some:
    """Michelson `option.some` type"""

    value: Any

    def __eq__(self, o):
        if type(o) == type(self):
            return self.value == o.value and self.value == o.value
        else:
            return False


@dataclass
class Or:
    """Michelson `or` type"""

    left: Any
    right: Any

    def __eq__(self, o):
        if type(o) == type(self):
            return self.left == o.left and self.right == o.right
        else:
            return False


@dataclass
class Left:
    """Michelson `LEFT` data type"""

    value: Any

    def __eq__(self, o):
        return type(o) == type(self) and self.value == o.value


@dataclass
class Right:
    """Michelson `RIGHT` data type"""

    value: Any

    def __eq__(self, o):
        return type(o) == type(self) and self.value == o.value


@dataclass
class FunctionPrototype:
    arg_type: t.Type
    return_type: t.Type

@dataclass
class MultiArgFunctionPrototype:
    arg_types: List[t.Type]
    return_type: t.Type


@dataclass
class Instr:
    name: str
    args: List[Any]
    kwargs: Dict[str, Any]

    def assert_n_args(self, n: int, error_message: str):
        if len(self.args) != n:
            raise E.InvalidMichelsonException(error_message)

    def assert_min_args(self, n: int, error_message: str):
        if len(self.args) < n:
            raise E.InvalidMichelsonException(error_message)

    def assert_arg_type(self, n: int, type_, error_message: str):
        self.assert_min_args(n, error_message)
        if not isinstance(self.args[n], type_):
            raise E.InvalidMichelsonException(error_message)

    def __str__(self):
        args = ""
        for arg in self.args:
            args += str(arg) + " "
        return f"{self.name} {args}"


@dataclass
class Entrypoint:
    prototype: FunctionPrototype
    instructions: List[Instr]


class ParameterTree(Tree):
    def make_node(self, left, right):
        return t.Or(left, right)

    def get_left(self, tree_node):
        return tree_node.left_type

    def get_right(self, tree_node):
        return tree_node.right_type

    def set_right(self, tree_node, value):
        tree_node.right_type = value

    def left_side_tree_height(self, tree, height=0):
        if type(tree) is not Or:
            return height
        else:
            return self.left_side_tree_height(self.get_left(tree), height + 1)

    def navigate_to_tree_leaf(self, tree, leaf_number, param):
        if type(tree) is not Or:
            return param

        left_max_leaf_number = 2 ** self.left_side_tree_height(tree.left)
        if leaf_number <= left_max_leaf_number:
            return Left(self.navigate_to_tree_leaf(tree.left, leaf_number, param))
        else:
            return Right(
                self.navigate_to_tree_leaf(
                    tree.right, leaf_number - left_max_leaf_number, param
                )
            )


class EntrypointTree(Tree):
    def make_node(self, left=None, right=None):
        if not left:
            left = []
        if not right:
            right = []
        return Instr("IF_LEFT", [left, right], {})

    def get_left(self, tree_node):
        return tree_node.args[0]

    def get_right(self, tree_node):
        return tree_node.args[1]

    def set_right(self, tree_node, value):
        tree_node.args[1] = value

    def get_leaf_from_element(self, element):
        return element.instructions

    def format_leaf(self, leaf):
        return leaf if type(leaf) == list else [leaf]


@dataclass
class Contract:
    storage: Any
    storage_type: t.Type
    entrypoints: Dict[str, Entrypoint]
    instructions: List[Instr]

    def add_entrypoint(self, name: str, entrypoint: Entrypoint):
        self.entrypoints[name] = entrypoint

    def make_contract_param(self, entrypoint_name, entrypoint_param):
        entrypoint_names = sorted(self.entrypoints.keys())
        if len(entrypoint_names) == 1:
            return entrypoint_param

        parameter_tree = ParameterTree()
        tree = parameter_tree.list_to_tree(entrypoint_names)
        entrypoint_index = entrypoint_names.index(entrypoint_name)
        return parameter_tree.navigate_to_tree_leaf(
            tree, entrypoint_index + 1, entrypoint_param
        )

    def get_storage_type(self):
        return self.storage_type

    def get_parameter_type(self):
        entrypoint_names = self.entrypoints.keys()
        if len(entrypoint_names) == 1:
            return self.entrypoints[entrypoint_names[0]].arg_type
        else:
            parameter_tree = ParameterTree()
            entrypoints = [
                    self.entrypoints[name].prototype.arg_type
                    for name in sorted(entrypoint_names)
                ]

            for i, entrypoint in enumerate(entrypoints):
                if type(entrypoint) == t.Record:
                    # we do not want to override the record annotation for all record calls
                    # but want to annotate them with the entrypoint name, so we copy it
                    # and set the annotation then
                    entrypoints[i] = copy.deepcopy(entrypoint)
                    entrypoints[i].annotation = "%" + sorted(list(entrypoint_names))[i]
                else:
                    entrypoint.annotation = "%" + sorted(list(entrypoint_names))[i]

            return parameter_tree.list_to_tree(entrypoints)

    def get_contract_body(self):
        entrypoints = [
            self.entrypoints[name] for name in sorted(self.entrypoints.keys())
        ]
        entrypoint_tree = EntrypointTree()
        return entrypoint_tree.list_to_tree(entrypoints)

