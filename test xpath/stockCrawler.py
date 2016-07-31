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
import petl as etl
import codecs
import re
import lxml
import web_utils
import logging, sys

PATH = 'data/'

# RATE 105
URL_RATE = 'http://stock.wespai.com/rate{}'
HTML_RATE = PATH + 'RATE_{}.HTML'
CSV_RATE = PATH + 'RATE_{}.CSV'

URL_RATE_105 = URL_RATE.format(105)
HTML_RATE_015 = HTML_RATE.format(105)
CSV_RATE_015 = CSV_RATE.format(105)

HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')

class stockCrawler():
    def  __init__(self, url, outfile):
        year = 105
        self.url=url if (url is not None) else URL_RATE.format(year)
        self.outfile=outfile if (outfile is not None) else CSV_RATE.format(year)
        self.infile=self.outfile.lower().replace('.html', 'csv')
        self.doc = None
        self.rows = None
        self.header = None

    def get_header(self):
        ehead = self.doc.xpath('//*[@id="example"]/thead/tr/th/text()')  # //*[@id="example"]/tbody/tr[1]/td[2]  --
        self.header = ehead #HEADER_RATE_105

    def get_body(self):
        f_parse = lambda x: web_utils.get_text(x)
        #if self.doc is None: _

        elist = self.doc.xpath('//*[@id="example"]/tbody/tr')  # //*[@id="example"]/tbody/tr[1]/td[2]  --
        table = [map(f_parse, el.xpath('td')) for el in elist]  # loop to get each rows

        table = etl.headers.pushheader(table, self.header)
        self.rows = etl.sort(table, 0)
        #etl.tocsv(self.rows, self.outfile, encoding='utf8')

    def save(self):
        etl.tocsv(self.rows, self.outfile, encoding='utf8')

    def run(self):
        web_utils.save_html(self.url, self.infile)
        self.doc = web_utils.get_from_file(self.infile)
        self.get_header()
        self.get_body()
        self.save()
        #logging.debug('\n{}'.format(self.rows))

def get_exwright(year=105):
    URL = URL_RATE.format(year)
    HTML_FILE = HTML_RATE.format(year)
    CSV_FILE = CSV_RATE.format(year)
    web_utils.save_html(URL, HTML_FILE)

    doc = web_utils.get_from_file(HTML_FILE)
    #doc = clean_html(doc)
    f_parse = lambda x: web_utils.get_text(x)

    elist = doc.xpath('//*[@id="example"]/tbody/tr')        # //*[@id="example"]/tbody/tr[1]/td[2]  --
    table = [map(f_parse, el.xpath('td')) for el in elist]  # loop to get each rows

    table = etl.headers.pushheader(table, HEADER_RATE_105)
    table = etl.sort(table, 0)
    etl.tocsv(table, CSV_FILE, encoding='utf8')

    print(table)

def main():
    #get_exwright(105)
    #extend for another criteria to load
    url_ROE = 'http://stock.wespai.com/p/20494'
    #sc = stockCrawler(url=URL_RATE_105, outfile=CSV_RATE_015)
    sc = stockCrawler(url=url_ROE, outfile=(PATH+'ROE.CSV'))
    sc.run()
    print(sc.rows)

if __name__ == '__main__':
    #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()