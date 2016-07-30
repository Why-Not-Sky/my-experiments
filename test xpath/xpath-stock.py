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

TRADE_DATE='20041201' #''20160701'
#taiwan_date_str = '105/07/12'
TAIWAN_DATE = '{0}/{1:02d}/{2:02d}'.format(int(TRADE_DATE[:4]) - 1911, int(TRADE_DATE[4:6]), int(TRADE_DATE[6:]))
PATH = 'data/'

# 上市：
HTML_URL = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL".format(TAIWAN_DATE)
HTML_STOCK = PATH + 'quotes-tse.html'

# RATE 105
URL_RATE_105 = 'http://stock.wespai.com/rate105'
HTML_RATE_015 = PATH + 'RATE_105.HTML'
CSV_RATE_015 = PATH + 'RATE_105.CSV'
HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')

# Using Google Sheets as a basic web scraper
# http://www.benlcollins.com/spreadsheets/google-sheet-web-scraper/
HTML_NYTIMES = 'http://www.nytimes.com/2015/09/23/us/los-angeles-plans-100-million-effort-to-end-homelessness.html'

def save_to_file(url, fname):
    r = requests.get(url)

    with open(fname, "wb") as code:
        code.write(r.content)
        #code.close()

def get_from_file(html_file):
    #infile = open(html_file, 'r')  # 'r')  # otc's object type is str
    #data = infile.read()   # unicode error
    #tree = html.fromstring(data)

    #http: // stackoverflow.com / questions / 12468179 / unicodedecodeerror - utf8 - codec - cant - decode - byte - 0x9c
    with codecs.open(html_file, "r", encoding='utf-8', errors='ignore') as fdata:
        tree = html.fromstring(fdata.read())

    #html = etree.parse(html_file)
    #tree = html.document_fromstring(html)
    return tree

def get_table_tse():
    '''
    infile = open(HTML_STOCK, 'r')  # 'r')  # otc's object type is str
    data = infile.read()
    tree = html.fromstring(data)
    '''
    tree = get_from_file(HTML_STOCK)  # parse error

    table = tree.xpath('/html/body/table/tbody/tr')
    rows = list(map(lambda x: x.xpath('td/text()'), table))

    print(etl.cut(rows, *range(0, len(rows[0])-1)))

def get_from_url(url):
    #f = urllib.request.urlopen(url)
    #data = f.read()
    response = requests.get(url)
    data = response.text
    tree = html.fromstring(data)
    return tree

def parse_text(td):  #td element
    '''
       # todo: process <td></td>
       <td><a href="http://tw.stock.yahoo.com/d/s/dividend_0050.html" target="_blank">台灣50</a></td>
       <td><a href="" title="0050-歷年扣抵率" rel="rate" class="chart">0%</a></td>
       <td><a href="" title="0050-歷年股利" class="rate">0.85</a></td>
       <td>07/28</td>
       <td> </td>
    '''
    e = td.xpath('a')
    if len(e) < 1:
        e = td.xpath('text()')
        if len(e) < 1: r = ''
        else: r = e[0]
    else: # <td><a href="" title="0050-歷年股利" class="rate">0.85</a></td>
        r = e[0].xpath('text()')[0] #[0]  #r = e[0].text

    return (r.strip('\t').strip(' '))

def test_wright_loop():
    #save_to_file(URL_RATE_105, HTML_RATE_015)
    tree = get_from_file(HTML_RATE_015)                    #UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb1 in position 5608: invalid start byte

    table = tree.xpath('//*[@id="example"]/tbody/tr')      #--> table/ thead | tbody //*[@id="example"]/tbody

    r=[]
    for tr in table: #[:1]
        #tds = list(tr.xpath('td/text()'))  # space column was lost   'td//text(), td/text()[1]
        tds_elmement = tr.xpath('td')  # return td

        # f_tds = lambda x: x.xpath('text()')[0].strip('\t').strip(' ') if len(x.xpath('text()')) > 0 else ''
        # can't find <a></a>

        f_parse = lambda x: parse_text(x)
        tds = list(map(f_parse, tds_elmement))

        #print (parse_text(tds_elmement))
        #tds = list(map(f_tds, tds_elmement))
        #cname = tr.xpath('td/*[@target="_blank"]/text()')   # [normalize-space()]
        #tds.insert(1, cname[0])

        r.append(tds)

    r =  etl.headers.pushheader(r, HEADER_RATE_105)
    r = etl.sort(r, 0)
    print (r)
    etl.tocsv(r, CSV_RATE_015, encoding='utf8')
    #print (etl.cut(r, *range(0, 12)))

def test_wright():
    #tree = get_from_url(URL_RATE_105)
    tree = get_from_file(HTML_RATE_015)  # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb1 in position 5608: invalid start byte
    table = tree.xpath('//*[@id="example"]/tbody/tr')      #--> table/ thead | tbody //*[@id="example"]/tbody

    sname = tree.xpath(
        '//*[@id="example"]/tbody/tr/td/*[@target="_blank"]/text()')  # --> table/ thead | tbody //*[@id="example"]/tbody
    #print(sname)

    # 公司: //*[@id="example"]/tbody/tr/td[2]/a
    # <a href="http://tw.stock.yahoo.com/d/s/dividend_1101.html" target="_blank">台泥</a>

    rows = list(map(lambda x: x.xpath('td/text()'), table))

    #print(rows) something wrong
    dest_table = etl.headers.pushheader(rows, HEADER_RATE_105)  # _CHINESE_HEADER) #_ENGLISH_HEADER) # _CHINESE_HEADER)
    dest_table = etl.addcolumn(dest_table, 'name', sname)

    #dest_table = etl.cut(rows, 0, 1, 2) #*range[0:])
    print (etl.cut(dest_table, 'name', *range(0, 12)))  #0, 1, 2) #*range[0:])

def test_nytimes():
    tree = get_from_url(HTML_NYTIMES)
    span = tree.xpath('//*[@id="story-meta-footer"]/p/span/a/span')
    text = tree.xpath("//span[@class='byline-author']/text()")  # //*[@id="story-meta-footer"]/p/span/a/span
    #http://stackoverflow.com/questions/16241197/xpath-to-retrieve-text-within-span
    last = tree.xpath("//span[@class='byline-author']/text()[last()]")  # //*[@id="story-meta-footer"]/p/span/a/span

    #tt = span[0].xpath("/text()")
    #print (tt)   #not worked

    print (span, span[0].text)
    print (text, text[0])
    print (last, last[0])
    # print (author_chrome)   # same span

def main():
    #get_table_tse()
    #get_table()
    #test_nytimes()
    #test_wright()
    test_wright_loop()


def test_xpath():
    #html = etree.parse(HTML_FILE)
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

if __name__ == '__main__':
    main()