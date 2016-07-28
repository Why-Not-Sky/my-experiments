# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------



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

HTML_FILE = './quotes-tse.html'

def get_from_file():
    html = etree.parse(HTML_FILE)
    result = etree.tostring(html, pretty_print=True)
    print(result)
    infile = open(infname, 'r')  # 'r')  # otc's object type is str
    data = infile.read()

    # Parse page
    tree = html.fromstring(data)

'''
        for tr in tree.xpath('//table[2]/tbody/tr'):
            tds = tr.xpath('td/text()')

            sign = tr.xpath('td/font/text()')
'''

def get_table():
    infile = open(HTML_FILE, 'r')  # 'r')  # otc's object type is str
    data = infile.read()
    tree = html.fromstring(data)

    table = tree.xpath('/html/body/table/tbody/tr')
    rows = list(map(lambda x: x.xpath('td/text()'), table))

    print (rows)

def main():
    get_table()

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