from ..Items import VirtualDisks, HardDrives, PCIeCards, Services, Towers, Item
from philh_myftp_biz.pc.hardware import HealthStatus as HS
from philh_myftp_biz.terminal import cls, print
from philh_myftp_biz.time import sleep
from philh_myftp_biz.db import Color
from philh_myftp_biz.pc import Path

def LogStatus(
    title: str,
    items: list[Item]
) -> None:
    
    if len(items) > 0:

        print(f'\n{title}:')
    
        for item in items:

            print(
                f'   {item.Name.ljust(35, '.')}: ',
                end = ''
            )

            print(
                item.HealthStatus.name,
                color = {
                    HS.UNKNOWN: Color.GRAY,
                    HS.HEALTHY: Color.GREEN,
                    HS.WARNING: Color.YELLOW,
                    HS.NOTGOOD: Color.RED,
                    HS.MISSING: Color.GRAY,
                    HS.RUNNING: Color.GREEN,
                    HS.STOPPED: Color.RED,
                } [item.HealthStatus],
            )

while True:

    cls()

    print("\n|-----------------------------------| Server Status |-----------------------------------|\n")    

    LogStatus('Hard Drives', HardDrives)

    LogStatus('PCIe Cards', PCIeCards)

    LogStatus('Virtual Disks', VirtualDisks)

    LogStatus('Towers', Towers)

    LogStatus('Services', Services)

    print("\n|---------------------------------------------------------------------------------------|\n")

    sleep(15, show=True)
