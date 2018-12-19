#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re,urllib.request,urllib.error,urllib.parse
class Getmyip:
    
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except Exception:
            try:
                myip = self.visit("http://www.whereismyip.com/")
            except:
                myip = "So sorry!!!"
        return myip

    def visit(self,url):
        opener = urllib.request.urlopen(url)
        str = opener.read()
        opener.close()
        pattern = re.compile(r'\d+\.\d+\.\d+\.\d+')
        return pattern.search(str.decode('gbk')).group(0)
getmyip = Getmyip()
localip = getmyip.getip()
print(localip)
out = open('trust.list', 'w')
out.write(localip)
out.close()
print('DONE!')
