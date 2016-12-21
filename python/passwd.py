from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import Flask,request
app=Flask(__name__)
aa=18+19
@app.route("/api")
def aa():
    username=request.args.get("username")
    password=request.args.get("password")
    if username=='5':
      #  bb=18+29
        return 11
#    cc=username+password
   # cc=int(username)
    return 22
#g.user=aa
#print g.user
#s = Serializer('secret-key',expires_in=600)
#d=BadSignature('aaaa')
#print d.dumps({'q':88})
#print s.dumps({'x': 42})
#print s.loads('eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3OTQ0MTI5MCwiaWF0IjoxNDc5NDM3NjkwfQ.eyJ4Ijo0Mn0.d1MTfoDNF-y2bwk271Q8LKeHnuFSpJzF29oV6wYgo7M',return_header=True)
if __name__=='__main__':
    app.run()