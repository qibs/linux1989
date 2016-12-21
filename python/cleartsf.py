import paramiko
import sys
import time
import hello
myclient = paramiko.SSHClient()
myclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
myclient.connect("192.168.42.105", port=6022, username="logview", password="logview")
#stdin, stdout, stderr = myclient.exec_command("ls /home/logview/")
class rmts():
    def __init__(self,m3u8,btime,etime):
        self.m3u8=m3u8
        self.btime=btime
        self.etime=etime
    tsdir=r"/data/live/live2/ts"
    ttsdir=r"/data/tmlive/ts"
    def mkback(self):
        stdin,stdout,stderr=myclient.exec_command("ls %s" %(self.tsdir))
        if stderr.read() == '':
            stdin,stdout,stderr=myclient.exec_command("ls %s | grep %s" %(self.tsdir,self.m3u8))
            m3u8dir=stdout.read().splitlines()
            for i in m3u8dir:
                stdin,stdout,stderr=myclient.exec_command("ls %s/%s/%s" %(self.tsdir,i,self.btime[:8]))
                if stderr.read() == '':
                    stdin,stdout,stderr=myclient.exec_command("mkdir %s/%s%s/backup" %(self.tsdir,i,self.btime[:8]))
                    bday=self.btime[:8]
                    eday=self.etime[:8]
                    bminutes=int(self.btime[10:12])
                    bhour=int(self.btime[8:10])
                    eminutes=int(self.etime[10:12])
                    ehour=int(self.etime[8:10])
              #      if ehour > bhour:
                    while ehour - bhour > 0:
                        for x in range(bminutes,60):
                            stdin,stdout,stderr=myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" %(self.tsdir,i,bday,i,bday,bhour,x,self.tsdir,i,bday))
                           #     bminutes+=1
                        for y in range(0,eminutes):
                            stdin, stdout, stderr = myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" %(self.tsdir,i,bday,i,bday,bhour,y,self.tsdir,i,bday))
                            #    eminutes+=1
                        bhour+=1
                        stdin,stdout,stderr=myclient.exec_command("mv %s/%s/%s/%s_%s_%s* %s/%s/%s/backup" %(self.tsdir,i,bday,i,bday,bhour,self.tsdir,i,bday))
                    if ehour == bhour:
                        for z in range(bminutes,eminutes+1):
                            stdin, stdout, stderr = myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" % (self.tsdir, i, bday, i, bday, bhour, z, self.tsdir, i, bday))

        else:
             print "file is not exiting"
             sys.exit(1)
 #               else:
 #                   print "file is not exiting"
 #                   sys.exit(1)
    def tmkback(self):
        stdin,stdout,stderr=myclient.exec_command("ls %s" %(self.ttsdir))
        if stderr.read() == '':
            stdin,stdout,stderr=myclient.exec_command("ls %s | grep %s" %(self.ttsdir,self.m3u8))
            m3u8dir=stdout.read().splitlines()
            for i in m3u8dir:
                stdin,stdout,stderr=myclient.exec_command("ls %s/%s/%s" %(self.ttsdir,i,self.btime[:8]))
                if stderr.read() == '':
                    stdin,stdout,stderr=myclient.exec_command("mkdir %s/%s%s/backup" %(self.ttsdir,i,self.btime[:8]))
                    bday=self.btime[:8]
                    eday=self.etime[:8]
                    bminutes=int(self.btime[10:12])
                    bhour=int(self.btime[8:10])
                    eminutes=int(self.etime[10:12])
                    ehour=int(self.etime[8:10])
              #      if ehour > bhour:
                    while ehour - bhour > 0:
                        for x in range(bminutes,60):
                            stdin,stdout,stderr=myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" %(self.ttsdir,i,bday,i,bday,bhour,x,self.ttsdir,i,bday))
                           #     bminutes+=1
                        for y in range(0,eminutes):
                            stdin, stdout, stderr = myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" %(self.ttsdir,i,bday,i,bday,bhour,y,self.ttsdir,i,bday))
                            #    eminutes+=1
                        bhour+=1
                        stdin,stdout,stderr=myclient.exec_command("mv %s/%s/%s/%s_%s_%s* %s/%s/%s/backup" %(self.ttsdir,i,bday,i,bday,bhour,self.ttsdir,i,bday))
                    if ehour == bhour:
                        for z in range(bminutes,eminutes+1):
                            stdin, stdout, stderr = myclient.exec_command("mv %s/%s/%s/%s_%s_%s%s*.ts %s/%s/%s/backup/" % (self.ttsdir, i, bday, i, bday, bhour, z, self.ttsdir, i, bday))

        else:
             print "file is not exiting"
             sys.exit(1)
#                else:
#                    print "file is not exiting"
#                    sys.exit(1)
def main():
    test=rmts(sys.argv[1],sys.argv[2],sys.argv[3])
    nowtime=time.strftime("%Y%m%d%H%M")
    now=nowtime[:6]
    if len(sys.argv[2])==12 and len(sys.argv[3]) == 12 and now in sys.argv[2] and now in sys.argv[3]:
      if sys.argv == 4 and 'tm' in sys.argv[1]:
         test.tmkback()
      elif sys.argv == 4:
         test.mkback()
      else:
          print "parameter is incorrent"
          sys.exit(1)
    else:
        print "time is false"
        sys.exit(1)


if __name__=='__main__':
     main()
