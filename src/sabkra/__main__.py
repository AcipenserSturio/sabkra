import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--standalone",
    help="Launch without tk wrapper.",
    default=False,
    action=argparse.BooleanOptionalAction,
)
args = parser.parse_args()
map_path_default = "./src/sabkra/maps/lungorajapan_ai.Civ5Map"

if args.standalone:
    from .src import world_display
    world_display.display_world(map_path_default, None)
else:
    from .src import gui
