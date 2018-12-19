#!/usr/bin/env python
# coding: utf-8

# pywin32
import win32clipboard as w
import win32con
import sys

cols = 70
quote = False


#print 'cols: ', cols

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


def fmt(text):
    newtext=[]
    length = len(text)
    begin = 0
    count = 0
    buffer_line = "";
    newline = True
    last = None
    for i in xrange(0, length):
        if text[i] == u'\r':
            pass
        elif text[i] == u'\n':
            if newline and len(buffer_line) > 0:
                newtext.append(buffer_line)
                buffer_line = ''
                count = 0
                newtext.append('')
            else:
                newline = True
                continue
        elif text[i] == '\t' or text[i] == ' ':
            if newline:
                #skip
                #print ('skip leading space')
                pass
            elif last == '\t' or last == ' ':
                # skip
                #print ('skip more then one space')
                pass
            else:
                buffer_line += ' '
                count += 1
                last = ' '
        else:
            newline = False
            last = text[i]
            buffer_line += text[i]
            code = ord(text[i])
            #print "code: ", code
            # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
            if (0x4e00 <= code and code <= 0x9fa5 ) or  \
                (0x2e80 <= code and code <= 0xa4cf ) or \
                (0xf900 <= code and code <= 0xfaff ) or \
                (0xfe30 <= code and code <= 0xfe4f ) :
                count += 2
            else: 
                count += 1

            if (count % cols) == 0 or count > cols:
                #print count
                newtext.append(buffer_line)
                buffer_line = ""
                count = 0
        
    if buffer_line != "":
        #print count
        newtext.append(buffer_line)
        buffer_line = ""
    return u"\r\n".join(newtext)


# def fmtSignLeading(text, leading):
#     '''
#     text starts with *SPC
#     @TODO: split into lines and process leading string
#     '''
#     return fmtSameLeading(text, leading)
#     newtext=[]
#     length = len(text)
#     pad_length = len(leading)
#     count = pad_length
#     buffer_line = leading
#     newline = True
#     last = None
#     for i in xrange(pad_length, length):
#         if text[i] == u'\r':
#             pass
#         elif text[i] == u'\n':
#             if newline:
#                 # empty line
#                 if len(buffer_line) > pad_length:
#                     newtext.append(buffer_line)
#                     buffer_line = leading
#                     count = pad_length
#                     newtext.append(leading)
#                 continue
#             newline = True
#             if last is not None and ord(last) < 10175 and \
#                     count > pad_length and count < cols:
#                 # add space
#                 buffer_line += ' '
#                 count += 1
#                 last = ' '
#             else:
#                 # skip
#                 pass
            
#         elif text[i] == '\t' or text[i] == ' ':
#             if newline:
#                 #skip
#                 #print ('skip leading space')
#                 pass
#             elif last == '\t' or last == ' ':
#                 # skip
#                 #print ('skip more then one space')
#                 pass
#             else:
#                 buffer_line += ' '
#                 count += 1
#                 last = ' '
#         else:
#             newline = False
#             last = text[i]
#             buffer_line += text[i]
#             code = ord(text[i])
#             #print "code: ", code
#             # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
#             if (0x4e00 <= code and code <= 0x9fa5 ) or  \
#                 (0x2e80 <= code and code <= 0xa4cf ) or \
#                 (0xf900 <= code and code <= 0xfaff ) or \
#                 (0xfe30 <= code and code <= 0xfe4f ) :
#                 count += 2
#             else: 
#                 count += 1

#             if count % cols == 0 or count > cols:
#                 #print count
#                 newtext.append(buffer_line)
#                 buffer_line = leading
#                 count = pad_length
        
#     if buffer_line != "":
#         #print count
#         newtext.append(buffer_line)
#         buffer_line = ""
#     return u"\r\n".join(newtext)



