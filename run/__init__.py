from philh_myftp_biz.pc.hardware import DiskUsage, HealthStatus as HS
from philh_myftp_biz.terminal import Log
from logger2 import VERBOSE
from .. import Items

def process_HardDrives():

    VERBOSE.value = 1

    # Iter through Hard Drives
    for hdd in Items.HardDrives:

        Log.VERB(
            f'Processing Hard Drive:\n'+ \
            f"name='{hdd.Name}'\n"+ \
            f"connected={hdd.Connected}"
        )

        # Check if disk is connected
        if hdd.Connected:

            hdd.Online = True
            hdd.Usage = DiskUsage.AutoSelect
        
            # Set FriendlyName
            if hdd.FriendlyName != hdd.Name:
                Log.VERB(f'Renaming HDD: "{hdd.FriendlyName}" to "{hdd.Name}"')
                hdd.FriendlyName = hdd.Name

            # Retire if Unhealthy
            if hdd.HealthStatus in [HS.WARNING, HS.NOTGOOD]:
                Log.VERB(f'Retiring HDD: {hdd.Name}')
                hdd.Usage = DiskUsage.Retired
                hdd.Online = False

        else: # disconnected
            hdd.FriendlyName = "<Unknown Disk>"

    VERBOSE.resume()

