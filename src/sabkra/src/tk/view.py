import tkinter as tk
import os
import platform
import pygame

from ..pygame.scene import WorldPygame


class View:
    def __init__(self, parent, width, height):
        self.frame = tk.Frame(
            parent,
            width=width,
            height=height,
            background="black",
        )
        os.environ["SDL_WINDOWID"] = str(self.frame.winfo_id())
        os.environ["SDL_VIDEODRIVER"] = (
            "windows" if platform.system() == "Windows" else "x11"
        )

    def run(self, sidebar, file_path=None):
        pygame.init()

        if file_path:
            with open(file_path, "rb") as f:
                world = WorldPygame.from_file(f, sidebar)
        else:
            world = WorldPygame.blank(32, 20, sidebar)

        def on_click(event):
            world.set_current_tile_to_mouse((event.x, event.y))

        def on_click_drag(event):
            world.mouse.update(event.x, event.y)
            world.set_current_tile_to_mouse((event.x, event.y))

        def on_motion(event):
            world.mouse.update(event.x, event.y)

        def on_drag(event):
            world.mouse.update(event.x, event.y)
            world.camera.drag(world.mouse.vector())

        def on_zoom(event):
            # zoom out
            if event.num == 5 or event.delta < 0:
                world.camera.clean_rescale(-1)
            # zoom in
            if event.num == 4 or event.delta > 0:
                world.camera.clean_rescale(1)
            world.draw()

        self.frame.bind("<Button-1>", on_click)
        self.frame.bind("<B1-Motion>", on_click_drag)
        self.frame.bind("<B3-Motion>", on_drag)
        self.frame.bind("<Motion>", on_motion)
        # Windows worldroll
        self.frame.bind("<MouseWheel>", on_zoom)
        # X11 worldroll
        self.frame.bind("<Button-4>", on_zoom)
        self.frame.bind("<Button-5>", on_zoom)

        world.draw()
