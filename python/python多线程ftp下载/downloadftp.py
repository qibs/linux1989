import re
import config
import multiprocessing
from ftplib import FTP
import time,os
import logging
import threading
#aa = ['anhuigf__47B099nbOaBo', 'anhuigf__4OLDjYX6AR12','anhuigf__4OLDK91Pg7ow', 'anhuigf__4OLDr5KP4k0V', 'anhuigf__4OLDrA1aAKVw', 'anhuigf__4OLX0DN8eLAV', 'anhuigf__4OLX0KxZm2W5', 'anhuigf__4OLXMz8rOz5w']
tongdao=config.tongdao
tongdn=len(tongdao)/8
tongdaog=[]
i=0
while i< len(tongdao):
    tongdaog.append(tongdao[i:i+8])
    i+=8
#tongdaog=(tongdao[0:8],tongdao[8:16],tongdao[16:24],tongdao[24:32],tongdao[32,40],tongdao[40:48],tongdao[]
patt = re.compile(r'\.flv$')
date = time.strftime('%Y-%m-%d')
#year = date[:4]
year="2017"
#month = date[5:7]
month="03"
#day = date[8:10]
day="31"
ftpd = '/media.target.obj/dvr/live'
ip = "192.168.190.20"
port = 5789
user = 'root'
passwd = "R7iV9Jxn4IKp"
#localdir=r"e:\anhuigf"


#localdir=r"e:\%s"
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=r'e:\test\%s.log' % date,
                filemode='a')
def download(ftpdir,localdir):
    ftp=FTP()
    try:
     logging.debug(ftp.connect(ip,port))
    except Exception as a:
        logging.error(a)
        exit(1)
    try:
     logging.debug(ftp.login(user,passwd))
    except Exception as b:
        logging.error(b)
        exit(1)
    try:
      ftp.cwd(ftpdir)
    except Exception as c:
        logging.error(c)
        logging.debug(ftp.quit())
        return "%s is not found!" %ftpdir
    jihe=set(ftp.nlst())
    flvf=[x for x in jihe if patt.search(x)]
    if flvf:
      for i in flvf:

                localf=open(localdir+i,'wb').write
                try:
                 logging.debug(ftp.retrbinary("RETR %s" % i,localf,1024))
                except Exception as f:
                    logging.error(f)
                    continue
      logging.debug(ftp.quit())
      return "download successfully!"
    else:
         logging.debug("no flv file found in the %s !" %ftpdir)
         logging.debug(ftp.quit())
         return "no flv file in the %s!" %ftpdir
   # logging.debug(ftp.quit())
if __name__ == '__main__':

    for d in tongdaog:
        threads = []
        for i in d:
            ftpdir=ftpd+"/"+i+"/"+year+"/"+month+"/"+day+"/"
            localdir = r"e:\anhuigf1" + os.sep + year + os.sep + month + os.sep + day + os.sep + i + os.sep
            if not os.path.exists(localdir):
                os.makedirs(localdir)

            threads.append(threading.Thread(target=download,args=(ftpdir,localdir)))
        for t in threads:
            t.start()
        for t in threads:
             t.join()

#bb=re.compile(r'\.flv$')

