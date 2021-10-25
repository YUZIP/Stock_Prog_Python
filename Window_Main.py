'''
用以搭配Pyqt做成顯示介面
'''
import sys,time,os

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow ,QListWidget ,QDoubleSpinBox,QSpinBox ,QFileDialog
from PyQt5.QtCore import *
#from PyQt5.QtGui import QWheelEvent
import math

import pandas as pd
from Frame_Main import *
from threading import Thread

import Get_Stock_Data_Save_Load as stk_sl
import Get_Stock_ID as stk_id
import Cal_Stock_Theorem as stk_thm
import Cal_Stock_Decision as stk_des
import Cal_Stock_Identify as stk_idn

import Cal_Opt_Operation as stk_opt
from PyQt5.QtChart import QChart, QChartView, QBarSet
from PyQt5 import QtChart
import time


class MainWindow(QMainWindow, Ui_MainWindow):
    class ChartView(QChartView):
        def __init__(self, chart ,DispLabel):
            super().__init__(chart)
            self.Ch = chart
            self.SerialDatas = []
            self.LB = DispLabel
            self.Rank = []
            self.Tit = []
            self.CalData = []
            self.Buys = []
            self.Dates = []
            self.Cal_History = []

        def mouseMoveEvent(self, event):
            '''
            建立讓滑鼠滑過Chart的時候，可以在下面的qlabel顯示對應的資料跟資金成長的比例
            '''
            #print("ChartView.mouseMoveEvent", event.pos().x()-self.Ch.plotArea().left(), event.pos().y())
            try:

                #self.Ch = QtCharts.QChart()
                #self.Ch.update()
                #self.Ch.plotArea().
                position  = event.pos().x()-self.chart().plotArea().left()
                Total_Pos = self.chart().plotArea().right() - self.chart().plotArea().left()
                #print(position,Total_Pos)
                ind = int((position/ Total_Pos)*(len(self.SerialDatas)-2) +0.5)
                #print("index",ind)
                out_String = ""

                #aa = self.SerialDatas
                #for s in aa[ind]:
                out_String = ind.__str__() + " == " + "%.4f" % self.SerialDatas[ind] + " : "
                try:
                    out_String +=  self.Cal_History[ind][0] + " :: " + self.Dates[ind]+' : ' +'\n'
                    for i in range(5):
                        out_String += '('+self.Rank[ind][i].__str__() + ')' +\
                                        '[' +stk_sl.Stock_index[self.Rank[ind][i]][0] + '_'+\
                                            stk_sl.Stock_index[self.Rank[ind][i]][1] + '],' + \
                                      "%.2f" % ((self.CalData[self.Rank[ind][i]][ind]-1)*100) + '_' +\
                                         self.Buys[self.Rank[ind][i]][ind]+" : "
                        if i == 1:
                            out_String += '\n'
                    try:
                        out_String += '\n' + self.Cal_History[ind].__str__()
                    except:
                        pass
                except:
                    pass
                    #out_String += self.Rank[ind][i].__str__() + ':'
                #print(self.CalData[self.Rank[ind][i]][ind])
                self.LB.setText(out_String)
                #print(self.Ch.mapToPosition(event.pos().x()))
                time.sleep(0.1) #避免滑鼠滑很快結果資源被更新塞滿
                print("Get Mouse position",position)
            except:
                pass#print("Have error with mouse point")
            return QChartView.mouseMoveEvent(self, event)
        def SetData(self,data):
            #將目前顯示的Chart的資料先暫存到這邊，等一下滑鼠在滑的時候要顯示資料用
            self.SerialDatas = data
            self.Tit = data[0]
        def SetRank(self,rank,calData,buys,history=[]):
            #將計算完的結果放這邊，等一下滑鼠滑過可以顯示
            self.Rank = rank
            self.CalData = calData
            self.Buys = buys
            self.Dates = stk_sl.List_Day_Datas
            self.Cal_History = history

            #print("in Drawing CalData",self.Dates)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        #處德上市且有發行權證的公司名稱跟代號
        stk_id.Get_ID_List_form_Web()
        #在Chart顯示的選擇器那邊建立可以選擇顯示的股票名稱，其中還包含運算結果的Chart
        self.Chart_list = ["Result"]
        for i in stk_id.WarrantStock:
            self.Chart_list.append(i[1])
        self.CB_Select_Chart.addItems(self.Chart_list)

        #從會用到的Method那邊取得名稱，在做最佳話的時候可以選擇要的功能
        self.CB_Method_Sel.addItems(stk_thm.Method_Name)
        self.CB_Decisin_Sel.addItems(stk_des.Method_Name)
        self.CB_Identify_Sel.addItems(stk_idn.Method_Name)

        #build Button Connection
        self.PB_Load_Stock_CSV.clicked.connect(self.Click_Load_Stock_Data_Form_CSV)
        self.PB_Load_Stock_WEB.clicked.connect(self.Click_Load_Stock_Data_Form_WEB)
        self.PB_Save_Stock_CSV.clicked.connect(self.Click_Save_Stock_Data_To_CSV)
        self.PB_Load_Conditin.clicked.connect(self.Click_Load_Condition)
        self.PB_Save_Condition.clicked.connect(self.Click_Save_Condition)
        self.PB_Run_one_time.clicked.connect(self.Click_Run_One_Time)
        self.PB_Optimize.clicked.connect(self.Click_Optimize)
        self.PB_Stop.clicked.connect(self.Click_Stop)
        self.CB_Select_Chart.currentIndexChanged.connect(self.Select_Chart_Change)
        self.PB_Reset.clicked.connect(self.Click_Reset)
        self.PB_Display_log10.clicked.connect(self.ReDrawChart)

        #建立一個Htread，讓Thread可以做監控，而不是採用event的形式，好處是遇到比較耗時間的可以動做到一半停掉他
        QueueProcessing(window=self)

        #Build Chart
        self.chart = QChart()
        self.chart_view = self.ChartView(self.chart,self.LB_Select_Display)#QtCharts.QChartView(self.chart) ##
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart.legend().hide()
        self.SC_Main_Chart.setWidget(self.chart_view)


        self.serial = QtChart.QLineSeries()
        self.chart.addSeries(self.serial)
        self.chart.createDefaultAxes()
        #self.chart.setAnimationOptions(QChart.SeriesAnimations)

        #多建立一個加權指數的Chart，參考用
        self.mainChart = QChart()
        self.MainChartView = QChartView(self.mainChart)
        self.SC_Sub_Chart_1.setWidget(self.MainChartView)
        self.MainSerial = QtChart.QLineSeries()
        self.mainChart.addSeries(self.MainSerial)
        self.mainChart.createDefaultAxes()
        self.mainChart.legend().hide()

        #一些會用到的變數，先在這邊令了等一下到處都可以用
        self.BestParameter = []
        self.Chart_Result = []
        self.Caled_Datas = []
        self.Oprmize_Array = []
        self.Cal_History = []

        #因為從網頁取得股票資料是要時間的，所以取得股票資料的部分是使用另外一個Thread去取得的，這樣就不會有一取得就卡住的感覺
        self.Get_Data_Form_Web_Processing = False
        self.Get_Data_Form_Web_Count = 0

        #如果計算完了Chart有改變或是更改想顯示的Chart，就會執行更改Chart的動作，使用另外一個Thread的原因是避免因為更新太快會把資源塞死
        self.Chart_HaveChange = False

    def Click_Reset(self):
        #改變要送入計算的參數，如果BestParameter是空的話，運算式會自動用亂數生成一組參數
        self.BestParameter = []
        self.Click_Run_One_Time()

    def Click_Load_Stock_Data_Form_CSV(self):
        #從一堆股票的vcs檔案將股票的資料讀入，這樣就不用每次都要從網路上抓
        if self.PB_Load_Stock_CSV.isChecked():
            self.LB_Finish_Stock.setText("0")
            self.LB_Total_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            stk_sl.Read_Stock_Data_from_csv()
            self.LB_Finish_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            self.PB_Load_Stock_CSV.setChecked(False)
            self.DrewMainChart()
    def Click_Load_Stock_Data_Form_WEB(self):
        #從網路更新股票資料，但是這還只是暫存，更新後記得要將它儲存成csv後再用讀csv的方式讀回#
        #更新因為比較耗時間，所以使用Thread去更新，只要按了Thread就會依序抓取資料
        if self.PB_Load_Stock_WEB.isChecked():
            self.Get_Data_Form_Web_Count = 1
            stk_sl.Start_Read_Stock_Data_Form_Web()
            self.LB_Total_Stock.setText((len(stk_id.WarrantStock) - 1).__str__())
            self.Get_Data_Form_Web_Processing = True
        else:
            self.Get_Data_Form_Web_Processing = False

        #stk_sl.Read_Stock_Data_From_Web()
    def Click_Save_Stock_Data_To_CSV(self):
        #將網路抓到的資料儲存成csv檔，因為有時可能會抓到一半網路斷掉還是怎樣就要重抓，所以將抓取跟儲存兩個功能分開
        stk_sl.Write_Stock_Data_to_csv()
    def Click_Load_Condition(self):
        #讀取已經儲存過的參數，可能是最佳化完的參數
        #因為演算法有分三塊，所以每塊的名稱也會在讀取的時候自動更新上去
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Open Recipe File",
                                                                os.path.join(os.getcwd(), 'Recipe'),
                                                                "Process Files (*.prs)")
        if fileName_choose == "":
            return
        self.BestParameter = stk_opt.Read_Optimize_Parameter_Form_File(os.path.basename(fileName_choose))
        self.CB_Method_Sel.setCurrentText(self.BestParameter[0][0])
        self.CB_Decisin_Sel.setCurrentText(self.BestParameter[1][0])
        self.CB_Identify_Sel.setCurrentText(self.BestParameter[2][0])
        self.Click_Run_One_Time()
    def Click_Save_Condition(self):
        #將目前的參數儲存起來，因為只會存到"Recipe"的資料夾，所以不管怎麼改位置都會被修回到"Recipe"那邊
        try:
            os.makedirs(os.path.join(os.getcwd(), 'Recipe'))
        except:
            pass
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "Open Recipe File",
                                                                os.path.join(os.getcwd(), 'Recipe'),
                                                                "Process Files (*.prs)")
        if fileName_choose == "":
            return
        stk_opt.Write_Optimize_Parameter_To_File(os.path.basename(fileName_choose),self.BestParameter)

    def Click_Run_One_Time(self):
        #以現有的參數run一次演算，如果沒有參數的話就會自己產生一個
        if len(stk_sl.Stock_Data) ==0:
            return
        if self.BestParameter ==[]:
            aa = [[self.CB_Method_Sel.currentText(), stk_thm.Index_Method_Name(self.CB_Method_Sel.currentText())],
                  [self.CB_Decisin_Sel.currentText(), stk_des.Index_Method_Name(self.CB_Decisin_Sel.currentText())],
                  [self.CB_Identify_Sel.currentText(), stk_idn.Index_Method_Name(self.CB_Identify_Sel.currentText())]]
            self.BestParameter = stk_opt.MakeNormalRanDom(aa,self.SB_Alpha.value())

            print("1st Parameter : ",self.BestParameter[0])
            print("2nd Parameter : ", self.BestParameter[1])
            print("3rd Parameter : ", self.BestParameter[2])
        self.PrintBestParameter()
        #這邊開始計算，計算的方式有兩個，run_Onece的話會取得比較完整的演算資料。
        # 另外一種真正在計算最佳化的也是有一個Thread進行最佳化，最後只傳回
        aa = stk_opt.Opt_Cal_Onece(self.BestParameter)
        #因為是另外一個Thread，所以使用這種方式計算等待時間
        for i in range(1000):
            if not aa.isRunning :
                break
            time.sleep(0.01)

        #計算結果暫存起來，等一下顯示時使用
        #print("Result ==",aa.Result)
        self.Chart_Result = aa.Result[0]
        self.Caled_Datas = aa.Cal_Datas
        self.Get_Rank = aa.Rank
        self.Cal_Data = aa.Cal_Datas
        self.Buys = aa.BuySell
        self.Cal_History = aa.Cal_History
        #print("in Main Cal_Datas" , self.Buys)
        #更新Chart的畫面跟資訊
        self.ReDrawChart()
        self.Disp_Final_Result(aa.Final_Score)
        del aa

    def PrintBestParameter(self):
        #將目前最佳的參數寫到Label上
        self.LB_Status.setText(self.BestParameter[0].__str__() + '\n' +
                               self.BestParameter[1].__str__() + '\n' +
                               self.BestParameter[2].__str__())
    def Disp_Final_Result(self,Scores):
        #將演算結果寫到Label上
        tx = self.LB_Status.text() + '\n' + "Result = " + Scores.__str__() +"\n::"+self.Chart_Result[-1].__str__()+'\n'
        print(len(self.ChartData))
        for i in self.Get_Rank[len(self.ChartData)-1]:
            tx += '['+stk_sl.Stock_index[i][0] +'_'+ stk_sl.Stock_index[i][1] + ']_' + self.Buys[i][-1] +'\n'
        self.LB_Status.setText(tx)


    def Click_Optimize(self):
        '''
        建立一個新的Thread去跑最佳化演算，並加整個畫面傳入Thread，供Thread取得部分設定內容
        最佳化的Thread也會生出一堆Thread自己去逼最佳化結果
        '''

        if self.PB_Optimize.isChecked():
            self.optProcess = Optmize_Processing(window=self)
        else:
            try:
                del self.optProcess
            except:
                pass




    def Click_Stop(self):
        #嘗試將目前正在執行最佳化的Thread給停掉
        if self.PB_Stop.isChecked():
            try:
                for i in self.Oprmize_Array:
                    i.Running = False
            except:
                self.PB_Stop.setChecked(False)

    def Select_Chart_Change(self):
        #更改讀取的Chart，這樣分開的原因是因為避免滑鼠選很快就把資源塞爆，會當
        self.Chart_HaveChange = True
    def DrewMainChart(self):
        #Chart的畫面有分兩個，一個是看計算結果等的，一個是只顯示加權指數供參考的，這個是顯示加權的
        self.mainChart.removeSeries(self.MainSerial)
        self.MainSerial.clear()

        dat = stk_sl.TWII_Data['Close'].to_list()
        for i in range(len(dat)):
            dx = i + 1
            dy = dat[i]  # [self.Select_Line.currentRow()]
            self.MainSerial.append(dx, dy)
            # print(dx,dy)
        self.mainChart.addSeries(self.MainSerial)

    def ReDrawChart(self):
        # Chart的畫面有分兩個，一個是看計算結果等的，一個是只顯示加權指數供參考的，這個是顯示結果或是選擇要看的公司的
        self.chart.removeSeries(self.serial)
        #print("Redraw Chart",self.CB_Select_Chart.currentText())


        self.serial.clear()

        if self.CB_Select_Chart.currentIndex() == 0:
            self.ChartData = [1] + self.Chart_Result
            del self.ChartData[-1]
        else:
            dat = stk_sl.Get_Stock_List_Data(self.CB_Select_Chart.currentText())
            #print(dat)
            self.ChartData = dat['Close'].to_list()
        #如果log 10有被選擇，則股票顯示會使用log 10的方式顯示，當遇到成長比比較大的狀況就會比較好觀察
        if self.PB_Display_log10.isChecked():
            for i in range(len(self.ChartData)):
                dx= i+1
                dy= math.log10(self.ChartData[i])#[self.Select_Line.currentRow()]
                self.serial.append(dx,dy)
                #print(dx,dy)
        else:
            for i in range(len(self.ChartData)):
                dx= i+1
                dy= self.ChartData[i]#[self.Select_Line.currentRow()]
                self.serial.append(dx,dy)
                #print(dx,dy)

        #將等下滑鼠滑過Chart的時候要顯示的內容也傳進去
        self.chart.addSeries(self.serial)
        self.chart_view.SetData(self.ChartData)
        self.chart_view.SetRank(self.Get_Rank,self.Cal_Data,self.Buys,self.Cal_History)
        #self.chart.createDefaultAxes()
        #self.serial.

        #self.chart.update()
        print("Get Draw Data", self.serial)
        #
        '''
        try:
            self.chart.removeAxis(self.axis_x)
            #self.chart.removeAxis(self.axis_y)
        except:
            pass

        self.axis_x = QtChart.QValueAxis()
        self.axis_x.setTickCount(100)#len(self.ChartData))
        self.axis_x.setLabelFormat("%d")
        self.axis_x.setTitleText("Time")

        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        
        self.axis_y = QtChart.QValueAxis()
        self.axis_y.setTickCount(10)
        self.axis_y.setLabelFormat("%.1f")
        self.axis_y.setTitleText("Magnitude")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.serial.attachAxis(self.axis_x)
        self.serial.attachAxis(self.axis_y)
        '''


