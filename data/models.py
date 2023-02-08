import json

from dataclasses import dataclass
from copy import deepcopy
from abc import ABCMeta, abstractmethod, abstractclassmethod


from data.model_types import *


class Director(object, metaclass=ABCMeta):

    def __init__(self):
        self._builder = None

    @abstractmethod
    def construct(self):
        pass

    def set_builder(self, builder):
        self._builder = builder

    def get_constructed_object(self):
        return self._builder.obj


class Builder(object, metaclass=ABCMeta):
    
    def __init__(self, constructed_object):
        self.obj = constructed_object


@dataclass
class DataModel(metaclass=ABCMeta):
    id: int
    type: str


@dataclass
class Data(metaclass=ABCMeta):

    id: int = None
    type: str = None

    @abstractmethod
    def data(self) -> dict  :
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    def get_type(self) -> str:
        return self.type

    def get_id(self) -> int:
        return self.id

    def set_id(self, sid: int):
        if isinstance(sid, int):
            self.id = sid

    def clone(self) -> object:
        return deepcopy(self)


class DataCollectionCache(metaclass=ABCMeta):
    
    cache = {}

    @staticmethod
    def add(data: Data, sid: int) -> None:
        # ID must be integer type and data must be derived class of Data
        if not isinstance(sid, int):
            raise TypeError(f'ID must be integer type, not {type(sid).__name__}')
        if not isinstance(data, Data):
            raise TypeError(f'Wrong data type. Class {type(data).__name__}')

        # get table name
        data_type = data.get_type()
        # get id if there is not table with data_type return [None]
        idx = [i.id if i else None for i in DataCollectionCache.cache.get(data_type, [])]

        # ID must be unique
        if sid in idx:
            raise IndexError('ID must be unique.')

        # if there is not yet data_type in cache initialize new cache key
        if not idx:
            DataCollectionCache.cache[data_type] = []

        data.set_id(sid)
        DataCollectionCache.cache[data_type].append(data)

    @abstractmethod
    def data(self) -> dict:
        pass

    @abstractclassmethod
    def get(cls, gid: int, data_type: str) -> Data:
        if not isinstance(gid, int):
            raise IndexError(f'Index must be integer type, not {type(gid).__name__}')
        if not (DATA := DataCollectionCache.cache.get(data_type, None)):
            raise KeyError(f'There is not data with the key {data_type}')
        else:
            if gid not in [data.id for data in DATA]:
                raise IndexError(f'There is no data with id {gid}')
            return [data for data in DATA if data.id == gid][0].clone()
    
    @abstractclassmethod
    def delete(cls, sid: int, data_type: str) -> None:
        if not  isinstance(sid, int):
            pass
        try:
            del DataCollectionCache.cache[data_type][sid]
        except KeyError:
            raise KeyError(f'There is no data with type {data_type}')
        except IndexError as err:
            raise IndexError(f'There is no datatype {data_type} with index {sid}')

    @abstractmethod
    def json_serialize(self, type) -> list:
        pass

    @abstractmethod
    def json_deserialize(self, fp) -> dict:
        return json.load(fp)

    def __str__(self):
        string = ''
        for data in self.cache.values():
            string += str(data)
        return string

    def __repr__(self):
        string = ''
        for data in self.cache.values():
            string += repr(data)
        return string
