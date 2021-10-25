
import datetime
import time
import sys
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QRandomGenerator
import random
from PyQt5.QtGui import QPainter, QCursor, QColor, QBrush
from PyQt5.QtWidgets import QToolTip,QWidget

from PyQt5.QtChart import *
from QCustomPlot2 import *



class View_event(QWidget):
    # view 总窗口
    def __init__(self):
        super(View_event, self).__init__()
        # self.setupUi(self)
        self.i=0
        # 执行折线视图函数
        self.create_chart()
        self.timer = QTimer(self)#更新时间戳，
        self.timer.start(10)#每隔0.01秒刷新数据
        self.timer.timeout.connect(self.create_series)
    def create_chart(self):
        # 创建折线视图窗口
        self.chart = QChartView(self)
        self.chart.setRubberBand(QChartView.RectangleRubberBand)
        self.chart.setGeometry(QtCore.QRect(0, 0, 980, 480))

        self.chart.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chart.raise_()
        self.chart._chart = QChart()  # 创建折线视图
        self.chart._chart.setBackgroundVisible(visible=False)      # 背景色透明
        self.chart._chart.setBackgroundBrush(QBrush(QColor("#000FFF")))     # 改变图背景色
        #  图形项默认无法接收悬停事件，可以使用QGraphicsItem的setAcceptHoverEvents()函数使图形项可以接收悬停事件。
        # self.chart._chart.setAcceptHoverEvents(True)
        # 4条折线的坐标值
        # 执行创建折线的函数
        self.series = QLineSeries(self)
        self.chart._chart.addSeries(self.series)
        self.series2 = QLineSeries(self)
        self.chart._chart.addSeries(self.series2)


        self.chart._chart.createDefaultAxes()  # 创建默认的轴
        self.chart._chart.axisX().setRange(0, 5)
        self.chart._chart.axisY().setTickCount(11)  # y1轴设置10个刻度
        self.chart._chart.axisY().setLabelFormat("%d")
        self.chart._chart.axisY().setTitleText('VehSpd')
        self.chart._chart.legend().setVisible(False)
        self.chart._chart.axisY().setRange(100, 200)  # 设置y1轴范围
        # 定义多个y轴
        self.y2_Aix = QValueAxis()  # 定义y2轴
        self.y2_Aix.setLabelFormat("%d")
        self.y2_Aix.setRange(100,250)
        self.y2_Aix.setLabelsColor(QColor(22,233,251))
        self.y2_Aix.setLabelsEditable(True)
        self.y2_Aix .setTickCount(11)
        self.y2_Aix.setTitleText('VehSpd')
        self.chart._chart.addAxis(self.y2_Aix, Qt.AlignLeft)  # 添加到左侧

        #
        # y3_Aix = QValueAxis()  # 定义y3轴
        # y3_Aix.setLabelFormat("%d")
        # y3_Aix.setRange(0, 110)
        # y3_Aix.setTickCount(11)
        # chart._chart.addAxis(y3_Aix, Qt.AlignLeft)  # 添加到右侧
        #
        # y4_Aix = QValueAxis()  # 定义y4轴
        # y4_Aix.setLabelFormat("%d")
        # y4_Aix.setRange(3870, 3980)
        # y4_Aix.setTickCount(11)
        # chart._chart.addAxis(y4_Aix, Qt.AlignLeft)  # 添加到右侧
        # chart._chart.axisX().setTickCount(11)  # X轴设置10个刻度
        # 执行定义X轴的函数
        # self.customAxisX(self.chart._chart)
        self.chart.setChart(self.chart._chart)

    def create_series(self):
        dataTable=random.randint(100,200)

        self.series.append(self.i, dataTable)
        self.series2.append(self.i, dataTable+20)
        self.i += 0.1

        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        if self.i>=5 :
            self.chart._chart.axisX().setRange(self.i-5, self.i)
        if self.series.count() > 100:
            self.series.removePoints(0, self.series.count() - 100)
        if self.series2.count() > 100:
            self.series2.removePoints(0, self.series2.count() - 100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # 初始化所有视图
    login = View_event()

    login.show()

    sys.exit(app.exec_())