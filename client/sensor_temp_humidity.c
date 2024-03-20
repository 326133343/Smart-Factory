#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "sensor_temp_humidity.h"

//初始化温湿度传感器
void temp_humidity_init(void) 
{
    srand(time(NULL));
}

//读取温湿度传感器数据
void temp_humidity_read_data(TempHumidityData *data)
{
    data->temperature = (float)rand() / RAND_MAX * 10.0 + 20.0;
    data->humidity = (float)rand() / RAND_MAX * 20.0 + 40.0;
    strcpy(data->unit_temp, "°C");
    strcpy(data->unit_humidity, "%RH");
}