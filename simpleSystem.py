# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 23:27:15 2020

@author: 皮卡丘
"""
import tkinter
from tkinter.constants import *
import sys
import os,shutil
import getopt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QDate
from dBase import *
from myDialog import *
import datetime
import csv


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("管理系统")
        self.setFont(QFont("宋体",15 ,5 ))
        self.__db = DBase()                     #连接数据库
        self.common = ""
        self.save_status = True
        self.link_dir = {}
        self.initUi()
        self.initDir()
        self.table_name = "BUSINESS" if self.table_combo.currentIndex() == 0 else "COMMISSION"
        self.addStaff_bt.clicked.connect(self.addStaff)
        self.delStaff_bt.clicked.connect(self.delStaff)
        self.add_button.clicked.connect(self.addButton) 
        self.mod_button.clicked.connect(self.modButton)
        self.del_button.clicked.connect(self.delButton)
        self.pro_button.clicked.connect(self.ProButton)
        self.sev_button.clicked.connect(self.SevButton)
        self.buy_button.clicked.connect(self.BuyButton)
        self.link_button.clicked.connect(self.linkButton)
        self.date.dateChanged.connect(self.DateButton)
        self.recall_bt.clicked.connect(self.backEvent)
        self.dload_button.clicked.connect(self.downEvent)
        self.staff_combo.activated.connect(self.staffComBoBox)
        self.ser_button.clicked.connect(self.SearchButton)
        self.save_bt.clicked.connect(self.saveEvent)
        self.table_combo.activated.connect(self.flushTableWidget)
        
    def initUi(self):
        self.setGeometry(300, 200, 1000, 800)  
        self.__mainLayout=QVBoxLayout()
        self.setLayout(self.__mainLayout)
        self.initStatistics()
        self.initCommission()
        self.initTable()
        self.initTail()
        self.show()
        
    def initStatistics(self):
        hbox1 = QHBoxLayout()
        self.total_day = QLabel(self)
        self.actpay_day = QLabel(self)
        self.arrears_day = QLabel(self)
        hbox1.addWidget(self.total_day)
        hbox1.addWidget(self.actpay_day)
        hbox1.addWidget(self.arrears_day)
        hbox2 = QHBoxLayout()
        self.total_mon = QLabel(self)
        self.actpay_mon = QLabel(self)
        self.arrears_mon = QLabel(self)
        hbox2.addWidget(self.total_mon)
        hbox2.addWidget(self.actpay_mon)
        hbox2.addWidget(self.arrears_mon)
        self.__mainLayout.addLayout(hbox1)
        self.__mainLayout.addLayout(hbox2)
        self.flushStatistics()
        
    def flushStatistics(self):
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m-%d'), "TOTAL")
        self.total_day.setText("今日总额：%s"%count[0])
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m-%d'), "ACTPAYMENT")
        self.actpay_day.setText("今日实付总额：%s"%count[0])
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m-%d'), "arrears")
        self.arrears_day.setText("今日欠款总额：%s"%count[0])
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m'), "TOTAL")
        self.total_mon.setText("本月总额：%s"%count[0])
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m'), "ACTPAYMENT")
        self.actpay_mon.setText("本月实付总额：%s"%count[0])
        e, count = self.__db.countDBaseByMon("BUSINESS", datetime.datetime.now().strftime('%Y-%m'), "arrears")
        self.arrears_mon.setText("本月欠款总额：%s"%count[0])
    
    def initCommission(self):
        hbox = QHBoxLayout()
        self.staff_combo=QComboBox(self)
        self.initStaffCombo()
        self.addStaff_bt=QPushButton("添加员工")
        self.delStaff_bt=QPushButton("删除员工")
        self.staff_com=QLabel(self)
        self.staffComBoBox()
        hbox.addWidget(self.staff_combo)
        hbox.addWidget(self.staff_com)
        hbox.addStretch()
        hbox.addWidget(self.addStaff_bt)
        hbox.addWidget(self.delStaff_bt)
        self.__mainLayout.addLayout(hbox)
        
    def initTable(self):    
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        self.table_combo=QComboBox(self)
        self.table_combo.addItem("营业表")
        self.table_combo.addItem("提成表")
        self.date = QDateEdit(QDate.currentDate(), self)
        self.date.setDisplayFormat('yyyy-MM-dd')
        self.date.setCalendarPopup(True)
        self.name_text = QLineEdit(self)
        self.name_text.setFont(QFont('黑体',15))
        self.name_text.setPlaceholderText("姓名或者日期")
        self.ser_button = QPushButton("查找", self)
        self.pro_button = QPushButton("产    品", self)
        self.sev_button = QPushButton("服    务", self)
        self.buy_button = QPushButton("购买卡项", self)
        self.add_button = QPushButton("添加营业", self)
        self.mod_button = QPushButton("修改营业", self)
        self.del_button = QPushButton("删除营业", self)
        self.initTableWidget()
        hbox1.addWidget(self.table_combo)
        hbox1.addWidget(self.date)
        hbox1.addStretch(1)
        hbox2.addWidget(self.name_text)
        hbox2.addWidget(self.ser_button)
        hbox2.addStretch(1)
        hbox1.addWidget(self.pro_button)
        hbox1.addWidget(self.sev_button)
        hbox1.addWidget(self.buy_button)
        hbox2.addWidget(self.add_button)
        hbox2.addWidget(self.mod_button)
        hbox2.addWidget(self.del_button)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.table_widget)
        self.__mainLayout.addLayout(vbox)
    
    def initTail(self):
        hbox = QHBoxLayout(self)
        self.dload_button = QPushButton("下载", self)
        self.link_button = QPushButton("产品关联", self)
        self.recall_bt=QPushButton("撤销")
        self.save_bt=QPushButton("保存")
        label = QLabel()
        label.setFont(QFont("宋体",10))
        label.setStyleSheet("color:red")
        label.setText("保存后将无法撤销")
        hbox.addWidget(self.dload_button)
        hbox.addWidget(self.link_button)
        hbox.addStretch(1)
        hbox.addWidget(label)
        hbox.addWidget(self.recall_bt)
        hbox.addWidget(self.save_bt)
        self.__mainLayout.addLayout(hbox)
    
    
    def initDir(self):
        try:
            fp = open("dir.db", "r", newline = "")
        except:
            fp = open("dir.db", "w", newline = "")
            return
        lines = fp.read()
        fp.close()
        try:
            words = lines.split(' ')
            for i in range(len(words)-1):
                 if i % 2:
                     continue
                 self.link_dir[words[i]] = words[i+1]
                
        except BaseException as e:
            print(e)
            return
    
    def initStaffCombo(self):
        self.staff_combo.clear()
        self.staff_combo.addItem("选择查看")
        rows = self.__db.selectDBase("ADVISER")
        #print(rows)
        for row in rows:
            if row[2] == "1":
                self.staff_combo.addItem(row[1])
    
    def addStaff(self):
        staff_name, ok = QInputDialog.getText(self, "员工姓名", "输入姓名:", QLineEdit.Normal)
        data = [staff_name, "1"]
        if len(staff_name) > 0 and ok:
            var = self.__db.insertDBase(data, "ADVISER")
            if var:
                QMessageBox.information(self, "提示框", "输入成功", QMessageBox.Ok)
                self.initStaffCombo()   
            else:
                QMessageBox.warning(self, "提示框", "输入失败: %s"%var, QMessageBox.Ok)
        self.save_status = False
            
                
    def delStaff(self):
        staff_name, ok = QInputDialog.getText(self, "员工姓名", "输入姓名",  QLineEdit.Normal)
        data = ['status', '0', 'name', staff_name]
        if len(staff_name) > 0 and ok:
            var = self.__db.updateDBase(data, "ADVISER")
            if var == 1:
                QMessageBox.information(self, "提示框", "删除成功", QMessageBox.Ok)
                self.initStaffCombo()
            else:
                QMessageBox.warning(self, "提示框", "删除失败: %s"%var, QMessageBox.Ok)
        self.save_status = False
            
    # def initTableCombo(self):
        
    def initTableWidget(self):
        rows = self.__db.selectDBase("BUSINESS")
        if(len(rows) > 0):
            self.table_widget=QTableWidget(len(rows),len(rows[0]))
        else:
            self.table_widget=QTableWidget(0,0)
        self.flushTableWidget()
        
    def flushTableWidget(self, index = 0, dateType = datetime.datetime.now().strftime('%Y-%m')):
        if not self.table_combo.currentIndex():
            self.add_button.setText("添加营业")
            self.mod_button.setText("修改营业")
            self.del_button.setText("删除营业")
        if self.table_combo.currentIndex():
            self.add_button.setText("添加提成")
            self.mod_button.setText("修改提成")
            self.del_button.setText("删除提成")
        self.table_name = "BUSINESS" if self.table_combo.currentIndex() == 0 else "COMMISSION"
        b, rows = self.__db.selectDBaseByDate(self.table_name, dateType)
        # print(rows)
        if not b:
            QMessageBox.warning(self,"提示框","提示：%s"%rows,QMessageBox().Ok)
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(0)
        if(len(rows) > 0):
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(rows[0]))
            if self.table_name == "BUSINESS":
                self.table_widget.setHorizontalHeaderLabels(["序列号", "日期","客户姓名","购买产品","购买卡项", "购买总额", "实付金额", "欠款金额", "支付方式", "美容顾问", "是否发放提成"])
            else:
                self.table_widget.setHorizontalHeaderLabels(['序列号', "日期", "客户姓名", "服务项目", "手工提成", "美容师"])
            i = 0
            for row in rows:
                for j in range(len(row)):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(row[j])))
                    j = j + 1
                i = i + 1
            
    def addButton(self):
        print(self.link_dir)
        self.mydialog = MyDialog(self.table_name, "add", self.link_dir)
        p1 = self.getProduct()
        p2 = self.getProtype()
        s = self.getService()
        a = self.getAdviser()
        if self.table_name == "BUSINESS":
            self.mydialog.initBussiness((p1,p2,a))
        elif self.table_name == "COMMISSION":
            self.mydialog.initCommission((s, a))
        else:
            return
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
            
    def modButton(self):
        num, ok = QInputDialog.getText(self, "修改", "输入序列号:", QLineEdit.Normal)
        if not ok or len(num) < 0:
            return
        self.mydialog = MyDialog(self.table_name, "mod", self.link_dir)
        var, data = self.__db.selectDBase2(self.table_name, num)
        if not var:
            QMessageBox.warning(self,"提示框","%s"%e,QMessageBox().Ok)
            return
        # print(data[0])
        p1 = self.getProduct()
        p2 = self.getProtype()
        s = self.getService()
        a = self.getAdviser()
        if self.table_name == "BUSINESS":
            self.mydialog.initBussiness((p1,p2,a), data[0])
        elif self.table_name == "COMMISSION":
            self.mydialog.initCommission((s, a), data[0])
        else:
            return
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
        
    def delButton(self):
        num, ok = QInputDialog.getText(self, "删除", "输入序列号:", QLineEdit.Normal)
        if not ok or len(num) < 0:
            return
        var, name = self.__db.selectName(self.table_name, num)
        if not var:
            QMessageBox.warning(self,"提示框","提示：%s"%name,QMessageBox().Ok)
            return
        ok = QMessageBox.warning(self,"提示框","是否删除\n姓名：%s"%name[0],QMessageBox().Ok, QMessageBox().Cancel)
        if ok != 0x400:
            return
        e = self.__db.deleteDBase(num, self.table_name)
        if e:
            QMessageBox.information(self, "提示框", "删除成功", QMessageBox.Ok)
            self.flushTableWidget()
        else:
            QMessageBox.warning(self,"提示框","提示：%s"%e,QMessageBox().Ok)
        self.flushTableWidget()
        self.flushStatistics()
        self.save_status = False
        
    def DateButton(self):
        self.flushTableWidget(True, self.date.text())
    
    def SearchButton(self):
        b, rows = self.__db.searchDBase(self.table_name, self.name_text.text())
        if not b:
            QMessageBox.warning(self,"提示框","提示：%s"%rows,QMessageBox().Ok)
            return
        self.table_widget.clear()
        if(len(rows) > 0):
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(rows[0]))
            if self.table_name == "BUSINESS":
                self.table_widget.setHorizontalHeaderLabels(["序列号", "日期","客户姓名","购买产品","购买卡项", "购买总额", "实付金额", "欠款金额", "支付方式", "美容顾问", "是否发放提成"])
            else:
                self.table_widget.setHorizontalHeaderLabels(['序列号', "日期", "客户姓名", "服务项目", "手工提成", "美容师"])
            i = 0
            for row in rows:
                for j in range(len(row)):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(row[j])))
                    j = j + 1
                i = i + 1
        
    def ProButton(self):
        self.common = "PRODUCT"
        e, rows = self.__db.selectName2(self.common)
        r = ("不需要删除可以不选", )
        if not e:
            QMessageBox.warning(self,"提示框","提示：%s\n没有记录"%rows,QMessageBox().Ok)
        else:
            for row in rows:
                r = r + row
        self.mydialog = MyDialog("产品", "ach")
        self.mydialog.initCommon(r)
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
    
    def SevButton(self):
        self.common = "SERVICE"
        e, rows = self.__db.selectName2(self.common)
        r = ("不需要删除可以不选", )
        if not e:
            QMessageBox.warning(self,"提示框","提示：%s\n没有记录"%rows,QMessageBox().Ok)
        else:
            for row in rows:
                r = r + row
        self.mydialog = MyDialog("服务", "ach")
        self.mydialog.initCommon(r)
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
        
    def BuyButton(self):
        self.common = "PROTYPE"
        e, rows = self.__db.selectName2(self.common)
        r = ("不需要删除可以不选", )
        if not e:
            QMessageBox.warning(self,"提示框","提示：%s\n没有记录"%rows,QMessageBox().Ok)
        else:
            for row in rows:
                r = r + row
        self.mydialog = MyDialog("购买卡选", "ach")
        self.mydialog.initCommon(r)
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
    
    def staffComBoBox(self):
        e, count = self.__db.countDBaseByName("COMMISSION", datetime.datetime.now().strftime('%Y-%m'), "PRICE", self.staff_combo.currentText())
        #e, count2 = self.__db.countDBaseByName2(datetime.datetime.now().strftime('%Y-%m'), self.staff_combo.currentText())
        self.staff_com.setText("这个月提成费 ：%s"%(count[0][0]))
    
    def linkButton(self):
        self.common = "link"
        p1 = self.getProduct()
        p2 = self.getProtype()
        p1 = ("点击选择产品    ",) + p1
        p2 = ("点击选择选购卡项",) + p2 
        self.mydialog = MyDialog("link", "link")
        self.mydialog.initLink((p1,p2))
        self.mydialog.run()
        self.mydialog.my_signal.connect(self.dialogClose)
        
    def getProduct(self):
        e, rows = self.__db.selectName2("PRODUCT")
        t = ()
        try:
            for row in rows:
                t = t + row
        except:
            return t
        return t
    
    def getProtype(self):
        e, rows = self.__db.selectName2("PROTYPE")
        t = ()
        try:
            for row in rows:
                t = t + row
        except:
            return t
        return t
    
    def getService(self):
        e, rows = self.__db.selectName2("SERVICE")
        t = ()
        try:
            for row in rows:
                t = t + row
        except:
            return t
        return t
    
    def getAdviser(self):
        e, rows = self.__db.selectName3("ADVISER")
        t = ()
        try:
            for row in rows:
                t = t + row
        except:
            return t
        return t
    
    def dialogClose(self, b, d):
        if(b):
            data = self.mydialog.getMessage()
            # print(data)
            if(d[1] == "add"):
                e = self.__db.insertDBase(data[1:], self.table_name)
            elif d[1] == "mod":
                e = self.__db.updateDBase(data, self.table_name)
            elif d[1] == "ach":
                e = "none"
                if data[0]:
                    e = self.__db.deleteDBaseByName(data[1], self.common)
                if data[2]:
                    e = self.__db.insertDBase(data[3], self.common)
            elif d[1] == "link":
                if not data[0]:
                    e = "选择有错"
                else:
                    self.link_dir[data[0]] = data[1]
                    e = True
            if e != True:
                QMessageBox.warning(self,"提示框","提示：%s"%e,QMessageBox().Ok)
            else:
                self.flushTableWidget()
                self.flushStatistics()
                self.save_status = False
        self.mydialog.close()
        
    def saveEvent(self):
        self.__db.sabeDBase()
        self.saveDir()
        self.backups()
        QMessageBox.information(self, "提示框", "保存成功", QMessageBox.Ok)
        self.save_status = True
    
    def backEvent(self):
        self.__db.backDBase()
        self.flushStatistics()
        self.flushTableWidget()
        self.initStaffCombo()
        QMessageBox.information(self, "提示框", "已撤销", QMessageBox.Ok)
    
    def downEvent(self, f, path = "./下载文件", date = datetime.datetime.now().strftime('%Y-%m')):
        num = 0
        if not os.path.exists(path):
            os.mkdir(path)
        file = date + "营业表.csv"
        e, rows = self.__db.selectDBaseByDate("BUSINESS",date)
        if e:
            print(path, date)
            p = os.path.join(path,file)
            csv_writer = open(p,'w',newline = "")
            w = csv.writer(csv_writer)
            w.writerow(["日期", "客户姓名", "产品", "购买卡选", "购买总额", "实付金额", "欠款金额", "支付方式", "美容顾问", "是否发放提成"])
            for row in rows:
                num= num +1
                w.writerow([row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]])
            csv_writer.close()
            file = date + "提成表.csv"
            e, rows = self.__db.selectDBaseByDate("COMMISSION",date)
            p = os.path.join(path,file)
            print(rows)
            csv_writer = open(p,'w',newline = "")
            w = csv.writer(csv_writer)
            w.writerow(["日期", "客户姓名", "服务项目", "手工提成", "美容顾问"])
            for row in rows:
                num= num +1
                w.writerow([row[1], row[2], row[3], row[4], row[5]])
            csv_writer.close()
            QMessageBox.information(self, "提示框", "已下载\n下载数据数：%s"%num, QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "提示框", "%s"%rows, QMessageBox.Ok)
    
    def backups(self):
        path = "./backups"
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.copyfile('business.db','./backups/business.db')
        shutil.copyfile('dir.db','./backups/dir.db')
        date = datetime.datetime.now().strftime('%d')
        print(date)
        if date == "01":
            date = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%Y-%m')
            print(date)
            self.downEvent(True, path, date)
            
    
    def saveDir(self):
        fp = open("dir.db", "w")
        for name in self.link_dir:
            fp.write("%s %s "%(name,self.link_dir[name]))
        fp.close()
    
    def closeEvent(self, event):
        if not self.save_status:
            ok = QMessageBox.warning(self, "提示框", "还没有保存!!!!!\n\n是否保存", QMessageBox.Ok, QMessageBox.Cancel)
            if ok == 0x400:
                self.saveEvent()
        self.__db.disConn()
  
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = MainWindow()
    sys.exit(app.exec_())

    
    
    
    