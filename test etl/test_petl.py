# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
2016/07/28
    http://blog.csdn.net/winterto1990/article/details/47903653
    # test clean function where means only convert the row satisfied in where
    # issue: error as assing lambada by defined function
    # todo: sign = '-' if len(sign) == 1 and sign[0] == u'－' else ''
             replace <td> <font color="#FF3300">＋</font> </td>:
    # todo: add trade_date into the table

-----------------------------------------------------------------------------------------------------------------------------------------
to-do:
---------------------------------------------------------------------------------------------------------------------------------------'''

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
#FILE_NAME = 'tse'  # only the data for the table, change xpath for the full
_TSET_FILE = '20041201'
_TRADE_DATE = '20160712' #'20041201' #''20160712'
_FILE_NAME = _TRADE_DATE  # only the data for the table, change xpath for the full
_HTML_FILE = '{}{}.html'.format(_DATA_PATH, _FILE_NAME)
_CSV_FILE = '{}{}.csv'.format(_DATA_PATH, _FILE_NAME)

_CHINESE_HEADER_LINE = '證券代號,證券名稱,成交股數,成交筆數,成交金額,開盤價,最高價,最低價,收盤價,漲跌(+/-),漲跌價差,最後揭示買價,最後揭示買量,最後揭示賣價,最後揭示賣量,本益比'
_CHINESE_HEADER = _CHINESE_HEADER_LINE.split(',')
_ENGLISH_HEADER = 'symbol_id,name,volume,trans,amount,open,high,low,close,sign,change,af_buy,af_buy_amount,af_sell, af_sell_amout,pe'.split(',')

_HEADER_LINE = 'symbol_id,trade_date,volume,amount,open,high,low,close,change,trans'
_HEADER = _HEADER_LINE.split(',')
_CONVERT_ZERO = ['', '--', '---', 'x', 'X', 'null', 'NULL']   # convert illegal value into 0

_XPATH_TSE = '//table[2]/tbody/tr'
_XAPTH_TSE_SIMPLE = '/html/body/table/tbody/tr'


def _clean_row(self, row):
    # f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else x

    for index, content in enumerate(row):
        '''decimal with , thousand'''
        col = re.sub(",", "", content.strip())
        # filter() in python 3 does not return a list, but a iterable filter object. Call next() on it to get the first filtered item:
        col = ''.join(list(filter(lambda x: x in string.printable, col)))
        row[index] = '0' if (col in _CONVERT_ZERO) else col

# error as assigned into convertall method
def _clean_fun():
    return(lambda x: '0' if (x in _CONVERT_ZERO) else x)

# error as assigned into convertall method
def _filter_fun():
    symbol_list = ['0050', '0051', '1503']
    return (lambda rec: rec.symbol_id in symbol_list)

def test_clean():
    '''input file should be trimmed'''
    src = _ORIGINAL
    dest = _TRANSFORMED

    src_table=etl.fromcsv(src)
    dest_table = etl.headers.pushheader(src_table, _HEADER)
    print(dest_table)

    # todo: test filter function
    # filter unwanted records: keep only on the market/otc
    symbol_list = ['0050', '0051', '1503']
    #return (lambda rec: rec.symbol_id in symbol_list)  # len(id)==4 )

    dest_table = etl.select(dest_table, lambda rec: rec.symbol_id in symbol_list) #lambda rec: len(rec.symbol_id) == 4)
    print (dest_table)

    # test clean function where means only convert the row satisified in where
    # error as assing lambada by defined function
    f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else x
    dest_table = etl.transform.conversions.convertall(dest_table, f_clean) #, where=lambda r: len(r.symbol_id) == 4)
    print(dest_table)

    etl.tocsv(dest_table, dest)

def get_table():
    infile = open(_HTML_FILE, 'r')  # 'r')  # otc's object type is str
    data = infile.read()
    data=data.replace('<font color="#FF3300">＋</font>', '+')
    data=data.replace('<font color="#009900">－</font>', '-')
    tree = html.fromstring(data)

    table = tree.xpath(_XPATH_TSE) # '/html/body/table/tbody/tr')  # for tse with only 1 table
    rows = list(map(lambda tr: tr.xpath('td/text()'), table))
    #sign = tr.xpath('td/font/text()')

    with open(_HTML_FILE+'.bak', 'w') as f:
        f.write(data)

    return (rows)

def test_transform_from_html():
    src_table=get_table()
    #for l in src_table[:10]: print(l)

    #dest_table=etl.headers.pushheader(src_table, _HEADER)
    dest_table = etl.headers.pushheader(src_table, _ENGLISH_HEADER) #_CHINESE_HEADER) #_ENGLISH_HEADER) # _CHINESE_HEADER)
    #print (etl.cut(dest_table, 'symbol_id', 'close', 'sign', 'change'))

    # filter the fields expected
    # todo: filter result according to the symbol table
    dest_table = etl.select(dest_table, lambda rec: len(rec.symbol_id.strip(" ")) <= 4)

    # select the columns to insert
    # string to the args?  can't catch the signed value
    dest_table =  etl.cut(dest_table, 0, 1, 4, 5, 6, 7, 8, 9, 10, 3)
    dest_table = etl.rename(dest_table, 'name', 'trade_date')

    # convert the big number 1,000,000 --> 10000000
    # convert unexpected 'x' --> '0'...
    f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else re.sub(",", "", x.strip())
    dest_table = etl.transform.conversions.convertall(dest_table, f_clean)

    # http://petl.readthedocs.io/en/latest/transform.html#converting-values
    dest_table = etl.transform.conversions.convert(dest_table
                                                    , {'trade_date': lambda v, row: _TRADE_DATE
                                                    #, 'change': lambda v, row: (row.sign + ':' + str(len(row.sign)) + ':' + row.sign[0] + ':' + v)}
                                                    , 'change': lambda v, row: ('-' + v) if (len(row.sign) == 1 and (row.sign[0] in ['-', u'－'])) else v}
                                                    , pass_row=True)  # cause _trade_date not worked --> need row values

    dest_table = etl.cutout(dest_table, 'sign')
    #print (dest_table)

    # save to csv file.
    etl.tocsv(dest_table, _CSV_FILE)

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
    test_transform_from_html()
    test_load_db(trade_date)
    print('after load...')
    test_select_db()

if __name__ == '__main__':
    #test_transform()
    #test_clean()
    test_transform_from_html()