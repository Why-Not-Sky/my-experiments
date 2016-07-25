# -*- coding: utf-8 -*-
# http://quickteckiteasy.blogspot.tw/2009/03/python-string-and-unicode-string.html
# http://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

#import urllib2
import sys
import locale

print (sys.getdefaultencoding())
print (locale.getpreferredencoding())

# sys.setdefaultencoding("utf-8")
# locale -a in terminal to get the localization list
locale.setlocale(locale.LC_ALL, 'zh_TW.UTF-8')
print ('locale.getpreferredencoding', locale.getpreferredencoding())
print ('locale.getlocale', locale.getlocale())

from urllib.request import urlopen
url = 'https://www.google.com.tw/#q=叡揚資訊'
response = urlopen(url)
data = response.read()      # a `bytes` object
print (data)
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary --> error
print (text)

url = 'http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/06/23&s=0,asc,0'
f = urlopen(url)
data = f.read()
d8 = data[:64]
print (d8, type(d8), len(d8))

print (d8.encode('utf-8'))

ud8 = d8.decode('utf-8')
print (ud8, type(d8), len(d8))

#print d8.decode('utf8')
