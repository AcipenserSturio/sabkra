import os
import pygame
from pygame._sdl2 import Renderer, Texture, Window
from pygame._sdl2 import error as SDL_error

from .camera import Camera
from .world import World
from .mouse import Mouse
from .sprite import Sprite

background_colour = (0, 0, 0)

default_window_width = 1920
default_window_height = 1080


class Scene:
    def __init__(self, world, sidebar):
        self.camera = Camera(self)
        self.mouse = Mouse()
        self.sidebar = sidebar
        self.images = {}
        self.canvas = None

        # Load world info and map

        self.world = world
        self.spritemap = {(tile.col, tile.row): Sprite(self, tile)
                          for tile in self.world.tiles()}
        self._current_sprite = self.get_sprite(self.world.get_tile(0, 0))
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
        self.canvas = self.get_sprite(
            self.world.get_tile(0, self.world.width-1)).canvas()
        self.render()
        self.camera.drag_to_centre(*pygame.display.get_window_size())

    def load_images(self):
        for terrain in self.world.terrain:
            self.add_image(terrain, "./src/sabkra/assets/terrain/{}.png"
                           .format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.world.feature:
            self.add_image(feature, "./src/sabkra/assets/feature/{}.png"
                           .format(feature.replace("FEATURE_", "").lower()))
        for resource in self.world.resource:
            self.add_image(resource, "./src/sabkra/assets/resource/{}.png"
                           .format(resource.replace("RESOURCE_", "").lower()))
        self.add_image("selected", "./src/sabkra/assets/selected.png")
        self.add_image("neighbour", "./src/sabkra/assets/neighbour.png")
        self.add_image("grid", "./src/sabkra/assets/grid.png")
        self.add_image("MOUNTAIN", "./src/sabkra/assets/mountain.png")
        self.add_image("HILL", "./src/sabkra/assets/hill.png")
        self.add_image("river_nw", "./src/sabkra/assets/rivers/nw.png")
        self.add_image("river_w", "./src/sabkra/assets/rivers/w.png")
        self.add_image("river_sw", "./src/sabkra/assets/rivers/sw.png")
        self.add_image("river_ne", "./src/sabkra/assets/rivers/ne.png")
        self.add_image("river_e", "./src/sabkra/assets/rivers/e.png")
        self.add_image("river_se", "./src/sabkra/assets/rivers/se.png")

    def get_sprite(self, tile):
        return self.spritemap[(tile.col, tile.row)]

    def get_sprites(self, tiles):
        return [self.get_sprite(tile) for tile in tiles]

    # Current tile
    @property
    def current_sprite(self):
        return self._current_sprite

    @current_sprite.setter
    def current_sprite(self, sprite):
        prev = self._current_sprite
        if sprite == prev:
            return
        self._current_sprite = sprite
        # prev.highlight = False
        # sprite.highlight = True
        if self.sidebar:
            self.sidebar.sprite = sprite

        self.brush = self.get_sprites(
            self.world.get_tiles_in_radius(
                self.current_sprite.tile,
                4,
            )
        )
        self.draw()

    @property
    def brush(self):
        return self._brush

    @brush.setter
    def brush(self, value):
        removed_sprites = list(set(self._brush) - set(value))
        added_sprites = list(set(value) - set(self._brush))
        for sprite in removed_sprites:
            sprite.highlight = False
        for sprite in added_sprites:
            sprite.highlight = True
        self._brush = value
        self.draw()

    def set_current_sprite_to_mouse(self, mousepos):
        self.current_sprite = self.nearest_sprite(mousepos)

    def nearest_sprite(self, canvaspos):
        # Bad code. Rewrite when you can think of a better structure
        world_x, world_y = self.camera.get_world_pos_from_canvas_pos(canvaspos)
        min_distance = float("inf")
        nearest_sprite = self.world.get_tile(0, 0)
        for tile in self.world.tiles():
            sprite = self.get_sprite(tile)
            sprite_x, sprite_y = self.get_sprite(tile).centre_pos
            distance = (sprite_x - world_x) ** 2 + (sprite_y - world_y) ** 2
            if distance < min_distance:
                nearest_sprite = sprite
                min_distance = distance
        return nearest_sprite

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
        for tile in self.world.tiles():
            self.get_sprite(tile).render()
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
