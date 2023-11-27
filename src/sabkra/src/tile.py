from __future__ import annotations

from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
)


@dataclass
class Tile:
    world: World
    row: int
    col: int
    terrain_id: int
    resource_id: int
    feature_id: int
    river_sw: bool
    river_se: bool
    river_e: bool
    elevation_id: int
    continent_id: int
    wonder_id: int
    resource_amount: int

    @classmethod
    def from_file(cls, world, row, col, f):
        terrain = get_byte(f)
        resource = get_byte(f)
        feature = get_byte(f)
        (_, _, _, _, _, river_sw, river_se, river_e) = get_flags(f)
        elevation = get_byte(f)
        continent = get_byte(f)
        wonder = get_byte(f)
        resource_amount = get_byte(f)

        return cls(
            world,
            row,
            col,
            terrain,
            resource,
            feature,
            river_sw,
            river_se,
            river_e,
            elevation,
            continent,
            wonder,
            resource_amount,
        )

    def get_terrain(self):
        if not self.terrain_id == 255:
            return self.world.terrain[self.terrain_id]
        return ""

    def get_resource(self):
        if not self.resource_id == 255:
            return self.world.resource[self.resource_id]
        return ""

    def get_feature(self):
        if not self.feature_id == 255:
            return self.world.feature[self.feature_id]
        return ""

    def get_elevation(self):
        if not self.elevation_id == 255:
            return self.world.elevation[self.elevation_id]
        return ""

    def get_wonder(self):
        if not self.wonder_id == 255:
            return self.world.wonder[self.wonder_id]
        return ""

    def get_river_state(self):
        river = []
        if self.river_e:
            river.append("river_e")
        if self.river_se:
            river.append("river_se")
        if self.river_se:
            river.append("river_sw")
        # TODO: ne, nw, wx
        return river
