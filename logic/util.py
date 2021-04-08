
import os
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
from hashlib import md5
from itertools import zip_longest




def createDir(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)


def loadProductHtml(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    filePath = os.path.join("download/product", md5_url)
    text = ""
    if os.path.exists(filePath):
        text = open(filePath, 'r', encoding='utf-8')
        text = text.read()
    else:
        try:
            print("loadProductHtml requests product:", url)
            response = requests.get(url)
            with open(filePath, "w", encoding='utf-8')as f:
                f.write(response.text)
            text = response.text
        except:
            pass
    
    if len(text) > 0:
        return BeautifulSoup(text, 'lxml')
    else:
        return None


def loadSiteHtml(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    filePath = os.path.join("download/site", "productsPage", md5_url)
    text = ""
    if os.path.exists(filePath):
        text = open(filePath, 'r', encoding='utf-8')
        text = text.read()
    else:
        try :
            print("loadSiteHtml requests site:", url)
            response = requests.get(url)
            with open(filePath, "w", encoding='utf-8')as f:
                f.write(response.text)
            text = response.text
        except:
            pass
    
    if len(text) > 0:
        return BeautifulSoup(text, 'lxml')
    else:
        return None


def loadImage(url):
    
    filePath = findImagePage(url)
    content = ""
    if os.path.exists(filePath):
        data = open(filePath, 'rb')
        content = data.read()
        print("loadImage:", filePath)
    else:
        try:
            print("loadImage requests url:", url)
            response = requests.get(url)
            content = response.content
            with open(filePath, "wb")as f:
                f.write(content)
        except:
            pass
    
    return content

def findImagePage(url):
    houzui = ".png"
    if url.endswith('.jpg') or url.endswith('.JPG'):
        houzui = ".jpg"

    md5_url = md5(url.encode('utf8')).hexdigest() + houzui
    filePath = os.path.join("download/image", md5_url)
    return filePath

def urlAddPath(url, p):
    if url.endswith("/"):
        return url + p
    else:
        return url + "/" + p
    
def checkHttp(url):
    if "http" in url:
        return url
    else:
        if(url.startswith("//")):
            return "https:" + url
        else:
            return "https://" + url

def replace(x, old, new=None, strip=False) -> str:
    '''批量替换字符串内容

    :param x: 原始字符串
    :param old: 要替换的内容，可为 `str` , `list`
    :param new: 新内容，可为 `str` , `list` , `None`
    :param strip: 是否删除前后空格
    '''
    if not new:
        new = ''
    if isinstance(old, str):
        x = x.replace(old, new)
    if isinstance(old, list):
        for _old, _new in zip_longest(old, new, fillvalue=''):
            if _new == None:
                _new = ''
            x = x.replace(_old, _new)
    if strip:
        x = x.strip()
    return x

def url2filename(url):
    '''url转文件名'''
    filename = urllib.request.url2pathname(url)
    filename = replace(filename, ['S:', '.', '<', '>', '/', '\\', '|', ':', '*', '?'])
    return filename