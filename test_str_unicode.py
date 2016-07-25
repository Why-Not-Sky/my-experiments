# coding=UTF-8
# http://www.codedata.com.tw/python/python-tutorial-the-1st-class-4-unicode-support-basic-input-output/
# http://python.ez2learn.com/basic/unicode.html

msg = u'上市櫃股票'
encoded = msg.encode('utf8')
print repr(encoded)

stock = '\xe4\xb8\x8a\xe5\xb8\x82\xe6\xab\x83\xe8\x82\xa1\xe7\xa5\xa8'
print stock.decode('utf8')
print '\xe4\xb8\x8a'.decode('utf8')   #上

# erro 
# fp = '\xa4W\xc2d\xaa\xd1\xb2\xbc\xa6\xe6\xb1\xa1(\xa7t\xb5\xa5\xbb\xf9\xa1B\xb9s\xaa\xd1\xa1B\xbdL\xab\xe1\xa1B\xb9d\xc3B\xa5\xe6\xa9\xf6)\r\nData Date:105/06/23\r'
# print fp.decode('utf8')

# '\xa4W\xc2d\xaa\xd1\xb2\xbc\xa6\xe6\xb1\xa1(\xa7t\xb5\xa5\xbb\xf9\xa1B\xb9s\xaa\xd1\xa1B\xbdL\xab\xe1\xa1B\xb9d\xc3B\xa5\xe6\xa9\xf6)\r\nData Date:105/06/23\r'

msg = u'今天天氣真好'
encoded = msg.encode('utf8')
print repr(encoded)
print msg[:1], msg[:1].encode('utf8'), repr(msg[:1].encode('utf8'))

encoded = '\xe4\xbb\x8a\xe5\xa4\xa9\xe5\xa4\xa9\xe6\xb0\xa3\xe7\x9c\x9f\xe5\xa5\xbd'
msg = encoded.decode('utf8')
print msg

print '-'*60

str = '測試'
print str, type(str), len(str)  # 顯示 "<type 'str'>", 6

strU = str.decode('utf8')

print strU, type(strU), len(strU)  # 顯示 "<type 'unicode'>", 2

backToBytes = strU.encode('utf8')

print backToBytes, type(backToBytes), len(backToBytes)  # 顯示 "<type 'str'>", 6

# print str.encode('big5')   #err: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128) 
# print str.encode('utf-8')  #err: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)


print '-'*60

utext = u'測試'
print utext, type(utext),  len(utext)  # 顯示 "<type 'unicode'>", 2

strU = utext.encode('utf8')
backToBytes = strU.decode('utf8')

print 'utext.encode()', strU, type(strU), len(strU) # 顯示 "<type 'str'>", 2
print 'strU.decode()', backToBytes, type(backToBytes), len(backToBytes) # 顯示 "<type 'unicode'>", 2

