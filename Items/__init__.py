from .. import install # Run install.py

from subprocess import run
from os.path import exists

lib = 'C:/Scripts/lib'
pyd = 'C:/Scripts/Items/_cpp.pyd'

#==========================================================
# BUILD

exists(pyd) or run([
    'Powershell.exe', '-File', f'{lib}/pybind/build.ps1',
    '-Src', f"{lib}/pyobj/main.cpp",
    '-Dst', pyd,
    '-Include', f"{lib}/json/include"
])

#==========================================================
# SCAN ITEMS

from philh_myftp_biz.pc import NAME, Path
from philh_myftp_biz.terminal import Log
from importlib import import_module
from wmi import WMI

from ._cpp import HardDrive, PCIeCard, VirtualDisk
from ._py import Module, Service, Tower

VirtualDisks: list[VirtualDisk]
HardDrives: list[HardDrive]
PCIeCards: list[PCIeCard]
Services: list[Service]
Modules: list[Module]
Towers: list[Tower]

_cache = {}

def __getattr__(name:str):

    if name in _cache:
        return _cache[name]

    Log.VERB(f'Collecting Items: {name}')

    try:
        items: list = import_module(
            name = f'.{NAME.replace('-', '')}.{name}', 
            package = __name__
        ).Items.copy()
    except ModuleNotFoundError:
        items = []

    match name:

        case 'HardDrives':
            for disk in WMI().Win32_DiskDrive():

                sn: str = disk.SerialNumber.strip()
                _not_exists = not any(i.SN==sn for i in items)
                _valid_sn = not sn.startswith('{')

                if _not_exists and _valid_sn: 
                    items += [HardDrive(
                        Tower = '?',
                        Conn = '?',
                        ID = 0,
                        SN = sn
                    )]

        case 'Services':
            _dir = Path('C:/Scripts/Services/')
            items += [Service(d) for d in _dir.children if d.is_dir and d.name[0]!='_']

        case 'Modules':
            items.insert(0, Module('C:/Scripts/'))

    _cache[name] = items
    return items

