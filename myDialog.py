# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:35:44 2020

@author: 皮卡丘
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from dBase import *

class MyDialog(QDialog):
    my_signal = pyqtSignal(bool, tuple)
    com_signal = pyqtSignal(bool, str)
    def __init__(self, name, mod, link = {}):
        super().__init__()
        self.link_dir = link
        self.vbox = QVBoxLayout()
        self.table_name = name
        self.setWindowTitle(name)
        self.crol_data = (self.table_name, mod)
        
    def initBussiness(self, com, data=("", "", "", "", "", "", "", "", "", "", "")):
        self.id = data[0]
        self.date, hbox1 = self.getDate(data[1])
        self.name, hbox2 = self.getLine("客户姓名",data[2])
        self.combo1, hbox3 = self.getCombo(com[0], "购买产品",data[3])
        self.combo2, hbox4 = self.getCombo(com[1], "购买选项",data[4])
        self.total, hbox5 = self.getLine("购买总额",str(data[5]))
        self.total.setValidator(QDoubleValidator(-250.0,290.0,2,self))
        self.actpay, hbox6 = self.getLine("实付金额",str(data[6]))
        self.actpay.setValidator(QDoubleValidator(-250.0,290.0,2,self))
        self.arrears, hbox7 = self.getLine("欠款金额",str(data[7]))
        self.arrears.setValidator(QDoubleValidator(-250.0,290.0,2,self))
        self.Paymethod, hbox8 = self.getLine("付款方式",data[8])
        self.adviser, hbox9 = self.getCombo(com[2], "美容顾问",data[9])
        self.commission, hbox10 = self.getCombo(("已发放", "未发放"), "提成    ",data[10])
        hbox11 = self.getButton()
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(hbox4)
        self.vbox.addLayout(hbox5)
        self.vbox.addLayout(hbox6)
        self.vbox.addLayout(hbox7)
        self.vbox.addLayout(hbox8)
        self.vbox.addLayout(hbox9)
        self.vbox.addLayout(hbox10)
        self.vbox.addLayout(hbox11)
        self.setLayout(self.vbox)
        self.btOk.clicked.connect(self.yesEvent)
        self.btCl.clicked.connect(self.closeEvent)
        self.arrears.textEdited.connect(self.lineFocusIn)
        self.combo1.activated.connect(self.dirLink)
        self.Paymethod.textEdited.connect(self.payFocusIn)
        
    def payFocusIn(self):
        if self.Paymethod.text() == "1":
            self.Paymethod.setText("支付宝全款")
        if self.Paymethod.text() == "2":
            self.Paymethod.setText("微信全款")
        if self.Paymethod.text() == "3":
            self.Paymethod.setText("现金全款")
        
    def initCommission(self, com, data=("", "", "", "", "", "")):
        print(com)
        self.id = data[0]
        self.date, hbox1 = self.getDate(data[1])
        self.name, hbox2 = self.getLine("客户姓名",data[2])
        self.ser_bo, hbox3 = self.getCombo(com[0], "服务项目",data[3])
        self.total, hbox4 = self.getLine("手工提成", str(data[4]))
        self.adviser, hbox5 = self.getCombo(com[1], "美容师  ",data[5])
        hbox6 = self.getButton()
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(hbox4)
        self.vbox.addLayout(hbox5)
        self.vbox.addLayout(hbox6)
        self.setLayout(self.vbox)
        self.btOk.clicked.connect(self.yesEvent)
        self.btCl.clicked.connect(self.closeEvent)
    
    def initCommon(self,data=()):
        if len(data) <=0:
            return
        self.common, hbox1 = self.getCombo(data, "选择需要删除的项目")
        self.com_name, hbox2 = self.getLine("需要添加项目的名称")
        hbox3 = self.getButton()
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.setLayout(self.vbox)
        self.btOk.clicked.connect(self.yesEvent)
        self.btCl.clicked.connect(self.closeEvent)
    
    def initLink(self, data):
        if len(data) <=0:
            return
        self.common1, hbox1 = self.getCombo(data[0], "产  品  ")
        self.common2, hbox2 = self.getCombo(data[1], "购买选卡")
        hbox3 = self.getButton()
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.setLayout(self.vbox)
        self.btOk.clicked.connect(self.yesEvent)
        self.btCl.clicked.connect(self.closeEvent)
        
    def getMessage(self):
        if self.table_name == "BUSINESS":
            data = (self.id, self.date.text(), self.name.text(), self.combo1.currentText(), 
                    self.combo2.currentText(), self.total.text(), self.actpay.text(), 
                    self.arrears.text(), self.Paymethod.text(), self.adviser.currentText(), 
                    self.commission.currentText())
        elif self.table_name == "COMMISSION":
            data = (self.id, self.date.text(), self.name.text(), self.ser_bo.currentText(), 
                    self.total.text(), self.adviser.currentText())
        elif self.table_name == "link":
            if not self.common1.currentIndex() or not self.common2.currentIndex():
                data = (False,)
            else :
                data = (self.common1.currentText(), self.common2.currentText())
        else:
            data = (False if not self.common.currentIndex() else True, self.common.currentText(), 
                    False if self.com_name.text() == "" else True, self.com_name.text())
        return data
    
    def dirLink(self):
        try:
            for i in range(self.combo2.count()):
                if self.link_dir[self.combo1.currentText()] == self.combo2.itemText(i):
                    self.combo2.setCurrentIndex(i)
                    return
        except:
            return
    
    def yesEvent(self):
        self.my_signal.emit(True, self.crol_data)
        return True
    
    def closeEvent(self, event):
        self.my_signal.emit(False, self.crol_data) 
    
    def getDate(self, m=''):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("日期    "))
        date = QDateEdit(QDate.currentDate())
        date.setDisplayFormat('yyyy-MM-dd')
        if len(m) > 0:
            date.setDate(QDate.fromString(m, "yyyy-MM-dd"))
        date.setCalendarPopup(True)
        hbox.addWidget(date)
        hbox.addStretch()
        return date, hbox
    
    def getText(self, name, m=''):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(name))
        text = QTextEdit()
        if len(m) > 0:
            text.setText(m)
        hbox.addWidget(text)
        return text, hbox
        
    def getLine(self, name, m=''):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(name))
        line = QLineEdit()
        if len(m) > 0:
            line.setText(m)
        hbox.addWidget(line)
        return line, hbox
    
    def getCombo(self, data, name,m=''):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(name))
        combo= QComboBox()
        for d in data:
            combo.addItem(d)
        if len(m) > 0:
            combo.setCurrentIndex(list(data).index(m))
        hbox.addWidget(combo)
        hbox.addStretch()
        return combo, hbox
    
    def getButton(self):
        hbox = QHBoxLayout()
        self.btOk = QPushButton("确认")
        self.btCl = QPushButton("取消")
        hbox.addWidget(self.btOk)
        hbox.addStretch()
        hbox.addWidget(self.btCl)
        return hbox
    
    def lineFocusIn(self):
        self.arrears.setText("%d"%((int(self.total.text()) - int(self.actpay.text()))))
        
    def run(self):
        self.show()