def fmtQuoteLeading(text, quoteLeading='    '):
    newtext=[]
    length = len(text)
    pad_length = len(quoteLeading)

    leading = ' ' * pad_length
    # print pad_length, leading, pad_length
    count = pad_length
    buffer_line = quoteLeading
    global cols
    cols -= pad_length
    last = None
    newline = True
    if text[0:pad_length] == quoteLeading:
        start = pad_length
    else:
        start = 0
    for i in xrange(start, length):
        if text[i] == u'\r':
            pass
        elif text[i] == u'\n':
            if newline:
                # empty line
                if len(buffer_line) > pad_length:
                    newtext.append(buffer_line)
                    buffer_line = leading
                    count = pad_length
                    newtext.append(leading)
                continue
            newline = True
            if last is not None and ord(last) < 10175 and count > pad_length:
                # add space
                buffer_line += ' '
                count += 1
                last = ' '
            else:
                # skip
                pass
            
        elif text[i] == '\t' or text[i] == ' ':
            if newline:
                #skip
                #print ('skip leading space')
                pass
            elif last == '\t' or last == ' ':
                # skip
                #print ('skip more then one space')
                pass
            else:
                buffer_line += ' '
                count += 1
                last = ' '
        else:
            newline = False
            buffer_line += text[i]
            last = text[i]
            code = ord(text[i])
            #print "code: ", code
            # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
            if (0x4e00 <= code and code <= 0x9fa5 ) or  \
                (0x2e80 <= code and code <= 0xa4cf ) or \
                (0xf900 <= code and code <= 0xfaff ) or \
                (0xfe30 <= code and code <= 0xfe4f ) :
                count += 2
            else: 
                count += 1

        if count % cols == 0 or count > cols:
            #print count
            newtext.append(buffer_line)
            buffer_line = leading
            count = pad_length
        
    if buffer_line != "":
        #print count
        newtext.append(buffer_line)
        buffer_line = leading
    return u"\r\n".join(newtext)


def fmtNumberLeading(text, leading):
    return fmtQuoteLeading(text, leading)


def fmt3StarLeading(text):
    '''
    text starts with ***SPC
    @TODO: split into lines and process leading string
    '''
    return fmtQuoteLeading(text, '*** ')
    # newtext=[]
    # length = len(text)
    # pad_length = 4
    # leading = '    '
    # count = pad_length
    # buffer_line = "*** "
    # last = None
    # newline = True
    # for i in xrange(pad_length, length):
    #     if text[i] == u'\r':
    #         pass
    #     elif text[i] == u'\n':
    #         if newline:
    #             # empty line
    #             if len(buffer_line) > pad_length:
    #                 newtext.append(buffer_line)
    #                 buffer_line = leading
    #                 count = pad_length
    #                 newtext.append(leading)
    #             continue
    #         newline = True
    #         if last is not None and ord(last) < 10175 and count > pad_length:
    #             # add space
    #             buffer_line += ' '
    #             count += 1
    #             last = ' '
    #         else:
    #             # skip
    #             pass
            
    #     elif text[i] == '\t' or text[i] == ' ':
    #         if newline:
    #             #skip
    #             #print ('skip leading space')
    #             pass
    #         elif last == '\t' or last == ' ':
    #             # skip
    #             #print ('skip more then one space')
    #             pass
    #         else:
    #             buffer_line += ' '
    #             count += 1
    #             last = ' '
    #     else:
    #         newline = False
    #         buffer_line += text[i]
    #         last = text[i]
    #         code = ord(text[i])
    #         #print "code: ", code
    #         # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
    #         if (0x4e00 <= code and code <= 0x9fa5 ) or  \
    #             (0x2e80 <= code and code <= 0xa4cf ) or \
    #             (0xf900 <= code and code <= 0xfaff ) or \
    #             (0xfe30 <= code and code <= 0xfe4f ) :
    #             count += 2
    #         else: 
    #             count += 1

    #     if count % cols == 0 or count > cols:
    #         #print count
    #         newtext.append(buffer_line)
    #         buffer_line = "    "
    #         count = pad_length
        
    # if buffer_line != "":
    #     #print count
    #     newtext.append(buffer_line)
    #     buffer_line = ""
    # return u"\r\n".join(newtext)


