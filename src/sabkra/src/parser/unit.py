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
    name_id: int
    xp: int
    health: int
    unit_type_id: int
    owner_id: int
    facing: int
    garrisoned: bool
    embarked: bool
    fortified: bool

    @classmethod
    def from_file(cls, version, f):
        get_byte(f)
        get_byte(f)
        name_id = get_int(f)
        xp = get_int(f)
        health = get_int(f)
        unit_type_id = get_int(f) if version == 12 else get_byte(f)
        owner_id = get_byte(f)
        facing = get_byte(f)
        _, _, _, _, _, garrisoned, embarked, fortified = get_flags(f)
        if version == 12:
            get_byte(f)
        for _ in range(64 if version == 11 else 32):
            get_byte(f)  # TODO: Promotion data
        return cls(
            name_id,
            xp,
            health,
            unit_type_id,
            owner_id,
            facing,
            garrisoned,
            embarked,
            fortified,
        )
