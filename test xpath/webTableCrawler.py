# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
function:
    get the taiwan trade information from http://stock.wespai.com/rate105
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
0.1     2016/07/31      refactor from xpath-stock.py
                    # <td><a href="http://tw.stock.yahoo.com/d/s/dividend_1101.html" target="_blank">台泥</a></td>


------------------------------------------------------------------------------------------------------------------------------------------
non-function requirement: 
    * 
    * 
    *
------------------------------------------------------------------------------------------------------------------------------------------
feature list:
    * write the result into excel/ google sheet/ database
    * 
    *
---------------------------------------------------------------------------------------------------------------------------------------'''
from lxml import etree, html
import urllib
import requests
import codecs
import re
import datetime
import lxml
import logging, sys
import petl as etl
import os.path

import web_utils

PATH = 'data/'

# RATE 105
URL_RATE = 'http://stock.wespai.com/rate{}'
HTML_RATE = PATH + 'rate_{}.html'
CSV_RATE = PATH + 'rate_{}.csv'

HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')
XPATH_HEADER = '//*[@id="example"]/thead/tr/th/text()' # for 'http://stock.wespai.com/rate{}'
XPATH_BODY = '//*[@id="example"]/tbody/tr'   # for

DEFAULT_OUT = PATH + 'output.csv'

class webTableCrawler():
    def  __init__(self, url=None, xheader=None, xbody=None, outfile=None, fn_clean=None, fn_transform=None, reload=False):
        self.url = url #if (url is not None) else URL_RATE.format(105)
        self.reload = reload
        self.outfile= outfile if (outfile is not None) else DEFAULT_OUT
        self.infile = self.outfile.lower().replace('.csv', '.html')
        self.doc = None
        self.rows = None
        self.header = None
        self.xpath_header = xheader if (xheader is not None) else XPATH_HEADER
        self.xpath_body = xbody if (xbody is not None) else XPATH_BODY
        self.column_clean =  fn_clean if (fn_clean is not None) else self._do_nothing
        self.row_transform = fn_transform if (fn_transform is not None) else self._do_nothing

    def _do_nothing(self, x):
        return(x)

    def get_doc(self, url=None, infile=None):
        infile = infile if (infile is not None) else self.infile

        if (self.reload) or (not os.path.exists(infile)):
            url = url if (url is not None) else self.url
            web_utils.save_html(url, infile)

        self.doc = web_utils.get_from_file(infile)

        return(self.doc)

    def get_header(self, xheader=None):
        xheader = xheader if (xheader is not None) else self.xpath_header
        ehead = self.doc.xpath(xheader)  # //*[@id="example"]/tbody/tr[1]/td[2]  --

        #f_parse = lambda x: web_utils.get_text(x)
        #ehead = [map(f_parse, ehead)]  # //*[@id="example"]/tbody/tr[1]/td[2]  --

        self.header = ehead #HEADER_RATE_105
        return (self.header)

    def get_body(self, xbody=None):
        xbody = xbody if (xbody is not None) else self.xpath_body
        fn_clean = lambda x: self.column_clean(web_utils.get_text(x))
        #fn_transform = lambda x: self._row_transform(x)
        #if self.doc is None: _

        elist = self.doc.xpath(xbody)  # //*[@id="example"]/tbody/tr[1]/td[2]  --
        table = []  # loop to get each rows

        if self.row_transform is None:
          table = [map(fn_clean, el.xpath('td')) for el in elist]  # loop to get each rows
        else:
            for el in elist:
                r= list(map(fn_clean, el.xpath('td')))
                r = self.row_transform(r)
                table.append(r)

        table = etl.headers.pushheader(table, self.header)
        self.rows = etl.sort(table, 0)
        #etl.tocsv(self.rows, self.outfile, encoding='utf8')
        return (self.rows)

    def get_table(self):
        self.get_doc()
        self.get_header()
        return self.get_body()

    def save(self):
        etl.tocsv(self.rows, self.outfile, encoding='utf8')

    def run(self):
        self.get_table()
        self.save()
        #logging.debug('\n{}'.format(self.rows))

_CONVERT_ZERO = ['', '--', '---', 'x', 'X', 'null', 'NULL']  # convert illegal value into 0
_ENGLISH_HEADER = 'symbol_id,name,volume,trans,amount,open,high,low,close,sign,change,af_buy,af_buy_amount,af_sell, af_sell_amout,pe'.split(',')
_HEADER_LINE = 'symbol_id,trade_date,volume,amount,open,high,low,close,change,trans'
_HEADER = _HEADER_LINE.split(',')

def clean_number(x):
    return '0' if (x in _CONVERT_ZERO) else re.sub(",", "", x.strip(""))

class tseCrawler(webTableCrawler):
    def __init__(self, trade_date='20160701'):
        self._taiwan_date = to_taiwan_date(trade_date)
        self._url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL"
        self.url = self._url.format(self._taiwan_date)

        outfile = PATH + ('{}-t.csv').format(trade_date)  # outdate.replace('/', ''))
        xheader = '//*[@id="main-content"]/table[2]/thead/tr[2]/td/text()'  # '//*[@id="main-content"]/table[2]/thead/tr[2]'
        xbody = '//table[2]/tbody/tr'  # loop for td to get the table content

        super(tseCrawler, self).__init__(url=self.url, xheader=xheader, xbody=xbody, outfile=outfile, fn_clean=self._clean, fn_transform=self._transform)

    def _clean(self, x):
        return '0' if (x in _CONVERT_ZERO) else re.sub(",", "", x.strip(""))

    def _transform(self, row=None): #, date_str=None):
        #to-do: use dynamic arguments
        sign = '-' if len(row[9]) == 1 and row[9] in ['-', u'－'] else ''
        change = sign + row[10]
        return(row[0], row[1], row[2], row[4], row[5], row[6], row[7], row[8], change, row[3])

def get_wespai(url, outfile):
    sc = webTableCrawler(url=url, xheader=XPATH_HEADER, xbody=XPATH_BODY, outfile=outfile)
    sc.run()
    print(sc.rows)

def get_exwright(year=105):
    url, outfile = URL_RATE.format(year), CSV_RATE.format(year)
    get_wespai(url, outfile)

def date_to_int(date_str='20160712', esc_char='/'):
    date_str = date_str.replace(esc_char, '')
    return int(date_str[:4]), int(date_str[4:6]), int(date_str[6:])

def to_taiwan_date(date_str='20160712', esc_char='/'):
    year, month, day = date_to_int(date_str, esc_char)
    taiwan_date = '{0}{esc_ch}{1:02d}{esc_ch}{2:02d}'.format(year - 1911, month, day, esc_ch=esc_char)
    return taiwan_date

def tse_transform(row=None): #, date_str=None):
    #to-do: use dynamic arguments
    sign = '-' if len(row[9]) == 1 and row[9] in ['-', u'－'] else ''
    change = sign + row[10]
    return(row[0], row[1], row[4], row[5], row[6], row[7], row[8], change, row[3])
    #return r

def test_tseCralwer(date_str='20160701'):
    """
    with standard clean & transform rules enabled
    :return:
    """
    tse = tseCrawler(trade_date=date_str)
    dest_table = tse.get_table()

    dest_table = etl.headers.setheader(dest_table,  _HEADER)
    dest_table = etl.transform.conversions.convert(dest_table
                                                   , {'trade_date': lambda v, row: date_str}
                                                   , pass_row=True)  # cause _trade_date not worked --> need row values

    return (etl.sort(dest_table, 0))

def test_tseTransform(date_str='20160701'):
    outdate = to_taiwan_date(date_str)
    url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL".format(outdate)
    outfile = PATH + ('{}-t.csv').format(date_str)
    xheader = '//*[@id="main-content"]/table[2]/thead/tr[2]/td/text()'  #'//*[@id="main-content"]/table[2]/thead/tr[2]'
    xbody = '//table[2]/tbody/tr'  #loop for td to get the table content

    src_table = webTableCrawler(url=url, xheader=xheader, xbody=xbody, outfile=outfile).get_table()

    #using etl to transform
    dest_table = etl.headers.setheader(src_table, _ENGLISH_HEADER)  # _CHINESE_HEADER) #_ENGLISH_HEADER) # _CHINESE_HEADER)
    dest_table = etl.cut(dest_table, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 3)
    dest_table = etl.rename(dest_table, 'name', 'trade_date')

    f_clean = lambda x: clean_number(x)
    dest_table = etl.transform.conversions.convertall(dest_table, f_clean)

    dest_table = etl.transform.conversions.convert(dest_table
                                                    , {'trade_date': lambda v, row: date_str
                                                    , 'change': lambda v, row: ('-' + v) if (len(row.sign) == 1 and (row.sign[0] in ['-', u'－'])) else v
                                                    }
                                                    , pass_row=True)  # cause _trade_date not worked --> need row values

    dest_table = etl.cutout(dest_table, 'sign')
    return (etl.sort(dest_table, 0))

#orign helper services
def get_exwright_origin(year=105):
    URL = URL_RATE.format(year)
    HTML_FILE = HTML_RATE.format(year)
    CSV_FILE = CSV_RATE.format(year)
    web_utils.save_html(URL, HTML_FILE)

    doc = web_utils.get_from_file(HTML_FILE)
    #doc = clean_html(doc)
    f_parse = lambda x: web_utils.get_text(x)

    elist = doc.xpath('//*[@id="example"]/tbody/tr')        # //*[@id="example"]/tbody/tr[1]/td[2]  --
    table = [map(f_parse, el.xpath('td')) for el in elist]  # loop to get each rows

    # hard coding header for rate 105
    table = etl.headers.pushheader(table, HEADER_RATE_105)
    table = etl.sort(table, 0)
    etl.tocsv(table, CSV_FILE, encoding='utf8')

    print(table)

def test_get_exwright(year=105):
    get_exwright(year)

def test_get_wespai():
    today = datetime.date.today().strftime('%Y%m%d')
    url, outfile = 'http://stock.wespai.com/p/20494', PATH + ('{}-ROE.CSV').format(today)
    get_wespai(url=url, outfile=outfile)

def test_get_header():
    url = URL_RATE.format(105)
    sc = webTableCrawler(url=url)
    sc.get_doc()
    #xheader = '//*[@id="example"]/thead/tr/th'
    #print(sc.get_header(xheader=xheader))

    xheader = '//*[@id="example"]/thead/tr/th/text()'
    sc.get_header(xheader=xheader)
    print(sc.header)

def test_get_tse(outdate='20160701'):
    transform_table = test_tseTransform(outdate)
    print('transform tse through outside clean & transform rules... ')
    print(transform_table)

    print('transform tse using build-in function... ')

    build_in_table = test_tseCralwer(outdate)
    print(build_in_table)

    outfile = PATH + ('{}-t.csv').format(outdate.replace('/', ''))
    etl.tocsv(build_in_table, outfile)

def main():
    test_get_header()
    #test_get_exwright(105)
    #test_get_wespai()
    #test_get_tse()

if __name__ == '__main__':
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()