#!/usr/bin/python3

import requests
import threading
#import _thread
import time
import os

def download(url, fileName, retry = False, chunk_size = 1024*4):
    #lock.acquire()
    print(fileName)
    
    #增加断点续传
    r_check = requests.get(url, stream = True)
    total_size = int(r_check.headers['Content-Length'])
    
    if os.path.exists(fileName):
        temp_size = os.path.getsize(fileName)
    else:
        temp_size = 0
        
    if not retry:
        if not temp_size < total_size:
            print(fileName + ': done! ' + fileName + ': done!')
            threadmax.release()
            return True
    
    headers = {'Range': 'bytes=%d-' % temp_size}
    
    #增加断点续传
    
    r = requests.get(url, stream = True, headers = headers)
    with open(fileName, 'ab') as f:
        for chunk in r.iter_content(chunk_size = chunk_size):
            if chunk:
                f.write(chunk)
                
    if os.path.exists(fileName):
        end_size = os.path.getsize(fileName)
    else:
        end_size = 0
        
    if end_size < total_size:
        print(fileName + ': erro!!!!!')
        #print(fileName + ': restart')
        #download(url, fileName, True)
        
    print(fileName + ': end')
    #lock.release()
    threadmax.release()

start = time.time()
host = '?'
listFile = 'list.txt'
file = open(listFile, "r", encoding="utf-8", errors="ignore")
threadmax = threading.BoundedSemaphore(5)
lock = threading.Lock()
l = []
while True:
    fileName = file.readline()
    
    if not fileName:
        break
        
    fileName = fileName.strip()
    url = host + fileName
    threadmax.acquire()
    t = threading.Thread(target = download, args = (url, fileName, ))
    t.start()
    l.append(t)
    #_thread.start_new_thread(download, (url, fileName, ))
    #download(url, fileName)
    
for t in l:
    t.join()
    
end = time.time()
print(end - start)
