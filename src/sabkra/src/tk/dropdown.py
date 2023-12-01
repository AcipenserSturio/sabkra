import tkinter as tk
from tkinter import ttk


class Dropdown:
    def __init__(self, parent, updater, label):
        self.parent = parent
        self.updater = updater
        self.var = tk.StringVar()
        ttk.Label(parent, text=label).pack()
        self.box = ttk.Combobox(
            parent,
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
