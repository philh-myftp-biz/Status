from philh_myftp_biz.pc.hardware import PCIeCard

Items = [

    #PCIeCard(
    #    Slot = 0, # 1
    #    Lanes = 1,
    #),

    PCIeCard(
        Slot = 1, # 2
        Lanes = 16,
        VendorID = 4318,
        DeviceID = 5050,
    ),

    #PCIeCard(
    #    Slot = 2, # 3
    #    Lanes = 4,
    #),

    PCIeCard(
        Slot = 3, # 4
        Lanes = 16,
        VendorID = 4096,
        DeviceID = 88,
    ),

    PCIeCard(
        Slot = 4, # M.2
        Lanes = 4,
        VendorID = 6945,
        DeviceID = 4454,
    )

]

# ===============================================================================================================