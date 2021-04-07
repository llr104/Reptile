import os
from logic.util import *

class Site(object):
    def __init__(self, siteUrl, siteName, keywords=None):
        self.siteUrl = checkHttp(siteUrl)
        self.siteName = siteName
        self.keywords = keywords

        if self.keywords is None:
            soup = loadSiteHtml(siteUrl)
            if soup is None:
                return
            
            self.keywords = soup.find(attrs={"name":"keywords"})['content']
        
    def tostring(self):
        des = 'siteUrl = %s, siteName = %s, keywords = %s' %(self.siteUrl, self.siteName, self.keywords)
        return des
    
    def getKeywords(self):
        return self.keywords