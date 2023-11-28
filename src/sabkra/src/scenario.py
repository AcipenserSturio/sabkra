from dataclasses import dataclass

from .utils import (
    get_byte,
    get_flags,
    get_int,
    get_string,
    get_string_array,
)


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

    @classmethod
    def from_file(cls, f):
        for _ in range(68):
            print(get_byte(f))
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
        length_units = get_int(f)
        length_unit_names = get_int(f)
        length_cities = get_int(f)
        length_victories = get_int(f)
        length_game_options = get_int(f)

        improvs = get_string_array(f, length_improvs)
        unit_types = get_string_array(f, length_unit_types)
        techs = get_string_array(f, length_techs)
        policies = get_string_array(f, length_policies)
        buildings = get_string_array(f, length_buildings)
        promotions = get_string_array(f, length_promotions)
        return cls(
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
        )
