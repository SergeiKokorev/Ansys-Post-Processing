import os
import sys

from abc import ABCMeta, abstractmethod

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from model.models import *


class GuiModel(Data):
    pass


class WidgetCollection(DataCollectionCache):
    pass
