from philh_myftp_biz.process import RunHidden
from philh_myftp_biz.modules import Repo
from philh_myftp_biz.terminal import Log
from philh_myftp_biz.web import URL
from philh_myftp_biz.pc import NAME
from warnings import filterwarnings
from .run.Api import get_data
from typing import Literal
from subprocess import run
from sys import executable
from . import Items

filterwarnings("ignore", category=RuntimeWarning, message=".*found in sys.modules.*")

IS_SERVER: bool = (NAME == 'PC-1')

try:
    main_repo = Repo('E:/')
except FileNotFoundError:
    main_repo = None

def pip(*args) -> None:
    run([executable, '-m', 'pip', *args])

def shutdown(
    mode: Literal['s', 'r'],
    t: int = 30
) -> None:

    # Show Prompt to abort shutdown
    Items.Modules[0].start('vbs/abort')

    # Restart the Server
    RunHidden(
        'shutdown',
        f'/{mode}',
        '/t', t
    )

_alert_url = URL("https://script.google.com/macros/s/AKfycbxLMSyiCEk5D2l7UmPUAzLVJ1BbGoRryuoiP718py2xJDD2fSM1GW4GDhuYqdHVH_EbtQ/exec")

def alert(msg:str) -> None:

    Log.MAIN(msg)

    # Show Alert Box
    Items.Modules[0].start('vbs/alert', msg)

    if IS_SERVER:
        _alert_url.copy(body = {
            'message': msg,
            'doAlert': False,
            'items': get_data(
                *Items.VirtualDisks,
                *Items.HardDrives,
                *Items.PCIeCards,
            ),
        }).post()

