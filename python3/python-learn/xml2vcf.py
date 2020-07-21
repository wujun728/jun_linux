# -*-encoding=utf-8-*-
from xml.dom.minidom import *
'''
The MIT License (MIT)

Copyright (c) 2014 mr.github

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

'''
    2014-02-09 01:23:51
    desc:   将刷机精灵软件导出的xml格式联系人转换为vcf格式联系人
    mail:   withfaker@gmail.com
    blog:   http://mktime.org

    0.使用前,先将刷机精灵导出的xml文件第一行删除.
    1.如果导出的文件有空行,  :g/^$/d
    2.如果导出的用户号码中间有横杠,   :%s/-//g
'''

def data(node):
    for i in node.childNodes:
        if i.nodeType == i.TEXT_NODE:
            return i.data

def main():
    filename = 'contacts.xml'
    dom = parse(filename)
    root = dom.documentElement
    l = root.getElementsByTagName('people')
    o = open('contacts.vcf', 'w')

    for i in l:
        phone_no = ""
        cust_name = i.getAttribute('displayname')

        phones = i.getElementsByTagName('phones')
        if len(phones) > 0:
            phone = phones[0].getElementsByTagName('phone')[0]
            #print phone.getAttribute('type')
            phone_no = data(phone)

        fmt = """
BEGIN:VCARD
VERSION:3.0
N:%s;;;;
FN:%s
TEL;TYPE=HOME:%s
END:VCARD"""  % (cust_name, cust_name, phone_no)
        fmt = fmt.encode('utf-8')
        o.write(fmt)
    o.close()

if __name__ == '__main__':
    main()
