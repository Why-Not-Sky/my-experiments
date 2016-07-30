# -*- coding: utf-8 -*-
'''---------------------------------------------------------------------------------------------------------------------------------------
version  date    author     memo
------------------------------------------------------------------------------------------------------------------------------------------
python lxml xpath 使用实例！，有需要的朋友可以参考下。

python lxml xpath 使用实例
目标：使用xpath定位节点，也可以说好像在sql 上提取数据！
例子

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
import lxml.html

html='''
<html>
<body>
<bookstore position="cn">
    <book category="A">
        <title lang="en">Everyday Italian</title>
        <author>Giada De Laurentiis</author>
        <year>2005</year>
        <price>30.00</price>
    </book>
    <book category="B">
        <title lang="en">Harry Potter</title>
        <author>J K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
</bookstore>
<bookstore position="pk">
    <book category="A">
        <title lang="en">Learning XML</title>
        <author>Erik T. Ray</author>
        <year>2003</year>
        <price>39.95</price>
    </book>
</bookstore>
<bookstore position="jp">
    <book category="C">
        <title lang="en">XQuery Kick Start</title>
        <author>James McGovern</author>
        <author>Per Bothner</author>
        <author>Kurt Cagle</author>
        <author>James Linn</author>
        <author>Vaidyanathan Nagarajan</author>
        <year>2003</year>
        <price>49.99</price>
    </book>
</bookstore>
</body>
</html>
'''
# get from file
html = lxml.etree.parse('data/books.html')
doc = lxml.html.document_fromstring(html)
#使用绝对值
print("总共有%d本书" %(len(doc.xpath('/html/body/bookstore/book'))))
#使用相对法,这果同文件路径表示法有出入，//在这里表示相对，在文件路径表示为没效果
#只要匹配book就可以了
print("使用相对")
print("总共有%d本书" %(len(doc.xpath('//book'))))
print("总共有%d本书" %(len(doc.xpath('//bookstore/book'))))
print("总共有%d本书" %(len(doc.xpath('//body//book'))))

#使用上级表示 ..
print("使用上级")

print("总共有%d本书" %(len(doc.xpath('//../title'))))
# 使用*来限制等级
print("总共有%d本书" %(len(doc.xpath('/html/body/*/book'))))
#反映用层的用法
print("这个不成功的,总共有%d本书" %(len(doc.xpath('/html/body/*/*/book'))))
#使用谓词（筛选表达式）
#类似 一些语言表达式  1 > 2 && 3 < 4
#已知文本节点一般当值值来使用了

print("2005 年出版的书有%d本"% (len(doc.xpath('/html/body/bookstore/book[year=2005]'))))
print("2003 年出版的书有%d本"% (len(doc.xpath('/html/body/bookstore/book[year=2003]'))))
print("价钱大于>39的书有%d本" %(len(doc.xpath('/html/body/bookstore/book[price>39]'))))


#一个轴，类似于已知一个节点怎样反求其他节点
#ancestor,ancestor-or-self,attribute,child,descendant,descendant-or-self,following,namespace,namespace...
print("2005 年出版的书在 %s" % (" ".join([ i.get("position")  for i in doc.xpath('/html/body/bookstore/book[year=2003]/parent::*') ])))

def main():
    pass


if __name__ == '__main__':
    main()