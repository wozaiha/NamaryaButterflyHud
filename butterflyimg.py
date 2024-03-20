import json
import math
import os
import queue
import threading

from dataqueue import data_queue
import tkinter as tk
from PIL import Image, ImageTk

RED = 0
BLUE = 1
FULL = 0
NOTFULL = 1
X = 0
Y = 1


class ButterflyImg:
    angle = math.pi / 3
    xw_angle = -math.pi / 12 * 4
    point1 = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    center = None
    radius = None

    colors = [['', ''], ['', '']]

    def __init__(self):
        self.purple = []
        self.blue = []

    def init_ButterflyImg(self, center, radius):
        self.center = center
        self.radius = radius

        blueimage = Image.open(os.path.split(os.path.realpath(__file__))[0] + "\\img\\blue.png")
        purpleimage = Image.open(os.path.split(os.path.realpath(__file__))[0] + "\\img\\purple.png")

        for i in range(6):
            the_angle = i * self.angle
            self.point1[i][X] = center[X] + radius * math.cos(the_angle + self.xw_angle)
            self.point1[i][Y] = center[Y] + radius * math.sin(the_angle + self.xw_angle)

            # 旋转图片
            rotated_blueimage = blueimage.rotate(-i * 60 + 20)
            rotated_purpleimage = purpleimage.rotate(-i * 60 + 20)

            # 将旋转后的PIL的Image对象转换为Tkinter的PhotoImage对象
            blueimg = ImageTk.PhotoImage(rotated_blueimage)
            purpleimg = ImageTk.PhotoImage(rotated_purpleimage)

            self.blue.append(blueimg)
            self.purple.append(purpleimg)

        self.colors[RED][FULL] = '#f88dff'
        self.colors[RED][NOTFULL] = '#a75fff'
        self.colors[BLUE][FULL] = '#6aaffc'
        self.colors[BLUE][NOTFULL] = '#0277fa'

    def draw_circle(self, canvas, color_flag, full_flag):
        canvas.create_oval(self.center[0] - 8, self.center[1] - 8, self.center[0] + 8, self.center[1] + 8,
                           fill=self.colors[color_flag][full_flag])

    def draw_flower(self, canvas, petal_num, color_flag, full_flag):
        for i in range(petal_num):
            x1 = self.point1[i][X]
            y1 = self.point1[i][Y]

            canvas.create_image(x1, y1, image=self.blue[i] if color_flag == BLUE else self.purple[i])


def update_gui_from_queue(root, canvas, butterfly_draw: ButterflyImg, last_data):
    try:
        # 非阻塞地从队列中获取数据
        data = data_queue.get_nowait()
        # data = (last_data + 1) % 7 if last_data is not None else 0

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

    f = open(os.path.split(os.path.realpath(__file__))[0] + '\\config.json', 'r')
    res = json.loads(f.read())
    f.close()

    size_rate = res["size"]
    radius_rate = res["radius"]

    size_base = 0.2775 * size_rate
    canvas_size = size_base * screenheight
    # size_base = 0.5

    # 创建一个Canvas用于绘制花瓣
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black',
                       highlightthickness=0)
    canvas.pack()

    # 设置花瓣的中心点和半径
    center = (canvas_size / 2, canvas_size / 2)
    radius = canvas_size / 7 * radius_rate
    butterfly_draw = ButterflyImg()
    butterfly_draw.init_ButterflyImg(center, radius)

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
    root.lift()
    root.wm_attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")

    # 启动周期性的GUI更新函数
    root.after(100, update_gui_from_queue, root, canvas, butterfly_draw, None)

    # 启动tkinter mainloop
    root.mainloop()


# draw_overlay()
