import os
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

from models import KeyAction, MacroProfile
os.environ.setdefault("DISPLAY", ":0")
sys.modules['pyautogui'] = SimpleNamespace(press=lambda *a, **k: None, click=lambda *a, **k: None)
sys.modules['pynput'] = SimpleNamespace(keyboard=SimpleNamespace(Listener=object))
from macro_engine import MacroEngine


def test_macro_delay():
    engine = MacroEngine()
    profile = MacroProfile(
        hotkey="F3",
        actions=[KeyAction(type="key", code="a", delay_ms=100)],
        loop=1,
    )
    with patch("pyautogui.press") as press:
        start = time.time()
        engine.play_macro(profile)
        # allow some time for thread
        time.sleep(0.2)
        engine.stop_macro(profile.hotkey)
        assert press.called
        elapsed = time.time() - start
        assert elapsed >= 0.1



