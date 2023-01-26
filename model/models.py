from copy import deepcopy
from abc import ABCMeta, abstractmethod


from model.model_types import *


class Data(metaclass=ABCMeta):

    def __init__(self):
        self.id: int = None
        self.type: str = None

    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def set_id(self, sid: int):
        if isinstance(sid, int):
            self.id = sid

    def clone(self):
        return deepcopy(self)


class DataCollectionCache(metaclass=ABCMeta):
    
    cache = {}

    # @staticmethod
    # @abstractmethod
    # def get(gid: int) -> Data:
    #     if isinstance(sid, int):
    #         DATA = DataCollectionCache.cache[sid]
    #         return DATA.clone()
    #     else:
    #         return DATA
    
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

    @staticmethod
    def delete(sid: int, type: str) -> None:
        if isinstance(sid, int):
            try:
                del DataCollectionCache.cache[type][sid]
            except KeyError:
                raise KeyError(f'There is no data with type {type}')
            except IndexError as err:
                raise IndexError(f'There is no datatype {type} with index {sid}')
        else:
            pass

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

    @abstractmethod
    def json_serialize(self, type) -> list:
        pass
