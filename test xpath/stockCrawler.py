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

import web_utils

PATH = 'data/'

# RATE 105
URL_RATE = 'http://stock.wespai.com/rate{}'
HTML_RATE = PATH + 'RATE_{}.HTML'
CSV_RATE = PATH + 'RATE_{}.CSV'

'''
URL_RATE_105 = URL_RATE.format(105)
HTML_RATE_015 = HTML_RATE.format(105)
CSV_RATE_015 = CSV_RATE.format(105)
'''

HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')
XPATH_HEADER = '//*[@id="example"]/thead/tr/th/text()' # for 'http://stock.wespai.com/rate{}'
XPATH_BODY = '//*[@id="example"]/tbody/tr'   # for

def ff_parse(x):
    return(lambda x: web_utils.get_text(x))

class stockCrawler():
    def  __init__(self, url=None, xheader=None, xbody=None, outfile=None):
        year = 105
        self.url = url if (url is not None) else URL_RATE.format(year)
        self.outfile= outfile if (outfile is not None) else CSV_RATE.format(year)
        self.infile = self.outfile.lower().replace('.csv', '.html')
        self.doc = None
        self.rows = None
        self.header = None
        self.xpath_header = xheader if (xheader is not None) else XPATH_HEADER
        self.xpath_body = xbody if (xbody is not None) else XPATH_BODY

    def get_doc(self, url=None, infile=None):
        url = url if (url is not None) else self.url
        infile = infile if (infile is not None) else self.infile
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
        f_parse = lambda x: web_utils.get_text(x)
        #if self.doc is None: _

        elist = self.doc.xpath(xbody)  # //*[@id="example"]/tbody/tr[1]/td[2]  --
        table = [map(f_parse, el.xpath('td')) for el in elist]  # loop to get each rows

        table = etl.headers.pushheader(table, self.header)
        self.rows = etl.sort(table, 0)
        #etl.tocsv(self.rows, self.outfile, encoding='utf8')
        return (self.rows)

    def save(self):
        etl.tocsv(self.rows, self.outfile, encoding='utf8')

    def run(self):
        self.get_doc()
        self.get_header()
        self.get_body()
        self.save()
        #logging.debug('\n{}'.format(self.rows))

def get_wespai(url, outfile):
    sc = stockCrawler(url=url, xheader=XPATH_HEADER, xbody=XPATH_BODY, outfile=outfile)
    sc.run()
    print(sc.rows)

def get_exwright(year=105):
    url, outfile = URL_RATE.format(year), CSV_RATE.format(year)
    get_wespai(url, outfile)

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
    sc = stockCrawler()
    sc.get_doc()
    #xheader = '//*[@id="example"]/thead/tr/th'
    #print(sc.get_header(xheader=xheader))

    xheader = '//*[@id="example"]/thead/tr/th/text()'
    sc.get_header(xheader=xheader)
    print(sc.header)

def test_get_tse():
    outdate = '105/07/29'
    url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL".format(outdate)
    outfile = PATH + ('{}-t.csv').format(outdate.replace('/', ''))
    xheader = '//*[@id="main-content"]/table[2]/thead/tr[2]/td/text()'  #'//*[@id="main-content"]/table[2]/thead/tr[2]'
    xbody = '//table[2]/tbody/tr'  #loop for td to get the table content

    sc = stockCrawler(url=url, xheader=xheader, xbody=xbody, outfile=outfile)
    sc.run()
    print(sc.rows)

def main():
    #test_get_header()
    test_get_exwright(105)
    #test_get_wespai()
    #test_get_tse()
    #extend for another criteria to load

if __name__ == '__main__':
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()