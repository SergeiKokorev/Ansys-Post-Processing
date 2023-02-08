import sys
import os



IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir
))
sys.path.append(IMPORTED)

from gui.model import *

from PySide6 import QtWidgets, QtCore, QtGui


# Concrete classes
class ExpressionTab(GridLayout):
    def __init__(self, parent=None):
        super().__init__(parent, margins=[5, 10, 5, 10], hspaing=5, vspacing=10)
        self.expressions = ListWidget(parent=self)
        self.addWidget(self.expressions)

        


class View(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

    