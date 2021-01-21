# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 20:48:08 2020

@author: 皮卡丘
"""


import sqlite3

class DBase:
    def __init__(self):
        self.__conn = sqlite3.connect('business.db')
        self.cursor = self.__conn.cursor()
        self.__initTable()
    
    def __initTable(self):
        # 创建营业表
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BUSINESS
            (ID          INTEGER         PRIMARY KEY autoincrement,
            date         date           NOT NULL,
            NAME         CHAR(20)       NOT NULL,
            PRODUCT      CHAR(50)       NOT NULL,
            PRODUCT_TYPE CHAR(50)       NOT NULL,
            TOTAL        MONEY          NOT NULL,
            ACTPAYMENT   MONEY          NOT NULL,
            arrears      MONEY          NOT NULL,
            Paymethod    CHAR(50)       NOT NULL,
            adviser      CHAR(50)               ,
            Commission   CHAR(20)        
            );
            ''')
        except:
            return -1
        # 创建员工表
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ADVISER
            (ID          INTEGER         PRIMARY KEY autoincrement,
            NAME         CHAR(20)       NOT NULL,
            STATUS       CHAR(1)        NOT NULL
            );
            ''')
        except:
            return -2
        # 创建产品表
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PRODUCT
            (
            name      CHAR(50)        PRIMARY KEY
            );
            ''')
        except BaseException as e:
            return e
         # 创建购买类型
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PROTYPE
            (
            name      CHAR(50)       PRIMARY KEY
            );
            ''')
        except:
            return -4
        # 提成表
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS COMMISSION
            (ID          INTEGER         PRIMARY KEY autoincrement,
            DATE         DATE            NOT NULL,
            NAME         CHAR(50)        NOT NULL,
            SERVICE      CHAR(50)        NOT NULL,
            PRICE        MONEY           NOT NULL,
            adviser      CHAR(50)        NOT NULL
            );
            ''')
        except:
            return -5
         # 创建服务类型
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SERVICE
            (
            name      CHAR(50)       PRIMARY KEY
            );
            ''')
        except:
            return -6
        self.cursor.fetchall()
        return 1
        
    def insertDBase(self, data, base):
        try:   
            if base == "ADVISER" and len(data) == 2:
                var = "insert into " + base + "(name, status) values ('%s', '%s');"%(data[0], data[1])
            elif base == "BUSINESS" and len(data) > 0:
                var = "insert into " + base + '''(date, NAME, PRODUCT, PRODUCT_TYPE, 
                TOTAL, ACTPAYMENT, arrears, Paymethod, adviser, Commission
                ) values ('%s', '%s', '%s', '%s', %d, %d, %d, '%s', '%s', '%s'
                );'''%(data[0], data[1], data[2], data[3], float(data[4]), float(data[5]), float(data[6]), data[7], data[8], data[9])
            elif base == "COMMISSION" and len(data) > 0:
                var = "insert into " + base + '''(DATE, NAME, SERVICE, PRICE, adviser) 
                VALUES ('%s','%s','%s',%d,'%s');'''%(data[0], data[1], data[2], float(data[3]), data[4])
            else :
                var = "insert into " + base + '''(name) values ('%s');'''%data
            print(var)
            self.cursor.execute(var)
            self.cursor.fetchall()
        except BaseException as e:
            return e
        except ValueError as ve:
            return ve
        return True
    
    def delDBase(self, data, base, mod):
        if mod == "num":
            var = "delete from %s where %s = %s"%(base, data[0], data[1])
        elif mod == "str":
            var = "delete from %s where %s = '%s'"%(base, data[0], data[1])
        try:
            self.cursor.execute(var)
            self.cursor.fetchall()
        except BaseException as e:
            print(e)
            
    def updateDBase(self, data, base):
        if base == "ADVISER":
            var = "UPDATE %s SET %s = %s WHERE %s = '%s';"%(base, data[0], data[1], data[2], data[3])
        elif base == "BUSINESS":
            var = '''UPDATE %s SET date = '%s', NAME = '%s', PRODUCT = '%s', PRODUCT_TYPE = '%s', 
                TOTAL = %d, ACTPAYMENT = %d, arrears = %d, Paymethod = '%s', adviser = '%s', 
                Commission = '%s' where id = %d;
                '''%(base, data[1], data[2], data[3], data[4], int(data[5]), int(data[6]), 
                int(data[7]), data[8], data[9], data[10], data[0])
        elif base == "COMMISSION":
            var = '''UPDATE %s SET DATE = '%s', NAME = '%s', SERVICE = '%s', PRICE = %d
            , NAME = '%s' where id = %d;'''%(base, data[1], data[2], data[3], int(data[4]), 
            data[5], data[0])
        try:
            # print(var)
            self.cursor.execute(var)
            self.cursor.fetchall()
            #print(self.cursor.rowcount)
            if self.cursor.rowcount == 0:
                raise BaseException("没有查到")
        except BaseException as e:
            return (e)
        return True
            
    def deleteDBase(self, data, base, col = "id"):
        var = "delete from %s where %s = %d;"%(base, col, int(data))
        try:
            self.cursor.execute(var)
            self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                raise BaseException("没有查到")
        except BaseException as e:
            return (e)
        return True
    
    def deleteDBaseByName(self, data, base):
        var = "delete from %s where name = '%s';"%(base, data)
        try:
            self.cursor.execute(var)
            self.cursor.fetchall()
            if self.cursor.rowcount == 0:
                raise BaseException("没有查到")
        except BaseException as e:
            return (e)
        return True
    
    def selectDBase(self, base):
        try:
            var = "select * from %s;"%base
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            return rows
        except BaseException as e:
            print(e)
        
    def selectDBase2(self,base,data):
        try:
            var = "select * from %s where ID = %d;"%(base,int(data))
            #print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            return True, rows
        except BaseException as e:
            return False, e
    
    def selectDBaseByDate(self,base,data):
        try:
            var = "select * from %s where date like '%s%%';"%(base,data)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            return True, rows
        except BaseException as e:
            return False, e
    
    def selectDBaseByDay(self,base,data):
        try:
            var = "select * from %s where date like '%s';"%(base,data)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            return True, rows
        except BaseException as e:
            return False, e
    
    def selectName(self,base,num):
        try:
            var = "select name from %s where ID = %d;"%(base, int(num))
            print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def selectName2(self, base):
        try:
            var = "select name from %s order by name ASC;"%(base)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def selectName3(self, base):
        try:
            var = "select name from %s where status = 1 order by name ASC;"%(base)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
        
    def searchDBase(self,base,data):
        try:
            var = "select * from %s where name = '%s' or date like '%%%s%%' or adviser = '%s';"%(base,data,data,data)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def countDBaseByMon(self, base, mon, data):
        try:
            var = "select sum(%s) from %s where date like '%%%s%%';"%(data, base, mon)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def countDBaseByName(self, base, mon, data, name):
        try:
            var = "select sum(%s) from %s where date like '%%%s%%' and adviser = '%s';"%(data, base, mon, name)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def countDBaseByName2(self, mon, name):
        try:
            var = '''select sum(c.price) from BUSINESS b join COMMISSION c on c.adviser = 
            b.adviser where c.date like '%%%s%%'
            and c.adviser = '%s' and b.Commission = '已发放';'''%(mon, name)
            # print(var)
            self.cursor.execute(var)
            rows = self.cursor.fetchall()
            if len(rows) == 0:
                raise BaseException("没有查到")
            return True, rows
        except BaseException as e:
            return False, e
    
    def showTables(self):
        self.cursor.execute("select name from sqlite_master where type='table' order by name")
        print(self.cursor.fetchall())
    
    def delTable(self, base):
        try:
            self.cursor.execute("drop table %s"%base)
            self.cursor.fetchall()
        except BaseException as e:
            print(e)
            
    def sabeDBase(self):
        self.__conn.commit()
    
    def backDBase(self):
        self.__conn.rollback()
    
    def disConn(self):
        self.cursor.close()
        self.__conn.close()
            