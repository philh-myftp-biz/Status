from philh_myftp_biz.pc.hardware import Device
from philh_myftp_biz.terminal import Args
from json import dumps
from .. import Items

Args.Arg('type')

data = {}

items: list[Device] = getattr(Items, Args['type'])

for item in items:
    for var, val in vars(item).items():
        if var[0] != '_':
            data[item.name][var] = val

print(dumps(
    obj = data,
    indent = 3
))

