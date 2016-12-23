#!/usr/bin/python
#coding=utf-8
import time,datetime,os,urllib2,logging
now=datetime.datetime.now()
old=datetime.timedelta(days = 7)
sevenold=(now-old).strftime("%Y%m%d")
nsevenold=int(sevenold)
datadir="/data/elk/elasticsearch-2.3.4/data/tysxlog/nodes/0/indices"
logging.basicConfig(level=logging.DEBUG,
             format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
             datefmt='%Y-%m-%d %H:%M:%S',
             filename='log/%s' %(now),
             filemode='w')
logger = logging.getLogger(__name__)
dirname=[]
for dir in os.listdir(datadir):
  if "vodlog" in dir or "logstash" in dir:
    aa=dir.strip().split("-")[1].replace(".","")
    dirname.append(aa)
filename=list(set(dirname))
oldday=[]
for i in filename:
  a=int(i)
  if a < nsevenold:
    b=str(a)
    c=str(a)[0:4] + "." +  str(a)[4:6] + "." +  str(a)[6:8]
    oldday.append(c)
#print oldday
for x in oldday:
  url1="http://192.168.51.110:9200/logstash-" + x 
  url2="http://192.168.51.110:9200/vodlog-" + x
  request1 = urllib2.Request(url1)
  request1.get_method = lambda:'DELETE'
  request1 = urllib2.urlopen(request1)
  print "logstash:" + request1.read()
  logger.debug("logstash:" + request1.read())
  request2 = urllib2.Request(url2)
  request2.get_method = lambda:'DELETE'
  request2 = urllib2.urlopen(request2)
  print "vodlog:" + request2.read() 
  logger.debug("vodlog:" + request2.read())
  
    

  




