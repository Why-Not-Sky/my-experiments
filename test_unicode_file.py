# -*- coding: utf-8 -*-

import io

foo = u'Δ, Й, ק, ‎ م, ๗, あ, 叶, 葉, and 말.'
filename = 'text.txt'

# process Unicode text
with io.open(filename,'w',encoding='utf8') as f:
    f.write(foo) # foo.encode('utf8'))
    f.close()

with io.open(filename,'r',encoding='utf8') as f:
    text = f.read()
    f.close()

print (text)
    
