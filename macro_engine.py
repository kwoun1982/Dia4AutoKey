from __future__ import annotations

import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict

import pyautogui
from pynput import keyboard

from models import MacroProfile, KeyAction

pyautogui.FAILSAFE = True
logger = logging.getLogger(__name__)

class MacroEngine:
    """Engine to record and play macros asynchronously."""

    def __init__(self) -> None:
        self._executor = ThreadPoolExecutor(thread_name_prefix="macro")
        self._running: Dict[str, threading.Event] = {}
        self._stop_listeners: list[Callable[[], None]] = []

    def add_stop_listener(self, cb: Callable[[], None]) -> None:
        self._stop_listeners.append(cb)

    def play_macro(self, profile: MacroProfile) -> None:
        """Start playing the given macro profile in another thread."""
        stop_event = threading.Event()
        self._running[profile.hotkey] = stop_event
        self._executor.submit(self._run_macro, profile, stop_event)

    def stop_macro(self, hotkey: str) -> None:
        event = self._running.get(hotkey)
        if event:
            event.set()
            for cb in self._stop_listeners:
                cb()
            del self._running[hotkey]

    def _run_macro(self, profile: MacroProfile, stop_event: threading.Event) -> None:
        logger.info("Macro %s started", profile.hotkey)
        for _ in range(profile.loop):
            for action in profile.actions:
                if stop_event.is_set():
                    logger.info("Macro %s stopped", profile.hotkey)
                    return
                self._execute_action(action)
                time.sleep(action.delay_ms / 1000.0)
            if profile.delay_between_loops_ms:
                time.sleep(profile.delay_between_loops_ms / 1000.0)
        logger.info("Macro %s finished", profile.hotkey)
        self.stop_macro(profile.hotkey)

    def _execute_action(self, action: KeyAction) -> None:
        if action.type == "key":
            pyautogui.press(action.code)
        elif action.type == "mouse":
            if action.code == "left":
                pyautogui.click(button="left")
            elif action.code == "right":
                pyautogui.click(button="right")
            elif action.code == "middle":
                pyautogui.click(button="middle")
            else:
                logger.warning("Unknown mouse action: %s", action.code)
        else:
            logger.warning("Unknown action type: %s", action.type)


class EmergencyStopListener:
    """Listens for ESC ESC to stop all macros."""

    def __init__(self, engine: MacroEngine) -> None:
        self.engine = engine
        self._count = 0
        self._listener = keyboard.Listener(on_press=self._on_press)

    def start(self) -> None:
        self._listener.start()

    def _on_press(self, key: keyboard.Key | keyboard.KeyCode) -> None:
        try:
            if key == keyboard.Key.esc:
                self._count += 1
            else:
                self._count = 0
            if self._count >= 2:
                logger.info("Emergency stop triggered")
                for hotkey in list(self.engine._running.keys()):
                    self.engine.stop_macro(hotkey)
                self._count = 0
        except Exception as exc:  # pragma: no cover
            logger.exception("Error in emergency stop listener: %s", exc)
