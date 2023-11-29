import tkinter as tk
from tkinter import ttk


class Sidebar:
    def __init__(self, parent, width, height):
        self.frame = tk.Frame(
            parent,
            width=width,
            height=height,
            padx=15,
            pady=15,
        )
        self._sprite = None

        self.plot = ttk.Label(self.frame)
        self.plot.pack()
        self.terr = Dropdown(self, self.set_terr, "Terrain")
        self.elev = Dropdown(self, self.set_elev, "Elevation")
        self.feat = Dropdown(self, self.set_feat, "Feature")
        self.reso = Dropdown(self, self.set_reso, "Resource")
        self.cont = Dropdown(self, self.set_cont, "Continent")
        self.wond = Dropdown(self, self.set_wond, "Wonder")

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value
        self.update()

    def set_terr(self, value):
        self.sprite.terrain = value

    def set_elev(self, value):
        self.sprite.elevation = value

    def set_feat(self, value):
        self.sprite.feature = value

    def set_reso(self, value):
        self.sprite.resource = value

    def set_cont(self, value):
        self.sprite.continent = value

    def set_wond(self, value):
        self.sprite.wonder = value

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


class Dropdown:
    def __init__(self, sidebar, updater, label):
        self.sidebar = sidebar
        self.updater = updater
        self.var = tk.StringVar()
        ttk.Label(sidebar.frame, text=label).pack()
        self.box = ttk.Combobox(
            sidebar.frame,
            state="readonly",
            textvariable=self.var,
        )
        self.box.pack(fill="x")
        self.var.trace_add("write", self.on_update)

    def on_update(self, var_, index, mode):
        self.updater(self.var.get())

    def update(self, value, options):
        self.box["values"] = options
        self.box.set(value)
