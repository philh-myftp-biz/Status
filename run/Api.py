from philh_myftp_biz.pc.hardware import Device
from philh_myftp_biz.terminal import Args
from json import dumps
from .. import Items

data = {}

items: list[Device] = getattr(Items, Args[0])

for item in items:

    data[item.Name] = {}

    for var, val in vars(item).items():

        if var[0] != '_':
            data[item.Name][var] = val

print(dumps(
    obj = data,
    indent = 3
))

