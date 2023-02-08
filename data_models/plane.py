import os
import sys
import re

from typing import IO

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from data.models import *
from data.model_types import PLANE


class PlaneDirector(Director):
    pass


class AbstractPlaneBuilder(object, metaclass=ABCMeta):

    def __init__(self):
        self._obj = None

    @abstractmethod
    def set_builder(self):
        pass

    @abstractmethod
    def get_builder(self):
        pass


class Plane(Data):
    
    def __init__(self):
        self.plane: str = None
        self.plane_type: str = None
        self.difinition: dict = None

        super().__init__()
        self.type = PLANE

    @abstractmethod
    def set_obj(self):
        pass

    def set_name(self, name: str) -> None:
        self.plane = name

    def update(self) -> None:
        return super().update()

    def data(self) -> dict:
        return super().data()

    def __repr__(self):
        return f'id: {self.get_id()}\nPlane: {self.plane}({self.plane_type})\nDifinition: {self.difinition}'

    def __str__(self):
        cse = f'PLANE: {self.plane}\n\tOption = {self.plane_type}\n'
        return cse


class PlaneThreePoints(Plane):

    def __init__(self):
        self.points: list = None
        super().__init__()

    def set_obj(self, plane_type: str, plane: str, points: list) -> None:
        self.plane = plane
        self.points = points
        self.plane_type = plane_type
        self.difinition = {
            'Point 1': self.points[0], 
            'Point 2': self.points[1], 
            'Point 3': self.points[2]
        }
        return super().set_obj()

    def update(self, points: list, plane: str) -> None:
        self.points = points
        self.plane = plane
        self.difinition = {
            'Point 1': self.points[0], 
            'Point 2': self.points[1], 
            'Point 3': self.points[2]
        }
        return super().update()

    def __str__(self):
        cse = super().__str__()
        for k, v in self.difinition.items():
            cse += f'\t{k} = {str(v)[1:-1]}\n'
        cse += 'END\n'
        return cse

class PlanePointNormal(Plane):

    def __init__(self):
        self.normal: list = None
        self.point: list = None
        super().__init__()

    def set_obj(self, plane_type: str, plane: str, point: list, normal: list) -> None:
        self.plane = plane
        self.point = point
        self.normal = normal
        self.plane_type = plane_type
        self.difinition = {'Normal': self.normal, 'Point': self.point}

    def update(self, point: list, normal: list, plane: str) -> None:
        self.plane = plane
        self.point = point
        self.normal = normal
        self.difinition = {'Normal': self.normal, 'Point': self.point}
        return super().update()

    def __str__(self):
        cse = super().__str__()
        for k, v in self.difinition.items():
            cse += f'{k} = {str(v)[1:-1]}\n'
        cse += 'END\n'
        return cse

class PlaneOffset(Plane):

    offset_axis = {
        'XY Plane': 'Z', 'YZ Plane': 'X', 'ZX Plane': 'Y'
    }

    def __init__(self):
        self.offset: float = None
        super().__init__()

    def set_obj(self, plane: str, plane_type: str, offset: float) -> None:
        self.plane = plane
        self.plane_type = plane_type
        self.offset = offset
        self.difinition = {self.offset_axis[self.plane_type]: self.offset}
        return super().set_obj()

    def update(self, plane_type: str, offset: float, plane: str) -> None:
        self.plane_type = plane_type
        self.plane = plane
        self.offset = offset
        self.difinition = {self.offset_axis[self.plane_type]: self.offset}
        return super().update()

    def __str__(self):
        cse = super().__str__()
        for k, v in self.difinition.items():
            cse += f'\t{k} = {v}\n'
        cse += 'END\n'
        return cse

class PlaneBuilder(AbstractPlaneBuilder):

    PlaneType = {
        'Three Points': PlaneThreePoints,
        'Point and Normal': PlanePointNormal,
        'YZ Plane': PlaneOffset,
        'ZX Plane': PlaneOffset,
        'XY Plane': PlaneOffset
    }

    def __init__(self, plane_type: str):
        self._obj = self.PlaneType.get(plane_type, PlaneThreePoints())()

    def buildPlane(self, **settings):
        self._obj.set_obj(**settings)
        return self._obj

    def set_builder(self, builder: Plane):
        self._obj = builder
        return super().set_builder()

    def get_builder(self) -> Plane:
        return self._obj

class PlaneCollection(DataCollectionCache):

    def __str__(self):
        string = ''
        for data in self.cache[PLANE]:
            string += str(data)
    
        return string

    def __repr__(self):
        string = ''
        for data in self.cache[PLANE]:
            string += repr(data)

        return string

    @classmethod
    def get(cls, gid: int):
        return super().get(gid, PLANE)

    @classmethod
    def delete(cls, sid: int):
        return super().delete(sid, PLANE)

    def data(self) -> dict:
        data = {}
        for plane in self.cache[PLANE]:
            data.update(plane.data())
        return data

    def json_serialize(self) -> dict:
        return self.data()

    def json_deserialize(self, fp) -> dict:
        return super().json_deserialize(fp)

