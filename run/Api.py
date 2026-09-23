from philh_myftp_biz.pc.hardware import Device
from philh_myftp_biz.terminal import Args
from json import dumps
from .. import Items

def _props(cls:type[Device]):
    _dict = (cls.__dict__ | Device.__dict__)
    return list(filter(
        lambda k: not (k.startswith('_') or callable(_dict[k])),
        _dict.keys()
    ))

def get_data(*items:list[Device]):
    data = []
    for item in items:
        idata = {}
        for prop in _props(item.__class__):
            idata[prop] = getattr(item, prop)
        data += [idata]
    return data

if __name__ == "__main__":
    print(dumps(
        obj = get_data(*getattr(Items, Args[0])),
        indent = 3
    ))

