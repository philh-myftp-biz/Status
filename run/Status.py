from ..Items import VirtualDisks, HardDrives, PCIeCards, Services, Towers, Item
from philh_myftp_biz.pc.hardware import HealthStatus as HS
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.time import sleep
from philh_myftp_biz.db import Color
from . import process_HardDrives
from itertools import cycle

def LogStatus(items: list[Item]) -> None:
    for item in items:

        print(
            f'   {item.Name.ljust(35, '.')}: ',
            end = ''
        )

        hs = item.HealthStatus
        print(
            hs.name,
            color = {
                HS.UNKNOWN: Color.GRAY,
                HS.HEALTHY: Color.GREEN,
                HS.WARNING: Color.YELLOW,
                HS.NOTGOOD: Color.RED,
                HS.MISSING: Color.GRAY,
                HS.RUNNING: Color.GREEN,
                HS.STOPPED: Color.RED,
            } [hs],
        )

for i in cycle(range(5)):

    cls()

    print("\n|-----------------------------------| Server Status |-----------------------------------|\n")    

    print('\nHard Drives:')
    for hdd in HardDrives:
        i or process_HardDrives(0, [hdd])
        LogStatus([hdd])

    print('\nPCIe Cards:')
    LogStatus(PCIeCards)

    print('\nVirtual Disks:')
    LogStatus(VirtualDisks)

    print('\nTowers:')
    LogStatus(Towers)

    print('\nServices:')
    LogStatus(Services)

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, show=True)
