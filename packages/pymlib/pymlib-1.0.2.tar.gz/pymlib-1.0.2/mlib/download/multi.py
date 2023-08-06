# coding: utf-8

from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from threading import Lock
import requests, os, shutil
import logging, time, mlib

if __name__ == "__main__":
    mlib.initLog()
mlog = mlib.getLog()

class ExceptDownload(Exception):
    pass

class Except403(Exception):
    pass

class Except404(Exception):
    pass

class MultiDownloader():
    def __init__(self, url, thread_num, save_path, proxy):
        self.url = url
        self.num = thread_num
        self.name = save_path
        self.files = []
        if proxy:
            self.proxies = {
                "http": proxy,
                "https": proxy,
            }
        else:
            self.proxies = None
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        }
        r = requests.head(self.url, proxies=self.proxies, headers=headers)
        # 若资源显示302,则迭代找寻源文件
        while r.status_code == 302:
            self.url = r.headers['Location']
            # mlog.warning("该url已重定向至{}".format(self.url))
            r = requests.head(self.url, proxies=self.proxies, headers=headers)
        self.size = int(r.headers['Content-Length'])
        if self.size <= 0:
            mlog.error("文件大小为0")
            raise Exception()
        mlog.info('该文件大小为：{} bytes'.format(self.size))

    def get_save_path(self, i, size):
        save_path = self.name + f".part_{i}_{size}"
        return save_path

    def down(self, start, end, i, size):
        # mlog.debug(f"下载线程 {i}")
        save_path = self.get_save_path(i, size)
        if os.path.exists(save_path):
            mlog.debug(f"文件[{save_path}]已完成")
            return
        try:
            headers = {
                'Range': 'bytes={}-{}'.format(start, end),
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            }
            # stream = True 下载的数据不会保存在内存中
            r = requests.get(self.url, headers=headers, stream=True, proxies=self.proxies)
            if r.status_code == 403:
                raise Except403("403禁止下载")
            if r.status_code == 404:
                raise Except404("404资源未找到")
            # mlog.error(r.headers)
            path = self.name + f".part_{i}_{size}.downloading"
            with open(path, "wb") as fp:
                for chunk in r.iter_content(1024 * 100):
                    if chunk:
                        fp.write(chunk)
            os.rename(path, save_path)
        except Except403 as e:
            mlog.error(e)
            raise e
        except Except404 as e:
            mlog.error(e)
            raise e
        except Exception as e:
            mlog.error(e)
            return
        mlog.debug(f"文件[{save_path}]已完成")

    def run(self):
        # 启动多线程写文件
        part = self.size // self.num
        pool = ThreadPoolExecutor(max_workers=self.num)
        futures = []
        for i in range(self.num):
            start = part * i
            # 最后一块
            if i == self.num - 1:
                end = self.size
            else:
                end = start + part - 1
            # mlog.debug('{}->{}-{}'.format(start, end, i))
            task = pool.submit(self.down, start=start, end=end, i=i, size=end-start)
            self.files.append(dict(start=start, end=end, i=i, size=end-start))
            futures.append(task)
        wait(futures,  return_when=ALL_COMPLETED)
        self.merge()
        mlog.info('%s 下载完成' % self.name)

    def download_chunk(self, chunk_size=1024*1024*2):
        # 启动多线程写文件
        part_num = self.size // chunk_size
        pool = ThreadPoolExecutor(max_workers=self.num)
        futures = []
        for i in range(part_num + 1):
            start = chunk_size * i
            # 最后一块
            if start >= self.size:
                continue
            else:
                end = start + chunk_size - 1
            # mlog.debug('{}->{}-{}'.format(start, end, i))
            task = pool.submit(self.down, start=start, end=end, i=i, size=end-start)
            self.files.append(dict(start=start, end=end, i=i, size=end-start))
            futures.append(task)
        wait(futures,  return_when=ALL_COMPLETED)
        self.merge()
        mlog.info('%s 下载完成' % self.name)

    def merge(self):
        for v in self.files:
            save_path = self.get_save_path(v["i"], v["size"])
            if not os.path.exists(save_path):
                raise ExceptDownload("文件未全部下载完成")
        with open(self.name, "wb") as fp:
            for v in self.files:
                save_path = self.get_save_path(v["i"], v["size"])
                with open(save_path, "rb") as f:
                    fp.write(f.read())
                os.remove(save_path)

if __name__ == "__main__":
    dl =  MultiDownloader('https://r3---sn-i3b7knse.googlevideo.com/videoplayback?expire=1617114935&ei=1uJiYNieO8LA4gLU1S8&ip=47.243.55.25&id=o-AN_wEHI7Urs31ZjXm3agAFllgi0Xcx8lmGqY5bfqTl7V&itag=133&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278&source=youtube&requiressl=yes&mh=bE&mm=31%2C26&mn=sn-i3b7knse%2Csn-30a7rn7l&ms=au%2Conr&mv=m&mvi=3&pl=16&initcwndbps=2426250&vprv=1&mime=video%2Fmp4&ns=D3DC4L9oOE6G5F6N37X4DroF&gir=yes&clen=26824308&dur=944.943&lmt=1567464427976867&mt=1617093162&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=WEB&txp=5535432&n=hQeZ-FF69hZ-BKn3tzRVm&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgVG7gkWwVBEJeCKXhWBcCIqEFPhgzH06ndyY8Fc9F1xsCIFNYuCPT26xvCElHhpyW2o2qHpQU96Azx87GGXvMsq7Y&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgB7XoryDzmN9b-LebvMAkDqLiA0JUxunB1ahjoWi4uwQCIQCK_FnKbiE9gFbRSjrdgmyjSIPuLXffcuzbel3X_wmmMA%3D%3D',
            6, 
            "data/aaa.mp4",
            "http://10.0.0.5:2081"
        )
    dl.download_chunk()