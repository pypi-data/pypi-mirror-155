import pymich.middle_end.ir.instr_types as t
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Env:
    vars: Dict[str, int]
    sp: int
    args: Dict[str, List[str]]
    types: Dict[str, t.Type]

    def copy(self):
        return Env(
            self.vars.copy(),
            self.sp,
            self.args.copy(),
            self.types.copy(),
        )

    def add_var(self, var_name: str, sp: int):
        self.vars[var_name] = sp

    def del_var(self, var_name: str):
        del self.vars[var_name]

    def is_var_defined(self, var_name: str):
        return var_name in self.vars

    def get_var_type(self, var_name: str):
        return self.types[var_name]
