import mysql.connector

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='123456',
            database='mydb'
        )

    def get_devices(self):
        cursor = self.connection.cursor()
        query = "SELECT device_id FROM Device"
        cursor.execute(query)
        devices = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        return devices

    def get_sensors_by_device(self, device_id):
        cursor = self.connection.cursor()
        query = "SELECT sensor_id FROM Sensor WHERE device_id = %s"
        cursor.execute(query, (device_id,))
        sensors = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        return sensors

    def get_sensor_type(self, sensor_id):
        cursor = self.connection.cursor()
        query = "SELECT sensor_type FROM Sensor WHERE sensor_id = %s"
        cursor.execute(query, (sensor_id,))
        sensor_type = cursor.fetchone()[0]
        cursor.close()
        return sensor_type

    def get_latest_data(self, sensor_id):
        # 从数据库获取指定传感器的最新数据
        # 根据传感器类型返回相应的数据格式
        pass

    def get_historical_data(self, sensor_id, start_time, end_time):
        # 从数据库获取指定传感器在给定时间范围内的历史数据
        # 根据传感器类型返回相应的数据格式
        pass

    def get_device_status(self, device_id):
        # 从数据库获取指定设备的状态信息
        pass