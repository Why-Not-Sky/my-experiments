# -*- coding: utf-8 -*-
# http://www.blog.pythonlibrary.org/2012/06/07/python-101-how-to-download-a-file/
import urllib
#import urllib2
from urllib.request import urlopen
import requests
import io
import sys
import locale
import time

print (sys.getdefaultencoding(), locale.getpreferredencoding())

# sys.setdefaultencoding("utf-8")
# locale -a in terminal to get the localization list
#locale.setlocale(locale.LC_ALL, 'zh_TW.UTF-8')
locale.setlocale(locale.LC_ALL, '')

#url1 = 'http://www.blog.pythonlibrary.org/wp-content/uploads/2012/06/wxDbViewer.zip'
date_str='20160712'
month_str=date_str[:6]
#taiwan_date_str = '105/07/12'
taiwan_date_str = '{0}/{1:02d}/{2:02d}'.format(int(date_str[:4]) - 1911, int(date_str[4:6]), int(date_str[6:]))

# 上市：
url_html = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=&qdate={}&selectType=ALL".format(taiwan_date_str)
url_csv = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=csv&qdate={}&selectType=ALL".format(taiwan_date_str)
url_excel = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX3_print.php?genpage=genpage/Report{}/A112{}ALL_1.php&type=csv".format(month_str, date_str)

# 上櫃：
# http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/07/12&s=0,asc,0
#url = 'http://www.tpex.org.tw/ch/stock/aftertrading/DAILY_CLOSE_quotes/stk_quote_download.php?d=105/07/12&s=0,asc,0'

ttime = str(int(time.time() * 100))
url_otc = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_result.php?l=zh-tw&d={}&_={}'.format(taiwan_date_str, ttime)

print ("downloading {} from tse:".format(date_str), url_html)
urllib.request.urlretrieve(url_html, date_str+".html")  #python 3
print ("downloading {} from tse:".format(date_str), url_csv)
urllib.request.urlretrieve(url_csv, date_str+".csv")  #python 3
exit()

print ("testing the download file to long:", url_otc)
# issue caused by excel's reader
r = requests.get(url_otc)
with open("0-otc.csv", "wb" ) as code:
    code.write(r.content)
    code.close()

print ("downloading version 1 with urllib:", url_csv)
#urllib.urlretrieve(url1, "1.csv")  #python 2
urllib.request.urlretrieve(url_csv, "1-urlretrieve.csv")  #python 3

print ("downloading version 1 with requests.post")
payload = {
    'download': 'csv',
    'qdate': taiwan_date_str,
    'selectType': 'ALL'
}
url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
# http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php?download=csv&qdate=105/07/12&selectType=ALL

# Get html page and parse as tree
r = requests.post(url, data=payload)
with open("1-post.csv", "wb") as code:
    code.write(r.content)
    code.close()

print ("downloading version 1 with requests.get")
r = requests.get(url_csv)
with open("1-get.csv", "wb" ) as code:
    code.write(r.content)
    code.close()

print ("downloading version 2 with urllib2")
#f = urllib2.urlopen(url)  #python 2
f = urllib.request.urlopen(url_excel)  #python 3
data = f.read()
with open("2-urlopen.csv", "wb") as code:
    code.write(data)
    code.close()


#f = urllib2.urlopen(url)
#f = urllib.request.urlopen(url)  #python 3
#data = f.read()
#with io.open("4.csv", "w", encoding="utf8") as code:
#    code.write(data) #.decode('utf8'))


