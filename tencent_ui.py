# -*- coding: utf-8 -*-

import os
import re
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def initSet(w):
    global title,left,top,width,height,host,url,dir
    title = 'm3u8视频下载工具 -version:1.0.0'
    left = 500
    top = 350
    width = 640
    height = 210
    host = ""
    url = ""
    dir = os.getcwd() + "\\" + "tmp"
    initUI(w)
    
def initUI(self):
    global title,left,top,width,height,host,url,dir
    self.setWindowTitle(title)
    self.setGeometry(left, top, width, height)
    self.setWindowFlags(Qt.WindowMinimizeButtonHint)
    self.setFixedSize(width, height)
    # self.setStyleSheet("background-image:url(images/bg.png)")
    palette = QPalette()
    # palette.setBrush(QPalette.Background, QBrush(QPixmap("images/bg.png")))
    self.setPalette(palette)
    
    lb = QLabel('m3u8链接:', self)
    lb.move(150, 56)
    
    self.textbox = QLineEdit(self)
    self.textbox.move(210, 50)
    self.textbox.resize(280, 25)
    
    quit_button = QPushButton('关闭程序', self)
    quit_button.setToolTip("点击退出程序！")
    start_button = QPushButton('开始下载', self)
    start_button.setToolTip("点击开始下载视频！")
    quit_button.clicked.connect(QCoreApplication.instance().quit)
    start_button.clicked.connect(lambda _:start_download(self))
    quit_button.resize(quit_button.sizeHint())
    start_button.resize(start_button.sizeHint())
    quit_button.move(360, 90)
    start_button.move(210, 90)
    
    self.show()
    
def start_download(self):
    global host,url,m3u8_file,ts_list
    if self.textbox.text() == "":
        return
    else:
        a = self.textbox.text().rsplit("/", 1)
        host = a[0]
        url = a[1]
        m3u8_file = soup_html(get_html(host + "/" + url))
        ts_list = match_m3u8(str(m3u8_file))
        start_process(host, ts_list, dir)
        
def get_html(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36;"}
    s = requests.Session()
    try:
        content = s.get(url, headers = header)
    except requests.ConnectionError as e:
        print(str(e),", try agin now......")
        get_html(url)
    return content
    
def soup_html(response):
    soup = BeautifulSoup(response.text)
    return soup
    
def match_m3u8(str):
    pattern = re.compile(r',\s(.*?)\s#EXTINF')
    result = pattern.findall(str)
    return result
    
def start_process(host, list, dir):
    pool = Pool(20)
    for n in list:
        url = n
        pool.apply_async(download_ts, (host, n, dir))
    pool.close()
    pool.join()
    
def download_ts(host, url, dir):
    content = get_html(host + "/" + url)
    name = re.match('(.*\.ts?)\?.*', url).group(1)
    if name == "":
        name = re.match('(.*\.mp4?)\?.*', url).group(1)
    f = open(dir + "\\" + name, "wb")
    f.write(content.content)
    f.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)    # 创建应用
    w = QWidget()
    initSet(w)
    sys.exit(app.exec_()) # 运行应用，并监听事件