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

from lxml import etree

def get_from_text():
    text = '''
    <div>
        <ul>
             <li class="item-0"><a href="link1.html">first item</a></li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-inactive"><a href="link3.html">third item</a></li>
             <li class="item-1"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a>
         </ul>
     </div>
    '''
    html = etree.HTML(text)
    result = etree.tostring(html)
    print(result)

def get_from_file():
    html = etree.parse('hello.html')
    result = etree.tostring(html, pretty_print=True)
    print(result)

def get_li():
    html = etree.parse('hello.html')
    print (type(html))
    result = etree.tostring(html, pretty_print=True)
    print(result)

    print ('1）獲取所有的<li> 標籤')
    result = html.xpath('//li')
    print(result)
    print(len(result), type(result))
    print(result[0], len(result[0]), type(result[0]))

    print ('2）獲取<li> 標籤的所有class(*****)')
    result = html.xpath('//li/@class')
    print(result)
    print(len(result), type(result))
    print(result[0], len(result[0]), type(result[0]))

    print('3）獲取 < li > 標籤下href為link1.html的 < a > 標籤')
    result = html.xpath('//li/a[@href="link1.html"]')
    print(result)
    print(len(result), type(result))
    if len(result) > 0: print(result[0].tag)

    print('4）獲取<li> 標籤下的所有<span> 標籤')
    result = html.xpath('//li//span')
    print(result)
    print(len(result), type(result))

    print('5）獲取<li> 標籤下的所有class，不包括<li>')
    result = html.xpath('//li/a//@class')
    print(result)
    print(len(result), type(result))

    print('6）獲取最後一個<li> 的<a> 的href')
    result = html.xpath('//li[last()]/a/@href')
    print(result)
    print(len(result), type(result))

    print('7）獲取倒數第二個元素的內容(*****)')
    result = html.xpath('//li[last()-1]/a')
    print(result)
    print(len(result), type(result))
    print(result[0].text)
    print(result[0])
    print(len(result[0]), type(result[0]))

    print('8）獲取class 為bold 的標籤名')
    result = html.xpath('//*[@class="bold"]')
    print(result, len(result), type(result))
    if len(result) >0 : print(result[0].tag)

def main():
    get_li()

if __name__ == '__main__':
    main()