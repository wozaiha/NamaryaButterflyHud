import math
import queue

from dataqueue import data_queue
import tkinter as tk
from tkinter import font


class FlowerDraw:
    angle = 2 * math.pi / 6
    sepa = angle / 3
    outline_width = 1
    point_x1 = [0, 0, 0, 0, 0, 0]
    point_y1 = [0, 0, 0, 0, 0, 0]
    point_x2 = [0, 0, 0, 0, 0, 0]
    point_y2 = [0, 0, 0, 0, 0, 0]

    point_outline_x1 = [0, 0, 0, 0, 0, 0]
    point_outline_y1 = [0, 0, 0, 0, 0, 0]
    point_outline_x2 = [0, 0, 0, 0, 0, 0]
    point_outline_y2 = [0, 0, 0, 0, 0, 0]

    center = None
    radius = None

    RED = 0
    BLUE = 1
    FULL = 0
    NOTFULL = 1
    colors = [['', ''], ['', '']]

    def init_FlowerDraw(self, center, radius):
        self.center = center
        self.radius = radius
        for i in range(6):
            start_angle = i * self.angle + self.sepa
            end_angle = start_angle + self.angle - self.sepa
            self.point_x1[i] = center[0] + (radius - self.outline_width) * math.cos(start_angle)
            self.point_y1[i] = center[1] + (radius - self.outline_width) * math.sin(start_angle)
            self.point_x2[i] = center[0] + (radius - self.outline_width) * math.cos(end_angle)
            self.point_y2[i] = center[1] + (radius - self.outline_width) * math.sin(end_angle)

            self.point_outline_x1[i] = center[0] + radius * math.cos(start_angle)
            self.point_outline_y1[i] = center[1] + radius * math.sin(start_angle)
            self.point_outline_x2[i] = center[0] + radius * math.cos(end_angle)
            self.point_outline_y2[i] = center[1] + radius * math.sin(end_angle)
        self.colors[self.RED][self.FULL] = '#DDAADD'
        self.colors[self.RED][self.NOTFULL] = '#CC00CC'
        self.colors[self.BLUE][self.FULL] = '#AADDDD'
        self.colors[self.BLUE][self.NOTFULL] = '#00BBBB'

    def draw_circle(self, canvas, color_flag, full_flag):
        canvas.create_oval(self.center[0] - 10, self.center[1] - 10, self.center[0] + 10, self.center[1] + 10,
                           fill=self.colors[color_flag][full_flag])

    def draw_flower(self, canvas, petal_num, color_flag, full_flag):
        for i in range(petal_num):
            x1 = self.point_outline_x1[i]
            y1 = self.point_outline_y1[i]
            x2 = self.point_outline_x2[i]
            y2 = self.point_outline_y2[i]
            canvas.create_polygon(self.center[0], self.center[1], x1, y1, x2, y2, fill="#E0E0E0", outline="#E0E0E0",
                                  width=self.outline_width)
            x1 = self.point_x1[i]
            y1 = self.point_y1[i]
            x2 = self.point_x2[i]
            y2 = self.point_y2[i]
            canvas.create_polygon(self.center[0], self.center[1], x1, y1, x2, y2,
                                  fill=self.colors[color_flag][full_flag], outline="#E0E0E0", width=0.5)


def update_gui_from_queue(root, canvas, flower_draw, last_data):
    try:
        # 非阻塞地从队列中获取数据
        data = data_queue.get_nowait()

        if last_data != data:
            last_data = data
            # 使用队列中的数据更新GUI
            num = data % 10
            color_flag = flower_draw.RED if data >= 10 else flower_draw.BLUE
            full_flag = flower_draw.FULL if num == 6 else flower_draw.NOTFULL

            canvas.delete("all")
            flower_draw.draw_flower(canvas, num, color_flag, full_flag)
            flower_draw.draw_circle(canvas, color_flag, full_flag)

        # 清除队列中的数据标记为已处理
        data_queue.task_done()
    except queue.Empty:
        # 队列为空，没有新数据
        pass
    # 100毫秒后再次调用自身进行更新
    root.after(100, update_gui_from_queue, root, canvas, flower_draw, last_data)


def draw_overlay():
    root = tk.Tk()
    root.title("Namarya Butterfly HUD")

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()

    size_base = 0.2775
    canvas_size = size_base * screenheight

    # 创建一个Canvas用于绘制花瓣
    canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg='black', highlightthickness=0)
    canvas.pack()

    # 设置花瓣的中心点和半径
    center = (canvas_size / 2, canvas_size / 2)
    radius = canvas_size / 4
    flower_draw = FlowerDraw()
    flower_draw.init_FlowerDraw(center, radius)

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
    root.after(100, update_gui_from_queue, root, canvas, flower_draw, None)

    # 启动tkinter mainloop
    root.mainloop()