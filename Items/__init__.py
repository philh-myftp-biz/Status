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

from philh_myftp_biz.modules import Module
from philh_myftp_biz.pc import NAME, Path
from philh_myftp_biz.terminal import Log
from importlib import import_module
from wmi import WMI

from ._cpp import HardDrive, PCIeCard, VirtualDisk
from .Service import Service
from .Tower import Tower

def getItems(file:str) -> list:    

    Log.VERB(f'Collecting Items: {file}')

    dirname = NAME.replace('-', '')

    try:
    
        return import_module(
            name = f'.{dirname}.{file}', 
            package = __name__
        ).Items
    
    except ModuleNotFoundError:
        return []

#=============

HardDrives: list[HardDrive] = getItems('HardDrives')

for disk in WMI().Win32_DiskDrive():

    sn: str = disk.SerialNumber.strip()

    if not any ([ 
        sn.startswith('{'),
        *((i.SN == sn) for i in HardDrives)
    ]):
        HardDrives += [HardDrive(
            Tower = '?',
            Conn = '?',
            ID = 0,
            SN = sn
        )]

#=============

Services: list[Service] = getItems('Services')

Services += [Service(d) for d in Path('C:/Scripts/Services/').children if d.is_dir and d.name[0]!='_']

#=============

Modules: list[Module] = []
Modules += [Module('C:/Scripts/')]
Modules += getItems('Modules')

#=============

PCIeCards: list[PCIeCard] = getItems('PCIeCards')

Towers: list[Tower] = getItems('Towers')

VirtualDisks: list[VirtualDisk] = getItems('VirtualDisks')

#==========================================================

