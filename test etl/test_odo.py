# -*- coding: utf-8 -*-

from odo import odo
import psycopg2
import time

'''
postgresql://localhost::accounts
postgresql://username:password@54.252.14.53:10000/default::accounts
SQL uris consist of the following

dialect protocol: postgresql://
Optional authentication information: username:password@
A hostname or network location with optional port: 54.252.14.53:10000
Optional database/schema name: /default
A table name with the :: separator: ::accounts

>>> odo(df, list)  # create new list from Pandas DataFrame
>>> odo(df, [])  # append onto existing list
>>> odo(df, 'myfile.json')  # Dump dataframe to line-delimited JSON
>>> odo('myfiles.*.csv', Iterator) # Stream through many CSV files
>>> odo(df, 'postgresql://hostname::tablename')  # Migrate dataframe to Postgres
>>> odo('myfile.*.csv', 'postgresql://hostname::tablename')  # Load CSVs to Postgres
>>> odo('postgresql://hostname::tablename', 'myfile.json') # Dump Postgres to JSON
>>> odo('mongodb://hostname/db::collection', pd.DataFrame) # Dump Mongo to DataFrame
'''

# 歷史報價
# source_folder = '/Users/sky_wu/Dropbox/myprojects/hunting/database/3-test/'
source_folder = './'


def import_symbol():
    src_csv = source_folder + 'symbol.csv'
    # 股市代號
    dest_table = 'postgresql://stock:stock@localhost:5432/stock::symbol'
    odo(src_csv, dest_table)

def import_quotes():
    src_csv = source_folder + 'tse.csv'
    # symbol_id,trade_date,volume,amout,open,high,low,close,change,trans
    # 股市交易：原始檔案有不合理資料需處理 (X, -)
    dest_table = 'postgresql://stock:stock@localhost:5432/stock::quotes'
    odo(src_csv, dest_table)

def test_import():
    # 測試匯入
    src_csv = source_folder + 'symbol.csv'

    dest_db_no_table = 'postgresql://stock:stock@localhost:5432/stock::symbol_id'
    dest_db_no_data = 'postgresql://stock:stock@localhost:5432/stock::symbol'
    # 會自動生成表格 (第一有欄位)
    odo(src_csv, dest_db_no_table)
    # 重複會入會有PKEY錯誤
    odo(src_csv, dest_db_no_data)

if __name__ == '__main__':
    import_quotes()

