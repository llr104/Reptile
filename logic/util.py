
import os
import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
from hashlib import md5


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
            strhtml=requests.get(url)
            with open(filePath, "w", encoding='utf-8')as f:
                f.write(strhtml.text)
            text = strhtml.text
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
            strhtml=requests.get(url)
            with open(filePath, "w", encoding='utf-8')as f:
                f.write(strhtml.text)
            text = strhtml.text
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