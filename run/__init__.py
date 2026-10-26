from philh_myftp_biz.pc.hardware import HealthStatus, DiskUsage, HardDrive
from philh_myftp_biz.terminal import Log
from logger2 import VERBOSE
from .. import Items

def _retire_disk(hdd: HardDrive):
    Log.VERB(f'Retiring HDD: {hdd.Name}')

    hdd.Usage = DiskUsage.Retired
    hdd.Online = False

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
        
            # If disk's FriendlyName differs from it's intended name
            if hdd.FriendlyName != hdd.Name:

                Log.VERB(f'Renaming HDD: "{hdd.FriendlyName}" to "{hdd.Name}"')
                
                hdd.FriendlyName = hdd.Name

            # Check if disk is unhealthy
            if hdd.HealthStatus != HealthStatus.HEALTHY:
                _retire_disk(hdd)

            # Check if disk is retired 
            elif hdd.Usage == DiskUsage.Retired:

                Log.VERB(f'Reactivating HDD: {hdd.Name}')

                hdd.Usage = DiskUsage.AutoSelect
                hdd.Online = True

        else:
            _retire_disk(hdd)
            hdd.FriendlyName = "<Unknown Disk>"

    VERBOSE.value = 0

