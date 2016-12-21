aa="aa.war.ccc"
import requests,json
import PyV8
#aa={"name":"zhangsan","sex":"man","age":25}
#bb=str(aa)
#print bb['name']
#gg=json.dumps(bb)
#cc=json.loads(gg)
#print cc['name']
def aaa(fn):
    print fn.__name__
  #  aa=7
  #  bb=9
    print "this "
#@aaa
def bbb():
    ccc="this "
    print ccc
aaa(bbb)
#cc=json.loads(gg)
#print cc
#print aa.get()
#time=time.strftime('%Y%m%d')
'''aa=requests.get('http://www.baidu.com')
bb=aa.headers
cc=bb['Set-Cookie'].split(';')
dd=[]
for i in cc:
    i.strip()
    dd.append(i)
print dd[2]


#bb='t'
#print time

#import os,sys
#f=os.listdir(r'f:\test')
#for i in f:
#    if re.search(time,i):
#        print i '''
