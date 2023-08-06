import sqlite3

from corgidb.objects.table import Table
from corgidb.constants import *
from corgidb.exceptions import *

class Utils:
    """
    This is a class for executing basic sqlite3 operations or to be called utilities class

    Attributes:
        connection (sqlite3.Connection): a Connection to the database it self
    """

    def __init__(self, connection: sqlite3.Connection, database_path: str):
        """
        The constructor for Utils class

        Parameters:
            connection (sqlite3.Connection): a Connection to the database it self
        """
        self.connection = connection
        self.cursor     = self.connection.cursor()
        self.database_path = database_path
        



    def sqlcmd(self, command: str):
        """
        This function to execute raw SQL command not recommened to be called if not necessary cannot return any data

        Parameters:
            command (str)   : Raw SQLite command
        
        Returns:
            list            : a list of fetched sql data return empty list if not fetched
        """
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            if "SELECT" in command.upper(): 
                cursor.execute(command)
                return cursor.fetchall()
            else:
                cursor.execute(command)
                return []

    
    def create_table(self, name: str, columns: list):
        """
        Create Table on the previously set *.sqlite file
        
        Parameters:
            name    (str)   : The name of the table which cannot be duplicate and cannot be named "sqlite_sequence" as the name is being use for auto increment
            columns (list)  : Table columns name and datatypes in tuple which can be int, float, bool, str

        Returns:
            Table           : A Table SQL Class
        """
        self.__check_create_table(name=name, columns=columns)

        # Create SQL command
        sql = f"CREATE TABLE {name} (row_id INTEGER PRIMARY KEY AUTOINCREMENT,"
        for column in columns:
            sql += f"{column[0]} {SQLDATATYPE[column[1]]},"
        sql = sql[0:-1] + ");"
        
   
        with self.connection:
            self.cursor.execute(sql)

        # Return Table object
        return Table(name=name, connection=self.connection, database_path=self.database_path)

    def delete_table(self, name: str, keep_table: bool=False):
        """
        Delete table on database

        Parameters:
            name        (str)   : Name of the Table that you wish to be delete
            keep_table  (bool)  : Delete only data of the table
        """
        if keep_table:
            self.sqlcmd(f"TRUNCATE TABLE {name};")
        else:
            self.sqlcmd(f"DROP TABLE {name};")

    def get_table(self, name: str):
        """
        Create table objects from already exists table on database

        Parameters:
            name    (str) : Name of already exist table

        Returns:
            Table         : class table object
        """
        return Table(name=name, connection=self.connection, database_path=self.database_path)


    def __check_create_table(self, name: str, columns: list):
        invalids = [column for column in columns if not any([type(column) is tuple, len(column)==2, type(column[0]) in [str, int], column[0] != "row_id", column[1] in list(SQLDATATYPE.keys())])]
        if len(invalids) != 0 or name=="sqlite_sequence":
            raise CreateTableArgumentsError()





