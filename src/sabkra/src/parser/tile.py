from __future__ import annotations

from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
)

from typing import (
    TYPE_CHECKING,
    BinaryIO,
    List,
    Optional,
    Literal,
)
if TYPE_CHECKING:
    from .world import World
    from .improvement import Improvement


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

    # def __eq__(self, other):
    #     return (self.col, self.row) == (other.col, other.row)

    def __hash__(self):
        return (self.col, self.row).__hash__()

    def __repr__(self):
        return f"Tile({self.col}, {self.row})"

    @classmethod
    def from_file(
                cls,
                world: World,
                row: int,
                col: int,
                f: BinaryIO,
            ):
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

    @classmethod
    def blank(
                cls,
                world: World,
                row: int,
                col: int,
            ):
        return cls(
            world=world,
            row=row,
            col=col,
            terrain_id=6,  # TERRAIN_OCEAN
            resource_id=-1,
            feature_id=-1,
            river_sw=False,
            river_se=False,
            river_e=False,
            elevation_id=0,  # FLAT
            continent_id=0,  # None
            wonder_id=-1,
            resource_amount=-1,
        )

    @property
    def improvement(self) -> Improvement:
        return self.world.scenario.get_improvement(self.row, self.col)

    @property
    def terrain(self) -> str:
        if not self.terrain_id == -1:
            return self.world.terrain[self.terrain_id]
        return ""

    @property
    def elevation(self) -> str:
        if not self.elevation_id == -1:
            return self.world.elevation[self.elevation_id]
        return ""

    @property
    def feature(self) -> str:
        if not self.feature_id == -1:
            return self.world.feature[self.feature_id]
        return ""

    @property
    def resource(self) -> str:
        if not self.resource_id == -1:
            return self.world.resource[self.resource_id]
        return ""

    @property
    def continent(self) -> str:
        if not self.continent_id == -1:
            return self.world.continent[self.continent_id]
        return ""

    @property
    def wonder(self) -> str:
        if not self.wonder_id == -1:
            return self.world.wonder[self.wonder_id]
        return ""

    def get_river_state(self) -> List[str]:
        river = []
        if self.river_e:
            river.append("river_e")
        if self.river_se:
            river.append("river_se")
        if self.river_sw:
            river.append("river_sw")
        if neighbour := self.get_neighbour("w"):
            if neighbour.river_e:
                river.append("river_w")
        if neighbour := self.get_neighbour("nw"):
            if neighbour.river_se:
                river.append("river_nw")
        if neighbour := self.get_neighbour("ne"):
            if neighbour.river_sw:
                river.append("river_ne")
        return river

    def get_road_state(self) -> List[Optional[str]]:
        if self.improvement.route_type == -1:
            return []
        road = []
        road_type = "road" if self.improvement.route_type == 0 else "railroad"
        if neighbour := self.get_neighbour("w"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_w")
        if neighbour := self.get_neighbour("nw"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_nw")
        if neighbour := self.get_neighbour("ne"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_ne")
        if neighbour := self.get_neighbour("e"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_e")
        if neighbour := self.get_neighbour("se"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_se")
        if neighbour := self.get_neighbour("sw"):
            if (neighbour.improvement.route_type != -1
                    or neighbour.improvement.city_id != -1):
                road.append(f"{road_type}_sw")
        if not road:
            road.append(f"{road_type}_point")
        return road

    def neighbours(self) -> List[Optional[Tile]]:
        return [tile for tile in [
            self.get_neighbour("w"),
            self.get_neighbour("nw"),
            self.get_neighbour("ne"),
            self.get_neighbour("e"),
            self.get_neighbour("se"),
            self.get_neighbour("sw"),
        ] if tile]

    def get_neighbour(self,
                      direction: Literal["w", "e", "ne", "nw", "se", "sw"],
                      ) -> Optional[Tile]:
        if direction == "w":
            return self.world.get_tile(self.row, self.col-1)
        if direction == "e":
            return self.world.get_tile(self.row, self.col+1)
        if direction == "ne":
            return self.world.get_tile(self.row+1, self.col + (self.row % 2))
        if direction == "nw":
            return self.world.get_tile(self.row+1, self.col + (self.row % 2)-1)
        if direction == "se":
            return self.world.get_tile(self.row-1, self.col + (self.row % 2))
        if direction == "sw":
            return self.world.get_tile(self.row-1, self.col + (self.row % 2)-1)
        return
