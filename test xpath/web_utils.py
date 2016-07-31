# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
* use get_text() or parse_text() to extract the text of td
       <td><a href="http://tw.stock.yahoo.com/d/s/dividend_0050.html" target="_blank">台灣50</a></td>
       <td><a href="" title="0050-歷年扣抵率" rel="rate" class="chart">0%</a></td>
       <td><a href="" title="0050-歷年股利" class="rate">0.85</a></td>
       <td>07/28</td>
       <td> </td>


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
import codecs
import lxml
import requests
import re

def save_html(url, fname):
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
        tree = lxml.html.fromstring(fdata.read())

    #html = etree.parse(html_file)
    #tree = html.document_fromstring(html)
    return tree

def get_from_url(url):
    #f = urllib.request.urlopen(url)
    #data = f.read()
    response = requests.get(url)
    data = response.text
    tree = lxml.html.fromstring(data)
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

def get_all_texts(el, class_name):
    return [e.text_content() for e in el.find_class(class_name)]

def main():
    pass


if __name__ == '__main__':
    main()