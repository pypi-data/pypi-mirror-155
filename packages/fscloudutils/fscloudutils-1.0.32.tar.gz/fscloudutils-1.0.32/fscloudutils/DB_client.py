
import mysql.connector
import pandas as pd
from pandas import DataFrame

# dir_path = os.path.dirname(sys.argv[0])
# os.chdir(dir_path)
'''tables = ['fruit_variety', 'project', 'project_plot', 'plot', 'customer','caliber']'''


class DBClient:
    def __init__(self, db_server: str, db_user: str, db_password: str, db_name: str):
        self._connector = None
        self.db_server = db_server
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name

    def connect(self):
        self._connector = mysql.connector.connect(
            host=self.db_server,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name)

    def execute(self, SQL_command: str, params=()) -> None:
        self.connect()
        cursor = self._connector.cursor()
        cursor.execute(SQL_command, params=params)
        self._connector.commit()
        cursor.close()
        self.close_connection()

    def select(self, SQL_command: str, params=()) -> pd.DataFrame:
        self.connect()
        cursor = self._connector.cursor()
        cursor.execute(SQL_command, params=params)
        df = DataFrame(cursor.fetchall(), columns=[i[0] for i in cursor.description])
        cursor.close()
        self.close_connection()
        return df

    def close_connection(self):
        self._connector.close()
