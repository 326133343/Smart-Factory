import tkinter as tk
from tkinter import ttk
from data_processing import DataProcessing
from visualization import Visualization

class Terminal:
    def __init__(self, master, data_processing):
        self.master = master
        master.title("生产数据终端")

        self.data_processing = data_processing

        # 创建选项卡
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.real_time_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.real_time_tab, text="实时数据")
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="历史数据")
        self.device_status_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.device_status_tab, text="设备状态")

        self.visualization = Visualization(master, self.data_processing, self.real_time_tab, self.history_tab, self.device_status_tab)

        self.create_widgets()

    def create_widgets(self):
        # 创建设备和传感器选择框
        self.create_selectors()

    def create_selectors(self):
        # 创建设备选择框
        device_label = ttk.Label(self.master, text="设备ID:")
        device_label.pack()
        self.device_combobox = ttk.Combobox(self.master, state="readonly")
        self.device_combobox.pack()
        self.device_combobox.bind("<<ComboboxSelected>>", self.update_sensor_options)
        self.device_combobox.bind("<<ComboboxSelected>>", self.update_button_states)

        # 创建传感器选择框
        sensor_label = ttk.Label(self.master, text="传感器ID:")
        sensor_label.pack()
        self.sensor_combobox = ttk.Combobox(self.master, state="readonly")
        self.sensor_combobox.pack()
        self.sensor_combobox.bind("<<ComboboxSelected>>", self.update_charts)
        self.sensor_combobox.bind("<<ComboboxSelected>>", self.update_button_states)

        # 更新设备选项
        self.update_device_options()

    def update_device_options(self):
        devices = self.data_processing.get_devices()
        self.device_combobox['values'] = devices
        self.device_combobox.set(devices[0] if devices else '')

    def update_sensor_options(self, event):
        device_id = self.device_combobox.get()
        sensors = self.data_processing.get_sensors_by_device(device_id)
        self.sensor_combobox['values'] = sensors
        self.sensor_combobox.set(sensors[0] if sensors else '')

    def update_charts(self, event):
        device_id = self.device_combobox.get()
        sensor_id = self.sensor_combobox.get()
        self.visualization.pause_data_collection()  # 暂停数据采集
        self.visualization.real_time_data.clear()  # 清除之前的实时数据
        self.visualization.start_data_collection(device_id, sensor_id)  # 开始新的数据采集
        self.visualization.update_historical_data(device_id=device_id, sensor_id=sensor_id)
        self.visualization.show_device_status(device_id)

    def update_button_states(self, event):
        device_id = self.device_combobox.get()
        sensor_id = self.sensor_combobox.get()
        self.visualization.update_button_states(device_id, sensor_id)

if __name__ == "__main__":
    root = tk.Tk()
    data_processing = DataProcessing()
    terminal = Terminal(root, data_processing)
    root.mainloop()