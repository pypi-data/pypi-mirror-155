import string
import pymysql
import os


class DatabaseService:

    def __init__(self,
                 host: str,
                 database_name: str,
                 port: int,
                 user: string,
                 passwd: str) -> None:
        
        self.host = host
        self.database_name = database_name
        self.port = port
        self.user = user
        self.passwd = passwd

    def __connect__(self):

        self.db_connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            database=self.database_name
        )

        self.cursor = self.db_connection.cursor(pymysql.cursors.DictCursor)

    def __commit__(self):
        self.db_connection.commit()

    def __disconnect__(self):
        self.db_connection.close()

    # TODO create and close a connection for each execution is quite expensive. Use pool?
    def execute(self, sql, data):
        try:
            self.__connect__()
            self.cursor.execute(sql, data)
            self.__commit__()
        except Exception as e:
            print(e)
        finally:
            self.__disconnect__()

    def get_all_rows(self, sql, data):
        self.__connect__()
        self.cursor.execute(sql, data)
        records = self.cursor.fetchall()
        return records

    def execute_all(self, sql, data):
        self.__connect__()
        self.cursor.executemany(sql, data)
        self.db_connection.commit()
        self.__disconnect__()
