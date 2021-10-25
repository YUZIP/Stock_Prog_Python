'''
這個函數裡面會有計算一次跟直接Thread一套性運算的的方式
'''
from threading import Thread
import random
from time import time as clock
import Get_Stock_Data_Save_Load as st_data

import json

import Cal_Stock_Theorem as theorem
import Cal_Stock_Decision as decision
import Cal_Stock_Identify as identify

# Result = [BaseScore,paramater]

import os
ContinueRuning = False
Base_opt_file = os.path.join(os.getcwd(),'Recipe')
if not os.path.exists(Base_opt_file):
    os.makedirs(Base_opt_file)


def Write_Optimize_Parameter_To_File(SetFileName,out): #將參數寫入檔案
    global Base_opt_file
    filepath = os.path.join(Base_opt_file,SetFileName)
    with open(filepath, 'w') as out_file:
        json.dump(out, out_file)

def Read_Optimize_Parameter_Form_File(ReadFileName): #將參數從檔案讀出
    global Base_opt_file
    filepath = os.path.join(Base_opt_file, ReadFileName)
    with open(filepath, 'r') as in_file:
        your_list = json.load(in_file)
    return your_list

def MakeNormalRanDom(param,alpha): #範圍內平均亂數
    if type(param).__name__ == 'list':
        param = [MakeNormalRanDom(i,alpha) for i in param]
        #print( "List is true")
        return param
    elif type(param).__name__ == 'str':
        return param
    else:
        #print("SScount", SScount)
        param = random.uniform( -1*alpha , alpha)
        return param

def MakeGaussianRandom(param,alpha): #具範圍的高斯亂數
    if type(param).__name__ == 'list':
        param = [MakeGaussianRandom(i,alpha) for i in param]
        #print( "List is true")
        return param
    elif type(param).__name__ == 'str':
        return param
    else:
        #print("SScount", SScount)
        param = random.gauss(mu=param, sigma=alpha)
        return param

class Opt_Cal_Onece(Thread): #只算一次的結果演算，會將產生比較詳細的演算結果
    def __init__(self,paramater = []):
        Thread.__init__(self)
        self.Paramater = paramater
        self.Throrem = theorem.Method()
        self.Decision = decision.Method()
        self.Identity = identify.Method()
        self.Result = []
        self.Cal_Datas = []
        self.Cal_History = []
        self.Rank = []
        self.BuySell = []
        self.isRunning =True
        self.Final_Score = []
        self.start()



    def __del__(self):
        del self.Paramater
        del self.Throrem
        del self.Decision
        del self.Identity
        del self.Result
        del self.Cal_Datas
        del self.Rank
        del self.BuySell
        del self.Cal_History


    def run(self):
        start = clock()
        resul_Method = self.Throrem.Method_Cal(self.Paramater)

        #print('resul_Method',resul_Method)
        self.Cal_Datas = self.Decision.Method_Cal(self.Paramater,resul_Method)
        #print("Get Avg Score", self.Decision.Method_Cal_By_Stock())
        #print('resul_Method',self.Cal_Datas)
        self.BuySell = self.Decision.BuySell
        del resul_Method
        self.Result = [self.Identity.Method_Cal(self.Paramater,self.Cal_Datas),self.Paramater]
        self.Rank = self.Identity.Ranks
        self.Final_Score = self.Identity.Final_Score
        self.Cal_History = self.Identity.History
        #print(self.Result)
        self.isRunning = False
        end = clock()
        print("Optimize one Time cost", start, ">>", end, '=', end - start)


class ThreadCalculate(Thread): #具最佳化的演算，會一直算到亂數距離低於設定的為止
    def __init__(self,numb=0, paramater=[],alpha = 30 ,alphaDiv=1.3, \
                 alphaLimit = 0.005 ,seedCount = 30,areaSeedCount = 20 ,\
                 labelqt = ""):
        Thread.__init__(self)
        self.Number = numb #Thread編號
        self.Paramater = paramater #參數
        self.Throrem = theorem.Method()
        self.Decision = decision.Method()
        self.Identity = identify.Method()
        self.Alpha = alpha #初始範圍
        self.Limit = alphaLimit #最後停止範圍
        self.SeedCount = seedCount #高斯亂數的數量
        self.BestScore = [1.0,[]] # Score and Paramater
        self.AlphaDiv = alphaDiv #每次計算後範圍的縮放比例
        self.AreaSeedCount = areaSeedCount #全域均勻亂數的數量
        self.QTLabel = labelqt #等一下要顯示資訊用的Qlabel
        self.Result = [] #最後結論 ， 這邊的結論只會回應score跟Parameter兩個

        self.Running = True

        self.start()

    def __del__(self):
        del self.Paramater
        del self.Throrem
        del self.Decision
        del self.Identity
        del self.Alpha
        del self.Limit
        del self.Result
        del self.BestScore
        del self.SeedCount
        del self.AlphaDiv
        del self.AreaSeedCount
        del self.Number

    def run(self):
        newParam = []
        self.BestScore = [1.0, []]  # Score and Paramater

        alp = self.Alpha
        while (self.Running):
            del newParam
            newParam = []
            #生一堆Seed
            for i in range(self.SeedCount):
                newParam.append(MakeGaussianRandom(self.Paramater,alp))
            for i in range(self.AreaSeedCount):
                newParam.append(MakeNormalRanDom(self.Paramater,self.Alpha))
            newParam.append(self.Paramater)

            #計算結果
            resul_Identify = []
            for parame in newParam:
                resul_Method = self.Throrem.Method_Cal(parame)
                resul_Decision = self.Decision.Method_Cal(parame, resul_Method)
                del resul_Method
                self.Identity.Method_Cal(parame, resul_Decision)
                res_Identyfy = self.Identity.Final_Score
                resul_Identify.append([res_Identyfy,parame])
                del resul_Decision

            #for i in resul_Identify:
            #    print("Optmize result ", i)

            #比較結果是不是有超過之前的結果
            haveBest = 0
            for scores in resul_Identify:
                try:
                    if(scores[0] > self.BestScore[0]):
                        haveBest = 1
                        self.BestScore = scores
                        self.Paramater = scores[1]

                except:
                    pass

            self.QTLabel.setText(self.Number.__str__()+"_Alp"+alp.__str__()+\
                                     " ; Bast Score= "+self.BestScore[0].__str__())
            print(self.Number,"_Alpha",alp," ;;Bast Score",self.BestScore)
            #如果 Alpha 小於設定就停
            if alp < self.Limit:
                break

            #如果有新的最大值就放大範圍，沒得化就縮小範圍
            if haveBest == 1 :
                alp *= self.AlphaDiv
            else:
                alp /= self.AlphaDiv

        #都算完了就儲存結果
        print(self.Number," __ one Thread run finish")
        self.Running = False
        self.Result = self.BestScore
