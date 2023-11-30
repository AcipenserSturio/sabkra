import tkinter as tk
import os
import platform
import pygame

from .world import World
from .scene import Scene

class View:
    def __init__(self, parent, width, height):
        self.frame = tk.Frame(
            parent,
            width=width,
            height=height,
        )
        os.environ["SDL_WINDOWID"] = str(self.frame.winfo_id())
        os.environ["SDL_VIDEODRIVER"] = (
            "windows" if platform.system() == "Windows" else "x11"
        )

    def open_scene(self, file_path, sidebar):
        with open(file_path, "rb") as f:
            world = World.from_file(f)
        self.run(Scene(world, sidebar))

    def new_scene(self, sidebar):
        world = World.blank(32, 20)
        self.run(Scene(world, sidebar))

    def run(self, sc):
        pygame.init()

        def on_click(event):
            sc.set_current_sprite_to_mouse((event.x, event.y))

        def on_click_drag(event):
            sc.mouse.update(event.x, event.y)
            sc.set_current_sprite_to_mouse((event.x, event.y))

        def on_motion(event):
            sc.mouse.update(event.x, event.y)

        def on_drag(event):
            sc.mouse.update(event.x, event.y)
            sc.camera.drag(sc.mouse.vector())

        def on_zoom(event):
            # zoom out
            if event.num == 5 or event.delta < 0:
                sc.camera.clean_rescale(-1)
            # zoom in
            if event.num == 4 or event.delta > 0:
                sc.camera.clean_rescale(1)
            sc.draw()

        self.frame.bind("<Button-1>", on_click)
        self.frame.bind("<B1-Motion>", on_click_drag)
        self.frame.bind("<B3-Motion>", on_drag)
        self.frame.bind("<Motion>", on_motion)
        # Windows scroll
        self.frame.bind("<MouseWheel>", on_zoom)
        # X11 scroll
        self.frame.bind("<Button-4>", on_zoom)
        self.frame.bind("<Button-5>", on_zoom)

        sc.draw()