class Optmize_Processing(Thread): #這是主要負責最佳化的Thread，目前使用的方式是區域亂數的模式進行最佳化
    def __init__(self,window = MainWindow):
        Thread.__init__(self)
        self.ww = window
        self.start()


    def run(self):
        while self.ww.PB_Optimize.isChecked():
            #建立一堆種子參數，先開一將到處撒點後，先短距最佳化看結果，在選擇幾個score比較好的繼續最佳化
            #參數格式 = ['演算法名稱',[參數],'演算法名稱',[參數],'演算法名稱',[參數]]
            seeds = []
            st = [
                [self.ww.CB_Method_Sel.currentText(),
                stk_thm.Index_Method_Name(self.ww.CB_Method_Sel.currentText())],
                [self.ww.CB_Decisin_Sel.currentText(),
                stk_des.Index_Method_Name(self.ww.CB_Decisin_Sel.currentText())],
                [self.ww.CB_Identify_Sel.currentText(),
                stk_idn.Index_Method_Name(self.ww.CB_Identify_Sel.currentText())]
            ]
            for i in range(self.ww.SB_Seed.value()):
                seeds.append(stk_opt.MakeNormalRanDom(st, self.ww.SB_Alpha.value()))
            #最後還要加一個上一次最好的結果，有可能是讀取進來的，如果有的話就會加進去
            if not self.ww.BestParameter == []:
                seeds.append(self.ww.BestParameter)

            optmize_array = []
            print('Get Seed :', seeds)
            a = 0
            ##### 利用多執行續將建立的Seed用Run一次的方式先取得結果 #####
            self.ww.LB_Opt_Display_2.setText("Start Opitmize")
            #先嘗試將上一次計算的所有Thread先砍掉，沒得砍就算了
            try:
                for i in range(len(self.ww.Oprmize_Array)):
                    del self.ww.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass

            for i in seeds:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb = a, #每個Thread的編號
                                                             paramater=i, #傳入的種子Parameter
                                                             alpha=self.ww.SB_Alpha.value(), #亂數範圍
                                                             alphaDiv=self.ww.SB_Alpha_Div.value(), #每次計算的縮放比例
                                                             alphaLimit=int(self.ww.SB_Alpha.value()/5), #最後停止的範圍值
                                                             seedCount=int(self.ww.SB_Gass_Random.value()*1.5), #產生特定範圍的亂數的量
                                                             areaSeedCount=int(self.ww.SB_Area_Random.value()*1.5), #產生全域亂數的量
                                                             labelqt=self.ww.LB_Opt_Display)) #送個QLabel，中間有任何訊息的時候就可以傳輸來直接顯示
                a+=1
            # 等待Run完成
            best_Score = 0
            while self.ww.PB_Optimize.isChecked():
                all_finish = True
                numb_Count = 0 #查看已經有幾個run完了
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count +=1
                #試著取得目前個別run的最好的score，並且把他顯示在另外一個QLabel
                try:
                    aa = float(self.ww.LB_Opt_Display.text().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass

                self.ww.LB_Opt_Display_2.setText("First Step Optmize is finish by : "+ numb_Count.__str__()+\
                                                 " : "+self.ww.SB_Seed.value().__str__() + ' :: Best_Score= ' +\
                                                 "%.4f" % best_Score)
                if all_finish == True:
                    break
                #time.sleep(1)
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                '''
                self.ww.PB_Optimize.setChecked(False)
                
                try:
                    for i in range(len(self.ww.Oprmize_Array)):
                        del self.ww.Oprmize_Array[0]
                except:
                    pass
                return
                '''
            # 將run完的結果提出後排序
            print("All Optmize is finish")
            self.ww.LB_Opt_Display_2.setText("First Optimize is finish")
            temp1 = []
            for i in self.ww.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)

            # 將獨立Thread的都砍掉
            '''
            for i in ss:
                print("Sorted Result",i)
            for i in range(len(optmize_array)):
                del optmize_array[0]
            '''
            try:
                for i in range(len(self.ww.Oprmize_Array)):
                    del self.ww.Oprmize_Array[0]
                # del self.Oprmize_Array
            except:
                pass
                # del self.Oprmize_Array

            self.ww.Oprmize_Array = []
            # 取Group的數值，然後將比較好的幾個重新做優化
            while len(ss) > self.ww.SB_Group.value():
                del ss[self.ww.SB_Group.value()]
            a = 0
            for i in ss:
                self.ww.Oprmize_Array.append(stk_opt.ThreadCalculate(numb=a,
                                                                  paramater=i[1],
                                                                  alpha=self.ww.SB_Alpha.value(),
                                                                  alphaDiv=self.ww.SB_Alpha_Div.value(),
                                                                  alphaLimit=self.ww.SB_Alpha_Limit.value(),
                                                                  seedCount=self.ww.SB_Gass_Random.value(),
                                                                  areaSeedCount=self.ww.SB_Area_Random.value(),
                                                                  labelqt=self.ww.LB_Opt_Display))
                a +=1
            best_Score = 0
            while self.ww.PB_Optimize.isChecked():
                all_finish = True
                numb_Count = 0
                for i in self.ww.Oprmize_Array:
                    if i.Running == True:
                        all_finish = False
                    else:
                        numb_Count +=1
                try:
                    aa = float(self.ww.LB_Opt_Display.text().split('Bast Score= ')[1])
                    if aa > best_Score:
                        best_Score = aa
                except:
                    pass
                self.ww.LB_Opt_Display_2.setText("Scend Step Optmize is finish by : " + numb_Count.__str__() +\
                                                 " : "+self.ww.SB_Group.value().__str__() + ' :: Best Score= '\
                                                 "%.4f" % best_Score)
                if all_finish == True:
                    break
                #time.sleep(1)
            if self.ww.PB_Stop.isChecked():
                self.ww.PB_Stop.setChecked(False)
                '''
                self.ww.PB_Optimize.setChecked(False)
                return
                # 優化完成後，在排序選最好的那個為結果
                然後使用run Once在跑一次取得更詳細的資料顯示出來
                '''
            temp1 = []
            for i in self.ww.Oprmize_Array:
                temp1.append(i.Result)

            ss = sorted(temp1, key=lambda temp1: temp1[0], reverse=True)
            self.ww.PB_Optimize.setChecked(False)
            self.ww.BestParameter = ss[0][1]
            self.ww.PB_Run_one_time.setChecked(True)


            #if not self.ww.PB_Stop.isChecked():
            self.ww.BestParameter = ss[0][1]
            self.ww.Click_Run_One_Time()
            self.ww.PB_Stop.setChecked(False)
            self.ww.PB_Optimize.setChecked(False)



