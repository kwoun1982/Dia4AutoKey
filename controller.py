from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import List

from PyQt5 import QtWidgets, QtCore

from models import MacroProfile, KeyAction
from macro_engine import MacroEngine, EmergencyStopListener

logger = logging.getLogger(__name__)

CONFIG_PATH = Path("macros.json")

class MacroDialog(QtWidgets.QDialog):
    """Dialog to add or edit a macro."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Macro")
        self.layout = QtWidgets.QVBoxLayout(self)

        form = QtWidgets.QFormLayout()
        self.hotkey_edit = QtWidgets.QLineEdit()
        self.desc_edit = QtWidgets.QLineEdit()
        self.loop_spin = QtWidgets.QSpinBox()
        self.loop_spin.setRange(1, 9999)
        self.actions_edit = QtWidgets.QPlainTextEdit()
        form.addRow("Hotkey", self.hotkey_edit)
        form.addRow("Description", self.desc_edit)
        form.addRow("Loop", self.loop_spin)
        form.addRow("Actions", self.actions_edit)
        self.layout.addLayout(form)

        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        self.layout.addWidget(btn_box)

    def get_profile(self) -> MacroProfile:
        actions: List[KeyAction] = []
        for line in self.actions_edit.toPlainText().splitlines():
            if not line.strip():
                continue
            typ, code, delay = line.split(",")
            actions.append(KeyAction(type=typ.strip(), code=code.strip(), delay_ms=int(delay)))
        return MacroProfile(
            hotkey=self.hotkey_edit.text(),
            description=self.desc_edit.text(),
            actions=actions,
            loop=self.loop_spin.value(),
        )


class Controller(QtWidgets.QMainWindow):
    """Main application controller."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Dia4AutoKey")
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Hotkey", "Description", "Loop", "Delay"])
        self.setCentralWidget(self.table)
        toolbar = QtWidgets.QToolBar()
        self.addToolBar(toolbar)
        add_act = toolbar.addAction("Add")
        del_act = toolbar.addAction("Delete")
        start_act = toolbar.addAction("Start")
        stop_act = toolbar.addAction("Stop")
        add_act.triggered.connect(self.add_macro)
        del_act.triggered.connect(self.delete_macro)
        start_act.triggered.connect(self.start_selected)
        stop_act.triggered.connect(self.stop_selected)
        self.status = self.statusBar()

        self.engine = MacroEngine()
        self.emergency = EmergencyStopListener(self.engine)
        self.emergency.start()

        self.macros: List[MacroProfile] = []
        self.load_profiles()

    def load_profiles(self) -> None:
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            self.macros = [MacroProfile(**m) for m in data]
            self.refresh_table()

    def save_profiles(self) -> None:
        CONFIG_PATH.write_text(json.dumps([m.dict() for m in self.macros], ensure_ascii=False, indent=2), encoding="utf-8")

    def refresh_table(self) -> None:
        self.table.setRowCount(len(self.macros))
        for row, macro in enumerate(self.macros):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(macro.hotkey))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(macro.description or ""))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(macro.loop)))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(macro.delay_between_loops_ms)))

    def add_macro(self) -> None:
        dlg = MacroDialog(self)
        if dlg.exec_() == QtWidgets.QDialog.Accepted:
            macro = dlg.get_profile()
            self.macros.append(macro)
            self.refresh_table()
            self.save_profiles()

    def delete_macro(self) -> None:
        row = self.table.currentRow()
        if row >= 0:
            self.macros.pop(row)
            self.refresh_table()
            self.save_profiles()

    def start_selected(self) -> None:
        row = self.table.currentRow()
        if row >= 0:
            macro = self.macros[row]
            self.engine.play_macro(macro)
            self.status.showMessage(f"Started {macro.hotkey}")

    def stop_selected(self) -> None:
        row = self.table.currentRow()
        if row >= 0:
            macro = self.macros[row]
            self.engine.stop_macro(macro.hotkey)
            self.status.showMessage(f"Stopped {macro.hotkey}")

