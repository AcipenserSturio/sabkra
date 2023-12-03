from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_short,
    get_string,
    get_string_array,
)


@dataclass
class Player:
    struct: str
    @classmethod
    def from_file(cls, f):
        struct = "".join(map(chr, [get_byte(f) for _ in range(436)]))
        return cls(
            struct,
        )
