# 编译器和编译选项
CC=arm-linux-gnueabihf-gcc
CFLAGS=-Wall
LDFLAGS=-static

# 源文件和目标文件
SRCS = client.c tcp_client.c sensor_mpu6050.c sensor_temp_humidity.c cJSON.c
OBJS = $(SRCS:.c=.o)
TARGET = client

# 头文件路径
INCLUDE_PATHS = -I./

# 默认目标
all: $(TARGET)

# 编译目标
$(TARGET): $(OBJS)
	$(CC) $(OBJS) $(LDFLAGS) -o $@ $(INCLUDE_PATHS)

# 编译源文件
%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDE_PATHS) -c $< -o $@

# 清理目标文件和可执行文件
clean:
	rm -f $(OBJS) $(TARGET)

# 伪目标
.PHONY: all clean
