from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_string,
    get_string_array,
)


@dataclass
class Unit:
    @classmethod
    def from_file(cls, f):
        get_byte(f)
        get_byte(f)
        name_id = get_int(f)

