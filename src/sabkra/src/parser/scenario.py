from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_string,
    get_string_array,
    get_buffer,
    get_buffered_string,
)
from .unit import Unit
from .city import City
from .player import Player


@dataclass
class Scenario:

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
    cities: list
    victories: list
    game_options: list
    unk: str
    teams: list
    players: list

    @classmethod
    def from_file(cls, version, f):
        print(f"version {version}")
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
        length_unit_names = get_int(f)
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

        cities = []
        if length_cities != -1:
            # ????
            get_int(f)
            cities = [City.from_file(version, f) for _ in range(length_cities)]

        victories = get_string_array(f, length_victories)
        game_options = get_string_array(f, length_game_options)

        print("teams:", team_count)
        print("players:", player_count + city_state_count)
        # Unknown buffer:
        # size  - map name            (size)     players x*y*pl remain
        # 86177 - earth2014_huge_2    (80, 128)  62      79360  6817

        # 84857 - earth2014_huge_1    (80, 128)  61      78080  6777
        # 34057 - earth2014_standard  (52, 80)   46      23920  10137
        # 34057 - earth2014_sta...eej (52, 80)   46      23920  10137
        # 0     - blank

        unk = get_buffer(f, 0)

        teams = [get_buffered_string(f, 64) for _ in range(team_count)]
        players = [Player.from_file(f)
                   for _ in range(player_count + city_state_count)]

        self = cls(
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
            cities,
            victories,
            game_options,
            unk,
            teams,
            players,
        )

        with open("log.txt", "w") as f:
            print(self, file=f)
        with open("log.txt", "r") as f:
            text = f.read()
        with open("log.txt", "w") as f:
            print(text.replace(", ", ",\n"), file=f)
        return self
