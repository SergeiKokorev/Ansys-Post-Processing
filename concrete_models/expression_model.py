import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from model.models import Data, DataCollectionCache


class ExpressionModel(Data):

    def __init__(self, *args):
        self.var: str = args[0]
        self.expr: str = args[1]
        self.descr: str = args[2]
        super().__init__()
        self.type = 'expression'

    def data(self) -> dict:
        return {'var': self.var, 'expr': self.expr, 'descr': self.descr}

    def update(self, *args) -> None:
        self.var: str = args[0]
        self.expr: str = args[1]
        self.descr: str = args[2]
        return super().update()

    def __repr__(self):
        return f'id: {self.get_id()}\t{self.var} = {self.expr} ({self.descr})\n'

    def __str__(self):
        return f'!\t{self.var} = {self.expr}; #{self.descr}\n'


class ExpressionCollectionCache(DataCollectionCache):
    cache = {}


    @staticmethod
    def get(sid: int):
        if isinstance(sid, int):
            DATA = ExpressionCollectionCache.cache.get(sid, None)
            return DATA.clone()
        else:
            pass

    @staticmethod
    def add(data: ExpressionModel, sid: int):
        if isinstance(sid, int) and isinstance(data, ExpressionModel):
            data.set_id(sid)
            ExpressionCollectionCache.cache[data.get_id()] = data
        else:
            pass

    @staticmethod
    def delete(sid: int):
        if isinstance(sid, int):
            del ExpressionCollectionCache.cache[sid]
        else:
            pass

    def json_serialize(self) -> list:
        data = []
        for val in self.cache.values():
            data.append(val.data())
        return data
