import os
import sys
sys.path.append("..")

import webbrowser
import requests

from PyQt5.QtCore import QResource, QUrl, QMimeData
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel

from logic.product import Product
from logic.util import loadImage, findImagePage

from PyQt5.QtWidgets import QApplication,QWidget,QMenu,QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class ImageView(QWidget):

    def __init__(self, imageUrl, *args, **kwargs):
        super(ImageView, self).__init__(*args, **kwargs)
        layout = QHBoxLayout(self)
       
        img = QPixmap("head.jpg")
        data = loadImage(imageUrl)
        img.loadFromData(data)
      
        img = img.scaledToHeight(100)
        img = img.scaledToWidth(100)
        self._img = img

        lable = QLabel(self, pixmap=img)
        lable.setMaximumSize(100, 100)
        layout.addWidget(lable)
    
    def getImage(self):
        return self._img


class ProductWidget(QWidget):

    def __init__(self, product:Product, *args, **kwargs):
        super(ProductWidget, self).__init__(*args, **kwargs)
        
        self.product = product

        layout = QHBoxLayout(self)
        layout.setSpacing(50)

        # 名字
        l = QLabel(self, text=product.name)
        l.setMaximumWidth(400)
        l.resize(300, 100)
        l.setWordWrap(True)
        layout.addWidget(l)

        l = QLabel(self, text=product.price)
        # l.setMaximumWidth(300)
        # l.resize(300, 100)
        # l.setWordWrap(True)
        layout.addWidget(l)

        l = QLabel(self, text=product.siteName)
        l.setMaximumWidth(300)
        l.resize(300, 100)
        l.setWordWrap(True)
        layout.addWidget(l)

        l = QLabel(self, text=product.keywords)
        l.setMaximumWidth(300)
        l.resize(300, 100)
        l.setWordWrap(True)
        layout.addWidget(l)


        self._img = ImageView(product.imageUrl)
        # 从文件加载图片
        print("product.imageUrl:", product.imageUrl)
        layout.addWidget(self._img)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 创建QMenu信号事件
        self.customContextMenuRequested.connect(self.showMenu)
        self.contextMenu = QMenu(self)
        self._copyShop = self.contextMenu.addAction('复制商品名')
        self._copyKey = self.contextMenu.addAction('复制关键字')
        self._copyImage = self.contextMenu.addAction('复制图片')
        self._openShop = self.contextMenu.addAction('打开商品')
        self._openSite = self.contextMenu.addAction('打开站点')
       

        # 事件绑定
        self._copyShop.triggered.connect(self.copyShop)
        self._copyKey.triggered.connect(self.copyKey)
        self._copyImage.triggered.connect(self.copyImage)
        self._openShop.triggered.connect(self.openShop)
        self._openSite.triggered.connect(self.openSite)
   
    
    def getProduct(self) -> Product:
        return self.product
    
    def showMenu(self, pos):
        # pos 鼠标位置
        print(pos)
        # 菜单显示前,将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

    def copyShop(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.product.siteName)
    
    def copyImage(self):
        # clipboard = QApplication.clipboard()
        # clipboard.setPixmap(self._img.getImage())
        # print("copyImage:", self._img.getImage())
        
        p = os.path.join(os.getcwd(), findImagePage(self.product.imageUrl))
        print("copyImage path:", p)

        url = QUrl.fromLocalFile(p)
        m = QMimeData()
        m.setUrls([url])
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(m)
        print("isValid:", url.isValid())

    def copyKey(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.product.keywords)

    def openShop(self):
        webbrowser.open(self.product.productUrl)

    def openSite(self):
        webbrowser.open(self.product.siteUrl)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    p = Product("产品名字", "10.0", "", "head.jpg", "", "商家", "关键字")
    w = ProductWidget(p)
    w.show()
    sys.exit(app.exec_())