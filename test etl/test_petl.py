# -*- coding: utf-8 -*-

import petl as etl
import csv
import psycopg2
from lxml import etree, html
import re
import string

# set up a CSV file to demonstrate with
_CONNECTION = 'dbname=stock user=stock password=stock'
_DATA_PATH = './data/'
_HEADER = 'symbol_id,trade_date,volume,amount,open,high,low,close,change,trans'.split(',')
_ORIGINAL = _DATA_PATH + 'before.csv' #'origin.csv'
_TRANSFORMED = _DATA_PATH + 'after.csv'
_SELECTED = _DATA_PATH + 'select.csv'

'''---note---
  2017/07/25 CSV file cannot conatain the empty row...
'''
FILE_NAME = 'tse'
HTML_FILE = '{}{}.html'.format(_DATA_PATH, FILE_NAME)
CSV_FILE = '{}{}.csv'.format(_DATA_PATH, FILE_NAME)

_CHINESE_HEADER_LINE = '證券代號,證券名稱,成交股數,成交筆數,成交金額,開盤價,最高價,最低價,收盤價,漲跌(+/-),漲跌價差,最後揭示買價,最後揭示買量,最後揭示賣價,最後揭示賣量,本益比'
_CHINESE_HEADER = _CHINESE_HEADER_LINE.split(',')
_ENGLISH_HEADER = 'symbol_id,name,volume,trans,amount,open,high,low,close,sign,change,trans,af_buy,af_buy_amount,af_sell, af_sell_amout,pe'.split(',')

_HEADER_LINE = 'symbol_id,trade_date,volume,amount,open,high,low,close,change,trans'
_HEADER = _HEADER_LINE.split(',')
_CONVERT_ZERO = ['', '--', '---', 'x', 'X', 'null', 'NULL']   # convert illegal value into 0


def get_table():
    infile = open(HTML_FILE, 'r')  # 'r')  # otc's object type is str
    data = infile.read()
    tree = html.fromstring(data)

    table = tree.xpath('/html/body/table/tbody/tr')
    rows = list(map(lambda x: x.xpath('td/text()'), table))

    return (rows)

def _clean_row(self, row):
    # f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else x

    for index, content in enumerate(row):
        '''decimal with , thousand'''
        col = re.sub(",", "", content.strip())
        # filter() in python 3 does not return a list, but a iterable filter object. Call next() on it to get the first filtered item:
        col = ''.join(list(filter(lambda x: x in string.printable, col)))
        # transform non-decimal number into decimal
        row[index] = '0' if (col in _CONVERT_ZERO) else col

def _clean_fun():
    return(lambda x: '0' if (x in _CONVERT_ZERO) else x)

def test_clean():
    src = _ORIGINAL
    dest = _TRANSFORMED

    src_table=etl.fromcsv(src)

    # test clean function
    dest_table = etl.transform.conversions.convertall(src_table, _clean_fun)

    # todo: test filter function

    etl.tocsv(dest_table, CSV_FILE)

def test_transform_from_html():
    src_table=get_table()
    #dest_table=etl.headers.pushheader(src_table, _HEADER)
    dest_table = etl.headers.pushheader(src_table, _CHINESE_HEADER) #_ENGLISH_HEADER) # _CHINESE_HEADER)

    f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else x
    #to-do: sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''
    '''
    row = self._clean_row([
                tds[0].strip(),  # symbol
                date_str,  # 日期
                tds[2],  # 成交股數
                tds[4],  # 成交金額
                tds[5],  # 開盤價
                tds[6],  # 最高價
                tds[7],  # 最低價
                tds[8],  # 收盤價
                sign + tds[9],  # 漲跌價差
                tds[3],  # 成交筆數
            ])
    '''

    dest_table = etl.transform.conversions.convertall(dest_table, f_clean)
    print (dest_table)

    etl.tocsv(dest_table, CSV_FILE)

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
    test_transform_from_html()