#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "sensor_mpu6050.h"

void mpu6050_init(void) 
{
    //初始化MPU6050传感器
    srand(time(NULL));
}

void mpu6050_read_data(MPU6050Data *data) 
{
    //读取MPU6050传感器数据
    data->acc_x = (float)rand() / RAND_MAX * 20.0 - 10.0;
    data->acc_y = (float)rand() / RAND_MAX * 20.0 - 10.0;
    data->acc_z = (float)rand() / RAND_MAX * 20.0 - 10.0;
    data->gyro_x = (float)rand() / RAND_MAX * 360.0 - 180.0;
    data->gyro_y = (float)rand() / RAND_MAX * 360.0 - 180.0;
    data->gyro_z = (float)rand() / RAND_MAX * 360.0 - 180.0;
    strcpy(data->unit_acc, "m/s^2");
    strcpy(data->unit_gyro, "deg/s");
}