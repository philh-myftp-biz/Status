from philh_myftp_biz.pc.hardware import Device
from functools import cached_property

class Tower(Device):

    def __init__(self, ID:str) -> None:
        super().__init__()
        self.ID = ID

    @cached_property
    def Name(self) -> str:
        return f'Tower {self.ID}'

    @cached_property
    def Connected(self) -> bool:
        from .__init__ import HardDrives

        _HardDrives = filter(
            lambda hdd: (hdd.Tower == self.ID),
            HardDrives
        )

        _HardDrives = filter(
            lambda hdd: hdd.Connected,
            _HardDrives
        )

        return next(_HardDrives, None) != None

