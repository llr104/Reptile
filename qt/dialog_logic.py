
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QToolButton
from qt.dialog import *
from qt.productWidget import ProductWidget

import sys
sys.path.append("..") 
from logic import Product, apiSearchProduct, site_productlist, site_product_page


class Dialog_logic(Ui_mainUI):
    def __init__(self):
        super(Dialog_logic, self).__init__()
        
        
    def setupUi(self, Dialog):
        super(Dialog_logic, self).setupUi(Dialog)
        self.mainUI = Dialog

        self.productSearchBtn.clicked.connect(lambda: self.searchProduct())
        self.siteSearchBtn.clicked.connect(lambda: self.searchSite())
        self.nextBtn.clicked.connect(lambda: self.nextPage())
        self.preBtn.clicked.connect(lambda: self.prePage())
        self.goBtn.clicked.connect(lambda: self.goPage())

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
        
        print("search product:", text)
        products = apiSearchProduct(text)
        self.__load_search_products__(products)
    
    def searchSite(self):
        text = self.siteLineEdit.text()
        if len(text) == 0:
            return
        
        page = self.pageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        
        self.__search_site_page__(text, page)
    
    def nextPage(self):
        site = self.siteLineEdit.text()
        if len(site) == 0:
            return
        
        page = self.pageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        totalPage = site_product_page(site, page)
        if page < totalPage:
            self.__search_site_page__(site, page+1)


    def prePage(self):
        site = self.siteLineEdit.text()
        if len(site) == 0:
            return
        
        page = self.pageLineEdit.text()
        if len(page) == 0 or page.isdigit() == False:
            page = 1
        
        page = int(page)
        if page > 1:
            self.__search_site_page__(site, page-1)

    def goPage(self):
        self.searchSite()
    
    def test1(self, item):
        print("test1:", item)

        
     
    
    def test2(self):
        print("test2")

    def __load_search_products__(self, products:Product):
        self.listWidget1.clear()
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

        self.pageLineEdit.setText(str(page))
        self.totalPageLab.setText("共"+str(totalPage)+"页")
        self.__load_search_site_products__(products)

