import threading
import tkinter as tk
from tkinter import ttk

from shippo_con import core

TITLE = f"{core.NAME} - {core.VERSION}"
CANVAS_SIZE = 100
ARROW_TAG = 'arrow'


class GUI:

    def __init__(self, core: core.Core):
        self._core = core

    def create(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        self.root = root = tk.Tk()
        root.geometry('400x300')
        root.protocol("WM_DELETE_WINDOW", self._core.kill)
        frm = ttk.Frame(root, padding=10)
        frm.grid()
        row = 0
        ttk.Label(frm, text=TITLE).grid(row=row, column=0, columnspan=2)
        #
        row += 1
        ttk.Label(frm, text="--var--").grid(row=row, column=0)
        ttk.Label(frm, text="--value--").grid(row=row, column=1)
        ttk.Label(frm, text="--graph--").grid(row=row, column=2)
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
        self.params_canvas = tk.Canvas(
            frm, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.params_canvas.grid(row=row, column=2, rowspan=2)
        self.params_canvas.create_rectangle(
            0, 0, CANVAS_SIZE, CANVAS_SIZE, fill='white')
        center_offset = CANVAS_SIZE/2
        self.params_canvas.create_line(
            center_offset,
            center_offset,
            center_offset,
            center_offset,
            width=3,
            arrow='last',
            fill='black',
            tag=ARROW_TAG)

        row += 1
        ttk.Label(frm, text="params_y").grid(row=row, column=0)
        self.var_params_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_params_y).grid(row=row, column=1)
        #
        row += 1
        ttk.Button(
            frm, text="Quit", command=self._core.kill).grid(row=row, column=0)
        root.mainloop()

    def update(self, raw_input, params):
        self.var_raw_input_x.set(raw_input[0])
        self.var_raw_input_y.set(raw_input[1])
        self.var_params_x.set(f"{params[0]:.2f}")
        self.var_params_y.set(f"{params[1]:.2f}")
        #
        # self.params_canvas.create_rectangle(
        #     0, 0, CANVAS_SIZE, CANVAS_SIZE, fill='white')
        center_offset = CANVAS_SIZE/2

        self.params_canvas.coords(
            ARROW_TAG,
            center_offset,
            center_offset,
            center_offset + params[0]*center_offset,
            center_offset - params[1]*center_offset,
        )
