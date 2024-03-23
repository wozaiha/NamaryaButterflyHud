import json
import math
import os
import queue
import threading
import sys
from dataqueue import data_queue

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore

RED = 0
BLUE = 1
X = 0
Y = 1

DEBUG = False


class ButterflyGif(QWidget):
    def __init__(self, canvas_size):
        super().__init__()
        self.width = canvas_size
        self.height = canvas_size
        self.last_data = None
        self.red_movie_list = list()
        self.blue_movie_list = list()
        for i in range(7):
            self.red_movie_list.append(QMovie(os.path.split(os.path.realpath(__file__))[0] + "\\img\\gif\\" + str(RED) + str(i) + ".gif"))
            self.blue_movie_list.append(QMovie(os.path.split(os.path.realpath(__file__))[0] + "\\img\\gif\\" + str(BLUE) + str(i) + ".gif"))
        self.initUI() 

    def initUI(self):
        self.label = QLabel(self)
        self.label.resize(int(self.height), int(self.height))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)  # 无边框
        self.mousePressEvent = self.startMove
        self.mouseMoveEvent = self.moveWindow
        self.oldPos = self.pos()
        # 创建一个 QTimer 实例
        self.timer = QTimer(self)
        # 设置定时器超时连接的槽函数
        self.timer.timeout.connect(self.onChangeGIF)
        # 设置定时器间隔（毫秒）
        self.timer.start(200)

    def startMove(self, event):
        self.oldPos = event.globalPos()

    def moveWindow(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def onChangeGIF(self):
        try:
            # 非阻塞地从队列中获取数据
            data = data_queue.get_nowait()
            print(data)
            if self.last_data != data:
                self.last_data = data
                # 使用队列中的数据更新GUI
                num = data % 10
                color_flag = 0 if data >= 10 else 1
                self.updateGIF(num, color_flag)
            # 清除队列中的数据标记为已处理
            data_queue.task_done()
        except queue.Empty:
            # 队列为空，没有新数据
            pass

    def updateGIF(self, num, color_flag):
        self.movie = self.red_movie_list[num] if color_flag == RED else self.blue_movie_list[num]
        self.movie.setScaledSize(self.label.size())
        self.label.setMovie(self.movie)
        self.movie.start()


def draw_overlay():
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    screenwidth, screenheight = screen_resolution.width(), screen_resolution.height()
    
    f = open(os.path.split(os.path.realpath(__file__))[0] + '\\config.json', 'r')
    res = json.loads(f.read())
    f.close()
    
    size_rate = res["size"]
    x_rate = res["x"]
    y_rate = res["y"]
    
    size_base = 0.12 * size_rate
    canvas_size = size_base * screenheight
    
    x = int(screenwidth * x_rate)  # 设置窗口左上角的X坐标为屏幕宽度的55%
    y = int(screenheight * y_rate)  # 设置窗口左上角的Y坐标为屏幕高度的60%
    
    
    
    root = ButterflyGif(canvas_size)
    root.move(x, y)
    root.show()
    sys.exit(app.exec_())


if DEBUG:
    draw_overlay()
