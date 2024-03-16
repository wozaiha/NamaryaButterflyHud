import math
import queue
import threading

from dataqueue import data_queue
import tkinter as tk
from tkinter import font

# from hudinjector import TestHUD

RED = 0
BLUE = 1
FULL = 0
NOTFULL = 1
X = 0
Y = 1


class ButterflyDraw:
    angle = 2 * math.pi / 6
    spa1 = angle / 12
    spa2 = angle / 6 * 2 + spa1
    spa3 = angle / 6 + spa2
    spa4 = angle / 6 * 1
    spa5 = angle / 6 + spa2
    spa6 = angle / 6 * 2 + spa2
    xw = - angle / 12 * 6
    point1 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point2 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point3 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point4 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point5 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point6 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point7 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point8 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point9 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point10 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point11 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point12 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point13 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    point14 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    center = None
    radius = None

    colors = [['', ''], ['', '']]

    def init_FlowerDraw(self, center, radius):
        self.center = center
        self.radius = radius
        for i in range(6):
            start_angle = i * self.angle + self.xw
            end_angle = start_angle + self.angle

            the_angle = start_angle if i % 2 else end_angle

            self.point1[i][X] = center[X] + radius * math.cos(the_angle)
            self.point1[i][Y] = center[Y] + radius * math.sin(the_angle)
            self.point2[i][X] = center[X] + (radius / 6) * math.cos(the_angle)
            self.point2[i][Y] = center[Y] + (radius / 6) * math.sin(the_angle)
            self.point3[i][X] = center[X] + (radius / 6 * 5) * math.cos(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point3[i][Y] = center[Y] + (radius / 6 * 5) * math.sin(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point4[i][X] = center[X] + (radius / 6 * 1.5) * math.cos(the_angle + self.spa4 * (-1 if i % 2 else 1))
            self.point4[i][Y] = center[Y] + (radius / 6 * 1.5) * math.sin(the_angle + self.spa4 * (-1 if i % 2 else 1))
            self.point5[i][X] = center[X] + (radius / 6 * 3) * math.cos(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point5[i][Y] = center[Y] + (radius / 6 * 3) * math.sin(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point6[i][X] = center[X] + (radius / 6 * 6.5) * math.cos(the_angle + self.spa2 * (-1 if i % 2 else 1))
            self.point6[i][Y] = center[Y] + (radius / 6 * 6.5) * math.sin(the_angle + self.spa2 * (-1 if i % 2 else 1))
            self.point7[i][X] = center[X] + (radius / 6 * 4) * math.cos(the_angle + self.spa5 * (-1 if i % 2 else 1))
            self.point7[i][Y] = center[Y] + (radius / 6 * 4) * math.sin(the_angle + self.spa5 * (-1 if i % 2 else 1))
            self.point8[i][X] = center[X] + (radius / 6 * 3) * math.cos(the_angle + self.spa2 * (-1 if i % 2 else 1))
            self.point8[i][Y] = center[Y] + (radius / 6 * 3) * math.sin(the_angle + self.spa2 * (-1 if i % 2 else 1))
            self.point9[i][X] = center[X] + (radius / 6 * 1.5) * math.cos(the_angle + self.spa3 * (-1 if i % 2 else 1))
            self.point9[i][Y] = center[Y] + (radius / 6 * 1.5) * math.sin(the_angle + self.spa3 * (-1 if i % 2 else 1))
            self.point10[i][X] = center[X] + (radius / 6 * 6) * math.cos(the_angle + self.spa3 * (-1 if i % 2 else 1))
            self.point10[i][Y] = center[Y] + (radius / 6 * 6) * math.sin(the_angle + self.spa3 * (-1 if i % 2 else 1))
            self.point11[i][X] = center[X] + (radius / 6 * 2.3) * math.cos(the_angle + self.spa6 * (-1 if i % 2 else 1))
            self.point11[i][Y] = center[Y] + (radius / 6 * 2.3) * math.sin(the_angle + self.spa6 * (-1 if i % 2 else 1))

            self.point12[i][X] = center[X] + (radius / 6 * 6.3) * math.cos(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point12[i][Y] = center[Y] + (radius / 6 * 6.3) * math.sin(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point13[i][X] = center[X] + (radius / 6 * 6.2) * math.cos(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point13[i][Y] = center[Y] + (radius / 6 * 6.2) * math.sin(the_angle + self.spa1 * (-1 if i % 2 else 1))
            self.point14[i][X] = center[X] + (radius / 6 * 6) * math.cos(the_angle + self.spa4 * (-1 if i % 2 else 1))
            self.point14[i][Y] = center[Y] + (radius / 6 * 6) * math.sin(the_angle + self.spa4 * (-1 if i % 2 else 1))

        self.colors[RED][FULL] = '#DDAADD'
        self.colors[RED][NOTFULL] = '#CC00CC'
        self.colors[BLUE][FULL] = '#AADDDD'
        self.colors[BLUE][NOTFULL] = '#00BBBB'

    def draw_circle(self, canvas, color_flag, full_flag):
        canvas.create_oval(self.center[0] - 10, self.center[1] - 10, self.center[0] + 10, self.center[1] + 10,
                           fill=self.colors[color_flag][full_flag])

    def draw_flower(self, canvas, petal_num, color_flag, full_flag):
        for i in range(petal_num):
            x1 = self.point1[i][X]
            y1 = self.point1[i][Y]
            x2 = self.point2[i][X]
            y2 = self.point2[i][Y]
            x3 = self.point3[i][X]
            y3 = self.point3[i][Y]
            x4 = self.point4[i][X]
            y4 = self.point4[i][Y]
            x5 = self.point5[i][X]
            y5 = self.point5[i][Y]
            x6 = self.point6[i][X]
            y6 = self.point6[i][Y]
            x7 = self.point7[i][X]
            y7 = self.point7[i][Y]
            x8 = self.point8[i][X]
            y8 = self.point8[i][Y]
            x9 = self.point9[i][X]
            y9 = self.point9[i][Y]
            x10 = self.point10[i][X]
            y10 = self.point10[i][Y]
            x11 = self.point11[i][X]
            y11 = self.point11[i][Y]
            x12 = self.point12[i][X]
            y12 = self.point12[i][Y]
            x13 = self.point13[i][X]
            y13 = self.point13[i][Y]
            x14 = self.point14[i][X]
            y14 = self.point14[i][Y]
            canvas.create_polygon(x1, y1, x2, y2, x3, y3,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x4, y4, x2, y2, x3, y3,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x5, y5, x6, y6, x3, y3,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x5, y5, x6, y6, x10, y10,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x5, y5, x7, y7, x10, y10,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x5, y5, x4, y4, x8, y8,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x11, y11, x4, y4, x8, y8,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x11, y11, x4, y4, x9, y9,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x1, y1, x12, y12, x13, y13,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)
            canvas.create_polygon(x12, y12, x13, y13, x14, y14,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)


def update_gui_from_queue(root, canvas, butterfly_draw: ButterflyDraw, last_data):
    try:
        # 非阻塞地从队列中获取数据
        data = data_queue.get_nowait()
        # data = 6

        if last_data != data:
            last_data = data
            # 使用队列中的数据更新GUI
            num = data % 10
            color_flag = RED if data >= 10 else BLUE
            full_flag = FULL if num == 6 else NOTFULL

            canvas.delete("all")
            butterfly_draw.draw_flower(canvas, num, color_flag, full_flag)
            butterfly_draw.draw_circle(canvas, color_flag, full_flag)

        # 清除队列中的数据标记为已处理
        data_queue.task_done()
    except queue.Empty:
        # 队列为空，没有新数据
        pass
    # 100毫秒后再次调用自身进行更新
    root.after(100, update_gui_from_queue, root, canvas, butterfly_draw, last_data)


def draw_overlay():
    root = tk.Tk()
    root.title("Namarya Butterfly HUD")

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()

    size_base = 0.2775
    # size_base = 0.5

    # 创建一个Canvas用于绘制花瓣
    canvas = tk.Canvas(root, width=size_base * screenheight, height=size_base * screenheight, bg='black',
                       highlightthickness=0)
    canvas.pack()



    # 设置花瓣的中心点和半径
    center = (size_base * screenheight / 2, size_base * screenheight / 2)
    radius = size_base * screenheight / 4
    butterfly_draw = ButterflyDraw()
    butterfly_draw.init_FlowerDraw(center, radius)

    # 设置窗口的默认位置
    x = int(screenwidth * 0.55)  # 设置窗口左上角的X坐标为屏幕宽度的55%
    y = int(screenheight * 0.60)  # 设置窗口左上角的Y坐标为屏幕高度的60%
    root.geometry(f"+{x}+{y}")

    def on_drag(event):
        # 计算鼠标移动的偏移量
        offset_x = event.x_root - root._drag_start_x
        offset_y = event.y_root - root._drag_start_y
        # 移动窗口
        root.geometry(f'+{root._start_x + offset_x}+{root._start_y + offset_y}')

    def start_drag(event):
        # 记录拖动开始时鼠标的位置和窗口的位置
        root._drag_start_x = event.x_root
        root._drag_start_y = event.y_root
        root._start_x = root.winfo_x()
        root._start_y = root.winfo_y()

    root._drag_start_x = None
    root._drag_start_y = None
    root._start_x = None
    root._start_y = None
    canvas.bind('<Button-1>', start_drag)  # 鼠标左键按下事件
    canvas.bind('<B1-Motion>', on_drag)  # 鼠标拖动事件（左键按下的情况下移动）

    root.overrideredirect(True)
    # screenwidth = root.winfo_screenwidth() // 2 + 300
    # screenheight = root.winfo_screenheight() // 4 * 3
    # root.geometry(f"+{screenwidth}+{screenheight}")
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")

    # 启动周期性的GUI更新函数
    root.after(100, update_gui_from_queue, root, canvas, butterfly_draw, None)

    # 启动tkinter mainloop
    root.mainloop()


# draw_overlay()
