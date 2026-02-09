# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Dialog_DownloaderidJOuB.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_Dialog_Main(object):
    def setupUi(self, Dialog_Main):
        if not Dialog_Main.objectName():
            Dialog_Main.setObjectName(u"Dialog_Main")
        Dialog_Main.resize(740, 596)
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        Dialog_Main.setPalette(palette)
        Dialog_Main.setAutoFillBackground(False)
        # Dialog_Main.setSizeGripEnabled(False)
        self.Label_Links = QLabel(Dialog_Main)
        self.Label_Links.setObjectName(u"Label_Links")
        self.Label_Links.setGeometry(QRect(30, 20, 56, 12))
        self.Btn_Paste = QPushButton(Dialog_Main)
        self.Btn_Paste.setObjectName(u"Btn_Paste")
        self.Btn_Paste.setGeometry(QRect(620, 70, 101, 91))
        self.Btn_Video_Down = QPushButton(Dialog_Main)
        self.Btn_Video_Down.setObjectName(u"Btn_Video_Down")
        self.Btn_Video_Down.setGeometry(QRect(130, 340, 161, 60))
        self.Btn_Audio_Down = QPushButton(Dialog_Main)
        self.Btn_Audio_Down.setObjectName(u"Btn_Audio_Down")
        self.Btn_Audio_Down.setGeometry(QRect(350, 340, 181, 60))
        self.Label_List_File = QLabel(Dialog_Main)
        self.Label_List_File.setObjectName(u"Label_List_File")
        self.Label_List_File.setGeometry(QRect(40, 420, 56, 12))
        self.LineEdit_ListFile_Path = QLineEdit(Dialog_Main)
        self.LineEdit_ListFile_Path.setObjectName(u"LineEdit_ListFile_Path")
        self.LineEdit_ListFile_Path.setGeometry(QRect(30, 440, 580, 30))
        self.Btn_Select_File = QPushButton(Dialog_Main)
        self.Btn_Select_File.setObjectName(u"Btn_Select_File")
        self.Btn_Select_File.setGeometry(QRect(620, 430, 100, 60))
        self.Btn_Close_App = QPushButton(Dialog_Main)
        self.Btn_Close_App.setObjectName(u"Btn_Close_App")
        self.Btn_Close_App.setGeometry(QRect(560, 500, 161, 51))
        self.ListWidget_Links = QListWidget(Dialog_Main)
        self.ListWidget_Links.setObjectName(u"ListWidget_Links")
        self.ListWidget_Links.setGeometry(QRect(30, 50, 581, 231))
        self.LineEdit_Link = QLineEdit(Dialog_Main)
        self.LineEdit_Link.setObjectName(u"LineEdit_Link")
        self.LineEdit_Link.setGeometry(QRect(29, 294, 581, 30))
        self.Btn_Add = QPushButton(Dialog_Main)
        self.Btn_Add.setObjectName(u"Btn_Add")
        self.Btn_Add.setGeometry(QRect(620, 280, 100, 60))
        self.Btn_Delete = QPushButton(Dialog_Main)
        self.Btn_Delete.setObjectName(u"Btn_Delete")
        self.Btn_Delete.setGeometry(QRect(620, 220, 100, 50))
        self.TextBrowser_Status = QTextBrowser(Dialog_Main)
        self.TextBrowser_Status.setObjectName(u"TextBrowser_Status")
        self.TextBrowser_Status.setGeometry(QRect(30, 490, 501, 81))

        self.retranslateUi(Dialog_Main)
        self.Btn_Paste.clicked.connect(self.ListWidget_Links.update)
        self.Btn_Add.clicked.connect(self.ListWidget_Links.update)
        self.Btn_Delete.clicked.connect(self.ListWidget_Links.update)
        self.LineEdit_Link.returnPressed.connect(self.ListWidget_Links.update)
        self.Btn_Select_File.clicked.connect(self.LineEdit_ListFile_Path.update)

        QMetaObject.connectSlotsByName(Dialog_Main)
    # setupUi

    def retranslateUi(self, Dialog_Main):
        Dialog_Main.setWindowTitle(QCoreApplication.translate("Dialog_Main", u"YouTube Downloader", None))
        self.Label_Links.setText(QCoreApplication.translate("Dialog_Main", u"Links", None))
        self.Btn_Paste.setText(QCoreApplication.translate("Dialog_Main", u"Paste \n"
"from \n"
"Clipboard", None))
        self.Btn_Video_Down.setText(QCoreApplication.translate("Dialog_Main", u"Video Download", None))
        self.Btn_Audio_Down.setText(QCoreApplication.translate("Dialog_Main", u"Audio Download", None))
        self.Label_List_File.setText(QCoreApplication.translate("Dialog_Main", u"List File", None))
        self.LineEdit_ListFile_Path.setText("")
        self.Btn_Select_File.setText(QCoreApplication.translate("Dialog_Main", u"Select", None))
        self.Btn_Close_App.setText(QCoreApplication.translate("Dialog_Main", u"Close App", None))
        self.Btn_Add.setText(QCoreApplication.translate("Dialog_Main", u"Add", None))
        self.Btn_Delete.setText(QCoreApplication.translate("Dialog_Main", u"Delete", None))
    # retranslateUi

