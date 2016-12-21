from flask import Flask,request
import requests,os
import paramiko,time,sys
import hashlib
import urllib
import binascii
import hmac
import copy
import random
import sys
import time
from pprint import pprint
from optparse import OptionParser
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import flaskauth

time=time.strftime("%Y%m%d%H%M")
hostname="192.168.42.105"
port=6022
username="logview"
password="logview"
reload(sys)
sys.setdefaultencoding("utf-8")

try: import simplejson as json
except: import json

class mvfile():
    def __init__(self,m3u8,stime,etime):
        self.m3u8=m3u8
        self.stime=stime
        self.etime=etime
    def tfile(self):
        aa=requests.get("http://hlive.tv189.cn/%s.m3u8?playseek=%s-%s&videotype=2&isdebug=csml" %(self.m3u8,self.starttime,self.endtime))
        bb=aa.content
        cc=bb.split("\n")
        dd=[]
        if os.path.exists(r"e:\freshurl\%s" %(time)):
            print "file have exiting"
        else:
            os.mkdir(r"e:\freshurl\%s" %(time))
        for i in cc:
           if "#" not in i:
              dd.append(i.split("?")[0])
        print dd
        f=open(r'e:\freshurl\%s\tm.txt','w' %(time))
        for x in dd:
         f.write(x+"\n")
        f.close()
    def file(self):
        live=requests.get("http://hlive.tv189.cn/live2/%s.m3u8?playseek=%s-%s&videotype=2&isdebug=csml" %(self.m3u8,self.starttime,self.endtime))
        live1=live.content
        live2=live1.split("\n")
        live3=[]
        if os.path.exists(r"e:\freshurl\%s" %(time)):
            print "file have exiting"
        else:
            os.mkdir(r"e:\freshurl\%s" %(time))
        for y in live2:
            if "#" not in y:
                live3.append(y.split("?")[0])
        f=open(r'e:\freshurl\%s\live.txt','w' %(time))
        for z in live3:
            f.write(z+"\n")
        f.close()
    def put(self):
        local_dir=r"e:\freshurl\%s" %(time)
        remote_dir="/tmp/"
        try:
           t = paramiko.Transport((hostname, port))
           t.connect(username=username,password=password)
           sftp = paramiko.SFTPClient.from_transport(t)
           files = sftp.listdir(local_dir)
           for f in files:
             sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))
        except Exception:
            print "connect error"
def urlfile():
        f = open(r"e:\freshurl\$s\tm.txt", 'r' %(time))
        n = open(r"e:\freshurl\%s\live.txt",'r' %(time))
        aa = f.readlines()
        bb=n.readlines()
        cc = []
        for i in aa:
            i = "http://ltetp3.tv189.com" + i.rstrip("\n")
            cc.append(i)
        for l in bb:
            l="http://ltetp3.tv189.com" + l.rstrip("\n")
            cc.append(l)
        u=open(r"f:\freshurl\%s\url.txt",'w' %(time))
        for x in cc:
            u.write(x+"\n")
        f.close()
        n.close()
class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestHost, requestUri, params, method = 'GET'):
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]

class Request:
    timeout = 10
    version = 'Python_Tools'
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def send(self, requestHost, requestUri, params, files = {}, method = 'GET', debug = 0):
        params['RequestClient'] = Request.version
        params['SecretId'] = self.secretId
        sign = Sign("AKIDPRsohihQJZGnWlSW5JbwPxrmp4WSi34l", "Atm30BHrBv2x27MLCoAGsupMpf4mGy6n")
        params['Signature'] = sign.make(requestHost, requestUri, params, method)

        url = 'https://%s%s' % (requestHost, requestUri)

        if debug:
            print method.upper(), url
            print 'Request Args:'
            pprint(params)
        if method.upper() == 'GET':
            req = requests.get(url, params=params, timeout=Request.timeout,verify=False)
        else:
            req = requests.post(url, data=params, files=files, timeout=Request.timeout,verify=False)

        if debug:
            print "Response:", req.status_code, req.text
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        rsp = {}
        try:
            rsp = json.loads(req.text)
        except:
            raise ValueError, "Error: response is not json\n%s" % req.text

        code = rsp.get("code", -1)
        message = rsp.get("message", req.text)
        if rsp.get('code', -404) != 0:
            raise ValueError, "Error: code=%s, message=%s" % (code, message)
        if rsp.get('data', None) is None:
            print 'request is success.'
        else:
            print rsp['data']




def Name(name):
    up = False
    new_name = ""
    for i in name:
        if i == '_':
            up = True
            continue
        if up:
            new_name += i.upper()
        else:
            new_name += i
        up = False
    return new_name


