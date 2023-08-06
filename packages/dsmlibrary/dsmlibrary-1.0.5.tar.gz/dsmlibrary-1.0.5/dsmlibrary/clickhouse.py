from tkinter.messagebox import NO
from .base import Base

from clickhouse_driver import Client
from .utils.clickhouse import create_table, insert_ddf, insert_df
import pandas as pd
import dask.dataframe as dd

class ClickHouse:
    
    def __init__(self, connection=None):
        if connection is None or type(connection)!= dict:
            """ 
            connection = {
                'host': 'localhost',
                'port': 9090,
                'database': 'warehouse',
                'user': 'clickhouse',
                'password': 'QWER!@#$qwer1234!@#$',
                'settings':{
                    'use_numpy': True
                },
                'secure': False
            }
            """
            raise Exception(f"plase input `connection` or but got connection {type(connection)}")
        client = Client(**connection)
        try:
            client.connection.connect()
        except Exception as e:
            raise e
        self._client = client
        self._connection = connection
        
    def get_or_createTable(self, ddf=None, df=None, tableName=None, key=None):
        if (ddf is None) and (df is None):
            raise Exception("Please input ddf(dask dataframe) or df(pandas dataframe)")
        if (type(ddf) != dd.DataFrame) and (type(df) != pd.DataFrame):
            raise Exception("Invalid type expect ddf(dask dataframe) or df(pandas dataframe)")
        if tableName is None:
            raise Exception("Please input `tableName`")
        if key is None:
            raise Exception("Please input `key`")
        _df = ddf if type(ddf) != None else df
        if key not in _df.columns:
            raise Exception(f"key `{key}` not found in columns, columns are {_df.columns}")
        status, e = create_table(self._client, _df, tableName, key)
        if status == False:
            if e.code == 57:
                print(f"table {tableName} already exists!")
            else:
                raise e
        return tableName
    
    def write(self, ddf=None, df=None, tableName=None, key=None):
        if tableName == None:
            raise Exception(f"Expect `tableName` type str, but got {type(tableName)} please input `tableName` str")
        if (ddf is None) and (df is None):
            raise Exception("Please input ddf(dask dataframe) or df(pandas dataframe)")
        if key is None:
            raise Exception("Please input `key`")
        _df = ddf if type(ddf) != None else df
        if key not in _df.columns:
            raise Exception(f"key `{key}` not found in columns, columns are {_df.columns}")
        if (ddf is not None) and (type(ddf) == dd.DataFrame):
            insert_ddf(connection=self._connection, ddf=ddf, tableName=tableName)
        elif (df is not None) and (type(df) == pd.DataFrame):
            insert_df(connection=self._connection, df=df, tableName=tableName)
    
    
    def read(self, sqlQuery=None):
        if sqlQuery is None:
            raise Exception(f"plese input `sqlQuery` str but got {type(sqlQuery)}")
        return self._client.query_dataframe(sqlQuery)