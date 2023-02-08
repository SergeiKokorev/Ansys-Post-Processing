import os
import sys


from abc import ABCMeta, abstractmethod
from PySide6 import QtWidgets, QtCore, QtGui

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from consts.gui import *



class TabWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None, **settings):
        super().__init__(parent, **settings)
        self.setFont(QtGui.QFont(*QTABBFONT))
        self.setTabPosition(settings.get('position', QtWidgets.QTabWidget.TabPosition.West))

    def setTabs(self, tabs: dict):
        for title, tab in tabs.items():
            if isinstance(tab, QtWidgets.QWidget):
                self.addTab(tab, title)
            elif isinstance(tab, (QtWidgets.QGridLayout,
            QtWidgets.QLayout, QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout)):
                self.setLayout(tab, title)


class GridLayout(QtWidgets.QGridLayout):

    def __init__(self, parent=None, **settings):
        super().__init__(parent)

        self.setContentsMargins(QtCore.QMargins(*settings.get('margins', [5, 5, 5, 5])))
        self.setHorizontalSpacing(settings.get('hspasing', 10))
        self.setVerticalSpacing(settings.get('vspacing', 10))


class Actions(QtGui.QAction):
    
    def __init__(self, parent=None, **settings):
        super().__init__(parent)
        
        self.setParent(parent)
        actions = settings.get('actions', {})
        for action, func in actions.items():
            self.setText(action)
            self.triggered.connect(func)


class ToolBar(QtWidgets.QToolBar):

    def __init__(self, parent=None, **settings):
        super().__init__(parent)

        self.setMovable(settings.get('movable', False))
        self.setFloatable(settings.get('floatable', False))
        self.setIconSize(QtCore.QSize(*settings.get('iconsize', [24, 24])))


class ListWidget(QtWidgets.QListWidget):
    
    def __init__(self, parent=None, **settings):
        super().__init__(parent)

        self.setFont(QtGui.QFont(*QLISTFONT))
        self.setMinimumSize(QtCore.QSize(*settings.get('minsize', [256, 64])))
