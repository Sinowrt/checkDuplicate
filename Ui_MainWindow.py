# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1200, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/Jacky/Pictures/20200401004730.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(714, 39, 91, 21))
        self.browseButton.setObjectName("browseButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 40, 621, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.label.setObjectName("label")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(960, 40, 81, 21))
        self.checkButton.setObjectName("checkButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 111, 1061, 681))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 80, 1011, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 41, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 691, 16))
        self.label_3.setObjectName("label_3")
        self.titleListView = QtWidgets.QListView(self.centralwidget)
        self.titleListView.setGeometry(QtCore.QRect(1080, 110, 111, 681))
        self.titleListView.setObjectName("titleListView")
        self.addTitleBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addTitleBtn.setGeometry(QtCore.QRect(1080, 40, 111, 23))
        self.addTitleBtn.setObjectName("addTitleBtn")
        self.delTitleBtn = QtWidgets.QPushButton(self.centralwidget)
        self.delTitleBtn.setGeometry(QtCore.QRect(1080, 70, 111, 23))
        self.delTitleBtn.setObjectName("delTitleBtn")
        self.titleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleLineEdit.setGeometry(QtCore.QRect(1080, 10, 111, 20))
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.enableTitleCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.enableTitleCheckBox.setGeometry(QtCore.QRect(840, 40, 101, 21))
        self.enableTitleCheckBox.setObjectName("enableTitleCheckBox")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "查重工具"))
        self.browseButton.setText(_translate("MainWindow", "浏览"))
        self.label.setText(_translate("MainWindow", "试卷路径:"))
        self.checkButton.setText(_translate("MainWindow", "开始查重"))
        self.label_2.setText(_translate("MainWindow", "进度："))
        self.label_3.setText(_translate("MainWindow", "Note:【查重前】请确认每个题目编号后为、或.号，并且选项ABCD的编号为纯文字类型，以图片形式承载的ABCD选项暂时无法处理"))
        self.addTitleBtn.setText(_translate("MainWindow", "添加标题"))
        self.delTitleBtn.setText(_translate("MainWindow", "删除标题"))
        self.enableTitleCheckBox.setText(_translate("MainWindow", "启用标题查找"))

