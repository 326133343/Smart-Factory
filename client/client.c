#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "cJSON.h"
#include "tcp_client.h"
#include "sensor_mpu6050.h"
#include "sensor_temp_humidity.h"
#include <unistd.h>

#define DEVICE_ID 1
#define SENSOR_ID_MPU6050 101
#define SENSOR_ID_TEMP_HUMIDITY 102
static const char device_status[] = "Active";
static const char device_name[] = "Device1";
static const char device_type[] = "Sensor";
//192.168.110.29
//169.254.231.242
int main() 
{
    TCPClient tcp_client;
    tcp_client_init(&tcp_client, "192.168.110.29", 8000);//服务器地址+监听端口

    //生成传感器信息
    char sensor_name_mpu6050[] = "MPU6050";
    char sensor_type_mpu6050[] = "Accelerometer";
    char sensor_name_temp_humidity[] = "TempHumidity";
    char sensor_type_temp_humidity[] = "TempHumiditySensor";

    //模拟数据采集和发送
    while (1) 
    {
        //生成时间戳
        time_t now = time(NULL);
        char current_time[26];
        strftime(current_time, sizeof(current_time), "%Y-%m-%d %H:%M:%S", localtime(&now));

        //获取MPU6050数据
        MPU6050Data mpu6050_data;
        mpu6050_read_data(&mpu6050_data);

        //获取温湿度数据
        TempHumidityData temp_humidity_data;
        temp_humidity_read_data(&temp_humidity_data);

        //构造要发送的JSON数据
        cJSON *data = cJSON_CreateObject();
        cJSON_AddNumberToObject(data, "device_id", DEVICE_ID);
        cJSON_AddStringToObject(data, "device_name", device_name);
        cJSON_AddStringToObject(data, "device_type", device_type);
        cJSON_AddStringToObject(data, "device_status", device_status);
        cJSON_AddStringToObject(data, "create_time", current_time);

        cJSON *mpu6050_json = cJSON_CreateObject();
        cJSON_AddNumberToObject(mpu6050_json, "sensor_id", SENSOR_ID_MPU6050);
        cJSON_AddStringToObject(mpu6050_json, "sensor_name", sensor_name_mpu6050);
        cJSON_AddStringToObject(mpu6050_json, "sensor_type", sensor_type_mpu6050);
        cJSON_AddNumberToObject(mpu6050_json, "acc_x", mpu6050_data.acc_x);
        cJSON_AddNumberToObject(mpu6050_json, "acc_y", mpu6050_data.acc_y);
        cJSON_AddNumberToObject(mpu6050_json, "acc_z", mpu6050_data.acc_z);
        cJSON_AddNumberToObject(mpu6050_json, "gyro_x", mpu6050_data.gyro_x);
        cJSON_AddNumberToObject(mpu6050_json, "gyro_y", mpu6050_data.gyro_y);
        cJSON_AddNumberToObject(mpu6050_json, "gyro_z", mpu6050_data.gyro_z);
        cJSON_AddStringToObject(mpu6050_json, "unit_acc", mpu6050_data.unit_acc);
        cJSON_AddStringToObject(mpu6050_json, "unit_gyro", mpu6050_data.unit_gyro);
        cJSON_AddStringToObject(mpu6050_json, "time", current_time);
        cJSON_AddItemToObject(data, "mpu6050_data", mpu6050_json);

        cJSON *temp_humidity_json = cJSON_CreateObject();
        cJSON_AddNumberToObject(temp_humidity_json, "sensor_id", SENSOR_ID_TEMP_HUMIDITY);
        cJSON_AddStringToObject(mpu6050_json, "sensor_name", sensor_name_temp_humidity);
        cJSON_AddStringToObject(mpu6050_json, "sensor_type", sensor_type_temp_humidity);
        cJSON_AddNumberToObject(temp_humidity_json, "temperature", temp_humidity_data.temperature);
        cJSON_AddNumberToObject(temp_humidity_json, "humidity", temp_humidity_data.humidity);
        cJSON_AddStringToObject(temp_humidity_json, "unit_temp", temp_humidity_data.unit_temp);
        cJSON_AddStringToObject(temp_humidity_json, "unit_humidity", temp_humidity_data.unit_humidity);
        cJSON_AddStringToObject(temp_humidity_json, "time", current_time);
        cJSON_AddItemToObject(data, "temp_humidity_data", temp_humidity_json);

        //将数据转换为JSON字符串
        char *json_data = cJSON_PrintUnformatted(data);
        if (json_data == NULL) {
            fprintf(stderr, "Failed to print JSON data.\n");
        } else {
            tcp_client_send_data(&tcp_client, json_data); // 发送数据
            free(json_data);
        }
        cJSON_Delete(data);

        sleep(1);
    }

    tcp_client_close(&tcp_client);

    return EXIT_SUCCESS;
}