def fmtSameLeading(text, leading):
    '''
    lines with the same leading or 
    lines starts with '* ', '# ', '; ', '// ','*', '#', ';', '//'
'''
    newtext=[]
    length = len(text)
    pad_length = len(leading)
    count = pad_length
    buffer_line = leading
    global cols
    cols -= pad_length
    last = None
    newline = True
    # print leading, pad_length
    lines = text.split(u"\n")
    for line in lines:
        newline = True
        #print "> ", line
        line = line.strip()
        if line[0:pad_length] == leading:
            line = line[pad_length:].strip()

        # print ">> ", line
        if line == "":
            if len(buffer_line) > pad_length:
                newtext.append(buffer_line)
                buffer_line = leading
                count = pad_length
                newtext.append(leading)
                newline = True
                continue
            elif last is not None and ord(last) < 10175 and \
                    count > pad_length and count < cols:
                # add space
                buffer_line += ' '
                count += 1
                last = ' '
                continue
            else:
                # skip
                continue 

        #print "---------------"
        for i in xrange(0, len(line)):               
            if line[i] == '\t' or line[i] == ' ':
                if newline:
                    #skip
                    #print ('skip leading space')
                    continue
                elif last == '\t' or last == ' ':
                    # skip
                    #print ('skip more then one space')
                    continue
                else:
                    buffer_line += ' '
                    count += 1
                    last = ' '
            else:
                newline = False
                buffer_line += line[i]
                last = line[i]
                code = ord(line[i])
                #print "code: ", code
                # 4E00－9FA5 || 2E80－A4CF  ||   F900-FAFF　||　FE30-FE4F
                if (0x4e00 <= code and code <= 0x9fa5 ) or  \
                    (0x2e80 <= code and code <= 0xa4cf ) or \
                    (0xf900 <= code and code <= 0xfaff ) or \
                    (0xfe30 <= code and code <= 0xfe4f ) :
                    count += 2
                else: 
                    count += 1
            #print count, buffer_line
            if count % cols == 0 or count > cols:
                #print count, buffer_line    
                newtext.append(buffer_line)
                buffer_line = leading
                count = pad_length
                newline = True
    
    #print 'end for lines...'  
    
    if buffer_line != "":
        #print count
        newtext.append(buffer_line)
        buffer_line = ""
        newline = True
    # print 'end last buffer, ', len(newtext), ' lines'
    # for line in newtext:
    #     print "< ", line

    return u"\r\n".join(newtext)


def look_like_number_start(text):
    '''line starts with number ex 1. 2. 1) 10)
    '''
    text = text.strip()
    a0 = ord('0') 
    a9 = ord('9')
    if len(text) == 0 or ord(text[0]) < a0 or ord(text[0]) > a9:
        return False, '',''

    continue_num = True
   
    for i in range(0, len(text)):
        ai = ord(text[i])
        if continue_num and ai >= a0 and ai <= a9:
            continue
        elif text[i] == ')' or text[i] == '.':
            s = text[0:i+1]
            if len(s) < 4:
                s += ' ' * (4 - len(s)) 
            else:
                s += ' '
            return True, s, text[i+1:].strip() 
        else:
            return False, '', ''

    return False,'',''


def isMode4(lines):
    '''
    lines with the same leading, only check 2 lines or 
    lines starts with '* ', '# ', '; ', '// ','*', '#', ';', '//'
    '''
    if len(lines) > 2:
        x_1_1 = lines[0].strip()
        x_2_1 = lines[1].strip()
        l1 = len(x_1_1)
        l2 = len(x_2_1)
        lead = 0
        #print x_1_1
        #print x_2_1
        for i in xrange(0, min(l1, l2)):
            if x_1_1[i] != x_2_1[i]:
                lead = i
                break
        if lead > 0:
            mode = 4
            pad = x_1_1[0:lead]
            return True, pad
        else:
            return False, ''
    else:
        return False, ''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            cols = int(sys.argv[1])
            if cols < 1:
                quote = True
                cols = 70
        except Exception, e:
            print e.message
            sys.exit(1)

    try:
        text = getText()
        #print "> ", text
        # mode
        # 1 normal
        # 2 line starts with number ex 1. 2. 1) 10)
        # 3 first lien starts with '*** ' and other indent 4 space
        # 4 lines with the same leading, only check 2 lines or 
        #   lines starts with '* ', '# ', '; ', '// ','*', '#', ';', '//'
        # 5 quote
        mode = -1

        if (stringWidth(text) < cols):
            sys.exit(2)

        text = text.strip()
        pad = ""
        x_1 = text[0]
        x_2 = text[0:2]
        x_3 = text[0:3]
        x_4 = text[0:4]
        # check ismode4
        lines = text.split('\n')
        flag, pad = isMode4(lines)
        flag2,pad2,text2 = look_like_number_start(text);
        #print flag, pad
        if quote:
            mode = 5
        elif flag:
            mode = 4
        elif flag2:
            mode = 2
            pad = pad2
            text = text2
        else:
            if x_4 == '*** ':
                mode = 3
                pad = x_4
            elif x_3 == '// ':
                mode = 4
                pad = x_3
            elif x_2 == '* ' or x_2 == '# ' or x_2 == '; ' or x_2 == '//':
                mode = 4
                pad = x_2
            elif x_1 == '*' or x_2 == '#' or x_2 == ';' :
                mode = 4
                pad = x_1
            else:
                mode = 1

        # print 'mode: ', mode
        if mode == 5:
            f = fmtQuoteLeading(text)
        elif mode == 4:
            f = fmtSameLeading(text, pad)
        elif mode == 3:
            f = fmt3StarLeading(text)
        elif mode == 2:
            f = fmtNumberLeading(text, pad) 
        else:
            f = fmt(text)
        setText(f)
        #print f
    except Exception, e:
        print e.message
