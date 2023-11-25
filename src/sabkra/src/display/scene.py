import os
import pygame

from .camera import Camera
from .. import civ5map_parser

background_colour = (0, 0, 0)

default_window_width = 1920
default_window_height = 1080

image_tiling_width = 34
image_tiling_height = 30
image_tiling_height_full = 40


def vector_diff(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])


def vector_sum(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])


def mouse_pos():
    return pygame.mouse.get_pos()


def euclidean(x1, y1, x2, y2):
    return (x1-x2) ** 2 + (y1-y2) ** 2


def get_tile_world_pos(tile):
    x = int(tile.col * image_tiling_width
            + tile.row % 2 * image_tiling_width / 2)
    y = int(- tile.row * image_tiling_height)
    return (x, y)


def get_tile_centre_world_pos(tile):
    x, y = get_tile_world_pos(tile)
    x += int(image_tiling_width / 2)
    y += int(image_tiling_height_full / 2)
    return (x, y)


class Scene:
    def __init__(self, file_path, ui):
        self.camera = Camera(self)
        self.ui = ui
        self.window = None
        self.worldinfo = None
        self.map = None
        self.current_tile = None
        self._sprites = {}
        self._sprites_scaled = {}

        self.mouse_vector = (0, 0)
        self._previous_mouse_position = None
        self._current_mouse_position = None

        # Load world info and map from path
        self.worldinfo, self.map = civ5map_parser.read_world_data(file_path)
        self.set_current_tile(self.map[0][0])

        # Create window
        self.on_resize_window(default_window_width, default_window_height)
        pygame.display.set_caption("World Display")

        # Load sprites
        for terrain in self.worldinfo.terrain:
            self.add_sprite(terrain, './src/sabkra/assets/terrain/{}.png'
                            .format(terrain.replace("TERRAIN_", "").lower()))
        for feature in self.worldinfo.feature:
            self.add_sprite(feature, './src/sabkra/assets/feature/{}.png'
                            .format(feature.replace("FEATURE_", "").lower()))
        self.add_sprite('selected', './src/sabkra/assets/selected.png')

        # Give tiles world positions
        for row in self.map:
            for tile in row:
                tile.worldpos = get_tile_world_pos(tile)
                tile.worldpos_centre = get_tile_centre_world_pos(tile)

        # Position camera by default
        middle_tile = (
            self.map[self.worldinfo.height // 2][self.worldinfo.width // 2]
        )
        tile_x, tile_y = middle_tile.worldpos_centre
        window_width, window_height = pygame.display.get_window_size()
        centre_x = tile_x - window_width/2
        centre_y = tile_y - window_height/2
        self.camera.drag((centre_x, centre_y))

        # Set defaults for mouse
        self._previous_mouse_position = mouse_pos()
        self._current_mouse_position = mouse_pos()

    def mouse_pos(self):
        return mouse_pos()

    # Event handling
    def on_resize_window(self, width, height):
        self.window = pygame.display.set_mode(
            (width, height), pygame.RESIZABLE
        )

    # Current tile
    def set_current_tile_to_mouse(self, mousepos):
        tile = self.get_nearest_tile_from_canvas_pos(mousepos)
        self.set_current_tile(tile)

    def get_nearest_tile_from_canvas_pos(self, canvaspos):
        # Bad code. Rewrite when you can think of a better structure
        world_x, world_y = self.camera.get_world_pos_from_canvas_pos(canvaspos)
        min_distance = float("inf")
        nearest_tile = self.map[0][0]
        for row in self.map:
            for tile in row:
                tile_world_x, tile_world_y = tile.worldpos_centre
                distance = euclidean(tile_world_x, tile_world_y,
                                     world_x, world_y)
                if distance < min_distance:
                    nearest_tile = tile
                    min_distance = distance
        # print(*nearest_tile.worldpos_centre, world_x, world_y)
        return nearest_tile

    def set_current_tile(self, tile):
        self.current_tile = tile
        # tell the ui to update here
        if self.ui:
            self.ui.configure(text=self.get_info_from_tile(tile))
            self.ui.update()

    def get_info_from_tile(self, tile):
        return "{}\n\n{}".format(self.worldinfo, tile)

    # Image manipulation
    def add_sprite(self, name, path):
        # print(name, path)
        # Skip missing images and hope they aren't used in the map!
        if not os.path.isfile(path):
            return
        image = pygame.image.load(path).convert_alpha()
        self._sprites[name] = image
        self.rescale_sprite(name, image)
        # print('added', name)

    def get_sprite(self, name):
        if name in self._sprites_scaled.keys():
            return self._sprites_scaled[name]

    def rescale_all_sprites(self):
        for name, image in self._sprites.items():
            self.rescale_sprite(name, image)
        # print(len(self._sprites_scaled))

    def rescale_sprite(self, name, image):
        self._sprites_scaled[name] = self.get_scaled_image(image,)

    def get_scaled_image(self, image):
        return pygame.transform.scale(
            image,
            (
                int(image.get_width()*self.camera.scale),
                int(image.get_height()*self.camera.scale)
            )
        )

    # Get image for tile
    def get_terrain_image(self, tile):
        return self.get_sprite(tile.get_terrain())

    def get_feature_image(self, tile):
        return self.get_sprite(tile.get_feature())

    # Coordinates
    def update_mouse_vector(self):
        self._previous_mouse_position = self._current_mouse_position
        self._current_mouse_position = mouse_pos()
        self.mouse_vector = vector_diff(self._previous_mouse_position,
                                        self._current_mouse_position)
        # print(self._current_mouse_position)

    def get_tile_canvaspos(self, tile):
        worldpos = tile.worldpos
        canvaspos = self.camera.get_canvas_pos_from_world_pos(worldpos)
        return canvaspos

    # Draw
    def draw(self):
        self.window.fill(background_colour)
        for row in self.map:
            for tile in row:
                self.draw_tile(tile, self.get_tile_canvaspos(tile))
        # Draw tile selection
        self.draw_sprite(self.get_sprite('selected'),
                         self.get_tile_canvaspos(self.current_tile))
        pygame.display.update()

    def draw_tile(self, tile, pos):
        # Draw terrain
        terrain = self.get_terrain_image(tile)
        if terrain:
            self.draw_sprite(terrain, pos)
        # Draw feature
        feature = self.get_feature_image(tile)
        if feature:
            self.draw_sprite(feature, pos)
        # print('tile drawn at', pos)

    def draw_sprite(self, image, canvaspos):
        self.window.blit(image, canvaspos)
