from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from qt.dialog_logic import Dialog_logic

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.resize(1280, 720)
    MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

    ui = Dialog_logic()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
