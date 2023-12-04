from __future__ import annotations

from dataclasses import dataclass

from .utils import (
    get_byte,
    get_short,
)


@dataclass
class Improvement:
    world: World
    row: int
    col: int
    city_id: int
    unit_id: int
    owner_id: int
    improvement_id: int
    route_type: int
    route_owner_id: int

    @classmethod
    def from_file(cls, world, row, col, f):
        city_id = get_short(f)
        unit_id = get_short(f)  # why is there 1 unit per tile?
        owner_id = get_byte(f)
        improvement_id = get_byte(f)
        route_type = get_byte(f)
        route_owner_id = get_byte(f)

        return cls(
            world,
            row,
            col,
            city_id,
            unit_id,
            owner_id,
            improvement_id,
            route_type,
            route_owner_id,
        )

    @property
    def tile(self):
        return self.world.get_tile(self.row, self.col)

    @property
    def improvement(self):
        if not self.improvement_id == -1:
            return self.world.scenario.improvs[self.improvement_id]
        return ""

    @improvement.setter
    def improvement(self, value):
        index = self.world.scenario.improvs.index(value) if value else -1
        if self.improvement != value:
            self.improvement_id = index
            # self.rerender()
