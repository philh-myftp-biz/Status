from philh_myftp_biz.pc.hardware import HardDrive, Device
from functools import cached_property
from pickle import dumps

class Tower(Device):

    def __init__(self, t:str) -> None:
        super().__init__()
        self.t = t

    @property
    def ID(self) -> int:
        return int.from_bytes( dumps(self.t, 4) )

    @cached_property
    def Name(self) -> str:
        return f'Tower {self.t}'

    @cached_property
    def Connected(self) -> bool:
        from . import _cache
        HardDrives: list[HardDrive] = _cache['HardDrives']

        _HardDrives = filter(
            lambda hdd: (hdd.Tower == self.t),
            HardDrives
        )

        _HardDrives = filter(
            lambda hdd: hdd.Connected,
            _HardDrives
        )

        return next(_HardDrives, None) != None

