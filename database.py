import sqlite3


class Database:
    """Initializes and manipulates SQLite3 database."""
    def __init__(self, db_name='sample.db'):
        self.db_name = db_name
        self.__connection = None
        self.__cursor = None

    def connect(self):
        """
        :return: Connection handle to the SQLite3 database
        """
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.ProgrammingError as e:
            print(e)

    def close(self):
        """Close the SQLite3 database."""
        try:
            self.__connection.close()
        except sqlite3.ProgrammingError as e:
            print(e)

    def query(self, query):
        """Execute SQL query."""
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query)
            self.__connection.commit()
        except sqlite3.Error as e:
            print(e, query)
        finally:
            self.close()

    def select(self, query):
        """
        :param query: SQL statement
        :return: Data from executed query
        """
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query)
            return self.__cursor.fetchall()
        except sqlite3.Error as e:
            print(e, query)
        finally:
            self.close()
