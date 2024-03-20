from tcp_connection import TCPServer
from db_connection import DatabaseConnection
from data_processing import DataProcessing

if __name__ == '__main__':
    #创建数据库连接
    db_connection = DatabaseConnection('127.0.0.1', 'mydb', 'root', '123456')
    db_connection.connect()

    #调用数据处理
    data_processing = DataProcessing(db_connection)

    #创建TCP服务器
    server = TCPServer('0.0.0.0', 8000, data_processing)

    #启动TCP服务器
    server.start()
