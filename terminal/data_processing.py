import random
from datetime import datetime, timedelta

class DataProcessing:
    def __init__(self):
        self.devices = ['1', '2']
        self.sensors = {
            '1': [('101', 'MPU6050'), ('102', 'TempHumidity')],
            '2': []
        }

    def get_devices(self):
        return self.devices

    def get_sensors_by_device(self, device_id):
        return [sensor[0] for sensor in self.sensors.get(device_id, [])]

    def get_sensor_type(self, device_id, sensor_id):
        for sensor in self.sensors.get(device_id, []):
            if sensor[0] == sensor_id:
                return sensor[1]
        return None

    def get_real_time_data(self, device_id, sensor_id):
        sensor_type = self.get_sensor_type(device_id, sensor_id)
        if sensor_type == 'MPU6050':
            return {
                'acc_x': random.uniform(-10, 10),
                'acc_y': random.uniform(-10, 10),
                'acc_z': random.uniform(-10, 10),
                'gyro_x': random.uniform(-180, 180),
                'gyro_y': random.uniform(-180, 180),
                'gyro_z': random.uniform(-180, 180),
                'time': datetime.now()
            }
        elif sensor_type == 'TempHumidity':
            return {
                'temperature': random.uniform(20, 30),
                'humidity': random.uniform(40, 60),
                'time': datetime.now()
            }

    def get_historical_data(self, device_id, sensor_id, start_time, end_time):
        sensor_type = self.get_sensor_type(device_id, sensor_id)
        if sensor_type == 'MPU6050':
            return {
                'acc_x': [random.uniform(-10, 10) for _ in range(100)],
                'acc_y': [random.uniform(-10, 10) for _ in range(100)],
                'acc_z': [random.uniform(-10, 10) for _ in range(100)],
                'gyro_x': [random.uniform(-180, 180) for _ in range(100)],
                'gyro_y': [random.uniform(-180, 180) for _ in range(100)],
                'gyro_z': [random.uniform(-180, 180) for _ in range(100)],
                'time': [start_time + timedelta(seconds=i) for i in range(100)]
            }
        elif sensor_type == 'TempHumidity':
            return {
                'temperature': [random.uniform(20, 30) for _ in range(100)],
                'humidity': [random.uniform(40, 60) for _ in range(100)],
                'time': [start_time + timedelta(seconds=i) for i in range(100)]
            }

    def get_device_status(self, device_id):
        return random.choice(['正常', '警告', '故障'])