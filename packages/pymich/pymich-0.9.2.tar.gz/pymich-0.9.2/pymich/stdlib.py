from typing import Union
from pymich.michelson_types import *


def transaction(contract: Contract[ParameterType], amount: Mutez, type: ParameterType) -> Operation:
    return Operation()

def len(
    data: Union[
        BigMap[KeyType, ValueType],
        Map[KeyType, ValueType],
        Set[ValueType],
        List[ValueType],
        String,
        Bytes,
    ]
) -> Nat:
    return data.__nat_len__()
