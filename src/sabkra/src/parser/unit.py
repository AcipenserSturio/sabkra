from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_short,
)


@dataclass
class Unit:
    unk_1: int
    unk_2: int
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
        unk_1 = get_byte(f)
        unk_2 = get_byte(f)
        name_id = get_short(f)
        xp = get_int(f)
        health = get_int(f)
        unit_type_id = get_int(f) if version == 12 else get_byte(f)
        owner_id = get_byte(f)
        facing = get_byte(f)
        _, _, _, _, _, garrisoned, embarked, fortified = get_flags(f)
        if version == 12:
            get_byte(f)
        for _ in range(64 if version == 12 else 32):
            get_byte(f)  # TODO: Promotion data
        return cls(
            unk_1,
            unk_2,
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
