#ifndef SENSOR_MPU6050_H
#define SENSOR_MPU6050_H

typedef struct 
{
    float acc_x;
    float acc_y;
    float acc_z;
    float gyro_x;
    float gyro_y;
    float gyro_z;
    char unit_acc[10];
    char unit_gyro[10];
} MPU6050Data;

void mpu6050_init(void);
void mpu6050_read_data(MPU6050Data *data);

#endif // SENSOR_MPU6050_H