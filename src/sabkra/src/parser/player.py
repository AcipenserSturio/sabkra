from dataclasses import dataclass

from .utils import (
    get_byte,
    get_int,
    get_buffer,
    get_buffered_string,
)


@dataclass
class Player:
    policies: bytes
    leader_name: bytes
    civ_name: bytes
    civ_type: bytes
    team_color: bytes
    era: bytes
    handicap: bytes
    culture: int
    gold: int
    start_x: int
    start_y: int
    team: int
    playable: int

    @classmethod
    def from_file(cls, f):
        policies = get_buffer(f, 32)
        leader_name = get_buffered_string(f, 64)
        civ_name = get_buffered_string(f, 64)
        civ_type = get_buffered_string(f, 64)
        team_color = get_buffered_string(f, 64)
        era = get_buffered_string(f, 64)
        handicap = get_buffered_string(f, 64)
        culture = get_int(f)
        gold = get_int(f)
        start_x = get_int(f)
        start_y = get_int(f)
        team = get_byte(f)
        playable = get_byte(f)
        get_byte(f)
        get_byte(f)

        return cls(
            policies,
            leader_name,
            civ_name,
            civ_type,
            team_color,
            era,
            handicap,
            culture,
            gold,
            start_x,
            start_y,
            team,
            playable,
        )
