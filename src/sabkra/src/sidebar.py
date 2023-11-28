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

        self.plot = ttk.Label(self.frame)
        self.plot.pack()
        self.terr, self.terr_var = self.make_dropdown()
        self.elev, self.elev_var = self.make_dropdown()
        self.feat, self.feat_var = self.make_dropdown()
        self.reso, self.reso_var = self.make_dropdown()

    def make_dropdown(self):
        var = tk.StringVar()
        dropdown = ttk.Combobox(
            self.frame,
            state="readonly",
            textvariable=var,
        )
        dropdown.pack(fill="x")
        return dropdown, var

    def update(self, sprite):
        self.plot["text"] = f"Plot: ({sprite.tile.row}, {sprite.tile.col})"

        self.terr["values"] = sprite.tile.world.terrain
        self.terr.set(sprite.tile.get_terrain())

        self.elev["values"] = sprite.tile.world.elevation
        self.elev.set(sprite.tile.get_elevation())

        self.feat["values"] = ["", *sprite.tile.world.feature]
        self.feat.set(sprite.tile.get_feature())

        self.reso["values"] = ["", *sprite.tile.world.resource]
        self.reso.set(sprite.tile.get_resource())
