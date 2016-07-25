# -*- coding: utf-8 -*-

import petl as etl
import csv
import psycopg2

# set up a CSV file to demonstrate with
_CONNECTION = 'dbname=stock user=stock password=stock'
_DATA_PATH = './data/'
_HEADER = 'symbol_id,trade_date,volume,amout,open,high,low,close,change,trans'.split(',')
_ORIGINAL = _DATA_PATH + 'before.csv' #'origin.csv'
_TRANSFORMED = _DATA_PATH + 'after.csv'
_SELECTED = _DATA_PATH + 'select.csv'

'''---note---
  2017/07/25 CSV file cannot conatain the empty row...
'''

def test_etl_csv():
    table1 = [['foo', 'bar'],
              ['a', 1],
              ['b', 2],
              ['c', 2]]
    with open('example.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table1)

    # now demonstrate the use of fromcsv()
    table2 = etl.fromcsv('example.csv')
    print(table2)

def test_transform():
    src = _ORIGINAL
    dest = _TRANSFORMED
    #_table = [_HEADER]
    #

    src_table=etl.fromcsv(src)
    dest_table=etl.headers.pushheader(src_table, _HEADER)

    f_clean = lambda x: '0' if (x in ['', '--', 'x', 'X', 'NULL']) else x
    # ...or alternatively via a list
    # table10 = etl.convert(table1, ['lower', float, lambda v: v * 2])
    #petl.transform.conversions.convertall(table, *args, **kwargs)
    dest_table = etl.transform.conversions.convertall(dest_table, f_clean)

    with open(dest, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(dest_table)

def test_select_db():
    connection = psycopg2.connect(_CONNECTION)
    table = etl.fromdb(connection, 'SELECT * FROM quotes')

    with open(_SELECTED, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    print(table)

def test_load_db(dte='20160712'):
    raw_file = _TRANSFORMED
    tse = etl.fromcsv(raw_file)
    connection = psycopg2.connect(_CONNECTION)

    execute_sql(connection, "delete from quotes where trade_date = '{}' ".format(dte))
    # assuming table "quotes" already exists in the database, and tse need to have the header.
    # petl.io.db.todb(table, dbo, tablename, schema=None, commit=True, create=False, drop=False, constraints=True,
    #                metadata=None, dialect=None, sample=1000)[source]
    etl.todb(tse, connection, 'quotes', drop=False)

def execute_sql(connection, sql=''):
    # get a cursor
    if not (connection is None): connection = psycopg2.connect(_CONNECTION)
    cursor = connection.cursor()
    cursor.execute(sql)
    # just in case, close and resurrect cursor
    cursor.close()

def test_db_command(dte='20160712'):
    execute_sql('delete from quotes where trade_date = {}'.format(dte))

def test_tse_etl():
    print('before load...')
    trade_date = '20160712'
    #test_extract_file()
    test_transform()
    test_load_db(trade_date)
    print('after load...')
    test_select_db()


if __name__ == '__main__':
    #test_transform()
    test_tse_etl()