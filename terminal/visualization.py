import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import matplotlib.dates as mdates

class Visualization:
    def __init__(self, master, data_processing, real_time_tab, history_tab, device_status_tab):
        self.master = master
        self.data_processing = data_processing
        self.real_time_tab = real_time_tab
        self.history_tab = history_tab
        self.device_status_tab = device_status_tab
        self.real_time_data = []
        self.sensor_type = None
        self.create_widgets()

    def create_widgets(self):
        # 创建实时数据可视化组件
        self.real_time_frame = ttk.Frame(self.real_time_tab)
        self.real_time_frame.pack(fill=tk.BOTH, expand=True)
        self.historical_frame = ttk.Frame(self.history_tab)
        self.device_status_label = ttk.Label(self.device_status_tab, text="设备状态:")

        self.fig_real_time = plt.Figure(figsize=(12, 6), dpi=100)
        self.real_time_canvas = FigureCanvasTkAgg(self.fig_real_time, master=self.real_time_frame)
        self.real_time_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 创建开始和暂停按钮
        self.start_button = ttk.Button(self.real_time_frame, text="开始", command=self.start_data_collection, state="disabled")
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = ttk.Button(self.real_time_frame, text="暂停", command=self.pause_data_collection, state="disabled")
        self.pause_button.pack(side=tk.LEFT, padx=10)

        # 创建历史数据可视化组件
        self.historical_frame = ttk.Frame(self.history_tab)
        self.historical_frame.pack(fill=tk.BOTH, expand=True)

        self.fig_historical = plt.Figure(figsize=(12, 6), dpi=100)
        self.historical_canvas = FigureCanvasTkAgg(self.fig_historical, master=self.historical_frame)
        self.historical_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 创建时间范围选择下拉菜单
        self.time_range_label = ttk.Label(self.historical_frame, text="时间范围:")
        self.time_range_label.pack(side=tk.LEFT, padx=10)
        self.time_range_combobox = ttk.Combobox(self.historical_frame, values=["分钟", "小时", "天", "月", "年"], state="readonly")
        self.time_range_combobox.current(0)  # 默认选择"分钟"
        self.time_range_combobox.pack(side=tk.LEFT, padx=10)
        self.time_range_combobox.bind("<<ComboboxSelected>>", self.update_historical_data)

        # 创建设备状态显示组件
        self.device_status_label = ttk.Label(self.device_status_tab, text="设备状态:")
        self.device_status_label.pack()

    def start_data_collection(self, device_id, sensor_id):
        self.data_collection_running = True
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.show_real_time_data(device_id, sensor_id)

    def pause_data_collection(self):
        self.data_collection_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")

    def show_real_time_data(self, device_id, sensor_id):
        if not self.data_collection_running:
            return

        real_time_data = self.data_processing.get_real_time_data(device_id, sensor_id)
        sensor_type = self.data_processing.get_sensor_type(device_id, sensor_id)

        if real_time_data:
            self.real_time_data.append(real_time_data)
            if len(self.real_time_data) > 60:  # 保留最近1分钟的数据
                self.real_time_data = self.real_time_data[-60:]

            self.fig_real_time.clear()

            if sensor_type == 'MPU6050':
                self.sensor_type = 'MPU6050'
                ax1 = self.fig_real_time.add_subplot(211)
                ax1.set_title('实时数据 - 加速度')
                ax1.set_xlabel('时间')
                ax1.set_ylabel('加速度 (m/s^2)')
                times = [data['time'] for data in self.real_time_data]
                ax1.plot(times, [data['acc_x'] for data in self.real_time_data], label='X')
                ax1.plot(times, [data['acc_y'] for data in self.real_time_data], label='Y')
                ax1.plot(times, [data['acc_z'] for data in self.real_time_data], label='Z')
                ax1.legend(loc='upper right')  # 固定图例位置
                ax1.set_ylim(-20, 20)
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置X轴时间戳格式

                ax2 = self.fig_real_time.add_subplot(212)
                ax2.set_title('实时数据 - 角速度')
                ax2.set_xlabel('时间')
                ax2.set_ylabel('角速度 (deg/s)')
                ax2.plot(times, [data['gyro_x'] for data in self.real_time_data], label='X')
                ax2.plot(times, [data['gyro_y'] for data in self.real_time_data], label='Y')
                ax2.plot(times, [data['gyro_z'] for data in self.real_time_data], label='Z')
                ax2.legend(loc='upper right')  # 固定图例位置
                ax2.set_ylim(-360, 360)
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))  # 设置X轴时间戳格式

            elif sensor_type == 'TempHumidity':
                self.sensor_type = 'TempHumidity'
                ax1 = self.fig_real_time.add_subplot(211)
                ax1.set_title('实时数据 - 温度')
                ax1.set_xlabel('时间')
                ax1.set_ylabel('温度 (°C)')
                times = [data['time'] for data in self.real_time_data]
                ax1.plot(times, [data['temperature'] for data in self.real_time_data])
                ax1.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))  # 设置X轴时间戳格式为自动

                ax2 = self.fig_real_time.add_subplot(212)
                ax2.set_title('实时数据 - 湿度')
                ax2.set_xlabel('时间')
                ax2.set_ylabel('湿度 (%)')
                ax2.plot(times, [data['humidity'] for data in self.real_time_data])
                ax2.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))  # 设置X轴时间戳格式为自动

            self.real_time_canvas.draw()

        self.master.after(1000, self.show_real_time_data, device_id, sensor_id)  # 每秒更新一次

    def update_historical_data(self, event=None, device_id=None, sensor_id=None):
        if device_id is None or sensor_id is None:
            return

        time_range = self.time_range_combobox.get()

        end_time = datetime.now()
        if time_range == "分钟":
            start_time = end_time - timedelta(minutes=60)
        elif time_range == "小时":
            start_time = end_time - timedelta(hours=1)
        elif time_range == "天":
            start_time = end_time - timedelta(days=1)
        elif time_range == "月":
            start_time = end_time - timedelta(days=30)
        else:  # 年
            start_time = end_time - timedelta(days=365)

        historical_data = self.data_processing.get_historical_data(device_id, sensor_id, start_time, end_time)
        self.show_historical_data(historical_data)

    def show_historical_data(self, historical_data):
        self.fig_historical.clear()
        ax = self.fig_historical.add_subplot(111)

        if historical_data:
            if 'temperature' in historical_data:
                ax.set_title('历史数据 - 温度/湿度')
                ax.set_xlabel('时间')
                ax.set_ylabel('温度 (°C) / 湿度 (%)')
                ax.plot(historical_data['time'], historical_data['temperature'], label='温度')
                ax.plot(historical_data['time'], historical_data['humidity'], label='湿度')
                ax.legend()
                ax.set_ylim(0, 100)  # 固定Y轴范围

        self.historical_canvas.draw()

    def show_device_status(self, device_id):
        device_status = self.data_processing.get_device_status(device_id)
        self.device_status_label.config(text=f"设备状态: {device_status}")
        self.master.after(5000, self.show_device_status, device_id)  # 每5秒更新一次

    def update_button_states(self, device_id, sensor_id):
        if device_id and sensor_id:
            self.start_button.config(state="normal")
            if self.data_collection_running:
                self.pause_button.config(state="normal")
            else:
                self.pause_button.config(state="disabled")
        else:
            self.start_button.config(state="disabled")
            self.pause_button.config(state="disabled")