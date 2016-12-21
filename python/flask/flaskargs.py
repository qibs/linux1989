#-*- encoding: utf-8 -*-
from flask import Flask,request
app=Flask(__name__)
#aa=[]
class qq():
    def __init__(self):
        pass
    @staticmethod
    def ipad(self):
        print "this is ipad"
    @staticmethod
    def portal(self):
        print "this is portal"
    @staticmethod
    def boss(self):
        print "this is boss"
#def first():
 #   global aa
#    aa.append("111,222")
#    return aa
@app.route('/')
def aaa():
  #  war=request.args.get('war')
   # t2=request.args.get('portal')
   # t3=request.args.get('boss')
 #   aa=t1+t2
   # if t1=="on" and t2=="on" and t3=="on":
   # print request.args.keys()
    print request.args.keys()
    for i in request.args.keys():
 #     if request.args.get(i)=="on":
     x=request.args.get(i)
     getattr(qq,x,"default")(qq)
      #getattr(qq,t2,"default")(qq)
    return "OK"

if __name__=='__main__':
    app.run()