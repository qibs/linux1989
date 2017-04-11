tongd=['47B099nbOaBo', '4OLDjYX6AR12', '4OLDK91Pg7ow', '4OLDr5KP4k0V', '4OLDrA1aAKVw', '4OLX0DN8eLAV', '4OLX0KxZm2W5', '4OLXMz8rOz5w', '4OLXVvygjdZw', '4Vro9oondLR2', '4Vroq6zDdd2X', '4VrorMm4M2W5', '4VrovXyZ4yW5', '4VroxyexLKL5', '82gqAJy5yBYr', '82gqkjlJ0M6k', '82gqkkZaLokg', '8ZEb6E8Jz1k4', '8ZEbvykLea7m', '8ZELk6XrybK0', '8ZELOEa6PLL4', '8ZELWeomNnmL', '95DYEPDzk8jO', '9q4O11VP7KLB', '9q4OAdZz1ENA', '9q4OLP6YjnkE', '9q4OqNXq0lYO', '9q4OyoDN9g70', '9q4OzLA7oZmY', 'aExr4l0AyDKa', 'aExrdox0017J', 'aExrDyJA6D6M', 'aN2aME7yoBvd', 'B15YAXNMZkYb', 'B15Yeeb6BWVX', 'BJlo0A7Km4X5', 'BJlo6J41DMRb', 'BJlovZWrnrdY', 'gnN5Er4a4Ejg', 'gnNJlYOqoZ7M', 'goE0eWE1Jav5', 'goE0MEgbKZ1q', 'goE0q2rx1kkM', 'goE0zRmdDLdE', 'mbN4knrkV8d7', 'mbN4YBr0jj7o', 'mbN4YobgARWv', 'mwoB1xZqxrLd', 'mwoBPwWjdZDw', 'mwoBPYNVnbWw', 'mwoBYEA8DMd4', 'O2y54d5R47ZB', 'O2y54n5Kvd8B', 'O2yg4qqWRgOB', 'O2yg7PNybL6g', 'O2ygbg9q1PrW', 'O2yge4EXdnyB', 'O2ygw0RbxwLa', 'O2ygYELk8eg6', 'OB6Wl6DoazWg', 'OB6WlBEwkOlX', 'P5l1EqRDd29N', 'P5l1xdPxdegZ', 'P5l1YNyNNOMv', 'PvZn94114aBn', 'PvZnqw59W2dY', 'PvZnzwbgKgBY', 'r4m70JkjdVmK', 'r4m7krY2gWBj', 'r4mbYmn1de17', 'rqj157BRqex8', 'rqj1AZBxM8kl', 'rqj1nO5J6Orq', 'Zb1WVRkB9jXb', 'ZnXoOZr8ZEWB', 'ZnXvABnJ7LL1', 'ZnXvDrLAxMnO', 'ZnXvez8R1vnO', 'ZnXvOXoWV1NO', 'ZnXvx02vR1AL']
tongdao=[]
for i in tongd:
    tongdao.append('anhuigf__'+i)
#print tongdao
names=locals()
for i in xrange(1,10):
    names['tongdao_%s' %i]=10
tongdn=len(tongdao)/8
print tongdn
tongdaog=[]
i=0
while i< len(tongdao):
    tongdaog.append(tongdao[i:i+8])
    i+=8
print tongdaog
'''
file=open(r'e:\test\test.txt','wb')
import logging,os
from ftplib import FTP
year="2017"
month="04"
day="07"
i="anhui"
ftpd="/aaa/bbb"
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=r'e:\test\%s.txt' %year,
                    filemode='a')
import psutil
aa=psutil.disk_usage('c:')
bb=str(aa).split(',')[2].strip().split('=')[1]
print long(bb)/1024/1024/1024
#ip="192.168.190.20"
#port=5789
#user="root"
#passwd="R7iV9Jxn4IKp"
#ftp=FTP()
#ftp.set_debuglevel(2)
#logging.debug(ftp.connect(ip,port))
#logging.debug(ftp.login(user,passwd))
#ftp.set_debuglevel(0)
#ftp.quit()
print len(tongdao)
ftpdir=ftpd+"/"+i+"/"+year+"/"+month+"/"+day+"/"
localdir = r"e:\anhui"+os.sep+year+os.sep+month+os.sep+day+os.sep
logging.debug(localdir)
print ftpdir
'''
