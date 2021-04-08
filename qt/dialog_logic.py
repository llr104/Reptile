import pandas as pd
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QToolButton, QMessageBox, QWidget
from qt.dialog import *
from qt.productWidget import ProductWidget

import sys
import os
sys.path.append("..") 
from logic import Product, apiSearchProduct, site_productlist, site_product_page
from logic import url2filename


class Dialog_logic(Ui_mainUI):
    def __init__(self):
        super(Dialog_logic, self).__init__()

        self._searchProductDict = {}
        self._siteProductDict = {}
        self._productTotalPage = 0
        
    def setupUi(self, Dialog):
        super(Dialog_logic, self).setupUi(Dialog)
        self.mainUI = Dialog

        self.productSearchBtn.clicked.connect(lambda: self.searchProduct())
        self.siteSearchBtn.clicked.connect(lambda: self.searchSite())

        self.siteNextBtn.clicked.connect(lambda: self.nextSitePage())
        self.sitePreBtn.clicked.connect(lambda: self.preSitePage())
        self.siteGoBtn.clicked.connect(lambda: self.goSitePage())

        self.productNextBtn.clicked.connect(lambda: self.nextProductPage())
        self.productPreBtn.clicked.connect(lambda: self.preProductPage())
        self.productGoBtn.clicked.connect(lambda: self.goProductPage())


        self.productOutPutBtn.clicked.connect(lambda: self.productOutPut())
        self.siteOutPutBtn.clicked.connect(lambda: self.siteOutPut())

        self.listWidget1.itemClicked.connect(self.test1)
        self.listWidget2.itemClicked.connect(self.test2)

        # for o in range(2):
        #     p = Product("产品名字", "10.0", "", "https://s.alicdn.com/@sc01/kf/Hb9fef37528924d2597e3e162ac8e71b9N.jpg_480x480.jpg", "", "商家", "关键字")
        #     w = ProductWidget(p)
        #     item = QListWidgetItem(self.listWidget)
        #     item.setSizeHint(w.sizeHint())
        #     self.listWidget.setItemWidget(item, w)
    

    def searchProduct(self):
        
        text = self.productLineEdit.text()
        if len(text) == 0:
            return
        
        page = self.productPageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1

        products, self._productTotalPage = apiSearchProduct(text)
        self.__search_products_page__(products, text, page, self._productTotalPage)
    
    def searchSite(self):
        text = self.siteLineEdit.text()
        if len(text) == 0:
            return
        
        page = self.sitePageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        
        self.__search_site_page__(text, page)
    
    def nextSitePage(self):
        site = self.siteLineEdit.text()
        if len(site) == 0:
            return
        
        page = self.sitePageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        totalPage = site_product_page(site, page)
        if page < totalPage:
            self.__search_site_page__(site, page+1)


    def preSitePage(self):
        site = self.siteLineEdit.text()
        if len(site) == 0:
            return
        
        page = self.sitePageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        if page > 1:
            self.__search_site_page__(site, page-1)

    def goSitePage(self):
        self.searchSite()


    def nextProductPage(self):
        keyword = self.productLineEdit.text()
        if len(keyword) == 0:
            return
        
        page = self.productPageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        if page < self._productTotalPage:
            products, self._productTotalPage = apiSearchProduct(keyword, page+1)
            self.__search_products_page__(products, keyword, page+1, self._productTotalPage)

    def preProductPage(self):
        keyword = self.productLineEdit.text()
        if len(keyword) == 0:
            return
        
        page = self.productPageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        if page > 1:
            products, self._productTotalPage = apiSearchProduct(keyword, page-1)
            self.__search_products_page__(products, keyword, page-1, self._productTotalPage)

    def goProductPage(self):
        self.searchProduct()

    def productOutPut(self):
        print("productOutPut")

        text = self.productLineEdit.text()
        if len(text) == 0:
            return
        
        names = []
        sites = []
        prices = []
        keys = []
        urls = []

        ps = self._searchProductDict.get(text)
        if ps is None:
            return

        for p in ps:
            names.append(p.name)
            sites.append(p.siteName)
            prices.append(p.price)
            keys.append(p.keywords)
            urls.append(p.productUrl)
        
        try:
            fp = os.path.join(os.getcwd(), "output", url2filename(text) + ".xlsx")
            data = {"商品名":names, "站名":sites, "价格":prices, "关键字":keys, "商品地址":urls}
            df = pd.DataFrame(data)
            df.to_excel(fp)

            QMessageBox.information(self.listWidget1, '导出成功', '导出成功,已经导出到目录:' + fp, QMessageBox.Yes)
        except:
            QMessageBox.warning(self.listWidget1, '导出失败', "导出失败,请检查文件:" + fp + "是否被其他应用占用", QMessageBox.Ok)

    def siteOutPut(self):
        print("siteOutPut")
        text = self.siteLineEdit.text()
        if len(text) == 0:
            return

        names = []
        sites = []
        prices = []
        keys = []
        urls = []

        ps = self._siteProductDict.get(text)
        if ps is None:
            return

        for p in ps:
            names.append(p.name)
            sites.append(p.siteName)
            prices.append(p.price)
            keys.append(p.keywords)
            urls.append(p.productUrl)
        
        try:
            fp = os.path.join(os.getcwd(), "output", url2filename(text) + ".xlsx")
            data = {"商品名":names, "站名":sites, "价格":prices, "关键字":keys, "商品地址":urls}
            df = pd.DataFrame(data)
            df.to_excel(fp)
            QMessageBox.information(self.listWidget2, '导出成功', '导出成功,已经导出到目录:' + fp, QMessageBox.Yes)
        except:
            QMessageBox.warning(self.listWidget2, '导出失败', "导出失败,请检查文件:" + fp + "是否被其他应用占用", QMessageBox.Ok)
    
    def test1(self, item):
        print("test1:", item)

    def test2(self):
        print("test2")

    def __search_products_page__(self, products:Product, keyword, curPage, totalPage):
        self.listWidget1.clear()
        self.productPageLineEdit.setText(str(curPage))
        self.productTotalPageLab.setText("共"+str(totalPage)+"页")

        self._searchProductDict[keyword] = products
        self.__load_search_products__(products)

    def __load_search_products__(self, products:Product):
       
        for p in products:
            w = ProductWidget(p)
            item = QListWidgetItem(self.listWidget1)
            item.setSizeHint(w.sizeHint())
            self.listWidget1.setItemWidget(item, w)
    
    def __load_search_site_products__(self, products:Product):
        for p in products:
            w = ProductWidget(p)
            item = QListWidgetItem(self.listWidget2)
            item.setSizeHint(w.sizeHint())
            self.listWidget2.setItemWidget(item, w)
    
    def __search_site_page__(self, site, page):
        self.listWidget2.clear()

        print("search site:", site, page)
        products = site_productlist(site, page)
        totalPage = site_product_page(site, page)

        ps = self._siteProductDict.get(site)
        if ps is None:
            self._siteProductDict[site] = products
        else:
            self._siteProductDict[site].extend(products)

        self.sitePageLineEdit.setText(str(page))
        self.siteTotalPageLab.setText("共"+str(totalPage)+"页")
        self.__load_search_site_products__(products)

