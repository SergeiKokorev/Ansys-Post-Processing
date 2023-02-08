import os
import sys
import re

from typing import IO

IMPORTED = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.path.pardir
))
sys.path.append(IMPORTED)

from data.models import Data, DataCollectionCache
from data.model_types import DOMAIN, INTERFACE


def builder(fp: IO):
    dmn_pattern = re.compile(r'domain:[\w\s\d]*')
    bnd_pattern = re.compile(r'boundary:[\s\d\w]*')
    dmn_type_pattern = re.compile(r'domain type = [\w\d\s]*')
    bnd_type_pattern = re.compile(r'boundary type = [\w\s\d]*')
    dmn_end = re.compile(r'domain\s+models:\s*')
    bnd_end = re.compile(r'boundary conditions:')
    dmn_find = False
    bnd_find = False
    dmn_id = 0
    bnd_id = 0
    domains = DomainCollectionCache()

    for line in fp.readlines():
        if re.fullmatch(dmn_end, line.lower().strip()):
            dmn_find = False
            bnd_find = False
        if re.fullmatch(bnd_end, line.lower().strip()):
            bnd_find = False
        if re.fullmatch(pattern=dmn_pattern, string=line.lower().strip()):
            dmn = Domain(domain=line.split(sep=':')[1].strip())
            dmn_find = True
            dmn.set_id(dmn_id)
            domains.add(dmn, dmn_id)
            dmn_id += 1
        if dmn_find and re.fullmatch(dmn_type_pattern, line.lower().strip()):
            dmn.domain_type = line.split('=')[1].strip()
        if dmn_find and re.fullmatch(bnd_pattern, line.lower().strip()):
            bnd_find = True
            bnd = Interface(interface=line.split(sep=':')[1].strip())
            bnd.set_id(bnd_id)
            dmn.add_interface(bnd)
            bnd_id += 1
        if bnd_find and re.fullmatch(bnd_type_pattern, line.lower().strip()):
            bnd.boundary = line.split('=')[1].strip()

    return domains

class Interface(Data):

    def __init__(self, **kwargs):
        self.interface: str = kwargs.get('interface', None)
        self.boundary: str = kwargs.get('boundary', None)

        super().__init__(self)
        self.type = INTERFACE

    def data(self) -> dict:
        return {self.id: {
            'interface': self.interface, 'boudary_type': self.boundary,
        }}

    def update(self, *kwargs) -> None:
        self.interface: str = kwargs.get('interface', None)
        self.boundary: str = kwargs.get('boundary', None)
        return super().update()

    def __str__(self) -> str:
        return f'\tBOUNDARY: {self.interface}\n\t\tBOUNDARY TYPE = {self.boundary}\n'

    def __repr__(self):
        return f'{self.id}: {self.__class__.__name__}(interface={self.interface}, type={self.type})\n'

class Domain(Data):

    def __init__(self, **kwargs):
        self.domain: str = kwargs.get('domain', None)
        self.interfaces: list = kwargs.get('interfaces', [])
        self.domain_type: str = kwargs.get('domain_type', None)

        super().__init__(self)
        self.type = DOMAIN

    def data(self) -> dict:
        return {self.id: {'domain': self.domain, 
                          'interfaces': [i.data() for i in self.interfaces],
                          'type': self.domain_type}}

    def update(self, **kwargs) -> None:
        self.domain: str = kwargs.get('domain', None)
        self.interfaces: list = kwargs.get('interfaces', None)
        self.domain_type: str = kwargs.get('domain_type', None)
        return super().update()

    def add_interface(self, interface: Interface) -> None:
        if not isinstance(interface, Interface):
            raise TypeError(f'Interface must be Iterface class type, not {type(interface).__name__}')
        self.interfaces.append(interface)

    def show_domain(self) -> str:
        return f'{self.get_id()} {self.get_type()}: {self.domain} ({self.domain_type})\n'

    def __str__(self) -> str:
        interfaces = ''
        for interface in self.interfaces:
            interfaces += f'{interface}\n'
        return f'DOMAIN: {self.domain}\n\tDomain type = {self.domain_type}\n' \
            f'\tBOUNDARIES = {str([interface.interface for interface in self.interfaces])[1:-1]}\n'

    def __repr__(self):
        return f'{self.id}: {self.__class__.__name__}(domain={self.domain}, type={self.type}, ' \
            f'interfaces={[interface.interface for interface in self.interfaces]})\n'

class DomainCollectionCache(DataCollectionCache):

    def __str__(self):
        string = ''
        for data in self.cache[DOMAIN]:
            string += str(data)
        return string

    def __repr__(self):
        string = ''
        for data in self.cache[DOMAIN]:
            string += repr(data)
        return string

    def data(self) -> dict:
        data = {}
        for dmn in self.cache[DOMAIN]:
            data.update(dmn.data())
        return data

    def show_domains(self) -> str:
        string = ''
        for val in self.cache[DOMAIN]:
            string += val.show_domain()
        return string

    @classmethod
    def get(cls, gid: int):
        return super().get(gid, DOMAIN)

    @classmethod
    def delete(cls, sid: int):
        return super().__init__(sid, DOMAIN)

    def json_serialize(self) -> list:
        return self.data()

    def json_deserialize(self, fp) -> dict:
        return super().json_deserialize(fp)
