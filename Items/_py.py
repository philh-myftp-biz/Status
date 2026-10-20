from philh_myftp_biz.pc.hardware import HealthStatus as HS
from philh_myftp_biz.pc.hardware import HardDrive, Device
from functools import cached_property
from pickle import dumps

class Tower(Device):

    def __init__(self, t:str) -> None:
        super().__init__()
        self.t = t

    @cached_property
    def HealthStatus(self) -> HS:

        if not self.Connected:
            return HS.MISSING

        for stat in (HS.NOTGOOD, HS.WARNING, HS.HEALTHY):
            if any(hdd.HealthStatus==stat for hdd in self._HardDrives):
                return stat
        
        return HS.UNKNOWN

    @cached_property
    def _HardDrives(self) -> tuple[HardDrive, ...]:
        from . import _cache
        return tuple(filter(
            lambda hdd: (hdd.Tower == self.t),
            _cache['HardDrives']
        ))

    @property
    def ID(self) -> int:
        return int.from_bytes( dumps(self.t, 4) )

    @cached_property
    def Name(self) -> str:
        return f'Tower {self.t}'

    @cached_property
    def Connected(self) -> bool:

        _HardDrives = filter(
            lambda hdd: hdd.Connected,
            self._HardDrives
        )

        return next(_HardDrives, None) is not None

