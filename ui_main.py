# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(697, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 671, 571))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_3.setGeometry(QtCore.QRect(20, 220, 611, 281))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser_3.setFont(font)
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.TienXuLyDL = QtWidgets.QPushButton(self.tab_3)
        self.TienXuLyDL.setGeometry(QtCore.QRect(440, 40, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.TienXuLyDL.setFont(font)
        self.TienXuLyDL.setObjectName("TienXuLyDL")
        self.XuatfileTienXuLy = QtWidgets.QPushButton(self.tab_3)
        self.XuatfileTienXuLy.setGeometry(QtCore.QRect(440, 130, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.XuatfileTienXuLy.setFont(font)
        self.XuatfileTienXuLy.setObjectName("XuatfileTienXuLy")
        self.label_18 = QtWidgets.QLabel(self.tab_3)
        self.label_18.setGeometry(QtCore.QRect(20, 10, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_SVthiHK_3 = QtWidgets.QLabel(self.tab_3)
        self.label_SVthiHK_3.setGeometry(QtCore.QRect(110, 40, 271, 21))
        self.label_SVthiHK_3.setText("")
        self.label_SVthiHK_3.setObjectName("label_SVthiHK_3")
        self.fileSVthiHK_3 = QtWidgets.QPushButton(self.tab_3)
        self.fileSVthiHK_3.setGeometry(QtCore.QRect(20, 40, 75, 23))
        self.fileSVthiHK_3.setObjectName("fileSVthiHK_3")
        self.label_27 = QtWidgets.QLabel(self.tab_3)
        self.label_27.setGeometry(QtCore.QRect(20, 80, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.file2CT_3 = QtWidgets.QPushButton(self.tab_3)
        self.file2CT_3.setGeometry(QtCore.QRect(20, 110, 75, 23))
        self.file2CT_3.setObjectName("file2CT_3")
        self.label_2CT_3 = QtWidgets.QLabel(self.tab_3)
        self.label_2CT_3.setGeometry(QtCore.QRect(110, 110, 271, 21))
        self.label_2CT_3.setText("")
        self.label_2CT_3.setObjectName("label_2CT_3")
        self.label_28 = QtWidgets.QLabel(self.tab_3)
        self.label_28.setGeometry(QtCore.QRect(20, 150, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.file_alter_subject_3 = QtWidgets.QPushButton(self.tab_3)
        self.file_alter_subject_3.setGeometry(QtCore.QRect(20, 180, 75, 23))
        self.file_alter_subject_3.setObjectName("file_alter_subject_3")
        self.label_alter_subject_3 = QtWidgets.QLabel(self.tab_3)
        self.label_alter_subject_3.setGeometry(QtCore.QRect(110, 180, 271, 21))
        self.label_alter_subject_3.setText("")
        self.label_alter_subject_3.setObjectName("label_alter_subject_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.tab_4)
        self.textBrowser_4.setGeometry(QtCore.QRect(20, 240, 611, 281))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser_4.setFont(font)
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.label_29 = QtWidgets.QLabel(self.tab_4)
        self.label_29.setGeometry(QtCore.QRect(20, 10, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.file_cbdl_4 = QtWidgets.QPushButton(self.tab_4)
        self.file_cbdl_4.setGeometry(QtCore.QRect(20, 30, 75, 23))
        self.file_cbdl_4.setObjectName("file_cbdl_4")
        self.label_cbdl_4 = QtWidgets.QLabel(self.tab_4)
        self.label_cbdl_4.setGeometry(QtCore.QRect(110, 30, 311, 21))
        self.label_cbdl_4.setText("")
        self.label_cbdl_4.setObjectName("label_cbdl_4")
        self.label_30 = QtWidgets.QLabel(self.tab_4)
        self.label_30.setGeometry(QtCore.QRect(20, 70, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_room_4 = QtWidgets.QLabel(self.tab_4)
        self.label_room_4.setGeometry(QtCore.QRect(110, 100, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_room_4.setFont(font)
        self.label_room_4.setText("")
        self.label_room_4.setObjectName("label_room_4")
        self.file_room_4 = QtWidgets.QPushButton(self.tab_4)
        self.file_room_4.setGeometry(QtCore.QRect(20, 100, 75, 23))
        self.file_room_4.setObjectName("file_room_4")
        self.label_31 = QtWidgets.QLabel(self.tab_4)
        self.label_31.setGeometry(QtCore.QRect(20, 140, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.file_date_4 = QtWidgets.QPushButton(self.tab_4)
        self.file_date_4.setGeometry(QtCore.QRect(20, 170, 75, 23))
        self.file_date_4.setObjectName("file_date_4")
        self.label_date_4 = QtWidgets.QLabel(self.tab_4)
        self.label_date_4.setGeometry(QtCore.QRect(110, 170, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_date_4.setFont(font)
        self.label_date_4.setText("")
        self.label_date_4.setObjectName("label_date_4")
        self.Phanlich = QtWidgets.QPushButton(self.tab_4)
        self.Phanlich.setGeometry(QtCore.QRect(460, 30, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Phanlich.setFont(font)
        self.Phanlich.setObjectName("Phanlich")
        self.XuatfilePL = QtWidgets.QPushButton(self.tab_4)
        self.XuatfilePL.setGeometry(QtCore.QRect(460, 120, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.XuatfilePL.setFont(font)
        self.XuatfilePL.setObjectName("XuatfilePL")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_SVthiHK = QtWidgets.QLabel(self.tab)
        self.label_SVthiHK.setGeometry(QtCore.QRect(110, 30, 271, 21))
        self.label_SVthiHK.setText("")
        self.label_SVthiHK.setObjectName("label_SVthiHK")
        self.label_2CT = QtWidgets.QLabel(self.tab)
        self.label_2CT.setGeometry(QtCore.QRect(110, 80, 271, 21))
        self.label_2CT.setText("")
        self.label_2CT.setObjectName("label_2CT")
        self.label_alter_subject = QtWidgets.QLabel(self.tab)
        self.label_alter_subject.setGeometry(QtCore.QRect(110, 130, 271, 21))
        self.label_alter_subject.setText("")
        self.label_alter_subject.setObjectName("label_alter_subject")
        self.fileSVthiHK = QtWidgets.QPushButton(self.tab)
        self.fileSVthiHK.setGeometry(QtCore.QRect(20, 30, 75, 23))
        self.fileSVthiHK.setObjectName("fileSVthiHK")
        self.file2CT = QtWidgets.QPushButton(self.tab)
        self.file2CT.setGeometry(QtCore.QRect(20, 80, 75, 23))
        self.file2CT.setObjectName("file2CT")
        self.file_alter_subject = QtWidgets.QPushButton(self.tab)
        self.file_alter_subject.setGeometry(QtCore.QRect(20, 130, 75, 23))
        self.file_alter_subject.setObjectName("file_alter_subject")
        self.KtrCBDL = QtWidgets.QPushButton(self.tab)
        self.KtrCBDL.setGeometry(QtCore.QRect(450, 40, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.KtrCBDL.setFont(font)
        self.KtrCBDL.setObjectName("KtrCBDL")
        self.XuatfileCBDL = QtWidgets.QPushButton(self.tab)
        self.XuatfileCBDL.setGeometry(QtCore.QRect(450, 130, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.XuatfileCBDL.setFont(font)
        self.XuatfileCBDL.setObjectName("XuatfileCBDL")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(20, 220, 611, 281))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.file_cbdl = QtWidgets.QPushButton(self.tab)
        self.file_cbdl.setGeometry(QtCore.QRect(20, 180, 75, 23))
        self.file_cbdl.setObjectName("file_cbdl")
        self.label_cbdl = QtWidgets.QLabel(self.tab)
        self.label_cbdl.setGeometry(QtCore.QRect(110, 180, 271, 21))
        self.label_cbdl.setText("")
        self.label_cbdl.setObjectName("label_cbdl")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(20, 10, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(20, 60, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(20, 160, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(20, 110, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.file_PhanLich = QtWidgets.QPushButton(self.tab_2)
        self.file_PhanLich.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.file_PhanLich.setObjectName("file_PhanLich")
        self.label_SVPhanLich = QtWidgets.QLabel(self.tab_2)
        self.label_SVPhanLich.setGeometry(QtCore.QRect(100, 20, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_SVPhanLich.setFont(font)
        self.label_SVPhanLich.setText("")
        self.label_SVPhanLich.setObjectName("label_SVPhanLich")
        self.fileCBDL = QtWidgets.QPushButton(self.tab_2)
        self.fileCBDL.setGeometry(QtCore.QRect(10, 70, 75, 23))
        self.fileCBDL.setObjectName("fileCBDL")
        self.file_date = QtWidgets.QPushButton(self.tab_2)
        self.file_date.setGeometry(QtCore.QRect(10, 120, 75, 23))
        self.file_date.setObjectName("file_date")
        self.label_cbdl_tab2 = QtWidgets.QLabel(self.tab_2)
        self.label_cbdl_tab2.setGeometry(QtCore.QRect(100, 70, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_cbdl_tab2.setFont(font)
        self.label_cbdl_tab2.setText("")
        self.label_cbdl_tab2.setObjectName("label_cbdl_tab2")
        self.label_date = QtWidgets.QLabel(self.tab_2)
        self.label_date.setGeometry(QtCore.QRect(100, 120, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_date.setFont(font)
        self.label_date.setText("")
        self.label_date.setObjectName("label_date")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(10, 0, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(10, 40, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(10, 100, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 250, 611, 281))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.KtrPhanLich = QtWidgets.QPushButton(self.tab_2)
        self.KtrPhanLich.setGeometry(QtCore.QRect(460, 20, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.KtrPhanLich.setFont(font)
        self.KtrPhanLich.setObjectName("KtrPhanLich")
        self.XuatfileKtr = QtWidgets.QPushButton(self.tab_2)
        self.XuatfileKtr.setGeometry(QtCore.QRect(460, 100, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.XuatfileKtr.setFont(font)
        self.XuatfileKtr.setObjectName("XuatfileKtr")
        self.XuatfileLichthi = QtWidgets.QPushButton(self.tab_2)
        self.XuatfileLichthi.setGeometry(QtCore.QRect(460, 180, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.XuatfileLichthi.setFont(font)
        self.XuatfileLichthi.setObjectName("XuatfileLichthi")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(10, 150, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.file_object = QtWidgets.QPushButton(self.tab_2)
        self.file_object.setGeometry(QtCore.QRect(10, 170, 75, 23))
        self.file_object.setObjectName("file_object")
        self.label_subject = QtWidgets.QLabel(self.tab_2)
        self.label_subject.setGeometry(QtCore.QRect(100, 170, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_subject.setFont(font)
        self.label_subject.setText("")
        self.label_subject.setObjectName("label_subject")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(10, 200, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.file_room = QtWidgets.QPushButton(self.tab_2)
        self.file_room.setGeometry(QtCore.QRect(10, 220, 75, 23))
        self.file_room.setObjectName("file_room")
        self.label_room = QtWidgets.QLabel(self.tab_2)
        self.label_room.setGeometry(QtCore.QRect(100, 220, 311, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.label_room.setFont(font)
        self.label_room.setText("")
        self.label_room.setObjectName("label_room")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 697, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        label_stylesheet = "background-color: lightblue;"
        self.label_SVthiHK.setStyleSheet(label_stylesheet)
        self.label_2CT.setStyleSheet(label_stylesheet)
        self.label_alter_subject.setStyleSheet(label_stylesheet)
        self.label_cbdl.setStyleSheet(label_stylesheet)
        self.label_SVPhanLich.setStyleSheet(label_stylesheet)
        self.label_cbdl_tab2.setStyleSheet(label_stylesheet)
        self.label_date.setStyleSheet(label_stylesheet)
        self.label_subject.setStyleSheet(label_stylesheet)
        self.label_room.setStyleSheet(label_stylesheet)

        self.label_SVthiHK_3.setStyleSheet(label_stylesheet)
        self.label_2CT_3.setStyleSheet(label_stylesheet)
        self.label_alter_subject_3.setStyleSheet(label_stylesheet)
        self.label_cbdl_4.setStyleSheet(label_stylesheet)
        self.label_room_4.setStyleSheet(label_stylesheet)
        self.label_date_4.setStyleSheet(label_stylesheet)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kiểm tra công cụ lập lịch thi"))
        self.textBrowser_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.TienXuLyDL.setText(_translate("MainWindow", "Thực hiện tiền xử lý dữ liệu"))
        self.XuatfileTienXuLy.setText(_translate("MainWindow", "Xuất tập tin tiền xử lý dữ liệu"))
        self.label_18.setText(_translate("MainWindow", "Danh sách sinh viên thi học kì"))
        self.fileSVthiHK_3.setText(_translate("MainWindow", "Browser"))
        self.label_27.setText(_translate("MainWindow", "Danh sách sinh viên 2 CT"))
        self.file2CT_3.setText(_translate("MainWindow", "Browser"))
        self.label_28.setText(_translate("MainWindow", "Danh sách học phần thay thế"))
        self.file_alter_subject_3.setText(_translate("MainWindow", "Browser"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tiền xử lý dữ liệu"))
        self.textBrowser_4.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.label_29.setText(_translate("MainWindow", "Danh sách tiền xử lý"))
        self.file_cbdl_4.setText(_translate("MainWindow", "Browser"))
        self.label_30.setText(_translate("MainWindow", "Danh sách phòng thi "))
        self.file_room_4.setText(_translate("MainWindow", "Browser"))
        self.label_31.setText(_translate("MainWindow", "Danh sách ngày thi"))
        self.file_date_4.setText(_translate("MainWindow", "Browser"))
        self.Phanlich.setText(_translate("MainWindow", "Phân lịch"))
        self.XuatfilePL.setText(_translate("MainWindow", "Xuất tập tin lịch thi"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Phân lịch thi"))
        self.fileSVthiHK.setText(_translate("MainWindow", "Browser"))
        self.file2CT.setText(_translate("MainWindow", "Browser"))
        self.file_alter_subject.setText(_translate("MainWindow", "Browser"))
        self.KtrCBDL.setText(_translate("MainWindow", "Kiểm tra tập tin tiền xử lý"))
        self.XuatfileCBDL.setText(_translate("MainWindow", "Xuất tập tin kiểm tra"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.file_cbdl.setText(_translate("MainWindow", "Browser"))
        self.label_13.setText(_translate("MainWindow", "Danh sách sinh viên thi học kì"))
        self.label_14.setText(_translate("MainWindow", "Danh sách sinh viên CT2"))
        self.label_15.setText(_translate("MainWindow", "Danh sách tiền xử lý dữ liệu"))
        self.label_16.setText(_translate("MainWindow", "Danh sách học phần thay thế"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Kiểm tra tập tin tiền xử lý dữ liệu"))
        self.file_PhanLich.setText(_translate("MainWindow", "Browser"))
        self.fileCBDL.setText(_translate("MainWindow", "Browser"))
        self.file_date.setText(_translate("MainWindow", "Browser"))
        self.label_7.setText(_translate("MainWindow", "Danh sách sinh viên đã phân lịch thi"))
        self.label_8.setText(_translate("MainWindow", "Danh sách tiền xử lý"))
        self.label_9.setText(_translate("MainWindow", "Danh sách ngày thi"))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8.25pt;\"><br /></p></body></html>"))
        self.KtrPhanLich.setText(_translate("MainWindow", "Kiểm tra tập tin phân lịch"))
        self.XuatfileKtr.setText(_translate("MainWindow", "Xuất tập tin kiểm tra"))
        self.XuatfileLichthi.setText(_translate("MainWindow", "Xuất tập tin lịch thi"))
        self.label_11.setText(_translate("MainWindow", "Danh sách học phần - khoa "))
        self.file_object.setText(_translate("MainWindow", "Browser"))
        self.label_12.setText(_translate("MainWindow", "Danh sách phòng thi "))
        self.file_room.setText(_translate("MainWindow", "Browser"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Kiểm tra tập tin phân lịch"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
