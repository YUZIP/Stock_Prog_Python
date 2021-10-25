
'''
主要為各股的計算每個取縣。

del 方法
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/delete.html
架構上Method , Decision , Identify 三個差不多

Method_Name = 最主要的名稱
Method_Format = 股要的變數的樣式跟數量
這個部份其他Cal系列應該都差不多
'''

import os

import Get_Stock_Data_Save_Load as st_data
from time import time as clock
from numba import jit
import numpy
import ctypes
from ctypes import *
#定義功能名稱，並且制定該功能所要的參數長度...因為有使用dll，所以所有資料必須為double寫法
Method_Name = ['各點加權(5日)','習慣演算','習慣演算差','習慣微灌'] # '習慣微灌 = dll方式運算'
#第一個是使用在基本資料處理，第二個才是演算法要用的主體資料
Method_Format = [[[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0]],
                 [[0.0,0.0,0.0,0.0,0.0,0.0],[0.0]],
                 [[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0]],
                 [[0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0]]
                ]

def Index_Method_Name(name = ''):
    #輸入演算法的名稱後，會回應所需的參數格是
    return Method_Format[Method_Name.index(name)]

class Method():
    global Method_Name
    def __init__(self):
        self.Paramater = []
        self.Data = []
        self.Result = []
        self.tempCal = []
        #self.Serial_Datas = []
        ll = ctypes.CDLL  # cdll.LoadLibrary
        self.dll = ll(os.path.join(os.getcwd(), 'Method_V01.dll'))

    def __delete__(self, instance):
        #避免資料殺不乾淨，所以在這又殺一遍
        del self.Paramater
        del self.Data
        del self.Result
        del self.tempCal
        #del self.Serial_Datas

    def Basic_Cal(self):
        #處理基本資料，決定六個數值比重後合成新的資料
        datas = st_data.Stock_Data
        self.Data = []
        for i in datas:
            #print("Data in Oneopt Basic", i)
            #for j in range(len(self.Paramater[1][0])):
            aa = i['Open'] * self.Paramater[1][0][0]
            aa += i['High'] * self.Paramater[1][0][1]
            aa += i['Low'] * self.Paramater[1][0][2]
            aa += i['Close'] * self.Paramater[1][0][3]
            aa += i['Adj Close'] * self.Paramater[1][0][4]
            aa += i['Volume'] * self.Paramater[1][0][5]

            bb = aa.shift(-1)
            bb.fillna(method='pad', inplace=True)
            cc = bb/aa

            #print("Data in Oneopt Basic", cc)
            self.Data.append(cc)

    
    def Method_Cal(self,paramater):

        #第一層先將基本資料作處理
        start = clock()
        self.Paramater = paramater[0]
        self.Basic_Cal()
        self.Result = []
        self.Serial_Datas = []


        if self.Paramater[0] == Method_Name[0]:  # '各點加權(5日)n'
            for i in self.Data:
                #print("eachData",i)

                self.Serial_Datas = []

                reverse_Value = i[0]

                self.Serial_Datas = i/i
                for j in range(len(self.Paramater[1][1])):
                    aa = i.shift(j)
                    aa.fillna(value=reverse_Value, inplace=True)
                    self.Serial_Datas = self.Serial_Datas * aa * self.Paramater[1][1][j]
                #print("eachData", len(self.Serial_Datas))
                self.Result.append(self.Serial_Datas)
            #print("All Result",self.Result)
            end = clock()
            print("Theorem Time cost", end - start)
            return self.Result
        if self.Paramater[0] == Method_Name[1]:  # '習慣演算'
            for i in self.Data:
                self.Serial_Datas = []
                reverse_Value = i[0]
                for j in i:
                    reverse_Value = (reverse_Value * self.Paramater[1][1][0] + j) / (self.Paramater[1][1][0] +1)
                    self.Serial_Datas.append(reverse_Value)
                #print("Theorem", self.Serial_Datas)
                self.Result.append(self.Serial_Datas)
            end = clock()

            print("Theorem Time cost", end - start)
            #print ("Theorem",self.Result)
            return self.Result

        if self.Paramater[0] == Method_Name[2]:  # '習慣演算差'


            def cal_2(i,p1,p2):
                reverse_Value = 1
                reverse_Value_b = 1
                res = []
                for j in i:
                    reverse_Value = (reverse_Value * p1 + j) / (p1 + 1)
                    reverse_Value_b = (reverse_Value_b * p2 + j) / (p2 + 1)
                    res.append(reverse_Value-reverse_Value_b)
                return res
            '''
            @jit
            def cals(a1,b1,m1,a2,b2,m2):
                return ((a1*m1 + b1)/(m1+1)),((a2*m2 + b2)/(m2+1)) ,(((a2*m2 + b2)/(m2+1)) - ((a1*m1 + b1)/(m1+1)))
            '''
            for i in self.Data:
                aa = numpy.array(i)
                self.Serial_Datas = cal_2(aa,self.Paramater[1][1][0],self.Paramater[1][1][1])
                self.Result.append(self.Serial_Datas)
                '''
                self.Serial_Datas = []
                reverse_Value = i[0]
                reverse_Value_b = i[0]
                for j in i:
                   
                    reverse_Value = (reverse_Value * self.Paramater[1][1][0] + j) / (self.Paramater[1][1][0] +1)
                    reverse_Value_b = (reverse_Value_b * self.Paramater[1][1][1] + j) / (self.Paramater[1][1][1] + 1)
                    self.Serial_Datas.append(reverse_Value-reverse_Value_b)
                    
                    reverse_Value,reverse_Value_b,c = cals(reverse_Value,j,self.Paramater[1][1][0],reverse_Value_b,j,self.Paramater[1][1][1])
                    self.Serial_Datas.append(c)
                '''
                #print("Theorem", self.Serial_Datas)
                #self.Result.append(self.Serial_Datas)

            end = clock()

            print("Theorem Time cost", end - start)
            #print ("Theorem",self.Result)
            return self.Result

        if self.Paramater[0] == Method_Name[3]:  # '習慣微灌 = dll方式運算'

            def cal_2(i, p1, p2):
                reverse_Value = 1
                reverse_Value_b = 1
                res = []
                for j in i:
                    reverse_Value = (reverse_Value * p1 + j) / (p1 + 1)
                    reverse_Value_b = (reverse_Value_b * p2 + j) / (p2 + 1)
                    res.append(reverse_Value - reverse_Value_b)
                return res

            '''
            @jit
            def cals(a1,b1,m1,a2,b2,m2):
                return ((a1*m1 + b1)/(m1+1)),((a2*m2 + b2)/(m2+1)) ,(((a2*m2 + b2)/(m2+1)) - ((a1*m1 + b1)/(m1+1)))
            '''
            meths = self.dll.method_03
            meths.argtypes = [POINTER(c_double), c_uint, POINTER(c_double), POINTER(c_double)]
            meths.restype = None

            for i in self.Data:
                aa = numpy.array(i)
                bb = aa.copy()
                pam = numpy.array(self.Paramater[1][1])

                dataPtr = aa.ctypes.data_as(POINTER(c_double))
                resdataPtr = bb.ctypes.data_as(POINTER(c_double))
                paramptr = pam.ctypes.data_as(POINTER(c_double))

                self.dll.method_03(dataPtr, aa.size, resdataPtr, paramptr)

                self.Serial_Datas = bb  #cal_2(aa, self.Paramater[1][1][0], self.Paramater[1][1][1])
                self.Result.append(self.Serial_Datas)
                '''
                self.Serial_Datas = []
                reverse_Value = i[0]
                reverse_Value_b = i[0]
                for j in i:

                    reverse_Value = (reverse_Value * self.Paramater[1][1][0] + j) / (self.Paramater[1][1][0] +1)
                    reverse_Value_b = (reverse_Value_b * self.Paramater[1][1][1] + j) / (self.Paramater[1][1][1] + 1)
                    self.Serial_Datas.append(reverse_Value-reverse_Value_b)

                    reverse_Value,reverse_Value_b,c = cals(reverse_Value,j,self.Paramater[1][1][0],reverse_Value_b,j,self.Paramater[1][1][1])
                    self.Serial_Datas.append(c)
                '''
                # print("Theorem", self.Serial_Datas)
                # self.Result.append(self.Serial_Datas)

            end = clock()

            print("Theorem Time cost", end - start)
            # print ("Theorem",self.Result)
            return self.Result


