import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from data.models import Data, DataCollectionCache
from data.model_types import PERFORMANCE


class PerfoprmanceMapModel(Data):

    def __init__(self, *args):
        self.curve: str = args[0]
        self.files: list = args[1]
        self.inlet: str = args[2]
        self.outlet: str = args[3]
        super().__init__()
        self.type = PERFORMANCE

    def data(self) -> dict:
        return {self.id: {'curve': self.curve, 'files': self.files, 
                'inlet': self.inlet, 'outlet': self.outlet}}

    def update(self, args) -> None:
        self.curve: str = str(args[0])
        self.files: list = args[1]
        self.inlet: str = str(args[2])
        self.outlet: str = str(args[3])
        return super().update()

    def __repr__(self):
        return f'Curve: {self.curve}\nRes files: {self.files}\nInlet: {self.inlet}\nOutlet: {self.outlet}\n'

    def __str__(self):
        return f'!\tmy @files = ({str(self.files)[1:-1]});\n'


class PerformanceMapCollection(DataCollectionCache):
    
    def __str__(self):
        string = ''
        for data in self.cache[PERFORMANCE]:
            string += str(data)
        return string

    def __repr__(self):
        string = ''
        for data in self.cache[PERFORMANCE]:
            string += repr(data)
        return string

    def data(self) -> dict:
        data = {}
        for pm in self.cache[PERFORMANCE]:
            data.update(pm.data())
        return data

    @classmethod
    def get(cls, gid: int):
        return super().get(gid, PERFORMANCE)

    @classmethod
    def delete(cls, sid: int):
        return super().delete(sid, PERFORMANCE)

    def json_serialize(self) -> list:
        return self.data()

    def json_deserialize(self, fp) -> dict:
        return super().json_deserialize(fp)
