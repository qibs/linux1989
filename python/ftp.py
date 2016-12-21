from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from flask import Flask,request
from flask import redirect
from ftplib import FTP
from optparse import OptionParser
import os,sys
import logging
class ftp():
    def __init__(self):
        self.ftp=None
        self.parser = OptionParser()

        def __del__(self):
            pass

        def setFtpParams(self, ip, uname, pwd, port=21, timeout=60):
            self.ip = ip
            self.uname = uname
            self.pwd = pwd
            self.port = port
            self.timeout = timeout

        def initEnv(self):
            if self.ftp is None:
                self.ftp = FTP()
                print '### connect ftp server: %s ...' % self.ip
                self.ftp.connect(self.ip, self.port, self.timeout)
                self.ftp.login(self.uname, self.pwd)
                print self.ftp.getwelcome()

        def clearEnv(self):
            if self.ftp:
                self.ftp.close()
                print '### disconnect ftp server: %s!' % self.ip
                self.ftp = None

        def uploadDir(self, localdir='./', remotedir='./'):
            if not os.path.isdir(localdir):
                return
            self.ftp.cwd(remotedir)
            for file in os.listdir(localdir):
                src = os.path.join(localdir, file)
                if os.path.isfile(src):
                    self.uploadFile(src, file)
                elif os.path.isdir(src):
                    try:
                        self.ftp.mkd(file)
                    except:
                        sys.stderr.write('the dir is exists %s' % file)
                    self.uploadDir(src, file)
            self.ftp.cwd('..')

        def uploadFile(self, localpath, remotepath='./'):
            if not os.path.isfile(localpath):
                return
            print '+++ upload %s to %s:%s' % (localpath, self.ip, remotepath)
            self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))



        def upload(self, src):
            filetype, filename = self.__filetype(src)

            self.initEnv()
            if filetype == _XFER_DIR:
                self.srcDir = src
                self.uploadDir(self.srcDir)
            elif filetype == _XFER_FILE:
                self.uploadFile(src, filename)
            self.clearEnv()
        def wget(self):
            self.parser.add_option('--local', dest='dirs', default=[], action="append",
                                   help="Flush the cache of these DIRs(use multi --dirs)")
            self.parser.add_option('--dirs-from', dest='dirs_from', default="", metavar="FILE",
                                   help="Flush the cache of these URLs(one dir per line)")


if __name__ == '__main__':
        srcDir = r"C:\sytst"
        srcFile = r'C:\sytst\sar.c'
        xfer = ftp()
        xfer.setFtpParams('192.x.x.x', 'jenkins', 'pass')
        xfer.upload(srcDir)
        xfer.upload(srcFile)
def log(logfile):
  logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=logfile,
                    filemode='w')

  logging.debug('debug message')
  logging.info('info message')
  logging.warning('warning message')
  logging.error('error message')
  logging.critical('critical message')





