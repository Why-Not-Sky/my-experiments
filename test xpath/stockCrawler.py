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
    * 
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

PATH = 'data/'

# RATE 105
URL_RATE = 'http://stock.wespai.com/rate{}'
URL_RATE_105 = URL_RATE.format(105)
HTML_RATE_015 = PATH + 'RATE_105_F.HTML'
CSV_RATE_015 = PATH + 'RATE_105_F.CSV'
HEADLINE_RATE_105 = '代號,公司,扣抵稅率,配息,除息日,配股,除權日,股價,現金殖利率,殖利率,還原殖利率,發息日,配息率,董監持股,3年平均股利,6年平均股利,10年平均股利,10年股利次數,1QEPS,2QEPS,3QEPS,今年累積EPS,去年EPS,本益比,股價淨值比,5%每萬元買抵稅,5%持有一張抵稅,12%萬買,12%一張,20%萬買,20%一張,30%萬買,30%一張,多少張以上要繳健保費,一張繳健保費'
HEADER_RATE_105 = HEADLINE_RATE_105.split(',')

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

def get_from_url(url):
    #f = urllib.request.urlopen(url)
    #data = f.read()
    response = requests.get(url)
    data = response.text
    tree = html.fromstring(data)
    return tree

def get_text(ele, tail=False):  #htmlElement
    """
    :param ele: htmlElement
    :return: the text but not include tail
    """
    s = ele.text if ele.text is not None else ""
    #for e in ele[1:]: #.iter()[1:]:
    for index, e in enumerate(ele.iter()):
        if index >=1: s +=  get_text(e)

    if (tail==True) : s += ele.tail if ele.tail is not None else ""
    s = re.sub("\t", "", s.strip("\r\n").strip(" "))
    return(s)

def parse_text(td):  #td element
    '''
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
        r = e[0].xpath('text()')[0] #[0]

    # r = e[0].text col = re.sub(",", "", content.strip())
    return (re.sub("\t", "", r.strip()))

def get_exwright(year=105):
    doc = get_from_file(HTML_RATE_015)
    #doc = clean_html(doc)
    f_parse = lambda x: get_text(x)

    elist = doc.xpath('//*[@id="example"]/tbody/tr')        # //*[@id="example"]/tbody/tr[1]/td[2]  --
    table = [map(f_parse, el.xpath('td')) for el in elist]  # loop to get each rows

    table = etl.headers.pushheader(table, HEADER_RATE_105)
    table = etl.sort(table, 0)
    etl.tocsv(table, CSV_RATE_015, encoding='utf8')

    print(table)

def main():
    get_exwright()

if __name__ == '__main__':
    main()