from philh_myftp_biz.modules.Module import Module
from .. import IS_SERVER

if IS_SERVER:

    MC = Module('E:/Minecraft/')
    MC.run('backup')

