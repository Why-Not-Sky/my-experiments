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
from os.path import basename
from urllib.parse import urljoin
from lxml import html
import requests

def test_html():
    base_url = 'http://www.cde.ca.gov/ds/sp/ai/'
    page = requests.get(base_url).text
    doc = html.fromstring(page)

    html_ele = [a for a in doc.cssselect('a')]

    hrefs = [a.attrib['href'] for a in doc.cssselect('a')]
    xls_hrefs = [href for href in hrefs if 'xls' in href]
    for href in xls_hrefs:
      print(href) # e.g. documents/sat02.xls

def main():
    test_html()

if __name__ == '__main__':
    main()