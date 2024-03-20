#ifndef SENSOR_TEMP_HUMIDITY_H
#define SENSOR_TEMP_HUMIDITY_H

typedef struct 
{
    float temperature;
    float humidity;
    char unit_temp[10];
    char unit_humidity[10];
} TempHumidityData;

void temp_humidity_init(void);
void temp_humidity_read_data(TempHumidityData *data);

#endif