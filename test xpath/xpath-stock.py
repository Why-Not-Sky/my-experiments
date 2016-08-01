# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
2016/07/30
<issue>: <td></td> 會有欄位縮減的問題
    | 代號   | 公司 | 扣抵稅率 | 配息 | 除息日 | 配股    | 除權日 |
    | 1101 | 台泥 |      |    |     | 07/25 |     |       | 33.9
     list(map(lambda x: x.xpath('td/text()'), table)) -->  會有欄位縮減的問題

<issue> 直接開啟utf-8的HTML file
    #http: // stackoverflow.com / questions / 12468179 / unicodedecodeerror - utf8 - codec - cant - decode - byte - 0x9c
    with codecs.open(html_file, "r", encoding='utf-8', errors='ignore') as fdata:
          tree = html.fromstring(fdata.read())
---------------------------------------------------------------------------------------------------------------------------------------'''
from lxml import etree, html
from urllib.request import urlopen
import urllib
import requests
import petl as etl
import codecs
import re
import lxml
from lxml.html.clean import clean_html

import web_utils
import stockCrawler

TRADE_DATE='20041201' #''20160701'
#taiwan_date_str = '105/07/12'
TAIWAN_DATE = '{0}/{1:02d}/{2:02d}'.format(int(TRADE_DATE[:4]) - 1911, int(TRADE_DATE[4:6]), int(TRADE_DATE[6:]))
PATH = 'data/'

# 上市：
HTML_URL = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL".format(TAIWAN_DATE)
HTML_STOCK = PATH + 'quotes-tse.html'

# RATE 105
URL_RATE_105 = 'http://stock.wespai.com/rate105'
HTML_RATE_015 = PATH + 'RATE_105_F.HTML'
CSV_RATE_015 = PATH + 'RATE_105_F.CSV'
HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')

def get_stock_by_element():
    doc = web_utils.get_from_file(HTML_RATE_015)
    #cleaner = lxml.html.cleaner(page_structure=False, links=False)
    doc = clean_html(doc)

    # <td><a href="http://tw.stock.yahoo.com/d/s/dividend_1101.html" target="_blank">台泥</a></td>
    #elist = doc.xpath('//*[@id="example"]/tbody/tr[1]/td[2]')  # //*[@id="example"]/tbody/tr[1]/td[2]  --
    elist = doc.xpath('//*[@id="example"]/tbody/tr')  # //*[@id="example"]/tbody/tr[1]/td[2]  --
    f_parse = lambda x: web_utils.get_text(x)
    table = [map(f_parse, el.xpath('td')) for el in elist]

    #solution 2: loop
    '''
    table=[]
    for el in elist: #[:2]:
        r = list(map(f_parse, el.xpath('td')))
        table.append(r)
    '''

    table = etl.headers.pushheader(table, HEADER_RATE_105)
    table = etl.sort(table, 0)
    print(table)

    #print (etl.cut(table, *range(0, 12)))
    #print([i for i in elist[0].itertext()])
    #print([i.text_content() for i in elist])

def test_exright():
    stockCrawler.get_exwright(105)

def test_exright_error():
    #tree = get_from_url(URL_RATE_105)
    tree = web_utils.get_from_file(HTML_RATE_015)  # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb1 in position 5608: invalid start byte

    f_parse_td = lambda c: web_utils.parse_text(c)

    # only 1 list generated
    tds = tree.xpath('//*[@id="example"]/tbody/tr/td')  # --> table/ thead | tbody //*[@id="example"]/tbody
    table = list(map(f_parse_td, tds))
    table = etl.sort(table, 0)
    print(table)

    # 公司: //*[@id="example"]/tbody/tr/td[2]/a
    # <a href="http://tw.stock.yahoo.com/d/s/dividend_1101.html" target="_blank">台泥</a>
    sname = tree.xpath(
        '//*[@id="example"]/tbody/tr/td/*[@target="_blank"]/text()')  # --> table/ thead | tbody //*[@id="example"]/tbody
    # print(sname)

    #print(rows) something wrong
    dest_table = etl.headers.pushheader(table, HEADER_RATE_105)  # _CHINESE_HEADER) #_ENGLISH_HEADER) # _CHINESE_HEADER)
    dest_table = etl.addcolumn(dest_table, 'name', sname)

    print (dest_table)

_CHINESE_HEADER_LINE = '證券代號,證券名稱,成交股數,成交筆數,成交金額,開盤價,最高價,最低價,收盤價,漲跌(+/-),漲跌價差,最後揭示買價,最後揭示買量,最後揭示賣價,最後揭示賣量,本益比'
_CHINESE_HEADER = _CHINESE_HEADER_LINE.split(',')
_ENGLISH_HEADER = 'symbol_id,name,volume,trans,amount,open,high,low,close,sign,change,af_buy,af_buy_amount,af_sell, af_sell_amout,pe'.split(',')

_HEADER_LINE = 'symbol_id,trade_date,volume,amount,open,high,low,close,change,trans'
_HEADER = _HEADER_LINE.split(',')
_CONVERT_ZERO = ['', '--', '---', 'x', 'X', 'null', 'NULL']  # convert illegal value into 0


def _clean(x):
    return('0' if (x in _CONVERT_ZERO) else re.sub(",", "", x.strip()))

def get_table_tse():
    '''
    infile = open(HTML_STOCK, 'r')  # 'r')  # otc's object type is str
    data = infile.read()
    tree = html.fromstring(data)
    '''

    tree = web_utils.get_from_file(HTML_STOCK)  # parse error

    f_clean = lambda x: '0' if (x in _CONVERT_ZERO) else re.sub(",", "", x.strip())
    f_parse = lambda x: web_utils.get_text(x)
    f_parse_clean = lambda x: _clean(web_utils.get_text(x))

    elist = tree.xpath('/html/body/table/tbody/tr')

    #solution 1
    table = [map(f_parse_clean, el.xpath('td')) for el in elist]

    #solution 2
    table = [map(f_parse, el.xpath('td')) for el in elist]
    table = etl.headers.pushheader(table, _CHINESE_HEADER)
    table = etl.transform.conversions.convertall(table, f_clean)
    print(etl.sort(table, 0))

    #wrong: cant' find the looped data...<a></a>
    rows = map(lambda x: x.xpath('td/text()'), elist)
    rows = etl.headers.pushheader(rows, _CHINESE_HEADER)
    rows = etl.sort(rows, 0)
    print (rows)
    #print(etl.cut(rows, *range(0, len(rows[0])-1)))

def test_xpath():
    #html = etree.parse(HTML_FILE)
    HTML_FILE= HTML_STOCK
    infile = open(HTML_FILE, 'r')  # 'r')  # otc's object type is str
    data = infile.read()

    # Parse page
    tree = html.fromstring(data)
    print(tree, type(tree))

    print ('1）read the body')
    result = tree.xpath('/html/body/table/tbody/tr')
    print(result)
    print(len(result), type(result)) # number of rows
    print(result[0], len(result[0]), type(result[0])) #number of columns (td)

    print ('2）read the all td')
    result = tree.xpath('/html/body/table/tbody/tr/td')
    print(result)
    print(len(result), type(result))

    print ('2.1）read the content of all td')
    result = tree.xpath('/html/body/table/tbody/tr//td/text()')
    print(result)
    print(len(result), type(result))
    print(result[0], len(result[0]), type(result[0]))

def main():
    get_table_tse()
    #get_stock_by_element()

if __name__ == '__main__':
    main()