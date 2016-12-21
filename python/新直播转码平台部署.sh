#!/bin/bash
set -u
#直播转码环境部署
date >> /root/tmp/install.log
mkdir -pv /data/log/liverecord/record/
mkdir -pv /mnt/tvmCloud/
mkdir -pv /data/live/
mkdir -pv /opt/scripts/chk_mount/
mkdir -pv /opt/pro/
mkdir -pv /opt/shell/
mkdir -pv /data/log/liverecord/
mkdir -pv /data/fastlive/fastlive/
mkdir -pv /root/tmp/
mkdir -pv /opt/pro/python27/
#mkdir -pv /data/NLTPStore/
echo "请输入servercode(2位数字):"
read code
echo "-------------------请输入yes 以及192.168.188.100密码：logview"
scp -P6022 logview@192.168.188.100:/home/logview/cq/live2trans/* /root/tmp/

echo >"[base]

name=RHEL-base
baseurl=http://192.168.73.59/base
gpgcheck=0
gpgkey=http://192.168.73.59/base/RPM-GPG-KEY-RHEL-6

[epel]

name=RHEL-epel
baseurl=http://192.168.73.59/epel
gpgcheck=0
gpgkey=http://192.168.73.59/base/RPM-GPG-KEY-RHEL-6

[rpmforge]

name=RHEL-rpmforge
baseurl=http://192.168.73.59/rpmforge
gpgcheck=0
gpgkey=http://192.168.73.59/base/RPM-GPG-KEY-RHEL-6

[streaming]

name=TYSX-streaming
baseurl=http://192.168.73.59/streaming
gpgcheck=0
gpgkey=http://192.168.73.59/streaming/RPM-GPG-KEY-RHEL-6

[leo]

name=leo
baseurl=http://192.168.73.59/leo
enabled=1
gpgcheck=0
gpgkey=http://192.168.73.58/base/RPM-GPG-KEY-redhat-release"
echo "##transcoder manager
192.168.45.224  livetask.tv189.cn" >> /etc/hosts


cd /root/tmp/
rpm -qa | grep zlib 
[ $? != 0 ] && tar jxvf zlib-1.2.3.tar.bz2 && cd zlib* && ./configure && make && {
make install || echo -e "\033[41;37m zlib安装失败 \033[0m" >> /root/tmp/install.log
}
cd /root/tmp/
rpm -qa | grep openssl
[ $? != 0 ] && tar zxvf openssl-1.0.2g.tar.gz && cd  openssl* && ./configure --prefix=/usr/local/openssl-devel && make depend && make && {
make install || echo -e "\033[41;37m openssl安装失败 \033[0m" >> /root/tmp/install.log
}
cd /root/tmp/
tar zxvf Python-2.7.11.tgz && cd Python-2.7.11 && ./configure --prefix=/opt/pro/python27/ --with-ensurepip=install &&  make && {
make install || echo -e "\033[41;37m python2711安装失败 \033[0m" >> /root/tmp/install.log
}
cd /root/tmp/
tar axvf psutil-2.0.0.tar.gz && cd psutil-2.0.0 && {
sleep 3
/opt/pro/python27/bin/python setup.py install || echo -e "\033[41;37m psutil安装失败 \033[0m" >> /root/tmp/install.log
}
cd /root/tmp/
tar zxvf kennethreitz-requests-v2.9.1-204-gaa1c3ad.tar.gz && cd kennethreitz-requests-aa1c3ad && {
sleep 3
/opt/pro/python27/bin/python setup.py install || echo -e "\033[41;37m requests安装失败 \033[0m" >> /root/tmp/install.log
}
mv /root/tmp/live2transcoder.tar.gz /opt/shell/ && cd /opt/shell/
tar xzvf live2transcoder.tar.gz
mv /root/tmp/LeoFS.172.16.42.119 /etc/init.d/

sed -i $"s/server_code = '[0-9]\{2\}'/server_code = '$code'/" /opt/shell/live_record_service/config.py || echo -e "\033[41;37m servercode修改失败 \033[0m" >> /root/tmp/install.log
ln -s /opt/pro/python27/bin/python /opt/pro/python27/bin/python-live-record-heart  || echo -e "\033[41;37m 创建软链接python-live-record-heart失败 \033[0m" >> /root/tmp/install.log
ln -s /opt/pro/python27/bin/python /opt/pro/python27/bin/python-live-record  || echo -e "\033[41;37m 创建软链接python-live-record失败 \033[0m" >> /root/tmp/install.log

echo "###ntp
* */2 * * * /usr/sbin/ntpdate 192.168.35.253 > /root/ntpdate.log 2>&1
## chk_mount_Leo
*/5 * * * * /opt/scripts/chk_mount/main.sh >> /opt/scripts/chk_mount/mount.log 2>&1

## clear ffmpeg run log
0 1 * * * /opt/scripts/clear_log/main.sh > /opt/scripts/clear_log/run.log 2>&1" >> /var/spool/cron/root
echo "#Leo
/LeoCluster/bin/leofs_cfgd
/LeoCluster/bin/leofs_mond -c /LeoCluster/conf/leofs_mond.conf

##mount --bind
/opt/scripts/chk_mount/main.sh >> /opt/scripts/chk_mount/mount.log 2>&1

mount --bind /mnt/tvmCloud/ /data/live
mount tmpfs /data/fastlive/fastlive -t tmpfs -o size=2g
route add -net 172.16.50.149 netmask 255.255.255.255 gw 192.168.42.193" >>/etc/rc.local
mv /root/tmp/LeoCluster66.tar.gz /
cd / && tar zxvf LeoCluster66.tar.gz
mv /LeoCluster/lib/* /lib/
/LeoCluster/bin/leofs_cfgd || echo -e "\033[41;37m 龙存客户端启动失败\033[0m" >/root/tmp/install.log
sleep 3
/etc/init.d/LeoFS.172.16.42.119 start && ls /data/live/live2 >/dev/null || echo -e "\033[41;37m 龙存客户端启动失败\033[0m" >/root/tmp/install.log
echo -e "\033[42;37m 提醒：1、检查是否已挂载龙存，请联系挂载后运行挂载脚本
2、执行start.sh后请检查数据库中服务器任务下发时间是否更新
 \033[0m"
mount tmpfs /data/fastlive/fastlive -t tmpfs -o size=2g
route add -net 172.16.50.149 netmask 255.255.255.255 gw 192.168.42.193
cat /root/tmp/install.log | grep "失败" && echo && echo -e "\033[41;37m 安装有异常！_____________________ \033[0m"
cat /root/tmp/install.log | grep "失败" || {
echo -e "\033[42;37m 安装顺利完成！！！ \033[0m"
}
exit 0