class Cdn:
    def __init__(self,urlf):
        self.params = {
                'Re.g.ion': 'gz',
                'Nonce': random.randint(1, sys.maxint),
                'Timestamp': int(time.time()),
                'secret_id' : "AKIDPRsohihQJZGnWlSW5JbwPxrmp4WSi34l",
                'secret_key' : "Atm30BHrBv2x27MLCoAGsupMpf4mGy6n",
                }
        self.files = {}
        self.urlf = urlf
        self.host = 'cdn.api.qcloud.com'
        self.uri = '/v2/index.php'
        self.method = "POST"
        self.debug = 1

    def parse_args(self):
        actions = []
        for method in dir(self):
            if method[0].isupper():
                actions.append( method )

        usage='usage: %prog Action [options]\nThis is a command line tools to access Qcloud API.\n\nSupport Actions:\n    '+"\n    ".join(actions)
        self.parser = OptionParser(usage=usage)
        from sys import argv


        action = "RefreshCdnUrl"
        self.params['Action'] = action
        usage='usage: %%prog Action [options]\n\nThis is help message for action "%s"\nMore Usage: http://www.qcloud.com/wiki/v2/%s' % (action, action)
        self.parser = OptionParser(usage=usage)
        self.parser.add_option('--debug', dest='debug', action="store_true", default=False, help='Print debug message')

        getattr(self, action)()


        (options, args) = self.parser.parse_args() # parse again
        self.debug = options.debug
        for key in dir(options):
            if not key.startswith("__") and getattr(options, key) is None:
                raise KeyError, ('Error: Please provide options --%s' % key)


        for option in self.parser.option_list:
            opt = option.dest
            if opt not in [None, 'secret_id', 'secret_key', 'debug']:
                self.params[ Name(opt) ] = getattr(options, opt)

        self.options = options
        method = 'get_params_' + action
        if hasattr(self, method): getattr(self, method)()

        # format params
        for key, value in self.params.items():
            if value == '':
                del self.params[key]
            if isinstance(value, list):
                del self.params[key]
                for idx, val in enumerate(value):
                    self.params["%s.%s"%(key, idx)] = val

        #request = Request(options.secret_id, options.secret_key)
        request = Request("AKIDPRsohihQJZGnWlSW5JbwPxrmp4WSi34l", "Atm30BHrBv2x27MLCoAGsupMpf4mGy6n")
        return request.send(self.host, self.uri, self.params, self.files, self.method, self.debug)


    def DescribeCdnHosts(self):
        self.parser.add_option('--offset', dest='offset', default='', help="offset")
        self.parser.add_option('--limit', dest='limit', default='',help="limit")

    def RefreshCdnUrl(self):

        self.parser.add_option('--urls', dest='urls', default=[], action="append", help="Flush thje cache of these URLs(use multi --urls)")
        self.parser.add_option('--urls-from', dest='urls_from', default=self.urlf, metavar="FILE", help="Flush the cache of these URLs(one url per line)")

#def main():
#    test = mvfile(sys.argv[1], sys.argv[2], sys.argv[3])
#    nowtime = time.strftime("%Y%m%d%H%M")
#    now = nowtime[:6]
#    if len(sys.argv[2]) == 12 and len(sys.argv[3]) == 12 and now in sys.argv[2] and now in sys.argv[3]:
#        if sys.argv == 4 and 'tm' in sys.argv[1]:
#            test.tfile()
#        elif sys.argv == 4:
#            test.file()
#        else:
#            print "parameter is incorrent"
#            sys.exit(1)
#        test.put()
#    else:
#        print "time is false"
#        sys.exit(1)
#    urlfile()
app = Flask(__name__)

@app.route('/')
@flaskauth.auth.login_required
def indix():
        urlfe = request.args.get('urlfe')
        cdn = Cdn(urlfe)
        try:
            cdn.parse_args()
        except Exception as e:
            print e
            return "error"

        return "OK %s" % urlfe
@app.route('/url')
@flaskauth.auth.login_required
def urlfile():
    m3u8=request.args.get('m3u8')
    stime=request.args.get('stime')
    etime=request.args.get('etime')
    test = mvfile(m3u8, stime, etime)
    nowtime = time.strftime("%Y%m%d%H%M")
    now = nowtime[:6]
    try:
       if len(stime) == 12 and len(etime) == 12 and now in stime and now in etime:
         if 'tm' in m3u8:
            test.tfile()
         else:
            test.file()
        #else:
        #    print "parameter is incorrent"
        #    sys.exit(1)
         test.put()
       else:
         print "time is false"
         sys.exit(1)
       urlfile()
    except Exception as e:
        print e
        return "error"
    return "OK"
if __name__ == '__main__':
#    main()
    app.run(host="192.168.6.123",port=8080)

             #cc="201611011203"
#cc1=int(cc)
#dd="201611011301"
#dd1=int(dd)
#print cc1[8:10]-dd1[8:10]