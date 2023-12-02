import tkinter as tk
from tkinter import ttk

from .dropdown import Dropdown


class Sidebar:
    def __init__(self, parent, width, height):
        self.frame = ttk.Notebook(
            parent,
            padding=5,
            width=width,
        )
        self._tile = None

        self.edit_tab = tk.Frame(
            self.frame,
            padx=15,
            pady=15,
        )

        self.plot = ttk.Label(self.edit_tab)
        self.plot.pack()
        self.terr = Dropdown(self.edit_tab, self.set_terr, "Terrain")
        self.elev = Dropdown(self.edit_tab, self.set_elev, "Elevation")
        self.feat = Dropdown(self.edit_tab, self.set_feat, "Feature")
        self.reso = Dropdown(self.edit_tab, self.set_reso, "Resource")
        self.cont = Dropdown(self.edit_tab, self.set_cont, "Continent")
        self.wond = Dropdown(self.edit_tab, self.set_wond, "Wonder")

        self.frame.add(
            self.edit_tab,
            text="Edit Plot",
            sticky="nsew",
        )

        self.brush_tab = tk.Frame(
            self.frame,
            padx=15,
            pady=15,
        )
        self.frame.add(
            self.brush_tab,
            text="Brush",
            sticky="nsew",
        )

    @property
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, value):
        self._tile = value
        self.update()

    @property
    def world(self):
        return self.tile.world

    def set_terr(self, value):
        self.tile.terrain = value
        self.world.draw()

    def set_elev(self, value):
        self.tile.elevation = value
        self.world.draw()

    def set_feat(self, value):
        self.tile.feature = value
        self.world.draw()

    def set_reso(self, value):
        self.tile.resource = value
        self.world.draw()

    def set_cont(self, value):
        self.tile.continent = value
        self.world.draw()

    def set_wond(self, value):
        self.tile.wonder = value
        self.world.draw()

    def update(self):
        self.plot["text"] = f"""Plot: {
            self.tile.row, self.tile.col
        }"""

        self.terr.update(
            self.tile.terrain,
            self.world.terrain
        )
        self.elev.update(
            self.tile.elevation,
            self.world.elevation
        )
        self.feat.update(
            self.tile.feature,
            ["", *self.world.feature]
        )
        self.reso.update(
            self.tile.resource,
            ["", *self.world.resource]
        )
        self.cont.update(
            self.tile.continent,
            self.world.continent
        )
        self.wond.update(
            self.tile.wonder,
            ["", *self.world.wonder]
        )
