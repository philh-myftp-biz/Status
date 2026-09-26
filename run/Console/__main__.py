from ... import install # Run install.py

from philh_myftp_biz.terminal.tree import Tree, Printer, run_tree
from philh_myftp_biz.pc import Path
from typing import Callable
from . import Memory

class TreeImpl(Tree):
    """
Phil's Server
[philh.myftp.biz]

MANAGEMENT  CONSOLE
"""
                   
    @staticmethod
    def run( 
        script: str,
        *args: str
    ) -> None:
        """
        Run a script in a new tab (Ex: run Startup [...])

        SCRIPTS:
        - Update  | Update 'philh_myftp_biz' python package
        - Status  | Open System Status Viewer
        - Console | Open Console Session
        - Api     | Call Items API
        - Hour    | Scheduled Hourly
        - Day     | Scheduled Daily
        - Week    | Scheduled Weekly
        - Startup | Runs at Startup
        """
        from ...Items import Modules

        Printer.RunFile(
            path = f"C:/Scripts/run/{script}.py",
            args = args
        )
        
        Modules[0].run(
            'vbs/run', script.title(), 
            'True', # VISIBLE
            *args
        )

    class select:
        """
        Select items
        [...] -> ['#', '#..', '..#', '#..#', '#,#']
        """

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
            """Select services (Ex: select service 1,3)"""
            from ...Items import Services

            TreeImpl.select._all(
                rslice = rslice,
                src = Services,
                dst = Memory.Services
            )
                 
            TreeImpl.list.service()

        @staticmethod
        def module(rslice:str) -> None:
            """Select modules (Ex: select module ..5)"""
            from ...Items import Modules

            TreeImpl.select._all(
                rslice = rslice,
                src = Modules,
                dst = Memory.Modules
            )
                 
            TreeImpl.list.module()

        @staticmethod
        def disk(rslice:str) -> None:
            """Select hard drives"""
            from ...Items import HardDrives

            TreeImpl.select._all(
                rslice = rslice,
                src = HardDrives,
                dst = Memory.Disks
            )
                 
            TreeImpl.list.disk()

        @staticmethod
        def pcie(rslice:str) -> None:
            """Select pcie cards"""
            from ...Items import PCIeCards

            TreeImpl.select._all(
                rslice = rslice,
                src = PCIeCards,
                dst = Memory.PCIeCards
            )
                 
            TreeImpl.list.pcie()

        @staticmethod
        def vdisk(rslice:str) -> None:
            """Select virtual disks"""
            from ...Items import VirtualDisks

            TreeImpl.select._all(
                rslice = rslice,
                src = VirtualDisks,
                dst = Memory.VDisks
            )
                 
            TreeImpl.list.vdisk()

        @staticmethod
        def tower(rslice:str) -> None:
            """Select towers"""
            from ...Items import Towers

            TreeImpl.select._all(
                rslice = rslice,
                src = Towers,
                dst = Memory.Towers
            )
                 
            TreeImpl.list.tower()

    class start:
        """Start items"""

        @staticmethod
        def service() -> None:
            """Start the selected services"""
            
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
        """List items"""

        @staticmethod
        def _hardware(
            src: list,
            mem: list
        ) -> None:

            for dev in mem:

                ACTIVE: str = (' Active ' if dev.Connected else 'Inactive')

                Printer.xitem(src.index(dev), f'[{ACTIVE}] {dev.Name}')

        @staticmethod
        def service() -> None:
            """Get a list of selected services"""
            from ...Items import Services

            for serv in Memory.Services:

                RUNNING: str = ('Running'  if serv.running else 'Stopped')
                ENABLED: str = (' Enabled' if serv.enabled else 'Disabled')

                Printer.xitem(Services.index(serv), f'[{RUNNING}, {ENABLED}] {serv.path}')

        @staticmethod
        def module() -> None:
            """Get a list of selected modules"""
            from ...Items import Modules

            for mod in Memory.Modules:

                EXISTS: str = (' Exists' if mod.exists else 'Missing')

                Printer.xitem(Modules.index(mod), f'[{EXISTS}] {mod.path}')

        @staticmethod
        def disk() -> None:
            """Get a list of selected hard drives"""
            from ...Items import HardDrives
            TreeImpl.list._hardware(
                src = HardDrives,
                mem = Memory.Disks
            )

        @staticmethod
        def vdisk() -> None:
            """Get a list of selected virtual disks"""
            from ...Items import VirtualDisks
            TreeImpl.list._hardware(
                src = VirtualDisks,
                mem = Memory.VDisks
            )

        @staticmethod
        def pcie() -> None:
            """Get a list of selected pcie cards"""
            from ...Items import PCIeCards
            TreeImpl.list._hardware(
                src = PCIeCards,
                mem = Memory.PCIeCards
            )

        @staticmethod
        def tower() -> None:
            """Get a list of selected towers"""
            from ...Items import Towers
            TreeImpl.list._hardware(
                src = Towers,
                mem = Memory.Towers
            )

    class stop:
        """Stop items"""

        @staticmethod
        def service() -> None:
            """Stop the selected services"""

            for serv in Memory.Services:

                if serv.exists:

                    Printer.RunFile(
                        path = serv.file('Stop')
                    )

                    serv.stop()

                else:
                    Printer.Error('ServiceMissing', serv)

    class enable:
        """Enable items"""

        @staticmethod
        def service() -> None:
            """Enable the selected services"""

            for serv in Memory.Services:

                serv.enable()

            TreeImpl.list.service()

        @staticmethod
        def module() -> None:
            """Setup dependencies for the selected modules"""

            for mod in Memory.Modules:

                print(f'Enabling: {mod}')
                
                mod.install(False)

    class disable:
        """Disable items"""

        @staticmethod
        def service() -> None:
            """Disable the selected services"""

            for serv in Memory.Services:

                serv.disable()

            TreeImpl.list.service()

    class args:
        """Set items' arguements"""

        @staticmethod
        def service(_, *args:str) -> None:
            """Set the args for selected services (ARGS SERVICE = *arg1* *arg2* ...)"""

            for serv in Memory.Services:

                serv.args = args

            TreeImpl.list.service()

    class logs:
        """Open items' logs"""

        @staticmethod
        def service() -> None:
            """Open the logs for the selected services"""
            from philh_myftp_biz.process import RunHidden

            for serv in Memory.Services:
                if serv.logfile:
                    Printer.RunFile(serv.logfile)
                    RunHidden('code', serv.logfile)

    class explore:
        """Open items in file explorer"""

        def _open(items:list[Path]) -> None:
            from philh_myftp_biz.process import RunHidden

            for i in items:
                Printer.RunFile(i.path)
                RunHidden('explorer.exe', i.wpath)

        @staticmethod
        def service() -> None:
            """Open the selected services in file explorer"""
            TreeImpl.explore._open(Memory.Services)

        @staticmethod
        def module() -> None:
            """Open the selected modules in file explorer"""
            TreeImpl.explore._open(Memory.Modules)

    @staticmethod
    def name() -> None:
        """Get the name of the current computer"""
        from philh_myftp_biz.pc import NAME

        print(f'\nPC Name: {NAME}')

    class ip:
        """Get IP Address"""

        @staticmethod
        def lan() -> None:
            """Get the current local ip"""
            from philh_myftp_biz.web import IP

            print(f'\nLocal IP: {IP.LAN}')

        @staticmethod
        def wan() -> None:
            """Get the current public ip"""
            from philh_myftp_biz.web import IP

            print(f'\nPublic IP: {IP.WAN}')

    class power:
        """Shutdown/Restart System"""

        shutdown: Callable
        """Shutdown system"""

        restart: Callable
        """Restart system"""

        def __getattribute__(self, name:str):
            from ...Interval import shutdown
            return lambda: shutdown(name[0])

#===========================================================================

TreeImpl.cls()

run_tree(TreeImpl)

