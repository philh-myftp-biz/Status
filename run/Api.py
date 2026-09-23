from philh_myftp_biz.pc.hardware import Device
from philh_myftp_biz.terminal import Args
from collections import defaultdict
from json import dumps
from .. import Items

items: list[Device] = getattr(Items, Args[0])

cls = (items[0].__class__ if items else object).__dict__ | Device.__dict__

props = list(filter(
    lambda k: not (k.startswith('_') or callable(cls[k])),
    cls.keys()
))

data = defaultdict(dict)

for item in items:
    for prop in props:
        data[item.Name][prop] = getattr(item, prop)

print(dumps(
    obj = data,
    indent = 3
))

