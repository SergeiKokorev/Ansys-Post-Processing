import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from model.models import Data, DataCollectionCache
from model.model_types import EXPRESSION



class ExpressionModel(Data):

    def __init__(self, *args):
        self.var: str = args[0]
        self.expr: str = args[1]
        self.descr: str = args[2]
        self.include: bool = True
        super().__init__()
        self.type = EXPRESSION

    def data(self) -> dict:
        return {self.id: {'var': self.var, 'expr': self.expr, 'descr': self.descr}}

    def update(self, *args) -> None:
        self.var: str = args[0]
        self.expr: str = args[1]
        self.descr: str = args[2]
        self.include: bool = args[3]
        return super().update()

    def __repr__(self):
        return f'id: {self.get_id()}\t{self.var} = {self.expr} ({self.descr})\n'

    def __str__(self):
        return f'!\t{self.var} = {self.expr}; #{self.descr}\n'


class ExpressionCollectionCache(DataCollectionCache):

    def __str__(self):
        string = ''
        for data in self.cache[EXPRESSION]:
            string += str(data)
        return string

    def __repr__(self):
        string = ''
        for data in self.cache[EXPRESSION]:
            string += repr(data)
        return string

    # @staticmethod
    # def get(gid: int):
    #     if isinstance(gid, int):
    #         DATA = ExpressionCollectionCache.cache[EXPRESSION]

    def json_serialize(self) -> list:
        data = {}
        for val in self.cache[EXPRESSION]:
            data.update(val.data())
        return data
