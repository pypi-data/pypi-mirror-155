# coding: utf-8

import datetime, time
from socket import timeout
from queue import Queue
import logging
import threading, queue
import json
import requests
import traceback
import socket

"""
syslog日志客户端
"""
_connection = None


class SysLogFormatter(logging.Formatter):

    DEFAULT_PROPERTIES = logging.LogRecord(
        '', '', '', '', '', '', '', '').__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        _datetime = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        document = {
            'timestamp': int(time.time()*1000000000), # 时间戳，精度还需要调整 1646641516605 1646641516605
            'datetime': _datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'levelname': record.levelname,
            'filename': record.pathname,
            'lineno': record.lineno,
            'thread': record.thread,
            'text': record.getMessage(),
            "type": getattr(record, "type", 0), #
            "weights": getattr(record, "weights", 1),#
            "flagid": getattr(record, "flagid", "default"),
            'name': record.name,
            "hostname": socket.gethostname(),
            # "remoteip": "",
            "options": getattr(record, "options", None),
            # 'threadName': record.threadName,
            # 'module': record.module,
            # 'method': record.funcName,
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update({
                'exception': {
                    'message': str(record.exc_info[1]),
                    'code': 0,
                    'stackTrace': self.formatException(record.exc_info)
                }
            })
        # Standard document decorated with extra contextual information
        if len(self.DEFAULT_PROPERTIES) != len(record.__dict__):
            contextual_extra = set(record.__dict__).difference(
                set(self.DEFAULT_PROPERTIES))
            if contextual_extra:
                for key in contextual_extra:
                    document[key] = record.__dict__[key]
        return document


class SysLogHandler(logging.Handler):

    def __init__(self, syslog: str, level=logging.NOTSET,
                 fail_silently=False, formatter=None, capped=False,
                 capped_max=1000, capped_size=1000000, reuse=True, **kwargs):
        """
        初始化日志客户端
        """
        logging.Handler.__init__(self, level)
        self.syslog = syslog
        self.fail_silently = fail_silently
        self.connection = None
        self.formatter = formatter or SysLogFormatter()
        self.capped = capped
        self.capped_max = capped_max
        self.capped_size = capped_size
        self.reuse = reuse
        self.queue = queue.Queue(999999)
        self._connect(**kwargs)

    def _connect(self, **kwargs):
        """
        连接服务器
        """
        self.server = threading.Thread(target=self.send2sys)
        self.server.setDaemon(True)
        self.server.start()
        self.collection = True

    def send2sys(self):
        while True:
            try:
                record = self.queue.get()
                r = requests.post(self.syslog, data={"data": json.dumps(record)}, timeout=5)
                if r.status_code != 200:
                    print("syslog refused", r.text)
                    continue
                j = json.loads(r.text)
                if j.get("code") != 0:
                    print("syslog send failed",r.text)
                    continue
            except Exception as e:
                msg = traceback.format_exc()
                print("send2sys error\n", msg)

    def close(self):
        """
        关闭服务器连接
        """
        self.collection = False

    def emit(self, record):
        """
        发送数据到服务器
        """
        try:
            record = self.format(record)
            self.queue.put(record, timeout=3)
        except Exception as e:
            if not self.fail_silently:
                self.handleError(record)

    def __exit__(self, type, value, traceback):
        self.close()


if __name__ == "__main__":
    import logging

    mlog = logging.getLogger("pysyslog")
    mlog.setLevel(logging.DEBUG)

    syslog = SysLogHandler(syslog="http://127.0.0.1:29721/report?token=uep7a2d2Z8HjnIYUE1UMy")
    syslog.setFormatter(SysLogFormatter())
    mlog.addHandler(syslog)

    format = "%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(thread)d|%(message)s"
    console = logging.StreamHandler()  
    console.setLevel(level=logging.WARNING)
    console.setFormatter( logging.Formatter(format))
    mlog.addHandler(console)


    mlog.debug("debug test")
    mlog.warning("warning test")
    mlog.error("error test")

    time.sleep(5)

