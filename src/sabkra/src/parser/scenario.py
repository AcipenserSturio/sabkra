from __future__ import annotations

from dataclasses import dataclass
from math import ceil

from .utils import (
    get_byte,
    get_int,
    get_string_array,
    get_buffer,
    get_buffered_string,
)
from .unit import Unit
from .city import City
from .player import Player
from .improvement import Improvement


@dataclass
class Scenario:
    world: World
    max_turns: int
    start_year: int
    player_count: int
    city_state_count: int
    team_count: int
    improvs: list
    unit_types: list
    techs: list
    policies: list
    buildings: list
    promotions: list
    units: list
    unit_names: list
    cities: list
    victories: list
    game_options: list
    diplomacy: list
    unk: bytes
    revealed: bytes
    teams: list
    major_civs: list
    minor_civs: list
    improvements: list
    route_types: list

    @classmethod
    def from_file(cls, world, version, width, height, f):
        print("version", version)

        for _ in range(68):
            get_byte(f)
        max_turns = get_int(f)
        get_int(f)
        start_year = get_int(f)
        player_count = get_byte(f)

        city_state_count = get_byte(f)
        team_count = get_byte(f)

        get_byte(f)
        length_improvs = get_int(f)
        length_unit_types = get_int(f)
        length_techs = get_int(f)
        length_policies = get_int(f)
        length_buildings = get_int(f)
        length_promotions = get_int(f)

        length_units = (get_int(f) - 4) // (84 if version == 12 else 48)
        length_unit_names = (get_int(f) - 4) // 64
        length_cities = (get_int(f) - 4) // (136 if version == 12 else 104)
        length_victories = get_int(f)
        length_game_options = get_int(f)

        improvs = get_string_array(f, length_improvs)
        unit_types = get_string_array(f, length_unit_types)
        techs = get_string_array(f, length_techs)
        policies = get_string_array(f, length_policies)
        buildings = get_string_array(f, length_buildings)
        promotions = get_string_array(f, length_promotions)

        units = []
        if length_units != -1:
            # ????
            get_int(f)
            units = [Unit.from_file(version, f) for _ in range(length_units)]

        unit_names = []
        if length_unit_names != -1:
            get_int(f)
            unit_names = [get_buffered_string(f, 64)
                          for _ in range(length_unit_names)]

        cities = []
        if length_cities != -1:
            # ????
            get_int(f)
            cities = [City.from_file(version, f) for _ in range(length_cities)]

        victories = get_string_array(f, length_victories)
        game_options = get_string_array(f, length_game_options)

        # print("teams:", team_count)
        # print("players:", player_count + city_state_count)
        # Unknown buffer:
        # size  - map name            (size)     players teams diplo -diplo  -revl
        # 86177 - earth2014_huge_2    (80, 128)  62      62    237   85940   5632
        # 84857 - earth2014_huge_1    (80, 128)  61      61    229   84628   5632
        # 34057 - earth2014_standard  (52, 80)   46      53    173   33884   5632
        # 34057 - earth2014_sta...eej (52, 80)   46      53    173   33884   5632
        # 0     - blank

        length_diplo = ceil((team_count * (team_count - 1) // 2) / 8)
        diplomacy = [get_buffer(f, length_diplo) for _ in range(5)]

        unk = [get_buffer(f, 256) for _ in range(player_count)]

        length_revealed = ceil(width * height * team_count / 8)
        revealed = get_buffer(f, length_revealed)

        teams = [get_buffered_string(f, 64) for _ in range(team_count)]
        major_civs = [Player.from_file(f)
                      for _ in range(player_count)]
        minor_civs = [Player.from_file(f)
                      for _ in range(city_state_count)]

        improvements = [
            [
                Improvement.from_file(world, row, col, f)
                for col in range(width)
            ]
            for row in range(height)
        ]

        route_types = ["Road", "Railroad"]

        self = cls(
            world,
            max_turns,
            start_year,
            player_count,
            city_state_count,
            team_count,
            improvs,
            unit_types,
            techs,
            policies,
            buildings,
            promotions,
            units,
            unit_names,
            cities,
            victories,
            game_options,
            diplomacy,
            unk,
            revealed,
            teams,
            major_civs,
            minor_civs,
            improvements,
            route_types,
        )

        # with open("log.txt", "w") as f:
        #     print(self, file=f)
        # with open("log.txt", "r") as f:
        #     text = f.read()
        # with open("log.txt", "w") as f:
        #     print(text.replace(", ", ",\n"), file=f)

        return self

    def get_improvement(self, row, col):
        if self.world.wrap:
            col = col % self.world.width
        if col >= self.world.width or col < 0:
            return
        if row >= self.world.height or row < 0:
            return
        return self.improvements[row][col]

    @property
    def civs(self):
        return (
            [player.civ_type for player in self.major_civs]
            + [""] * 10  # Works in Earth 2014. Doesn't work in Mongol Scenario
            + [player.civ_type for player in self.minor_civs]
        )

    def get_civ(self, value):
        for player in self.players:
            if player.civ_type == value:
                return player
