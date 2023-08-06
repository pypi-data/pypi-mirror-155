# coding: utf-8

import time
import pymlib

NAME = "pysyslog"

conf = {
    "name": NAME,
    "formatter": "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(thread)d|%(message)s",
    "level": "DEBUG",
    "syslog": "http://127.0.0.1:29721/report?token=uep7a2d2Z8HjnIYUE1UMy",
}

pymlib.initLog(**conf)
mlog = pymlib.getLog(name=NAME)
mlog.debug("debug1")
mlog.error("error1")

time.sleep(5)