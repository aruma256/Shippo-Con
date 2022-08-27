import threading
import tkinter as tk
from tkinter import ttk

from shippo_con import core

TITLE = f"{core.NAME} - {core.VERSION}"


class GUI:

    def __init__(self, core: core.Core):
        self._core = core

    def create(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        self.root = root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", self._core.kill)
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        row = 0
        ttk.Label(frm, text=TITLE).grid(row=row, column=0, columnspan=2)
        #
        row += 1
        ttk.Label(frm, text="raw_input_x").grid(row=row, column=0)
        self.var_raw_input_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_raw_input_x).grid(row=row, column=1)
        row += 1
        ttk.Label(frm, text="raw_input_y").grid(row=row, column=0)
        self.var_raw_input_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_raw_input_y).grid(row=row, column=1)
        #
        row += 1
        ttk.Label(frm, text="params_x").grid(row=row, column=0)
        self.var_params_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_params_x).grid(row=row, column=1)
        row += 1
        ttk.Label(frm, text="params_y").grid(row=row, column=0)
        self.var_params_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_params_y).grid(row=row, column=1)
        row += 1
        ttk.Button(
            frm, text="Quit", command=self._core.kill).grid(row=row, column=0)
        root.mainloop()

    # def close(self):
    #     self.root.destroy()

    def update(self, raw_input, params):
        self.var_raw_input_x.set(raw_input[0])
        self.var_raw_input_y.set(raw_input[1])
        self.var_params_x.set(f"{params[0]:.2f}")
        self.var_params_y.set(f"{params[1]:.2f}")
