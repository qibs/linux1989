from flask import Flask,request
import time,os,re,sys
import logging
import commands
import ConfigParser
day=time.strftime('%Y%m%d')
warre="\.war$"
app=Flask(__name__)
conf=ConfigParser.ConfigParser()
conf.read('pub.conf')
hostf=["172.16.76.16","172.16.76.17","172.16.72.18"]
hosth=["172.16.77.16","172.16.77.17","172.16.77.18"]
#user='logview'
user=conf.get("connection","user")
port=conf.get("connection","port")
password=conf.get("connection","password")
wardir=conf.get("publish","sourcewar")
backdir=conf.get("publish","backdir")
confdir=conf.get("publish","confdir")
tomcatdir=conf.get("publish","tomcat")
logdir=conf.get("publish","logdir")
#warname=["ipad","portal","boss","eclp"]
time=time.strftime('%Y%m%d%H%M%S')
logging.basicConfig(level=logging.DEBUG,
             format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
             datefmt='%Y-%m-%d %H:%M:%S',
             filename=conf.get("publish","logdir")+"/"+'publish-%s.log' %(day),
             filemode='w')
logger = logging.getLogger(__name__)
if os.path.exists(wardir+day):
    print "file have exist"
else:
    wardird=os.mkdir(wardir+day)
for i in os.listdir(wardird):
    if re.search(warre, i):
        try:
         commands.getoutput("cd %s && unzip i" % (wardird))
        except Exception as e:
         logger.error(e)
        web=i.rstrip(".war")
        webdir=wardird+'/'+web
        configpath=webdir+"/WEB-INF/conf"
        classpath=webdir+"/WEB-INF/classes"
        if os.path.isdir(webdir):
            for y in os.listdir(confdir+"/"+i):
              configf=os.path.join(confdir+"/"+i,y)
              try:
               if "cache.properties" == y:
                  commands.getoutput("cp -rf %s %s" %(configf,configpath))
               elif "server.properties" == y:
                  commands.getoutput("cp -rf %s %s" %(configf,configpath))
               elif "bank-config-beans.xml" ==y:
                  commands.getoutput("cp -rf %s %s" %(configf,configpath))
               elif "log4j.properties" == y:
                  commands.getoutput("cp -rf %s %s" %(configf,configpath))
               elif "quartz.properties" ==y:
                  commands.getoutput("cp -rf %s %s" %(configf,configpath))
               else:
                  print "no this config file"
              except Exception as e:
                  logger.error(e)
        commands.getoutput("gzip %s" %(webdir))
    else:
        print "war package does not find!"

