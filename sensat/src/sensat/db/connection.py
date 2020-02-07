import pymysql
from sensat.config import DatabaseConfig


class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    def getConnection(self) -> pymysql.connections.Connection:
        if not self.connection or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                db=self.config.db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

        return self.connection

    def fetchAll(self, query: str, parameters: tuple) -> list:
        with self.getConnection().cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()
