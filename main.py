import sys,os,checkDuplicate
from Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow, Ui_MainWindow):
    appendSignal = pyqtSignal(str)
    updateProgressSignal = pyqtSignal(float)
    string_list=['公共基础知识', '判断推理', '数量关系', '言语理解与表达', '资料分析']

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.browseButton.clicked.connect(self.open_directory)
        self.checkButton.clicked.connect(self.check_duplicate)
        self.addTitleBtn.clicked.connect(self.addTitle)
        self.delTitleBtn.clicked.connect(self.delTitle)

        self.appendSignal.connect(self.appendText)
        self.updateProgressSignal.connect(self.updataProgress)

        self.stringlistmodel = QStringListModel()  # 创建stringlistmodel对象
        self.stringlistmodel.setStringList(self.string_list)  # 把数据赋值到 model 上
        self.titleListView.setModel(self.stringlistmodel)  # 把 view 和 model 关联
        self.stringlistmodel.dataChanged.connect(self.save)

        self.enableTitleCheckBox.setChecked(True)

    def save(self):
        self.string_list = self.stringlistmodel.stringList()
        print(self.string_list)

    def addTitle(self):
        kw = self.titleLineEdit.text()
        if kw == '':
            self.appendSignal.emit('无法添加空标题！')
            return
        row = self.stringlistmodel.rowCount()

        self.stringlistmodel.insertRow(row)
        self.stringlistmodel.setData(self.stringlistmodel.index(row), kw)
        self.save()

    def delTitle(self):
        index = self.titleListView.currentIndex()
        print(index.row())
        self.stringlistmodel.removeRow(index.row())
        self.save()
        print(self.string_list)

    def open_directory(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        print(path)
        self.lineEdit.setText(path)

    def check_duplicate(self):
        self.textBrowser.clear()
        self.checkButton.setEnabled(False)
        self.browseButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        if self.enableTitleCheckBox.isChecked():
            checkDuplicate.ckduplicate(self.lineEdit.text(), self)
        else:
            checkDuplicate.checkDuplicateWithoutTitle(self.lineEdit.text(), self)
        self.checkButton.setEnabled(True)
        self.browseButton.setEnabled(True)
        self.lineEdit.setEnabled(True)

    def appendText(self,str):
        self.textBrowser.append(str)

    def updataProgress(self,percent):
        self.progressBar.setProperty("value", percent)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())