#commands.getoutput("")
ssh=paramiko.SSHClient()
class publish():
 @staticmethod
 def portal(self):
   curwar=sys._getframe().f_code.co_name
   for i in hostf:
    ssh.connect(hostname=i,port=port,username=user,password=password)
    ssh.set_missing_host_key_policy(paramiko.AuthAddPolicy())
    if os.path.exists(backdir):
        print "backup dir hsa exists"
    else:
        backdirw=os.mkdir(backdir+day)
    stdin,stdout,stderr=ssh.exec_command("ps -ef | grep java | grep %s | grep -v grep | awk '{print $2}' | xargs kill -9" %(curwar))
    logger.debug(stdout)
    stdin,stdout,stderr=ssh.exec_command("mv %s/%s/webapps/%s %s" %(tomcatdir,curwar,curwar,backdirw))
    logger.debug(stdout)
    t=paramiko.Transport((i,port))
    t.connect(username=user,password=password)
    sftp=paramiko.SFTPClient.from_transport(t)
    try:
     sftp.put(wardird+"/"+curwar+".gz",tomcatdir+curwar+".gz")
    except Exception as e:
     logger.error(e)
    t.close()
    stdin,stdout,stderr=ssh.exec_command("gunzip %s+%s+'.gz'" %(tomcatdir,curwar))
    logger.debug(stdout)
    stdin,stdout,stderr=ssh.exec_command("sh %s/%s/bin/startup.sh" %(tomcatdir,curwar))
    logger.debug(stdout)
    ssh.close()
 @staticmethod
 def boss(self):
     curwar=sys._getframe().f_code.co_name
     for i in hosth:
         ssh.connect(hostname=i, port=port, username=user, password=password)
         ssh.set_missing_host_key_policy(paramiko.AuthAddPolicy())
         if os.path.exists(backdir):
             print "backup dir hsa exists"
         else:
             backdirw = os.mkdir(backdir + day)
         stdin, stdout, stderr = ssh.exec_command("ps -ef | grep java | grep %s | grep -v grep | awk '{print $2}' | xargs kill -9" %(curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("mv %s/%s/webapps/%s %s" % (tomcatdir,curwar,curwar,backdirw))
         logger.debug(stdout)
         t = paramiko.Transport((i, port))
         t.connect(username=user, password=password)
         sftp = paramiko.SFTPClient.from_transport(t)
         try:
          sftp.put(wardird + "/"+curwar+".gz", tomcatdir + curwar+".gz")
         except Exception as e:
          logger.error(e)
         t.close()
         stdin, stdout, stderr = ssh.exec_command("gunzip %s+%s+'.gz'" % (tomcatdir, curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("sh %s/%s/bin/startup.sh" %(tomcatdir,curwar))
         logger.debug(stdout)
         ssh.close()
 @staticmethod
 def ipad(self):
     curwar=sys._getframe().f_code.co_name
     for i in hostf:
         ssh.connect(hostname=i, port=port, username=user, password=password)
         ssh.set_missing_host_key_policy(paramiko.AuthAddPolicy())
         if os.path.exists(backdir):
             print "backup dir hsa exists"
         else:
             backdirw = os.mkdir(backdir + day)
         stdin, stdout, stderr = ssh.exec_command("ps -ef | grep java | grep %s | grep -v grep | awk '{print $2}' | xargs kill -9" %(curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("mv %s/%s/webapps/%s %s" % (tomcatdir,curwar,curwar, backdirw))
         logger.debug(stdout)
         t = paramiko.Transport((i, port))
         t.connect(username=user, password=password)
         sftp = paramiko.SFTPClient.from_transport(t)
         try:
          sftp.put(wardird + "/"+curwar+".gz", tomcatdir + curwar+".gz")
         except Exception as e:
          logger.error(e)
         t.close()
         stdin, stdout, stderr = ssh.exec_command("gunzip %s+%s+'.gz'" % (tomcatdir, curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("sh %s/%s/bin/startup.sh" %(tomcatdir,curwar))
         logger.debug(stdout)
         ssh.close()
 @staticmethod
 def eclp(self):
     curwar=sys._getframe().f_code.co_name
     for i in hosth:
         ssh.connect(hostname=i, port=port, username=user, password=password)
         ssh.set_missing_host_key_policy(paramiko.AuthAddPolicy())
         if os.path.exists(backdir):
             print "backup dir hsa exists"
         else:
             backdirw = os.mkdir(backdir + day)
         stdin, stdout, stderr = ssh.exec_command("ps -ef | grep java | grep %s | grep -v grep | awk '{print $2}' | xargs kill -9" %(curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("mv %s/%s/webapps/%s %s" % (tomcatdir,curwar,curwar, backdirw))
         logger.debug(stdout)
         t = paramiko.Transport((i, port))
         t.connect(username=user, password=password)
         sftp = paramiko.SFTPClient.from_transport(t)
         try:
          sftp.put(wardird + "/"+curwar+".gz", tomcatdir + curwar+".gz")
         except Exception as e:
          logger.error(e)
         t.close()
         stdin, stdout, stderr = ssh.exec_command("gunzip %s+%s+'.gz'" % (tomcatdir, curwar))
         logger.debug(stdout)
         stdin, stdout, stderr = ssh.exec_command("sh %s/%s/bin/startup.sh" %(tomcatdir,curwar))
         logger.debug(stdout)
         ssh.close()
@app.route("/")
def war():
    war=request.args.get("war")
    try:
     getattr(publish,war,"default")(publish)
    except Exception as e:
     logger.error(e)
     return "publish failed,please check logfile"
    return war
if __name__=='__main__':
    app.run(host="172.16.20.11",port=80)