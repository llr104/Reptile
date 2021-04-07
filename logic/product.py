import os
from logic.util import *

class Product(object):
    def __init__(self, name, price, productUrl, imageUrl, siteUrl, siteName, keywords=None):
        self.name = name


        self.productUrl = checkHttp(productUrl)
        self.imageUrl = checkHttp(imageUrl)
        self.price = price
        self.siteUrl = checkHttp(siteUrl)
        self.siteName = siteName
        self.keywords = keywords

        if self.keywords is None:
            soup = loadProductHtml(self.productUrl)
            if soup is None:
               return
            self.keywords = soup.find(attrs={"name":"keywords"})['content']
        
    def tostring(self):
        des = 'name = %s, productUrl = %s imageUrl = %s, price = %s siteUrl = %s, \
             siteName = %s, keywords = %s' %(self.name, self.productUrl, self.imageUrl, self.price, self.siteUrl, self.siteName, self.keywords)
        return des
    
    def getKeywords(self):
        return self.keywords
