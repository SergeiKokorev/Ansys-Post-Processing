from copy import deepcopy
from abc import ABCMeta, abstractmethod


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


    @staticmethod
    @abstractmethod
    def get(sid: int) -> Data:
        if isinstance(sid, int):
            DATA = DataCollectionCache.cache.get(sid, None)
            return DATA.clone()
        else:
            pass
    
    @staticmethod
    @abstractmethod
    def add(data: Data, sid: int) -> None:
        if isinstance(sid, int) and isinstance(data, Data):
            data.set_id(sid)
            DataCollectionCache.cache[data.get_id()] = data
        else:
            pass
    
    @staticmethod
    @abstractmethod
    def delete(sid: int) -> None:
        if isinstance(sid, int):
            del DataCollectionCache.cache[sid]
        else:
            pass

    @abstractmethod
    def json_serialize(self) -> list:
        data = []
        for val in self.cache.values():
            data.append(val.data())

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
