import os
import pygame
from pygame._sdl2 import Renderer, Window, Texture

from .camera import Camera
from .world import init_world
from .mouse import Mouse
from .sprite import Sprite

background_colour = (0, 0, 0)

default_window_width = 1920
default_window_height = 1080

image_tiling_width = 76
image_tiling_height = 65
image_tiling_height_full = 86


def vector_diff(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])


def vector_sum(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])


def euclidean(x1, y1, x2, y2):
    return (x1-x2) ** 2 + (y1-y2) ** 2


class Scene:
    def __init__(self, file_path, update_sidebar):
        self.camera = Camera(self)
        self.mouse = Mouse()
        self.update_sidebar = update_sidebar
        self._current_sprite = None
        self.images = {}

        # Load world info and map from path
        self.world = init_world(file_path)
        self.spritemap = {(tile.col, tile.row): Sprite(self, tile)
                          for tile in self.world.tiles()}

        # Create window
        self.window = pygame.display.set_mode(
            (default_window_width, default_window_height), pygame.RESIZABLE
        )
        self.renderer = Renderer.from_window(Window.from_display_module())
        pygame.display.set_caption("World Display")

        # Load images
        self.load_images()

        # Draw
        self.canvas = self.get_sprite(self.world.get_tile(0, -1)).canvas()
        self.render()
        self.current_sprite = self.get_sprite(self.world.get_tile(0, 0))
        self.camera.drag_to_centre(*pygame.display.get_window_size())

    def load_images(self):
        for terrain in self.world.terrain:
            self.add_image(terrain, './src/sabkra/assets/terrain/{}.png'
                           .format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.world.feature:
            self.add_image(feature, './src/sabkra/assets/feature/{}.png'
                           .format(feature.replace("FEATURE_", "").lower()))
        self.add_image('selected', './src/sabkra/assets/selected.png')
        self.add_image('neighbour', './src/sabkra/assets/selected_neighbour.png')
        self.add_image('MOUNTAIN', './src/sabkra/assets/mountain.png')
        self.add_image('HILL', './src/sabkra/assets/hill.png')
        self.add_image('river_nw', './src/sabkra/assets/rivers/nw.png')
        self.add_image('river_w', './src/sabkra/assets/rivers/w.png')
        self.add_image('river_sw', './src/sabkra/assets/rivers/sw.png')
        self.add_image('river_ne', './src/sabkra/assets/rivers/ne.png')
        self.add_image('river_e', './src/sabkra/assets/rivers/e.png')
        self.add_image('river_se', './src/sabkra/assets/rivers/se.png')

    def get_sprite(self, tile):
        return self.spritemap[(tile.col, tile.row)]

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
        sprite.highlight = True
        sprite.rerender()
        if prev:
            prev.highlight = False
            prev.rerender()
        if self.update_sidebar:
            self.update_sidebar(sprite)

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
            distance = euclidean(sprite_x, sprite_y, world_x, world_y)
            if distance < min_distance:
                nearest_sprite = sprite
                min_distance = distance
        # print(*nearest_tile.worldpos_centre, world_x, world_y)
        return nearest_sprite

    # Image manipulation
    def add_image(self, name, path):
        # print(name, path)
        # Skip missing images and hope they aren't used in the map!
        if not os.path.isfile(path):
            return
        self.images[name] = pygame.image.load(path).convert_alpha()
        # print('added', name)

    # Draw
    def render(self):
        self.canvas.fill(background_colour)
        # Draw terrain
        for tile in self.world.tiles():
            self.get_sprite(tile).render()
        self.texture = Texture.from_surface(self.renderer, self.canvas)
        self.texture.blend_mode = 1

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
