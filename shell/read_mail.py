#!/usr/bin/env python
#encoding=utf-8

import email, os, sys
from optparse import OptionParser

class work:
    # class to get attachement
    def __init__(self, directory = 'd:\\'):
        self.directory = directory
        self.body = ''

    def getAtt(self):
        # traverse the directory
        for root, dirs, files in os.walk(self.directory):
            for fl in files:
                routine = self.directory + r'\\' + fl
                print routine
                filepointer = open(routine, 'r')
                # read file as email
                for line in filepointer:
                    self.body += line
                mail = email.message_from_string(self.body)
                # walk the stream, get attachement
                for part in mail.walk():
                    filename = email.Header.decode_header\
                            (part.get_filename())[0][0]
                    att_path = os.path.join(self.directory, filename)
                    outfile = open(att_path, 'wb')
                    if part.get_payload(decode = True):
                        outfile.write(part.get_payload(decode = True))
                    outfile.close()
    def parse_add(self, tostr):
        addresses = []
        if tostr == None :
            tostr = ''
        tostr = tostr.replace('\n','').replace('\t','').replace('"','').replace("'","")
        tol = tostr.split(',')
        for t in tol:
            p = email.utils.parseaddr(t)
            name = p[0]
            taddr = p[1]
            inx = taddr.find("@")
            if inx != -1:
                addresses.append("%s&lt;%s&gt;" % (name, taddr))
        return addresses
                
    def read_mail(self, file_path):
        fp = open(file_path)
        msg = email.message_from_file (fp)
        subject = msg.get("subject") # 取信件头里的subject,　也就是主题
        # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC?=这样的subject
        h = email.Header.Header(subject)
        dh = email.Header.decode_header(h)
        subject = dh[0][0]
        _from_user = email.utils.parseaddr(msg.get("from"))
        from_user = "%s<%s>" % _from_user;
        to = self.parse_add(msg.get('to'))
        cc = self.parse_add(msg.get('cc'))
        bc = self.parse_add(msg.get('bc'))
        # print "to: ", email.utils.parseaddr(msg.get("to"))[1] # 取to
        # print "cc: ", email.utils.parseaddr(msg.get("cc"))[1] # 取cc
        # 循环信件中的每一个mime的数据块
        content_file = ""
        content = ""
        file_cnt = 0;
        attachement_files = []
        for par in msg.walk():
            if not par.is_multipart(): # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
                name = par.get_param("name") #如果是附件，这里就会取出附件的文件名
                if name:
                    #有附件
                    # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                    h = email.Header.Header(name)
                    dh = email.Header.decode_header(h)
                    fname = "%d-%s" % (file_cnt, dh[0][0])
                    print '附件名:', fname
                    data = par.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
                    try:
                        att_path = os.path.join(self.directory, fname)
                        f = open(att_path, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
                    except:
                        print '附件名有非法字符，自动换一个'
                        fname = 'attach-' + file_cnt
                        f = open(fname, 'wb')
                    file_cnt += 1
                    f.write(data)
                    f.close()
                    attachement_files.append('<li><a href="./%s" target="_blank">%s</a></li>' % (fname, fname))
                else:
                    #不是附件，是文本内容
                    content = par.get_payload(decode=True) # 解码出文本内容，直接输出来就可以了
                # print '+'*60 # 用来区别各个部分的输出
        fp.close()
        content_file = os.path.join(self.directory, "email_content.htm")
        f = open(content_file, 'wb')
        header_content = """
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    </head>
    <body>
        """
        footer_content = """
    </body>
</html>
        """
        f.write(header_content)
        f.write("<p><strong>主题: </strong>%s</p>" % subject)
        f.write("<p><strong>来自: </strong>%s </p>" % from_user)
        f.write("<p><strong>收信人: </strong>%s </p>" % ", ".join(to))
        f.write("<p><strong>抄送: </strong>%s </p>" % ", ".join(cc))
        f.write("<p><strong>密抄:</strong> %s </p>" % ", ".join(bc))
        f.write("<hr/>")
        f.write(content)
        f.write("<hr/>")
        f.write("<p><ol>")
        f.write("".join(attachement_files))
        f.write("</ol></p>")
        f.write(footer_content)
        f.close()
        os.system("cmd /c start " + content_file)
        
def read_dir_main():
    # use OptionParser to privide opt
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-d", "--dir", dest="directory",
                            help="processing directory")
    opt, args = parser.parse_args()
    p = work(opt.directory)
    p.getAtt()

def main():
    if len(sys.argv) < 2:
        print "usage: sys.argv[0] file_path"
        sys.exit(1)
    p = work()
    p.read_mail(sys.argv[1])
    
if __name__ == '__main__':
    main()
