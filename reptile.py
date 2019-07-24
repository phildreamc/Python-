import re
import os,shutil
import requests,threading
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool

class video_down():
    def __init__(self,url):
        # 拼接全民解析url
        self.api='https://jx.618g.com'
        self.get_url = 'https://jx.618g.com/?url=' + url
        #设置UA模拟浏览器访问
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        #设置多线程数量
        self.thread_num=32
        #当前已经下载的文件数目
        self.i = 0
        # 调用网页获取
        html = self.get_page(self.get_url)
        if html:
            # 解析网页
            self.parse_page(html)

    def get_page(self,get_url):
        try:
            print('正在请求目标网页....',get_url)
            response=requests.get(get_url,headers=self.head)
            if response.status_code==200:
                #print(response.text)
                print('请求目标网页完成....\n 准备解析....')
                self.head['referer'] = get_url
                return response.text
        except Exception:
            print('请求目标网页失败，请检查错误重试')
            return None

    def parse_page(self,html):
        print('目标信息正在解析........')
        doc=pq(html)
        self.title=doc('head title').text().replace(" ","")
        print(self.title)
        url = doc('#player').attr('src')[14:]
        video_flag = "playlist"
        result = video_flag in url
        if result:
            self.url_down = url[:-13]
            #self.get_m3u8_2(url)
            pass
        else:
            print(url)
            self.url_down=url[:-28]
            url_movie=self.get_m3u8_1(url)
            url=url[:-28]+url_movie[0]+".m3u8"
        print('解析完成，获取缓存ts文件.........')
        self.get_m3u8_2(url)
    def get_m3u8_1(self,url):
        try:
            response=requests.get(url,headers=self.head)
            if response.status_code == 200:
                html=response.text
                #print(html)
                pattern = re.compile('/(.*?).m3u8')
                url_m3u8 = re.findall(pattern, html)
                return url_m3u8
        except Exception:
            print('缓存文件请求错误1，请检查错误')

    def get_m3u8_2(self,url):
        try:
            response=requests.get(url,headers=self.head)
            html=response.text
            print('获取ts文件成功，准备提取信息')
            self.parse_ts_2(html)
        except Exception:
            print('缓存文件请求错误2，请检查错误')
    def parse_ts_2(self,html):
        pattern=re.compile('.*?(.*?).ts')
        self.ts_lists=re.findall(pattern,html)
        #print(self.ts_lists)
        print('信息提取完成......\n准备下载...')
        self.pool()
    def pool(self):
        print('经计算需要下载%d个文件' % len(self.ts_lists))
        if self.title not in os.listdir():
            os.makedirs(self.title)
        print('正在下载...所需时间较长，请耐心等待..')
        #开启多进程下载
        pool=Pool(16)
        pool.map(self.save_ts,[ts_list for ts_list in self.ts_lists])
        pool.close()
        pool.join()
        print('下载完成')
        self.ts_to_mp4()
    def ts_to_mp4(self):
        print('ts文件正在进行转录mp4......')
        str='copy /b '+self.title+'\*.ts '+self.title+'.mp4'
        os.system(str)
        filename=self.title+'.mp4'
        if os.path.isfile(filename):
            print('转换完成，祝你观影愉快')
            shutil.rmtree(self.title)

    def save_ts(self,ts_list):
        try:
            ts_urls = self.url_down + '{}.ts'.format(ts_list)
            #self.i += 1
            #print('当前进度%d/%d'%(self.i,len(self.ts_lists)))
            print(ts_urls)
            urlretrieve(url=ts_urls, filename=self.title + '/{}.ts'.format(ts_urls[-10:-3]))
        except Exception:
            print('保存文件出现错误')


if __name__ == '__main__':
    #复仇者联盟3
    url="https://v.qq.com/x/cover/coqnq6i120wojq6.html"
    #电影碟中谍5：神秘国度
    url1='https://v.qq.com/x/cover/5c58griiqftvq00.html'
    # 电视剧我只喜欢你第四集
    url2 = 'https://v.qq.com/x/cover/ne187hrksyytdn4.html'
    video_down(url2)