# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
0.1     2017/07/28          http://blog.csdn.net/winterto1990/article/details/47903653


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

def test_xpath():
    html = """
        <!DOCTYPE html>
        <html>
            <head lang="en">
            <title>测试</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            </head>
            <body>
                <div id="content">
                    <ul id="ul">
                        <li>NO.1</li>
                        <li>NO.2</li>
                        <li>NO.3</li>
                    </ul>
                    <ul id="ul2">
                        <li>one</li>
                        <li>two</li>
                    </ul>
                </div>
                <div id="url">
                    <a href="http:www.58.com" title="58">58</a>
                    <a href="http:www.csdn.net" title="CSDN">CSDN</a>
                </div>
            </body>
        </html>
    """
    selector = etree.HTML(html)
    content = selector.xpath('//div[@id="content"]/ul[@id="ul"]/li/text()')  # 这里使用id属性来定位哪个div和ul被匹配 使用text()获取文本内容
    for i in content:
        print (i)

    con = selector.xpath('//a/@href')  # 这里使用//从全文中定位符合条件的a标签，使用“@标签属性”获取a便签的href属性值
    for each in con:
        print (each)
    '''
    # 输出结果为：
    http:www
    .58.com
    http:www.csdn.net
    '''

    con = selector.xpath('/html/body/div/a/@title')  # 使用绝对路径定位a标签的title
    con = selector.xpath('//a/@title')  # 使用相对路径定位 两者效果是一样的
    print (len(con), con[0], con[1])

def main():
    test_xpath()

if __name__ == '__main__':
    main()