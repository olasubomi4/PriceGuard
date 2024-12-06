import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine


class PostgreSql:
    load_dotenv()

    def __init__(self):
        self.__dbName=os.environ['DB_NAME']
        self.__dbPassword=os.environ['DB_PASSWORD']
        self.__dbUser=os.environ['DB_USER']
        self.__dbHost=os.environ['DB_HOST']
        self.__dbPort=os.environ['DB_PORT']

    def __getConnectionEngine(self):
        connection_string = f"postgresql://{self.__dbUser}:{self.__dbPassword}@{self.__dbHost}:{self.__dbPort}/{self.__dbName}"
        engine = create_engine(connection_string)
        return engine

    def __connect(self):
        return psycopg2.connect(database=self.__dbName,host=self.__dbHost,port=self.__dbPort,password=self.__dbPassword,user=self.__dbUser)

    def __getConn(self):
        return self.__connect()
    def execute(self):
        with self.__getConn() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM demo WHERE "Id" = 1;')
                res = cur.fetchone()
                return res

    def insertProducts(self, data:pd.DataFrame,productName:str):
        # with self.__getConn() as conn:
        try:
            data.to_sql(productName, con=self.__getConnectionEngine(), index=False,
                      if_exists="replace")
        except Exception as e:
            print(e)

    def retrieveTableAsDataFrame(self,tableName:str):
        return pd.read_sql_table(tableName,con=self.__getConnectionEngine())


    def dropTable(self, tableName:str):
        self.execute(f"DROP TABLE {tableName};")

    def execute(self,query:str):
        with self.__getConn() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                res = cur.fetchone()
                return res


if __name__ == '__main__':
    result= PostgreSql().getTablehasDataFrame(tableName='Iphone 16')
    print(result)




