import json
from mysql.connector import Error

class DataProcessing:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def process_and_store_data(self, json_data):
        print(f"Received data: {json_data}")
        try:
            recv_data = json.loads(json_data)
            self.insert_data(recv_data)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON data: {e}")
        except Error as e:
            print(f"Error while processing data: {e}")

    def insert_data(self, data):
        if self.db_connection.connection is None:
            print("Database connection is not established.")
            return

        try:
            cursor = self.db_connection.connection.cursor()

            # 插入设备数据
            insert_device_query = "INSERT INTO Device (device_id, device_name, device_type, device_status, create_time) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE device_status=%s"
            cursor.execute(insert_device_query, (data['device_id'], data['device_name'], data['device_type'], data['device_status'], data['create_time'], data['device_status']))
            self.db_connection.connection.commit()

            # 插入MPU6050传感器数据
            if 'mpu6050_data' in data:
                mpu6050_data = data['mpu6050_data']
                insert_sensor_query = "INSERT INTO Sensor (sensor_id, sensor_name, sensor_type) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sensor_name=%s, sensor_type=%s"
                cursor.execute(insert_sensor_query, (mpu6050_data['sensor_id'], mpu6050_data['sensor_name'], mpu6050_data['sensor_type'], mpu6050_data['sensor_name'], mpu6050_data['sensor_type']))

                data_id_query = "INSERT INTO DataID (device_id, sensor_id, create_time) VALUES (%s, %s, %s)"
                cursor.execute(data_id_query, (data['device_id'], mpu6050_data['sensor_id'], data['create_time']))
                data_id = cursor.lastrowid

                mpu6050_query = "INSERT INTO MPU6050Data (data_id, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, unit_acc, unit_gyro, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mpu6050_values = (data_id, mpu6050_data['acc_x'], mpu6050_data['acc_y'], mpu6050_data['acc_z'], mpu6050_data['gyro_x'], mpu6050_data['gyro_y'], mpu6050_data['gyro_z'], mpu6050_data['unit_acc'], mpu6050_data['unit_gyro'], data['create_time'])
                cursor.execute(mpu6050_query, mpu6050_values)

            # 插入温湿度传感器数据
            if 'temp_humidity_data' in data:
                temp_humidity_data = data['temp_humidity_data']
                insert_sensor_query = "INSERT INTO Sensor (sensor_id, sensor_name, sensor_type) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE sensor_name=%s, sensor_type=%s"
                cursor.execute(insert_sensor_query, (temp_humidity_data['sensor_id'], temp_humidity_data['sensor_name'], temp_humidity_data['sensor_type'], temp_humidity_data['sensor_name'], temp_humidity_data['sensor_type']))

                data_id_query = "INSERT INTO DataID (device_id, sensor_id, create_time) VALUES (%s, %s, %s)"
                cursor.execute(data_id_query, (data['device_id'], temp_humidity_data['sensor_id'], data['create_time']))
                data_id = cursor.lastrowid

                temp_humidity_query = "INSERT INTO TempHumidityData (data_id, temperature, humidity, unit_temp, unit_humidity, time) VALUES (%s, %s, %s, %s, %s, %s)"
                temp_humidity_values = (data_id, temp_humidity_data['temperature'], temp_humidity_data['humidity'], temp_humidity_data['unit_temp'], temp_humidity_data['unit_humidity'], data['create_time'])
                cursor.execute(temp_humidity_query, temp_humidity_values)

            self.db_connection.connection.commit()
            print("Data inserted successfully.")
        except Error as e:
            self.db_connection.connection.rollback()  # 回滚以处理错误
            print(f"Failed to insert data: {e}")