import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests

from shippo_con import core

TITLE = f"{core.NAME} - {core.VERSION}"
CANVAS_SIZE = 100
ARROW_TAG = 'arrow'
UPDATE_JSON_URL = 'https://github.com/aruma256/Shippo-Con/raw/main/version_info.json' # noqa


def _is_local_version_outdated(remote_version, local_version):
    remote = tuple(map(int, remote_version.split('.')))
    local = tuple(map(int, local_version.split('.')))
    return remote > local


class GUI:

    def __init__(self, core: core.Core):
        self._core = core
        self._created_event = threading.Event()

    def create(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        assert self._created_event.wait(timeout=5)

    def _run(self):
        self._root = root = tk.Tk()
        self._create_gui_elements()
        self._created_event.set()
        threading.Thread(target=self._update_check, daemon=True).start()
        root.mainloop()

    def _update_check(self):
        try:
            res = requests.get(UPDATE_JSON_URL, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if _is_local_version_outdated(data['recommended'], core.VERSION): # noqa
                    messagebox.showinfo(message='新しいバージョンが公開されています')
        except Exception:
            pass

    def _create_gui_elements(self):
        self._root.geometry('400x400')
        self._root.protocol("WM_DELETE_WINDOW", self._core.kill)
        self._create_top_frame()
        self._create_settings_frames()
        self._create_viewer_frame()

    def _create_top_frame(self):
        frm = ttk.Frame(self._root, padding=10)
        frm.grid()
        row = 0
        ttk.Label(frm, text=TITLE).grid(row=row, column=0, columnspan=2)

    def _connect_joycon(self, side):
        try:
            self._core.connect_joycon(side)
        except ValueError:
            messagebox.showerror('エラー', '接続できませんでした。')
        except Exception as e:
            messagebox.showerror('不明なエラー', str(e))

    def _create_settings_frames(self):
        frm = ttk.Frame(self._root, padding=10)
        frm.grid()
        ttk.Button(
            frm,
            text="Joy-Con L を使う",
            command=lambda: self._connect_joycon('L'),
            ).grid(row=0, column=0)
        ttk.Button(
            frm,
            text="Joy-Con R を使う",
            command=lambda: self._connect_joycon('R'),
            ).grid(row=0, column=1)
        #
        frm = ttk.Frame(self._root, padding=10)
        frm.grid()
        row = 0
        #
        ttk.Label(frm, text='振れやすさ(横)').grid(row=row, column=0)
        scale_x_label_value = tk.StringVar(
            value=str(self._core.engine_params.amp[0]))

        def on_change_x(value):
            value = int(float(value))
            scale_x_label_value.set(str(value))
            self._core.engine_params.amp[0] = value

        ttk.Scale(
            frm, from_=1, to=200, value=self._core.engine_params.amp[0],
            command=on_change_x).grid(row=row, column=1)
        ttk.Label(
            frm, textvariable=scale_x_label_value).grid(row=row, column=2)
        #
        row += 1
        ttk.Label(frm, text='振れやすさ(縦)').grid(row=row, column=0)
        scale_y_label_value = tk.StringVar(
            value=str(self._core.engine_params.amp[1]))

        def on_change_y(value):
            value = int(float(value))
            scale_y_label_value.set(str(value))
            self._core.engine_params.amp[1] = value

        ttk.Scale(
            frm, from_=1, to=200, value=self._core.engine_params.amp[1],
            command=on_change_y).grid(row=row, column=1)
        ttk.Label(
            frm, textvariable=scale_y_label_value).grid(row=row, column=2)

    def _create_viewer_frame(self):
        frm = ttk.Frame(self._root, padding=10)
        frm.grid()
        row = 0
        ttk.Label(frm, text="--var--").grid(row=row, column=0)
        ttk.Label(frm, text="--value_X--").grid(row=row, column=1)
        ttk.Label(frm, text="--value_Y--").grid(row=row, column=2)
        ttk.Label(frm, text="--graph--").grid(row=row, column=3)
        #
        row += 1
        ttk.Label(frm, text="raw_input").grid(row=row, column=0)
        self.var_raw_input_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_raw_input_x).grid(row=row, column=1)
        self.var_raw_input_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_raw_input_y).grid(row=row, column=2)
        #
        row += 1
        ttk.Label(frm, text="g1").grid(row=row, column=0)
        self.var_g1_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_g1_x).grid(row=row, column=1)
        self.var_g1_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_g1_y).grid(row=row, column=2)
        #
        row += 1
        ttk.Label(frm, text="g2").grid(row=row, column=0)
        self.var_g2_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_g2_x).grid(row=row, column=1)
        self.var_g2_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_g2_y).grid(row=row, column=2)
        #
        row += 1
        ttk.Label(frm, text="ExParams").grid(row=row, column=0)
        self.var_params_x = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_params_x).grid(row=row, column=1)
        self.var_params_y = tk.StringVar()
        ttk.Label(
            frm, textvariable=self.var_params_y).grid(row=row, column=2)
        self.params_canvas = tk.Canvas(
            frm, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.params_canvas.grid(row=row, column=3)
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
        #
        row += 1
        ttk.Button(
            frm, text="Quit", command=self._core.kill).grid(row=row, column=0)

    def update(self, status):
        self.var_raw_input_x.set(to_str(status.raw_input[0]))
        self.var_raw_input_y.set(to_str(status.raw_input[1]))
        self.var_g1_x.set(to_str(status.g1[0]))
        self.var_g1_y.set(to_str(status.g1[1]))
        self.var_g2_x.set(to_str(status.g2[0]))
        self.var_g2_y.set(to_str(status.g2[1]))
        self.var_params_x.set(to_str(status.params[0]))
        self.var_params_y.set(to_str(status.params[1]))
        #
        center_offset = CANVAS_SIZE/2
        self.params_canvas.coords(
            ARROW_TAG,
            center_offset,
            center_offset,
            center_offset + status.params[0]*center_offset,
            center_offset - status.params[1]*center_offset,
        )


def to_str(value):
    return f"{value:.2f}"
