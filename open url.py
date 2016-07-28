# -*- coding: utf-8 -*-

import urllib.request

url = 'https://www.google.com.tw/?ion=1&espv=2#q=叡揚'
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
data = response.read()
print (data)  #native html text data...
'''
b'<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="zh-TW">
<head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
<meta content="/images/branding/googleg/1x/googleg_standard_color_128dp.png" itemprop="image"><title>Google</title>
<script>(function(){window.google={kEI:\'wTyMV7j0DMOu0ATP8ongAg\',kEXPI:\'3700305,3700389,4029815,4031109,4032677,4036509,4036527,4038012,4039268,4043492,4045841,4048347,4052304,4057739,4058543,4061155,4062333,4062972,4063879,4064096,4064702,4064904,4065786,4065873,4065918,4066237,4066654,4067178,4067518,4067938,4068548,4068550,4068577,4068604,4068844,4068850,4068865,4069194,4069458,4069783,4069839,4069840,4069904,4070110,4070127,4070139,4070230,4070287,4070337,4070399,4070454,4070503,4070598,4071020,4071261,4071422,4071448,4071450,4071452,4071576,4071600,8300096,8300273,8502184,8503585,8505158,8505511,8505592,8505655,8505768,8505774,8505803,8505841,8505870,10200083,10201795\',authuser:0,kscs:\'c9c918f0_24\'};google.kHL=\'zh-TW\';})();(function(){google.lc=[];google.li=0;google.getEI=function(a){for(var b;a&&(!a.getAttribute||!(b=a.getAttribute("eid")))
'''
# print (data.decode('utf-8'))   #error...

