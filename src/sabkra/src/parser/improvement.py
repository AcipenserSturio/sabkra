from dataclasses import dataclass

from .utils import (
    get_byte,
    get_short,
)


@dataclass
class Improvement:
    row: int
    col: int
    city_id: int
    unit_id: int
    owner_id: int
    improvement_id: int
    route_type: int
    route_owner_id: int

    @classmethod
    def from_file(cls, row, col, f):
        city_id = get_short(f)
        unit_id = get_short(f)  # why is there 1 unit per tile?
        owner_id = get_byte(f)
        improvement_id = get_byte(f)
        route_type = get_byte(f)
        route_owner_id = get_byte(f)

        return cls(
            row,
            col,
            city_id,
            unit_id,
            owner_id,
            improvement_id,
            route_type,
            route_owner_id,
        )
