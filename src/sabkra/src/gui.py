import tkinter as tk
from tkinter import filedialog as fd
from .sidebar import Sidebar
from .view import View

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
        self.view = View(self.window, self.width - sidebar_width, self.height)
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
        self.view.run(filename, self.sidebar.update)

    def run(self):
        self.view.frame.pack(side="left", fill="both")
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
