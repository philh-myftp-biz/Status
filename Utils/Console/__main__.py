from ... import install # Run install.py

from philh_myftp_biz.terminal.tree import Tree, Printer, run_tree
from philh_myftp_biz.pc import Path
from . import Memory

def printx(x:int, val:str) -> None:
    print(f'{x:>2d}:', val)

class TreeImpl(Tree):
    """
Phil's Server
[philh.myftp.biz]

MANAGEMENT  CONSOLE
"""

    class help:

        _NoArgs = """
HELP    | Show help message
CLS     | Clear the terminal
EXIT    | Exit the terminal

RUN     | Run a script

NAME    | Get Computer Name
IP      | Get IP Address
POWER   | Shutdown/Restart System

LIST    | List items
SELECT  | Select items
START   | Start items
STOP    | Stop items
ENABLE  | Enable items
DISABLE | Disable items
ARGS    | Set items' arguements
LOGS    | Open items' logs
EXPLORE | Open items in file explorer
"""

        list = """
LIST SERVICE      | Get a list of selected services
LIST MODULE       | Get a list of selected modules
LIST DISK         | Get a list of selected hard drives
LIST VDISK        | Get a list of selected virtual disks
LIST PCIE         | Get a list of selected pcie cards
LIST TOWER        | Get a list of selected towers
"""
            
        select = """
SELECT SERVICE [...] | Select services (Ex: select service 1,3)
SELECT MODULE  [...] | Select modules (Ex: select module ..5)
SELECT DISK    [...] | Select hard drives
SELECT VDISK   [...] | Select virtual disks
SELECT PCIE    [...] | Select pcie cards
SELECT TOWER   [...] | Select towers

[...] -> ['#', '#..', '..#', '#..#', '#,#']
"""
            
        start = """
START SERVICE | Start the selected services
"""
    
        stop = """
STOP SERVICE | Stop the selected services
"""
            
        enable = """
ENABLE SERVICE | Enable the selected services
ENABLE MODULE  | Setup dependencies for the selected modules
"""
            
        disable = """
DISABLE SERVICE | Disable the selected services
"""
            
        run = """
RUN *SCRIPT*    | Run a script in a new tab (Ex: run Interval.Startup)
RUN *SCRIPT* -v | Run a script in a new tab [VERBOSE] (Ex: run Interval.Startup -v)

SCRIPTS:
    - Utils.Update
    - Utils.Status
    - Utils.Console
    - Interval.Hour
    - Interval.Day
    - Interval.Week
    - Interval.Startup
"""
            
        args = """
ARGS SERVICE = *arg1* *arg2* ...   | Set the args for selected services
"""

        logs = """
LOGS SERVICE | Open the logs for the selected services
"""

        explore = """
EXPLORE SERVICE | Open the selected services in file explorer
EXPLORE MODULE  | Open the selected modules in file explorer
"""

        name = """
NAME   | Get the name of the current computer
"""

        ip = """
IP LAN | Get the current local ip
IP WAN | Get the current public ip
"""

        power = """
POWER SHUTDOWN | Shutdown system
POWER RESTART  | Restart system
"""

    @staticmethod
    def run( 
        script: str,
        *args: str
    ) -> None:
        from ...Items import Modules

        Printer.RunFile(
            path = f"C:/Scripts/{script.replace('.', '/')}.py",
            args = args
        )
        
        Modules[0].run(
            'vbs/run', script.title(), 
            'True', # VISIBLE
            *args
        )

    class select:

        @staticmethod
        def _all(
            rslice: str, 
            src: list, 
            dst: list
        ) -> None:
            from philh_myftp_biz.text import to_slice

            dst.clear()

            for slice in to_slice(rslice):

                _mod = src[slice]

                if isinstance(_mod, list):
                    dst += _mod
                else:
                    dst += [_mod]

        @staticmethod
        def service(rslice:str) -> None:
            from ...Items import Services

            TreeImpl.select._all(
                rslice = rslice,
                src = Services,
                dst = Memory.Services
            )
                 
            TreeImpl.list.service()

        @staticmethod
        def module(rslice:str) -> None:
            from ...Items import Modules

            TreeImpl.select._all(
                rslice = rslice,
                src = Modules,
                dst = Memory.Modules
            )
                 
            TreeImpl.list.module()

        @staticmethod
        def disk(rslice:str) -> None:
            from ...Items import HardDrives

            TreeImpl.select._all(
                rslice = rslice,
                src = HardDrives,
                dst = Memory.Disks
            )
                 
            TreeImpl.list.disk()

        @staticmethod
        def pcie(rslice:str) -> None:
            from ...Items import PCIeCards

            TreeImpl.select._all(
                rslice = rslice,
                src = PCIeCards,
                dst = Memory.PCIeCards
            )
                 
            TreeImpl.list.pcie()

        @staticmethod
        def vdisk(rslice:str) -> None:
            from ...Items import VirtualDisks

            TreeImpl.select._all(
                rslice = rslice,
                src = VirtualDisks,
                dst = Memory.VDisks
            )
                 
            TreeImpl.list.vdisk()

        @staticmethod
        def tower(rslice:str) -> None:
            from ...Items import Towers

            TreeImpl.select._all(
                rslice = rslice,
                src = Towers,
                dst = Memory.Towers
            )
                 
            TreeImpl.list.tower()

    class start:

        @staticmethod
        def service() -> None:
            
            for serv in Memory.Services:

                if serv.exists:

                    Printer.RunFile(
                        path = serv.file('Start'),
                        args = serv.args
                    )

                    serv.start(force=True)

                else:
                    Printer.Error('ServiceMissing', serv)

    class list:

        @staticmethod
        def _hardware(
            src: list,
            mem: list
        ) -> None:

            for dev in mem:

                ACTIVE: str = (' Active ' if dev.Connected else 'Inactive')

                printx(src.index(dev), f'[{ACTIVE}] {dev.Name}')

        @staticmethod
        def service() -> None:
            from ...Items import Services

            for serv in Memory.Services:

                RUNNING: str = ('Running'  if serv.running else 'Stopped')
                ENABLED: str = (' Enabled' if serv.enabled else 'Disabled')

                printx(Services.index(serv), f'[{RUNNING}, {ENABLED}] {serv.path}')

        @staticmethod
        def module() -> None:
            from ...Items import Modules

            for mod in Memory.Modules:

                EXISTS: str = (' Exists' if mod.exists else 'Missing')

                printx(Modules.index(mod), f'[{EXISTS}] {mod.path}')

        @staticmethod
        def disk() -> None:
            from ...Items import HardDrives
            TreeImpl.list._hardware(
                src = HardDrives,
                mem = Memory.Disks
            )

        @staticmethod
        def vdisk() -> None:
            from ...Items import VirtualDisks
            TreeImpl.list._hardware(
                src = VirtualDisks,
                mem = Memory.VDisks
            )

        @staticmethod
        def pcie() -> None:
            from ...Items import PCIeCards
            TreeImpl.list._hardware(
                src = PCIeCards,
                mem = Memory.PCIeCards
            )

        @staticmethod
        def tower() -> None:
            from ...Items import Towers
            TreeImpl.list._hardware(
                src = Towers,
                mem = Memory.Towers
            )

    class stop:

        @staticmethod
        def service() -> None:

            for serv in Memory.Services:

                if serv.exists:

                    Printer.RunFile(
                        path = serv.file('Stop')
                    )

                    serv.stop()

                else:
                    Printer.Error('ServiceMissing', serv)

    class enable:

        @staticmethod
        def service() -> None:

            for serv in Memory.Services:

                serv.enable()

            TreeImpl.list.service()

        @staticmethod
        def module() -> None:

            for mod in Memory.Modules:

                print(f'Enabling: {mod}')
                
                mod.install(False)

    class disable:

        @staticmethod
        def service() -> None:

            for serv in Memory.Services:

                serv.disable()

            TreeImpl.list.service()

    class args:

        @staticmethod
        def service(_, *args:str) -> None:

            for serv in Memory.Services:

                serv.args = args

            TreeImpl.list.service()

    class logs:

        @staticmethod
        def service() -> None:
            from philh_myftp_biz.process import RunHidden

            for serv in Memory.Services:
                if serv.logfile:
                    Printer.RunFile(serv.logfile)
                    RunHidden('code', serv.logfile)

    class explore:

        def _open(items:list[Path]) -> None:
            from philh_myftp_biz.process import RunHidden

            for i in items:
                Printer.RunFile(i.path)
                RunHidden('explorer.exe', i.wpath)

        @staticmethod
        def service() -> None:
            TreeImpl.explore._open(Memory.Services)

        @staticmethod
        def module() -> None:
            TreeImpl.explore._open(Memory.Modules)

    @staticmethod
    def name() -> None:
        from philh_myftp_biz.pc import NAME

        print(f'\nPC Name: {NAME}')

    class ip:

        @staticmethod
        def lan() -> None:
            from philh_myftp_biz.web import IP

            print(f'\nLocal IP: {IP.LAN}')

        @staticmethod
        def wan() -> None:
            from philh_myftp_biz.web import IP

            print(f'\nPublic IP: {IP.WAN}')

    class power:

        def __getattribute__(self, name:str):
            from ...Interval import shutdown
            return lambda: shutdown(name[0])

#===========================================================================

TreeImpl.cls()

run_tree(TreeImpl)

