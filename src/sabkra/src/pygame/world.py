import os
import pygame
from pygame._sdl2 import Renderer, Texture, Window
from pygame._sdl2 import error as SDL_error

from ..parser.world import World

from .camera import Camera
from .mouse import Mouse
from .tile import TilePygame as Tile


background_colour = (0, 0, 0)

default_window_width = 1920
default_window_height = 1080


class WorldPygame(World):
    tile_class = Tile

    @classmethod
    def from_file(cls, f, sidebar):
        self = super().from_file(f)
        self.init_scene(sidebar)
        return self

    @classmethod
    def blank(cls, width, height, sidebar):
        self = super().blank(width, height)
        self.init_scene(sidebar)
        return self

    def init_scene(self, sidebar):
        self.sidebar = sidebar
        self.camera = Camera(self)
        self.mouse = Mouse()
        self.images = {}
        self.canvas = None

        # Load world info and map

        self._current_tile = self.get_tile(0, 0)
        self._brush = []

        # Create window
        self.window = pygame.display.set_mode(
            (default_window_width, default_window_height), pygame.RESIZABLE
        )
        try:
            self.renderer = Renderer.from_window(Window.from_display_module())
        except SDL_error:
            self.renderer = Renderer(Window.from_display_module())
        pygame.display.set_caption("World Display")

        # Load images
        self.load_images()

        # Draw
        self.canvas = self.get_tile(0, self.width-1).canvas()
        self.render()
        self.camera.drag_to_centre(*pygame.display.get_window_size())

    def load_images(self):
        for terrain in self.terrain:
            self.add_image(terrain, "./src/sabkra/assets/terrain/{}.png"
                           .format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.feature:
            self.add_image(feature, "./src/sabkra/assets/feature/{}.png"
                           .format(feature.replace("FEATURE_", "").lower()))
        for resource in self.resource:
            self.add_image(resource, "./src/sabkra/assets/resource/{}.png"
                           .format(resource.replace("RESOURCE_", "").lower()))
        self.add_image("selected", "./src/sabkra/assets/selected.png")
        self.add_image("starting", "./src/sabkra/assets/starting.png")
        self.add_image("grid", "./src/sabkra/assets/grid.png")

        self.add_image("MOUNTAIN", "./src/sabkra/assets/mountain.png")
        self.add_image("HILL", "./src/sabkra/assets/hill.png")

        self.add_image("city", "./src/sabkra/assets/city.png")

        self.add_image("river_nw", "./src/sabkra/assets/rivers/nw.png")
        self.add_image("river_w", "./src/sabkra/assets/rivers/w.png")
        self.add_image("river_sw", "./src/sabkra/assets/rivers/sw.png")
        self.add_image("river_ne", "./src/sabkra/assets/rivers/ne.png")
        self.add_image("river_e", "./src/sabkra/assets/rivers/e.png")
        self.add_image("river_se", "./src/sabkra/assets/rivers/se.png")

        self.add_image("road_nw", "./src/sabkra/assets/roads/nw.png")
        self.add_image("road_w", "./src/sabkra/assets/roads/w.png")
        self.add_image("road_sw", "./src/sabkra/assets/roads/sw.png")
        self.add_image("road_ne", "./src/sabkra/assets/roads/ne.png")
        self.add_image("road_e", "./src/sabkra/assets/roads/e.png")
        self.add_image("road_se", "./src/sabkra/assets/roads/se.png")
        self.add_image("road_point", "./src/sabkra/assets/roads/point.png")

        self.add_image("railroad_nw", "./src/sabkra/assets/railroads/nw.png")
        self.add_image("railroad_w", "./src/sabkra/assets/railroads/w.png")
        self.add_image("railroad_sw", "./src/sabkra/assets/railroads/sw.png")
        self.add_image("railroad_ne", "./src/sabkra/assets/railroads/ne.png")
        self.add_image("railroad_e", "./src/sabkra/assets/railroads/e.png")
        self.add_image("railroad_se", "./src/sabkra/assets/railroads/se.png")
        self.add_image("railroad_point", "./src/sabkra/assets/railroads/point.png")

    # Current tile
    @property
    def current_tile(self):
        return self._current_tile

    @current_tile.setter
    def current_tile(self, tile):
        prev = self._current_tile
        if tile == prev:
            return
        self._current_tile = tile
        # prev.highlight = False
        # tile.highlight = True
        if self.sidebar:
            self.sidebar.tile = tile

        self.brush = self.get_tiles_in_radius(self.current_tile, 0)
        self.draw()

    @property
    def brush(self):
        return self._brush

    @brush.setter
    def brush(self, value):
        removed_tiles = list(set(self._brush) - set(value))
        added_tiles = list(set(value) - set(self._brush))
        for tile in removed_tiles:
            tile.highlight = False
        for tile in added_tiles:
            tile.highlight = True
        self._brush = value

        # for tile in value:
        #     tile.terrain = "TERRAIN_SNOW"

        self.draw()

    def set_current_tile_to_mouse(self, mousepos):
        self.current_tile = self.nearest_tile(mousepos)

    def nearest_tile(self, canvaspos):
        # Bad code. Rewrite when you can think of a better structure
        world_x, world_y = self.camera.get_world_pos_from_canvas_pos(canvaspos)
        min_distance = float("inf")
        nearest_tile = self.get_tile(0, 0)
        for tile in self.tiles():
            tile_x, tile_y = tile.centre_pos
            distance = (tile_x - world_x) ** 2 + (tile_y - world_y) ** 2
            if distance < min_distance:
                nearest_tile = tile
                min_distance = distance
        return nearest_tile

    # Image manipulation
    def add_image(self, name, path):
        # print(name, path)
        # Skip missing images and hope they aren't used in the map!
        if not os.path.isfile(path):
            return
        self.images[name] = pygame.image.load(path).convert_alpha()

    # Draw
    def render(self):
        self.canvas.fill(background_colour)
        # Draw terrain
        for tile in self.tiles():
            tile.render()
        self.texture = Texture(
            self.renderer,
            (self.canvas.get_width(), self.canvas.get_height()),
            streaming=True,
            scale_quality=0,
        )
        self.texture.update(self.canvas)
        # self.texture.blend_mode = 1

    def draw(self):
        # print((self.camera.x, self.camera.y))
        self.renderer.clear()
        self.texture.draw(dstrect=(
            self.camera.x,
            self.camera.y,
            self.canvas.get_width() * self.camera.scale,
            self.canvas.get_height() * self.camera.scale,
        ))
        self.renderer.present()
