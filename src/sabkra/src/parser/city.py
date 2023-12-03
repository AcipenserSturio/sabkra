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
class City:
    # struct: str
    name: str
    owner_id: int
    settings: int
    population: int
    health: int
    building_data: str
    # unk: str

    @classmethod
    def from_file(cls, version, f):
        # struct = "".join(map(chr, [get_byte(f) for _ in range(84)]))
        name = "".join(map(chr, [get_byte(f) for _ in range(64)]))
        owner_id = get_byte(f)
        settings = get_byte(f)
        population = get_short(f)
        health = get_int(f)
        # # for _ in range(64 if version == 12 else 32):
        # #     get_byte(f)  # TODO: Building data
        building_data = "".join(map(chr, [get_byte(f) for _ in range(64 if version == 12 else 32)]))
        # unk = "".join(map(chr, [get_byte(f) for _ in range(64)]))
        return cls(
            # struct,
            name,
            owner_id,
            settings,
            population,
            health,
            building_data,
            # unk,
        )
