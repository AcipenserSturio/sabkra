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
        self._sprite = None

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
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value
        self.update()

    def set_terr(self, value):
        self.sprite.terrain = value
        self.sprite.scene.draw()

    def set_elev(self, value):
        self.sprite.elevation = value
        self.sprite.scene.draw()

    def set_feat(self, value):
        self.sprite.feature = value
        self.sprite.scene.draw()

    def set_reso(self, value):
        self.sprite.resource = value
        self.sprite.scene.draw()

    def set_cont(self, value):
        self.sprite.continent = value
        self.sprite.scene.draw()

    def set_wond(self, value):
        self.sprite.wonder = value
        self.sprite.scene.draw()

    def update(self):
        self.plot["text"] = f"""Plot: {
            self.sprite.tile.row, self.sprite.tile.col
        }"""

        self.terr.update(
            self.sprite.terrain,
            self.sprite.tile.world.terrain
        )
        self.elev.update(
            self.sprite.elevation,
            self.sprite.tile.world.elevation
        )
        self.feat.update(
            self.sprite.feature,
            ["", *self.sprite.tile.world.feature]
        )
        self.reso.update(
            self.sprite.resource,
            ["", *self.sprite.tile.world.resource]
        )
        self.cont.update(
            self.sprite.continent,
            self.sprite.tile.world.continent
        )
        self.wond.update(
            self.sprite.wonder,
            ["", *self.sprite.tile.world.wonder]
        )
