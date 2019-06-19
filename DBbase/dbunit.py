# coding=gbk
##############################################################
# FileName: dbunit.py
# Author: zanweb.zhan
# Version: 0.01
# History:
# <Author/Maintainer> <Date> <Modification>
# 2017/03/28 Create this file
#############################################################
import sys
# import ConfigParser
# import datetime

# import binascii
# import os
# import types
# import os
# import pdb
# from pymssql import connect
import pymssql
import time


class DBUnit:
    def __init__(self, user=None, passwd=None, host=None, database=None):
        try:
            self.connection = pymssql.connect(host=host, user=user, password=passwd, database=database, as_dict=True)
            self.cursor = self.connection.cursor()
        except:
            print("Could not connect to DataBase server.")
            exit(0)

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def read(self, sql, param=None):
        '''Exec select sql , return type is Tuple,use len fun return select row num
        use param like this:
        Sql=select * from table where param=%s and param1=%s
        param=(value1,valuei2)
        '''
        try:
            cursor = self.connection.cursor()
            if param is None:
                cursor.execute(sql)
                rs = cursor.fetchall()
                cursor.close()
            else:
                cursor.execute(sql, param)
                rs = cursor.fetchall()
                cursor.close()
        except Exception as e:
            print(e)
            rs = ()
        return rs

    def write(self, sql, param, iscommit=True):
        try:
            cursor = self.connection.cursor()
            # print(sql)
            n = cursor.executemany(sql, param)
            if iscommit:
                self.connection.commit()
            return n
        except Exception as e:
            print(e)
            self.connection.rollback()
            return -1

    def write_one_record(self, sql):
        try:
            cursor = self.connection.cursor()
            n = cursor.execute(sql)
            self.connection.commit()
            return int(cursor.lastrowid)
        except:
            self.connection.rollback()
            return -1


if __name__ == '__main__':
    a = time.time()
    # db = DBUnit('sa', 'zanweb5186', '127.0.0.1\zanwebsql', 'MFGMISCSSQL')
    # db = DBUnit('zyq', 'zyq123', 'stlsojsvr04', 'MFGMISCSSQL')  # 不使用默认端口
    # rs = db.read("SELECT * FROM tblPlan")
    db = DBUnit('zyq', 'zyq123', 'zanweb\STLSOJSVR04', 'DFactory')  # 不使用默认端口
    # db = DBUnit('zyq', 'zyq123', 'stlsojsvr04', 'DFactory')  # 不使用默认端口

    rs = db.read("SELECT * FROM [OracleData]")

    for row in rs:
        print(row)
