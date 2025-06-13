"""Auto-generated UI module."""
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Hotkey", "Description", "Loop", "Delay"])
        self.verticalLayout.addWidget(self.table)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add")
        self.editButton = QtWidgets.QPushButton("Edit")
        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.editButton)
        self.buttonLayout.addWidget(self.deleteButton)
        self.verticalLayout.addLayout(self.buttonLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
