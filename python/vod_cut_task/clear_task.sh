#!/bin/bash

set -x

echo "" > /data/log/vod_cut/abnormal_task.log
declare -a array=(192.168.187.183:01 192.168.187.185:02 192.168.187.188:03)
ip=$(/sbin/ifconfig bond0 | awk -F":" '/inet addr/{split($2,a," "); print a[1]}')
for i in ${array[@]}
do 
echo ${i} | grep "${ip}"
if [ $? = 0 ];then
  server_num=$(echo ${i} | awk -F":" '/'"${i}"'/{print $2}')
fi
done
dir="/data/vod_cut/tmp/${server_num}"
b=$(find ${dir} -type d -ctime 1 -depth -maxdepth 1)
for j in $b
do
#echo "${j}/result.txt"
echo "fail" > ${j}/result.txt
if [ $? = 0 ];then
  echo "${j}/result.txt set failed" >> /data/log/vod_cut/abnormal_task.log
  echo "${j}/result.txt set failed"
fi
done
