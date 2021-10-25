'''
會在此用演算法計算選股的演算
並利用此驗證股票的價格

架構上Method , Decision , Identify 三個差不多
del 方法
https://python-reference.readthedocs.io/en/latest/docs/dunderdsc/delete.html


'''
import Get_Stock_Data_Save_Load as st_data
from time import time as clock
import math

score_Ratio = [0.4,0.3,0.2,0.05,0.05] #購買比例，選股演算結果排名後，依照比例購入

Method_Name = ['潛伏天數1d','潛伏天數2d','均勻獲利','潛伏天數1d_Exp','潛伏天數_ExpAbs']
Method_Format = [[0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0],
                 [0,0,0,0,0]
                ]

def Index_Method_Name(name = ''):
    return Method_Format[Method_Name.index(name)]

class Method():
    global Method_Name
    def __init__(self):
        self.Paramater = []
        self.InputData = []
        self.EveryDayScore = []
        self.Result = []
        self.Ranks = []
        self.History = []
        self.Final_Score = 0

    def __delete__(self, instance):
        del self.Paramater
        del self.InputData
        del self.EveryDayScore
        del self.Result
        del self.Ranks
        del self.History
        del self.Final_Score


    def Basic_Cal(self): #取得基本的漲跌資料，主要是以當天結算跟明天結算的比例差
        self.EveryDayScore = st_data.List_1d_Score_Data
        '''
        self.EveryDayScore = []
        for i in st_data.Stock_Data:
            aa = i['Close']
            bb = aa.shift(-1)
            bb.fillna(method='pad', inplace=True)
            cc = bb/aa
            #print("EverySay Score",cc)
            self.EveryDayScore.append(cc)
        '''
    def Get_Rank(self,data): #經過演算後取得排序，並依照購買比例算價格
        self.Ranks = []
        self.History = []
        Current_Score = 1
        #print("in Decisoin datas Length",len(data[0]))
        #for i in data:
            #print("Each_Length",len(i))

        aa = [1, 1, 1, 1, 1]
        for i in range(len(data[0])):
            student_sort = sorted(data, key=lambda datas: datas[i] , reverse=True)
            #print("student_sort",student_sort)
            aa = [student_sort[0][0],student_sort[1][0],student_sort[2][0],student_sort[3][0],student_sort[4][0]]
            #print(aa)
            self.Ranks.append(aa)

        #print("Total Rank_Length",len(self.Ranks))
        #print("Total EveryDayScore_Length", len(self.EveryDayScore),len(self.EveryDayScore[0]))
        #print("in Identify Rank Length",len(self.Ranks))
        del self.Ranks[0] # Delect culoumun index
        #del self.Ranks[0]
        self.Result = []
        #for i in self.InputData:
            #print("InputData",len(i))
        for i in range(len(self.Ranks)):
            if i< 20:
                Current_Score = 1
                signal_history = [[1],[1],[1],[1],[1]]
                setp_Score = 1
            else:
                setp_Score = 0
                p_Score = 1
                signal_history = []
                #print(self.Ranks[i])
                for j in range(5):
                    p_Score = self.InputData[self.Ranks[i][j]][i]
                    #p_Score *= (self.EveryDayScore[self.Ranks[i][j]][i]) * self.InputData[self.Ranks[i][j]][i]
                    setp_Score += p_Score * score_Ratio[j]
                    signal_history.append([st_data.Stock_index[self.Ranks[i][j]][1],"%.2f" %((p_Score-1)*100)])
                #setp_Score += 1

                '''
                setp_Score = self.EveryDayScore[self.Ranks[i][0]][i]
                '''
                #signal_history.[setp_Score,signal_history]
                #signal_history.append([setp_Score,signal_history])
                Current_Score = Current_Score * setp_Score
            self.Result.append(Current_Score)
            self.History.append(["%.2f" %((setp_Score-1)*100),signal_history])
        #print("Get Fineal Result",self.History)
    def Get_Rank_Exp(self,data): #經過演算後取得排序，並依照購買比例算價格，但是使用expolation將之前的結果做衰竭
        self.Ranks = []
        self.History = []
        Current_Score = 1
        #print("in Decisoin datas Length",len(data[0]))
        #for i in data:
            #print("Each_Length",len(i))

        aa = [1, 1, 1, 1, 1]
        for i in range(len(data[0])):
            student_sort = sorted(data, key=lambda datas: datas[i] , reverse=True)
            #print("student_sort",student_sort)
            aa = [student_sort[0][0],student_sort[1][0],student_sort[2][0],student_sort[3][0],student_sort[4][0]]
            #print(aa)
            self.Ranks.append(aa)

        #print("Total Rank_Length",len(self.Ranks))
        #print("Total EveryDayScore_Length", len(self.EveryDayScore),len(self.EveryDayScore[0]))
        #print("in Identify Rank Length",len(self.Ranks))
        del self.Ranks[0] # Delect culoumun index
        #del self.Ranks[0]
        self.Result = []
        #for i in self.InputData:
            #print("InputData",len(i))
        #print("expss_Start")
        expss = math.exp(1)
        #print("expss",expss)
        Total_Length = len(self.Ranks)
        #print("Total_Length",Total_Length)
        for i in range(len(self.Ranks)):
            if i< 20:
                Current_Score = 1
                signal_history = [[1],[1],[1],[1],[1]]
                setp_Score = 1
            else:
                setp_Score = 0
                p_Score = 1
                signal_history = []
                #print(self.Ranks[i])
                for j in range(5):
                    p_Score = self.InputData[self.Ranks[i][j]][i]
                    #p_Score *= (self.EveryDayScore[self.Ranks[i][j]][i]) * self.InputData[self.Ranks[i][j]][i]
                    setp_Score += p_Score * score_Ratio[j]
                    signal_history.append([st_data.Stock_index[self.Ranks[i][j]][1],"%.2f" %((p_Score-1)*100)])
                #setp_Score += 1

                '''
                setp_Score = self.EveryDayScore[self.Ranks[i][0]][i]
                '''
                #signal_history.[setp_Score,signal_history]
                #signal_history.append([setp_Score,signal_history])
                #aa = ((i+1)/Total_Length)*0.2+0.9#(math.exp(i/Total_Length)/5)+1
                aa = math.exp(i/Total_Length)/math.exp(1)
                if aa > 1.0:
                    aa = 1.0
                setp_Score = ((setp_Score -1)*aa)+1
                Current_Score = Current_Score * setp_Score
            #print("Final aa",aa)
            self.Result.append(Current_Score)
            self.History.append(["%.2f" %((setp_Score-1)*100),signal_history])
        #print("Get Fineal Result",self.History)


    def Method_Cal(self,paramater,data):
        self.Paramater = paramater[2]
        self.InputData = data
        self.dataTemp = []
        start = clock()

        if self.Paramater[0] == Method_Name[0]:  # '潛伏天數_1d'
            #計算潛伏天數 * 放大率
            #self.Basic_Cal()
            self.EveryDayScore = st_data.List_1d_Score_Data
            #print("Every Days Data 1d", self.EveryDayScore)
            Datas_Step1 = []

            for i in range(len(self.EveryDayScore)): # Each
                score = 1
                MultiBase = 0
                each_Step1_Data = [i]
                for j in range(len(self.EveryDayScore[i])):
                    aa = self.EveryDayScore[i][j]
                    MultiBase = (MultiBase * self.Paramater[1][0] + self.EveryDayScore[i][j]) / (self.Paramater[1][0] +1)
                    if (abs((MultiBase -1)*100) < abs(self.Paramater[1][1])):
                        score += abs(self.Paramater[1][2])
                    else:
                        score /= abs(self.Paramater[1][2])
                    score = score * MultiBase
                    each_Step1_Data.append(score)
                Datas_Step1.append(each_Step1_Data)
                #print("in Decision Do Pre Datas",len(self.EveryDayScore[0]))
            self.Get_Rank(Datas_Step1)
            end = clock()
            self.Final_Score = self.Result[-1]
            '''
            lan = int(len(self.Result) / 5)
            a1 = self.Result[-(lan * 4): -(lan * 3)]
            a2 = self.Result[-(lan * 3): -(lan * 2)]
            a3 = self.Result[-(lan * 2): -(lan * 1)]
            a4 = self.Result[-(lan * 1):]
            b1 = (sum(a1) / len(a1)) - min(a1)
            b2 = (sum(a2) / len(a2)) - min(a2)
            b3 = (sum(a3) / len(a3)) - min(a3)
            b4 = (sum(a4) / len(a4)) - min(a4)
            li = [b1, b2, b3, b4]
            av = sum(li) / len(li)
            ag = 1 / ((max(li) - (av)) / av)
            self.Final_Score = ag *ag * self.Result[-1]
            '''
            print("Identify Time cost",end-start)
            return self.Result

        if self.Paramater[0] == Method_Name[1]:  # '潛伏天數_2d'
            #計算潛伏天數 * 放大率
            #self.Basic_Cal()
            self.EveryDayScore = st_data.List_2d_Score_Data
            #print("Every Days Data 2d",self.EveryDayScore)
            Datas_Step1 = []

            for i in range(len(self.EveryDayScore)): # Each
                score = 1
                MultiBase = 0
                each_Step1_Data = [i]
                for j in range(len(self.EveryDayScore[i])):
                    aa = self.EveryDayScore[i][j]
                    MultiBase = (MultiBase * self.Paramater[1][0] + self.EveryDayScore[i][j]) / (self.Paramater[1][0] +1)
                    if (abs((MultiBase -1)*100) < abs(self.Paramater[1][1])):
                        score += abs(self.Paramater[1][2])
                    else:
                        score /= abs(self.Paramater[1][2])
                    score = score * MultiBase
                    each_Step1_Data.append(score)
                Datas_Step1.append(each_Step1_Data)
                #print("in Decision Do Pre Datas",len(self.EveryDayScore[0]))
            self.Get_Rank(Datas_Step1)
            end = clock()
            self.Final_Score = self.Result[-1]
            print("Identify Time cost",end-start)
            return self.Result



        if self.Paramater[0] == Method_Name[2]:  # '均勻獲利'
            # 計算潛伏天數 * 放大率
            # self.Basic_Cal()
            self.EveryDayScore = st_data.List_1d_Score_Data
            # print("Every Days Data 1d", self.EveryDayScore)
            Datas_Step1 = []

            for i in range(len(self.EveryDayScore)):  # Each
                score = 1
                MultiBase = 0
                each_Step1_Data = [i]
                for j in range(len(self.EveryDayScore[i])):
                    aa = self.EveryDayScore[i][j]
                    MultiBase = (MultiBase * self.Paramater[1][0] + self.EveryDayScore[i][j]) / (
                                self.Paramater[1][0] + 1)
                    if (abs((MultiBase - 1) * 100) < abs(self.Paramater[1][1])):
                        score += abs(self.Paramater[1][2])
                    else:
                        score /= abs(self.Paramater[1][2])
                    score = score * MultiBase
                    each_Step1_Data.append(score)
                Datas_Step1.append(each_Step1_Data)
                # print("in Decision Do Pre Datas",len(self.EveryDayScore[0]))
            self.Get_Rank(Datas_Step1)

            end = clock()
            '''
            self.Final_Score = self.Result[-1]
            '''
            lan = int(len(self.Result) / 5)
            a1 = self.Result[-(lan * 4): -(lan * 3)]
            a2 = self.Result[-(lan * 3): -(lan * 2)]
            a3 = self.Result[-(lan * 2): -(lan * 1)]
            a4 = self.Result[-(lan * 1):]
            b1 = (sum(a1) / len(a1)) - min(a1)
            b2 = (sum(a2) / len(a2)) - min(a2)
            b3 = (sum(a3) / len(a3)) - min(a3)
            b4 = (sum(a4) / len(a4)) - min(a4)
            li = [b1, b2, b3, b4]
            av = sum(li) / len(li)
            ag = 1 / ((max(li) - (av)) / av)
            self.Final_Score = ag *ag * self.Result[-1]

            print("Identify Time cost", end - start)
            return self.Result

        if self.Paramater[0] == Method_Name[3]:  # '潛伏天數_1d_Exp'
            #計算潛伏天數 * 放大率
            #self.Basic_Cal()
            self.EveryDayScore = st_data.List_1d_Score_Data
            #print("Every Days Data 1d", self.EveryDayScore)
            Datas_Step1 = []

            for i in range(len(self.EveryDayScore)): # Each
                score = 1
                MultiBase = 0
                each_Step1_Data = [i]
                for j in range(len(self.EveryDayScore[i])):
                    aa = self.EveryDayScore[i][j]
                    MultiBase = (MultiBase * self.Paramater[1][0] + self.EveryDayScore[i][j]) / (self.Paramater[1][0] +1)
                    if (abs((MultiBase -1)*100) < abs(self.Paramater[1][1])):
                        score += abs(self.Paramater[1][2])
                    else:
                        score /= abs(self.Paramater[1][2])
                    score = score * MultiBase
                    each_Step1_Data.append(score)
                Datas_Step1.append(each_Step1_Data)
                #print("in Decision Do Pre Datas",len(self.EveryDayScore[0]))
            self.Get_Rank_Exp(Datas_Step1)
            end = clock()
            self.Final_Score = self.Result[-1]

            #print("Identify Time cost",end-start)
            return self.Result
        if self.Paramater[0] == Method_Name[4]:  # '潛伏天數_1d_Exp_Abs'
            #計算潛伏天數 * 放大率
            #self.Basic_Cal()
            self.EveryDayScore = st_data.List_1d_Score_Data
            #print("Every Days Data 1d", self.EveryDayScore)
            Datas_Step1 = []

            for i in range(len(self.EveryDayScore)): # Each
                score = 1
                MultiBase = 0
                each_Step1_Data = [i]
                for j in range(len(self.EveryDayScore[i])):
                    aa = abs(self.EveryDayScore[i][j]-1) + 1
                    MultiBase = (MultiBase * self.Paramater[1][0] + aa) / (self.Paramater[1][0] +1)
                    if (abs((MultiBase -1)*100) < abs(self.Paramater[1][1])):
                        score += abs(self.Paramater[1][2])
                    else:
                        score /= abs(self.Paramater[1][2])
                    score = score * MultiBase
                    each_Step1_Data.append(score)
                Datas_Step1.append(each_Step1_Data)
                #print("in Decision Do Pre Datas",len(self.EveryDayScore[0]))
            self.Get_Rank_Exp(Datas_Step1)
            end = clock()
            self.Final_Score = self.Result[-1]

            print("Identify Time cost",end-start)
            return self.Result



