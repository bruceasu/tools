#!/usr/bin/env python
# coding: utf-8

# pywin32
import win32clipboard as w
import win32con
import sys
import binascii
import json

def getText():
    w.OpenClipboard()
    #d = w.GetClipboardData(win32con.CF_TEXT)
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    #w.SetClipboardData(win32con.CF_TEXT, aString)
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

def stringWidth(aString):
    if aString is None or aString == "":
        return 0
    count = 0
    for ch in aString:
        code = ord(ch)
        #print "code: ", code
        # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
        if (0x4e00 <= code and code <= 0x9fa5 ) or  \
            (0x2e80 <= code and code <= 0xa4cf ) or \
            (0xf900 <= code and code <= 0xfaff ) or \
            (0xfe30 <= code and code <= 0xfe4f ) :
            count += 2
        else: 
            count += 1
    return count



if __name__ == '__main__':
    mode = 0;
    if len(sys.argv) > 1:
       try:
           mode = int(sys.argv[1])
       except Exception, e:
           print e.message
           sys.exit(1)
    try:
        text = getText()
        print "--> ", text
        if mode == 0:
            fmtText = json.dumps(json.loads(text), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            fmtText = json.dumps(json.loads(text), ensure_ascii=False)
        print "<-- ", fmtText
        setText(fmtText)
    except Exception, e:
        print e.message
