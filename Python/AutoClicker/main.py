import tkinter as tk
from tkinter import ttk
import threading
from clicker import Clicker
from hotkey import HotkeyListener

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("连点器")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", False)

        self.clicker = Clicker()
        self._build_ui()
        self._init_hotkey()
        self._update_status()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        row = 0

        ttk.Label(main_frame, text="点击类型：").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.click_type = tk.StringVar(value="single")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(type_frame, text="单击", variable=self.click_type, value="single").pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="双击", variable=self.click_type, value="double").pack(side=tk.LEFT)
        row += 1

        ttk.Label(main_frame, text="鼠标按键：").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.mouse_button = tk.StringVar(value="left")
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(btn_frame, text="左键", variable=self.mouse_button, value="left").pack(side=tk.LEFT)
        ttk.Radiobutton(btn_frame, text="中键", variable=self.mouse_button, value="middle").pack(side=tk.LEFT)
        ttk.Radiobutton(btn_frame, text="右键", variable=self.mouse_button, value="right").pack(side=tk.LEFT)
        row += 1

        ttk.Label(main_frame, text="点击间隔：").grid(row=row, column=0, sticky=tk.W, pady=2)
        interval_frame = ttk.Frame(main_frame)
        interval_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        self.interval_var = tk.StringVar(value="100")
        interval_spin = ttk.Spinbox(interval_frame, from_=1, to=999999, textvariable=self.interval_var, width=8)
        interval_spin.pack(side=tk.LEFT)
        self.interval_unit = tk.StringVar(value="ms")
        unit_combo = ttk.Combobox(interval_frame, textvariable=self.interval_unit, values=["ms", "秒", "分钟", "小时"], state="readonly", width=6)
        unit_combo.pack(side=tk.LEFT, padx=3)
        unit_combo.bind("<<ComboboxSelected>>", self._on_unit_change)
        row += 1

        ttk.Label(main_frame, text="点击次数：").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.count_var = tk.StringVar(value="0")
        count_frame = ttk.Frame(main_frame)
        count_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        count_spin = ttk.Spinbox(count_frame, from_=0, to=999999, textvariable=self.count_var, width=10)
        count_spin.pack(side=tk.LEFT)
        ttk.Label(count_frame, text="（0 = 无限）", foreground="gray").pack(side=tk.LEFT, padx=5)
        row += 1

        sep = ttk.Separator(main_frame, orient="horizontal")
        sep.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1

        ttk.Label(main_frame, text="点击位置：").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.position_mode = tk.StringVar(value="current")
        pos_frame = ttk.Frame(main_frame)
        pos_frame.grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Radiobutton(pos_frame, text="当前鼠标", variable=self.position_mode, value="current",
                        command=self._toggle_position_input).pack(side=tk.LEFT)
        ttk.Radiobutton(pos_frame, text="固定坐标", variable=self.position_mode, value="fixed",
                        command=self._toggle_position_input).pack(side=tk.LEFT)
        row += 1

        self.fixed_pos_frame = ttk.Frame(main_frame)
        self.fixed_pos_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        ttk.Label(self.fixed_pos_frame, text="X：").pack(side=tk.LEFT)
        self.fixed_x_var = tk.StringVar(value="0")
        fixed_x_spin = ttk.Spinbox(self.fixed_pos_frame, from_=0, to=9999, textvariable=self.fixed_x_var, width=6)
        fixed_x_spin.pack(side=tk.LEFT, padx=2)
        ttk.Label(self.fixed_pos_frame, text="Y：").pack(side=tk.LEFT, padx=(5, 0))
        self.fixed_y_var = tk.StringVar(value="0")
        fixed_y_spin = ttk.Spinbox(self.fixed_pos_frame, from_=0, to=9999, textvariable=self.fixed_y_var, width=6)
        fixed_y_spin.pack(side=tk.LEFT, padx=2)
        self.capture_pos_btn = ttk.Button(self.fixed_pos_frame, text="捕获", command=self._capture_mouse_position)
        self.capture_pos_btn.pack(side=tk.LEFT, padx=5)
        self.fixed_pos_frame.grid_remove()
        row += 1

        sep2 = ttk.Separator(main_frame, orient="horizontal")
        sep2.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1

        self.topmost_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="窗口置顶", variable=self.topmost_var,
                         command=self._toggle_topmost).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=5)
        self.start_stop_btn = ttk.Button(btn_frame, text="开始 (F6)", command=self._toggle_clicker, width=20)
        self.start_stop_btn.pack()
        row += 1

        status_frame = ttk.LabelFrame(main_frame, text="状态", padding="5")
        status_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack()
        self.count_label = ttk.Label(status_frame, text="点击次数：0")
        self.count_label.pack()
        row += 1

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _toggle_position_input(self):
        if self.position_mode.get() == "fixed":
            self.fixed_pos_frame.grid()
        else:
            self.fixed_pos_frame.grid_remove()

    def _capture_mouse_position(self):
        def capture():
            import pyautogui
            x, y = pyautogui.position()
            self.fixed_x_var.set(str(x))
            self.fixed_y_var.set(str(y))
        threading.Thread(target=capture, daemon=True).start()

    def _on_unit_change(self, event=None):
        unit = self.interval_unit.get()
        current = self.interval_var.get()
        try:
            val = int(current)
        except ValueError:
            val = 100
        limits = {"ms": (1, 999999), "秒": (1, 9999), "分钟": (1, 999), "小时": (1, 99)}
        lo, hi = limits.get(unit, (1, 999999))
        if val < lo:
            val = lo
        if val > hi:
            val = hi
        self.interval_var.set(str(val))

    def _toggle_topmost(self):
        self.root.attributes("-topmost", self.topmost_var.get())

    def _init_hotkey(self):
        self.hotkey = HotkeyListener(toggle_callback=self._toggle_clicker)
        self.hotkey.start()

    def _toggle_clicker(self):
        if self.clicker.is_running:
            self._stop_clicker()
        else:
            self._start_clicker()

    def _start_clicker(self):
        try:
            interval = int(self.interval_var.get())
            if interval < 1:
                interval = 1
        except ValueError:
            interval = 100

        unit = self.interval_unit.get()
        unit_map = {"ms": 1, "秒": 1000, "分钟": 60000, "小时": 3600000}
        multiplier = unit_map.get(unit, 1)
        interval_ms = interval * multiplier

        try:
            count = int(self.count_var.get())
            if count < 0:
                count = 0
        except ValueError:
            count = 0

        try:
            fixed_x = int(self.fixed_x_var.get())
        except ValueError:
            fixed_x = 0

        try:
            fixed_y = int(self.fixed_y_var.get())
        except ValueError:
            fixed_y = 0

        self.clicker.config["click_type"] = self.click_type.get()
        self.clicker.config["button"] = self.mouse_button.get()
        self.clicker.config["interval"] = interval_ms
        self.clicker.config["count"] = count
        self.clicker.config["position_mode"] = self.position_mode.get()
        self.clicker.config["fixed_x"] = fixed_x
        self.clicker.config["fixed_y"] = fixed_y

        self.clicker.start()
        self.start_stop_btn.config(text="停止 (F6)")
        self.status_label.config(text="运行中...")

    def _stop_clicker(self):
        self.clicker.stop()
        self.start_stop_btn.config(text="开始 (F6)")
        self.status_label.config(text="已停止")

    def _update_status(self):
        if self.clicker.is_running:
            self.count_label.config(text=f"点击次数：{self.clicker.click_count}")
        self.root.after(200, self._update_status)

    def _on_close(self):
        self.clicker.stop()
        self.hotkey.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()