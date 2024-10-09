# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tela.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QPushButton, QSizePolicy, QTabWidget, QTextEdit,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(1220, 860)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.CodigosSQL = QTextEdit(Dialog)
        self.CodigosSQL.setObjectName(u"CodigosSQL")
        self.CodigosSQL.setGeometry(QRect(210, 10, 1011, 851))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(9)
        font.setBold(False)
        self.CodigosSQL.setFont(font)
        self.CodigosSQL.setStyleSheet(u"")
        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(200, 10, 20, 851))
        self.line.setStyleSheet(u"background-color:  rgb(158, 158, 158);")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2 = QFrame(Dialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(0, 0, 1221, 16))
        self.line_2.setStyleSheet(u"background-color:  rgb(158, 158, 158);")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.botaoConsultar = QPushButton(Dialog)
        self.botaoConsultar.setObjectName(u"botaoConsultar")
        self.botaoConsultar.setEnabled(True)
        self.botaoConsultar.setGeometry(QRect(20, 100, 101, 41))
        font1 = QFont()
        font1.setKerning(True)
        self.botaoConsultar.setFont(font1)
        self.botaoConsultar.setAutoFillBackground(False)
        self.botaoConsultar.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.Tabela = QTabWidget(Dialog)
        self.Tabela.setObjectName(u"Tabela")
        self.Tabela.setGeometry(QRect(0, 500, 1231, 361))
        font2 = QFont()
        font2.setFamilies([u"Consolas"])
        self.Tabela.setFont(font2)
        self.botaoCancelar = QPushButton(Dialog)
        self.botaoCancelar.setObjectName(u"botaoCancelar")
        self.botaoCancelar.setEnabled(True)
        self.botaoCancelar.setGeometry(QRect(160, 110, 16, 16))
        self.botaoCancelar.setStyleSheet(u"background-color:rgb(255, 0, 0)")
        self.exportarExcel = QPushButton(Dialog)
        self.exportarExcel.setObjectName(u"exportarExcel")
        self.exportarExcel.setGeometry(QRect(20, 160, 161, 41))
        self.exportarExcel.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 50, 204, 811))
        self.label.setStyleSheet(u"background-color: rgb(216, 216, 216);")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 10, 204, 61))
        self.label_2.setStyleSheet(u"background-color: rgb(216, 216, 216);")
        self.botaoCopiar = QPushButton(Dialog)
        self.botaoCopiar.setObjectName(u"botaoCopiar")
        self.botaoCopiar.setGeometry(QRect(20, 220, 161, 41))
        self.botaoCopiar.setStyleSheet(u"background-color:rgb(255, 255, 255)")
        self.line.raise_()
        self.label_2.raise_()
        self.line_2.raise_()
        self.CodigosSQL.raise_()
        self.label.raise_()
        self.Tabela.raise_()
        self.botaoConsultar.raise_()
        self.botaoCancelar.raise_()
        self.exportarExcel.raise_()
        self.botaoCopiar.raise_()

        self.retranslateUi(Dialog)

        self.Tabela.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.CodigosSQL.setHtml(QCoreApplication.translate("Dialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Consolas'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'System'; font-size:12pt; font-weight:600;\"><br /></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.botaoConsultar.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.botaoConsultar.setText(QCoreApplication.translate("Dialog", u"Executar", None))
        self.botaoCancelar.setText("")
        self.exportarExcel.setText(QCoreApplication.translate("Dialog", u"Exportar para Excel", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Ferramentas</span></p></body></html>", None))
        self.botaoCopiar.setText(QCoreApplication.translate("Dialog", u"Copiar registros", None))
    # retranslateUi

