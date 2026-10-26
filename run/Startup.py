from philh_myftp_biz.pc.hardware import HealthStatus, DiskUsage
from philh_myftp_biz.web import FirewallException
from philh_myftp_biz.process import SysTask
from .. import alert, shutdown, main_repo
from philh_myftp_biz.terminal import Log
from philh_myftp_biz import VERBOSE
from .. import Items

VERBOSE.enable()

# ===============================================================================================================

Log.INFO('Checking for issues with PCIe Cards')

if not all(c.Connected for c in Items.PCIeCards):
    
    alert('Restarting due to PCIe card error', items=False)

    shutdown('r', '30')

    exit()

# ===============================================================================================================

Log.INFO('Processing Hard Drives')

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

            Log.VERB(f'Retiring HDD: {hdd.Name}')

            hdd.Usage = DiskUsage.Retired
            hdd.Online = False

        # Check if disk is retired 
        elif hdd.Usage == DiskUsage.Retired:

            Log.VERB(f'Reactivating HDD: {hdd.Name}')

            hdd.Usage = DiskUsage.AutoSelect
            hdd.Online = True

    else:

        Log.VERB(f'Retiring HDD: {hdd.Name}')

        hdd.Usage = DiskUsage.Retired
        hdd.Online = False

        hdd.FriendlyName = "<Unknown Disk>"

# ===============================================================================================================

Log.INFO('Processing Virtual Disks')

# Iter through Virtual Disks
for vdisk in Items.VirtualDisks:

    Log.VERB(
        f'Processing Virtual Disk:\n'+ \
        f"name='{vdisk.Name}'\n"+ \
        f"connected={vdisk.Connected}"
    )

    Log.VERB(f'Connecting Virtual Disk: {vdisk.Name}')

    vdisk.Connected = True

# ==================================================
# FIREWALL

FirewallException('RDP').set(3389)
FirewallException('SSH').set(22)

# ===============================================================================================================

# Remove the 'Nvidia Display Manager' Popup
SysTask("*NVDisplay*").stop()

# If any virtual disks are missing
if any(not d.Connected for d in Items.VirtualDisks):

    alert('Startup Failed: Virtual Disk Failure', items=True)

# If all mounts exist
else:

    alert('Startup Complete', items=True)

    #==============
    # Modules

    Log.INFO('Installing Modules')

    # Iter through all main modules
    for mod in Items.Modules:

        Log.VERB(f'Installing Module: {mod}')

        # Install/Update all dependencies
        mod.install(show=VERBOSE)

    #==============
    # Services
    
    Log.INFO('Starting Services')

    # Start All Services
    for service in Items.Services:
        if service.enabled:
            service.start()

    #==============

    main_repo and main_repo.update_submodules(force=True)

    #==============

# ===============================================================================================================
