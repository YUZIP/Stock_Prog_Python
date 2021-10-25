'''
計算瘸定選擇個股的方法
架構上Method , Decision , Identify 三個差不多
del 方法
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/delete.html

'''
import Get_Stock_Data_Save_Load as st_data
import numpy as np

from time import time as clock

Method_Name = ['習慣演算','KD']
Method_Format = [[0,0,0,0],
                 [0,0,0,0,0]
                ]
def Index_Method_Name(name = ''):
    return Method_Format[Method_Name.index(name)]

class Method():
    global Method_Name

    def __init__(self):
        self.Paramater = []
        self.Result = []
        self.BuySell = []

    def __delete__(self, instance):
        del self.Paramater
        del self.Result
        del self.BuySell


    def Basic_Cal(self):
        pass

    def Method_Cal(self,paramater,data):
        self.Paramater = paramater[1]
        #print("Datas",data)
        self.Result = []
        self.BuySell = []
        start = clock()

        if self.Paramater[0] == Method_Name[0]:  # '習慣演算'
            def Cal_rep(Paramater,a,j):#data , ScoreDay
                    return (a * Paramater + j) / (Paramater + 1)

            vfunc = np.vectorize(Cal_rep)
            for i,t in zip(data,st_data.List_1d_Score_Data): #開始針對每個股票做購買決策

                self.SerialData=[]
                self.bbss = []
                #print("in Desicion Everyday length",len(i))
                a = i[0]
                b = i[0]
                for j,k in zip(i,t): #每一天
                    a = (a * self.Paramater[1][0] + j) / (self.Paramater[1][0] + 1)
                    b = (b * self.Paramater[1][1] + j) / (self.Paramater[1][1] + 1)
                    if (a-b) > self.Paramater[1][2]:
                        self.SerialData.append(k)
                        self.bbss.append("購")
                    elif (a-b) < self.Paramater[1][3]:
                        self.SerialData.append((1-k)+1)
                        self.bbss.append("售")
                    else:
                        self.SerialData.append(1)
                        self.bbss.append("平")
                '''
                self.SerialData=[]
                self.bbss = []
                #print("in Desicion Everyday length",len(i))
                a = i[0]
                b = i[0]
                for j,k in zip(i,t): #每一天
                    a = vfunc(self.Paramater[1][0],a,j)
                    #a = (a * self.Paramater[1][0] + j) / (self.Paramater[1][0] + 1)
                    b = vfunc(self.Paramater[1][1],b,j)
                    #b = (b * self.Paramater[1][1] + j) / (self.Paramater[1][1] + 1)
                    if (a-b) > self.Paramater[1][2]:
                        self.SerialData.append(k)
                        self.bbss.append("購")
                    elif (a-b) < self.Paramater[1][3]:
                        self.SerialData.append((1-k)+1)
                        self.bbss.append("售")
                    else:
                        self.SerialData.append(1)
                        self.bbss.append("平")
                '''
                self.Result.append(self.SerialData)
                self.BuySell.append(self.bbss)

                #print("desision_Result")
                #print(self.SerialData)
            #print('Get_Average Score',self.Method_Cal_By_Stock())
            end = clock()
            #print("Decision Time cost",end-start)
            return self.Result


        if self.Paramater[0] == Method_Name[1]:  # 'KD'
            pass


    def Method_Cal_By_Stock(self):
        datas = st_data.Stock_Data
        counts = 0
        cores = 0
        for i,j in zip(datas,self.Result):
            aa = i['Close']
            bb = aa.shift(-1)
            bb.fillna(method='pad', inplace=True)
            cc = bb / aa #ratio
            counts +=1

            mainScore = 1
            for k in zip(cc,j):
                if k[1] != 0:
                    mainScore *= k[0]*k[1]
            cores += mainScore
        cores /= counts
        return cores





