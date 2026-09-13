from philh_myftp_biz.modules import Service as __Service
from philh_myftp_biz.modules import Module as __Module
from philh_myftp_biz.functools import clear_cache
from functools import cached_property
from dataclasses import dataclass

class Module(__Module):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.exists

class Service(__Service):

    @cached_property
    def Name(self) -> str:
        return self.path
    
    @property
    def Connected(self) -> bool:
        return self.running

@dataclass
class Tower:

    ID: str

    @cached_property
    def Name(self) -> str:
        return f'Tower {self.ID}'

    @cached_property
    def Connected(self) -> bool:
        from .__init__ import HardDrives

        clear_cache(self)

        _HardDrives = filter(
            lambda hdd: (hdd.Tower == self.ID),
            HardDrives
        )

        _HardDrives = filter(
            lambda hdd: hdd.Connected,
            _HardDrives
        )

        return next(_HardDrives, None) != None
