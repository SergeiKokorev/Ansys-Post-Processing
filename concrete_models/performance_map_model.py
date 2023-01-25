import os
import sys

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from model.models import Data, DataCollectionCache


class PerfoprmanceMapModel(Data):

    def __init__(self, *args):
        self.curve: str = str(args[0])
        self.files: list = args[1]
        self.inlet: str = str(args[2])
        self.outlet: str = str(args[3])
        super().__init__()
        self.type = 'performance_map'

    def data(self) -> dict:
        return {'curve': self.curve, 'files': self.files, 
                'inlet': self.inlet, 'outlet': self.outlet}

    def update(self, args) -> None:
        self.curve: str = str(args[0])
        self.files: list = args[1]
        self.inlet: str = str(args[2])
        self.outlet: str = str(args[3]        )
        return super().update()

    def __repr__(self):
        return f'Curve: {self.curve}\nRes files: {self.files}\nInlet: {self.inlet}\nOutlet: {self.outlet}'

    def __str__(self):
        return f'!\tmy @files = ({str(self.files)[1:-1]});\n'


class PerformanceMapCollection(DataCollectionCache):
    cache = {}


    @staticmethod
    def get(sid: int):
        if isinstance(sid, int):
            DATA = PerformanceMapCollection.cache.get(sid, None)
            return DATA.clone()
        else:
            pass

    @staticmethod
    def add(data: PerfoprmanceMapModel, sid: int):
        if isinstance(sid, int) and isinstance(data, PerfoprmanceMapModel):
            data.set_id(sid)
            PerformanceMapCollection.cache[data.get_id()] = data
        else:
            pass

    @staticmethod
    def delete(sid: int):
        if isinstance(sid, int):
            del PerformanceMapCollection.cache[sid]
        else:
            pass

    def json_serialize(self) -> list:
        data = []
        for val in self.cache.values():
            data.append(val.data())
        return data
