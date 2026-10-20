from .. import install # Run install.py

from philh_myftp_biz.pc import NAME, Path
from philh_myftp_biz.terminal import Log
from importlib import import_module

from philh_myftp_biz.pc.hardware import HardDrive, PCIeCard, VirtualDisk, Tower
from philh_myftp_biz.modules import Module, Service

VirtualDisks: list[VirtualDisk]
HardDrives: list[HardDrive]
PCIeCards: list[PCIeCard]
Services: list[Service]
Modules: list[Module]
Towers: list[Tower]

type Item = (VirtualDisk | HardDrive | PCIeCard | Service | Module | Tower)

_cache: dict[str, list[Item]] = {}

def __getattr__(name:str) -> list[Item]:

    if name in _cache:
        return _cache[name]

    Log.VERB(f'Collecting Items: {name}')

    try:
        items: list[Item] = import_module(
            name = f'.{NAME.replace('-', '')}.{name}', 
            package = __name__
        ).Items.copy()
    except ModuleNotFoundError:
        items = []

    match name:

        case 'HardDrives':
            items += filter(
                lambda d: not any(i.SN==d.SN for i in items),
                HardDrive.search()
            )

        case 'Services':
            _dir = Path('C:/Scripts/Services/')
            items += [Service(d) for d in _dir.children if d.is_dir and d.name[0]!='_']

        case 'Modules':
            items.insert(0, Module('C:/Scripts/'))

        case 'Towers':
            for t in items:
                t.HardDrives = __getattr__("HardDrives")

    _cache[name] = items
    return items

