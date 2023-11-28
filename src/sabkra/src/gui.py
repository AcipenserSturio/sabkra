import tkinter as tk
from tkinter import filedialog as fd
from . import world_display
from .sidebar import Sidebar
import os
import platform

desktop_panel = 50
sidebar_width = 250


def default_directory():
    return r"~/.local/share/Aspyr/Sid Meier's Civilization 5/MODS/gedemon's ynaemp (v 25)/"


class Gui:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sabkra - Civ 5 World previewer")

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height - desktop_panel
        self.window.geometry(f"{self.width}x{self.height}+{0}+{0}")

        self.menu = self.make_menu()
        self.frame_pygame = self.make_frame_pygame()
        self.sidebar = Sidebar(self.window, sidebar_width, self.height)

    def select_file(self):
        filename = fd.askopenfilename(
            title="Open",
            initialdir=default_directory(),
            filetypes=(
                ("Civilization V Map", "*.civ5map"),
                ("All files", "*.*")
            ),
        )
        self.window.title(f"Sabkra - {filename}")
        world_display.display_world_tk(
            filename,
            self.sidebar.update,
            self.frame_pygame,
        )

    def run(self):
        self.frame_pygame.pack(side="left", fill="both")
        self.sidebar.frame.pack_propagate(False)
        self.sidebar.frame.pack(side="right", fill="both")
        self.window.mainloop()

    def make_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        menu.add_command(
            label="Open",
            command=self.select_file
        )
        return menu

    def make_frame_pygame(self):
        frame = tk.Frame(
            self.window,
            width=self.width - sidebar_width,
            height=self.height,
        )
        os.environ["SDL_WINDOWID"] = str(frame.winfo_id())
        os.environ["SDL_VIDEODRIVER"] = (
            "windows" if platform.system() == "Windows" else "x11"
        )
        return frame
