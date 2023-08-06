# -*- coding: utf-8 -*-

__version__ = "0.9.5"

from . config import initConfig, getConfig
from . mongo import initMongo, getMongoClient
from . mysql import initMysql, getMysqlClient
from . log import initLog, getLog
from . ffmpeg import get_video_height, get_video_width, get_video_duration

__info__ = """
1. mysql支持多库
2. 0.2.3 utils 添加计算时间戳函数
3. 0.3.0 添加send163email 发送网易邮件
4. 0.4.0 添加文件md5和文件夹扫描
5. 0.5.0 添加文件中文繁体转简体
6. 0.6.0 添加ffmpeg信息获取
7. 0.7.0 添加日志初始化
8. 0.8.0 添加文件下载功能
9. 0.8.1 添加文件分块下载功能
10. 0.9.0 添加ffmpeg获取视频时长
10. 0.9.2 修复下载文件没有判断状态码
"""
