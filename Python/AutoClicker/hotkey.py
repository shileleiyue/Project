from pynput import keyboard

class HotkeyListener:
    def __init__(self, toggle_callback=None):
        self._toggle_callback = toggle_callback
        self._hotkey = {keyboard.Key.f6}
        self._pressed_keys = set()
        self._listener = None
        self._running = False

    def _on_press(self, key):
        self._pressed_keys.add(key)
        if self._pressed_keys == self._hotkey:
            if self._toggle_callback:
                self._toggle_callback()

    def _on_release(self, key):
        self._pressed_keys.discard(key)

    def start(self):
        if self._running:
            return
        self._running = True
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.daemon = True
        self._listener.start()

    def stop(self):
        self._running = False
        if self._listener:
            self._listener.stop()
            self._listener = None