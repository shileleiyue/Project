import threading
import time
import pyautogui

class Clicker:
    def __init__(self):
        self._running = False
        self._stop_event = threading.Event()
        self._thread = None
        self._click_count = 0
        self.config = {
            "click_type": "single",
            "button": "left",
            "interval": 100,
            "count": 0,
            "position_mode": "current",
            "fixed_x": 0,
            "fixed_y": 0,
        }

    @property
    def is_running(self):
        return self._running

    @property
    def click_count(self):
        return self._click_count

    def _get_button(self):
        return {
            "left": "left",
            "middle": "middle",
            "right": "right",
        }.get(self.config["button"], "left")

    def _perform_click(self):
        button = self._get_button()
        if self.config["position_mode"] == "fixed":
            x = self.config["fixed_x"]
            y = self.config["fixed_y"]
            pyautogui.click(x=x, y=y, button=button)
        else:
            pyautogui.click(button=button)
        self._click_count += 1

    def _perform_double_click(self):
        button = self._get_button()
        if self.config["position_mode"] == "fixed":
            x = self.config["fixed_x"]
            y = self.config["fixed_y"]
            pyautogui.doubleClick(x=x, y=y, button=button)
        else:
            pyautogui.doubleClick(button=button)
        self._click_count += 2

    def _click_loop(self):
        self._click_count = 0
        interval = self.config["interval"] / 1000.0
        max_count = self.config["count"]
        infinite = max_count <= 0

        while not self._stop_event.is_set():
            if not infinite and self._click_count >= max_count:
                break

            click_type = self.config["click_type"]
            if click_type == "double":
                self._perform_double_click()
            else:
                self._perform_click()

            if not infinite and self._click_count >= max_count:
                break

            self._stop_event.wait(interval)

        self._running = False

    def start(self):
        if self._running:
            return
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._click_loop, daemon=True)
        self._thread.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None