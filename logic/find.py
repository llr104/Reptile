import os
import json
import requests
import urllib.parse
import math
from bs4 import BeautifulSoup
from hashlib import md5
from logic.product import *
from logic.util import *

def site_all_productlist(siteUrl):
    site_productlist(siteUrl, 1)
    fileName = siteUrl + "productlist-1" + ".html"
    soup = loadSiteHtml(fileName)
    if soup is None:
        return
    
    grids = soup.select(".grid > div")

    totalPage = site_product_page(siteUrl, 1)
    if totalPage > 1:
        for pageNum in range(2, totalPage):
            site_productlist(siteUrl, pageNum)



def site_productlist(siteUrl, page) -> [Product]:
    siteUrl = checkHttp(siteUrl)

    fileName = "productlist-" + str(page) + ".html"
    url = urlAddPath(siteUrl, fileName)

    print("site_productlist:", url)
    soup = loadSiteHtml(url)
    if soup is None:
        return []
    
    #获取公司名字
    cpname = soup.select(".cp-name")[0].string
    print("cpname:", cpname)

    # keywords = soup.find(attrs={"name":"keywords"})['content']

    #获取商品列表，商品列表放在自定义的module-data里面
    grids = soup.select(".grid > div")
    ps = analysisProductList(grids, siteUrl, cpname)
    return ps

def site_product_page(siteUrl, page):

    siteUrl = checkHttp(siteUrl)
    fileName = "productlist-" + str(page) + ".html"
    url = urlAddPath(siteUrl, fileName)

    soup = loadSiteHtml(url)
    if soup is None:
        return 0
    
    grids = soup.select(".grid > div")
    totalPage = 1
    for gird in grids:
        if gird["module-title"] == "productListPc":
            data = urllib.parse.unquote(gird["module-data"])
            user_dic = json.loads(data)
            #总行数
            totalLines = user_dic["mds"]["moduleData"]["data"]["pageNavView"]["totalLines"]
            #每页有多少行
            pageLines = user_dic["mds"]["moduleData"]["data"]["pageNavView"]["pageLines"]
            totalPage = math.ceil(totalLines/pageLines)
    
    return totalPage


def analysisProductList(grids, siteUrl, siteTitle):
    productList = []
    for gird in grids:
        if gird["module-title"] == "productListPc":
            data = urllib.parse.unquote(gird["module-data"])
         
            # print("analysisProductList:", data)
            user_dic = json.loads(data)
            products = user_dic["mds"]["moduleData"]["data"]["productList"]

            # print("pl:", pl)
            for pd in products:
                price = pd["originalPrice"]
                subject = pd["subject"]
                url = siteUrl + pd["url"] #产品在站点的域名之下
                imageUrl = pd["imageUrls"]["x350"]
                p = Product(subject, price, url, imageUrl, siteUrl, siteTitle)
                productList.append(p)
                # print("p:", p.tostring())
    
    return productList


def apiSearchProduct(productName):
    
    url = "https://open-s.alibaba.com/openservice/galleryProductOfferResultViewService?SearchText=" + productName
    response = requests.get(url)
    if response.ok == False:
        return
    # print("response.text:", response.text)

    md5_url = md5(productName.encode('utf8')).hexdigest()
    fn = os.path.join("download/search", md5_url + ".json")
    with open(fn, "w", encoding='utf-8')as f:
        f.write(response.text)
    
    return analysisSearch(response.text)

def analysisSearch(text):
    user_dic = json.loads(text)
    # print("user_dic:", user_dic["data"]["offerList"][0]["information"])

    products = []
    try:
        print("offerList len:", len(user_dic["data"]["offerList"]))    
        for offer in user_dic["data"]["offerList"]:
            # print("offer:", offer)
            productUrl = offer["information"]["productUrl"]
            productTitle = offer["information"]["puretitle"] 
            buyNow = offer["information"]["buyNow"] 
            supplierName = offer["supplier"]["supplierName"]
            supplierHref = offer["supplier"]["supplierHref"]
            mainImage = offer["image"]["mainImage"]
            tradePrice =  offer["tradePrice"]["price"]

            p = Product(productTitle, tradePrice, productUrl, mainImage, supplierHref, supplierName)
            products.append(p)
    except:
        pass
    return products

# if __name__ == '__main__':
#     createDir("download/product")
#     createDir("download/search")
#     createDir(os.path.join("download/site", "productsPage"))

#     site_all_productlist("https://myz.en.alibaba.com/")
#     apiSearchProduct("table")

    