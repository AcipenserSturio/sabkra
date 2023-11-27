scale_factor = 1.2
scale_upper_bound = 6
scale_lower_bound = 0.1


class Camera:
    def __init__(self, scene):
        self.scene = scene
        self.x = 0
        self.y = 0
        self.scale = 1

    def drag(self, vector):
        self.x -= int(vector[0])
        self.y -= int(vector[1])
        self.scene.draw()
        # print(self.x, self.y)

    def drag_to_centre(self, window_width, window_height):
        # Position camera by default
        middle_sprite = self.scene.get_sprite(self.scene.world.get_tile(
            self.scene.world.height // 2,
            self.scene.world.width // 2,
        ))
        centre_x = middle_sprite.x - window_width / 2
        centre_y = middle_sprite.y - window_height / 2
        self.drag((centre_x, centre_y))

    def clean_rescale(self, direction):
        if direction > 0:
            if self.scale > scale_upper_bound:
                return
            self.rescale(scale_factor)
        else:
            if self.scale < scale_lower_bound:
                return
            self.rescale(1/scale_factor)

    def rescale(self, factor):
        # print(self.x, self.y, self.scene.mouse.x, self.scene.mouse.y)
        self.scale *= factor
        self.y += int((1 - factor) * (self.scene.mouse.y - self.y))
        self.x += int((1 - factor) * (self.scene.mouse.x - self.x))
        # print(self.scale)

    def get_world_pos_from_canvas_pos(self, canvaspos):
        return ((canvaspos[0] - self.x) / self.scale,
                (canvaspos[1] - self.y) / self.scale)