class QueueProcessing(Thread):
    def __init__(self,window = MainWindow):
        Thread.__init__(self)
        self.daemon = True
        self.ww = window
        self.start()

    def run(self):
        while self.daemon:
            try:
                if self.ww.Get_Data_Form_Web_Processing :
                    #採用Thread取得股票資料，這樣UI就有機會可以停止蒐集資料，也不會感覺起來當掉一樣
                    print("Try Get Stock Data Form web",self.ww.Get_Data_Form_Web_Processing,self.ww.Get_Data_Form_Web_Count)
                    self.ww.LB_Finish_Stock.setText(self.ww.Get_Data_Form_Web_Count.__str__())
                    stk_sl.Read_Stock_Data_From_Web(self.ww.Get_Data_Form_Web_Count)
                    self.ww.Get_Data_Form_Web_Count += 1
                    if self.ww.Get_Data_Form_Web_Count >= len(stk_id.WarrantStock):
                        self.ww.Get_Data_Form_Web_Processing = False
                        self.ww.PB_Load_Stock_WEB.setChecked(False)
                        stk_sl.data_toList()
                else:
                    time.sleep(0.1)

                if self.ww.Chart_HaveChange:
                    #改變Chart的繪製
                    time.sleep(0.1)
                    self.ww.ReDrawChart()
                    self.ww.Chart_HaveChange = False

            except:
                time.sleep(0.1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()

    sys.exit(app.exec_())

