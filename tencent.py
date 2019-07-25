# -*- coding: utf-8 -*-

import os
import re
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup

def get_html(url):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36;"}
    s = requests.Session()
    try:
        content = s.get(url, headers = header)
    except requests.ConnectionError as e:
        print(str(e))
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
    print(host + "/" + url)
    name = re.match('(.*\.ts?)\?.*', url).group(1)
    f = open(dir + "\\" + name, "wb")
    f.write(content.content)
    f.close()
    
if __name__ == "__main__":
    dir = os.getcwd() + "\\" + "tmp"
    host = "https://apd-07fe21833824f90bf892bd1cf2e7eb03.v.smtcdns.com/moviets.tc.qq.com/AhThDVul9E8NR3uQEq6r5D7mpkZDwCHKSwBt7lBBhlxg/uwMROfz2r5zAoaQXGdGnC2df644E7D3uP8M8pmtgwsRK9nEL/Yw8iF8QQkYsXWwX_t3wwJsjXGlZgGDIgVB3mJADdfVtX0KT2PkXkIcyCISPOAXiqROeRZatMlAG51nNgGFvNbwZscn9EE-HYVellyTAbNXdN49it-7oFYjksYqOmSZiRIZ5AQXxgQwCEPzBuNOQ706pZxVzNljrcMXFwXlPAYsw"
    url = "t0028woxqom.321002.ts.m3u8?ver=4"
    m3u8_file = soup_html(get_html(host + "/" + url))
    ts_list = match_m3u8(str(m3u8_file))
    start_process(host, ts_list, dir)