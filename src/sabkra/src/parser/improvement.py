from __future__ import annotations

from dataclasses import dataclass

from .utils import (
    get_byte,
    get_short,
)

from typing import (
    TYPE_CHECKING,
    BinaryIO,
    )
if TYPE_CHECKING:
    from .world import World
    from .tile import Tile


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
    def from_file(cls,
                  world: World,
                  row: int,
                  col: int,
                  f: BinaryIO,
                  ):
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
    def tile(self) -> Tile:
        return self.world.get_tile(self.row, self.col)

    @property
    def improvement(self) -> str:
        if not self.improvement_id == -1:
            return self.world.scenario.improvs[self.improvement_id]
        return ""

    @improvement.setter
    def improvement(self, value):
        index = self.world.scenario.improvs.index(value) if value else -1
        if self.improvement != value:
            self.improvement_id = index
            # self.rerender()

    @property
    def civ(self) -> str:
        if not self.owner_id == -1:
            return self.world.scenario.civs[self.owner_id]
        return ""

    @civ.setter
    def civ(self, value):
        index = self.world.scenario.civs.index(value) if value else -1
        if self.civ != value:
            self.owner_id = index
            # self.rerender()

    @property
    def road(self) -> str:
        if not self.route_type == -1:
            return self.world.scenario.route_types[self.route_type]
        return ""

    @road.setter
    def road(self, value):
        index = self.world.scenario.route_types.index(value) if value else -1
        if self.road != value:
            self.route_type = index
            # self.rerender()

    @property
    def route_owner(self) -> str:
        if not self.route_owner_id == -1:
            return self.world.scenario.civs[self.route_owner_id]
        return ""

    @route_owner.setter
    def route_owner(self, value):
        index = self.world.scenario.civs.index(value) if value else -1
        if self.civ != value:
            self.route_owner_id = index
            # self.rerender()
