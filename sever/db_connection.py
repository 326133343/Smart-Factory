import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to the database.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None


    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")