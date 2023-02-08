from PySide6.QtWidgets import (
    QMainWindow,
    QWidget, QLabel, QComboBox,
    QListWidget, QPushButton, 
)
from PySide6.QtCore import QSize


from gui.model import *
from consts.gui import *
from gui import view


class MainWindow(QMainWindow):
    def __init__(self, parent=None, **settings):
        super().__init__(parent)

        self.window = QMainWindow()
        self.resize(QSize(*settings.get('size', SCREEN_SIZE)))
        self.setWindowTitle(settings.get('title', 'Main Window'))

        myview = view.View()
        self.setCentralWidget(myview)
