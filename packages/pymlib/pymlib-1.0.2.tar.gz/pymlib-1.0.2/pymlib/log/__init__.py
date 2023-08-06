# coding: utf-8

import logging
from .syslog import SysLogHandler, SysLogFormatter

# 初始化日志
def initLog(**kwargs):
    name = kwargs.get("name", "mlog")
    mlog = logging.getLogger(name)
    level = kwargs.get("level")
    if level:
        level = getattr(logging, level)
    else:
        level = logging.DEBUG
    mlog.setLevel( level )

    ft = kwargs.get("formatter", "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(thread)d|%(message)s")
    formatter = logging.Formatter(ft)

    console = logging.StreamHandler()  
    console.setLevel(level)
    console.setFormatter(formatter)
    mlog.addHandler(console)

    # 日志中心服务器
    if kwargs.get("syslog"):
        syslog = SysLogHandler(syslog=kwargs.get("syslog"))
        syslog.setFormatter(SysLogFormatter())
        mlog.addHandler(syslog)


def getLog(**kwargs):
    name = kwargs.get("name", "mlog")
    mlog = logging.getLogger(name)
    return mlog