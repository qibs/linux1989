#!/bin/bash
set -u
echo "输入live2或者tm"
read fromcp
echo "请输入频道m3u8名字"
read m3u8head
echo "输入刷新时间段：年月日时分（201610311520-201610311540）"
read time_human
passwd='logview'
time_refresh="`echo $time_human|cut -b 1-12`00-`echo $time_human|cut -b 14-25`00"
case $fromcp in
    live2)
		echo -n "" > /tmp/list_fresh_s.txt
		echo -n "" > /tmp/list_fresh.txt
		echo -n "" > /tmp/list_remove.txt
        curl "http://hlive.tv189.cn/live2/${m3u8head}_450k_hls.m3u8?playseek=$time_refresh&videotype=2&isdebug=csml" |awk -F'?' '{print $1}'|grep '/ts/' |tee -a /tmp/list_fresh_s.txt|sed '/live2/s/^/\/data\/live/'|sed '/tm-/s/^/\/data\/tmlive\/ts/' > /tmp/list_remove.txt
        curl "http://hlive.tv189.cn/live2/${m3u8head}_600k_hls.m3u8?playseek=$time_refresh&videotype=2&isdebug=csml" |awk -F'?' '{print $1}'|grep '/ts/' |tee -a /tmp/list_fresh_s.txt|sed '/live2/s/^/\/data\/live/'|sed '/tm-/s/^/\/data\/tmlive\/ts/' >> /tmp/list_remove.txt
        cat /tmp/list_fresh_s.txt |tee  /tmp/list_tmp | sed  's/^/http:\/\/live3.nty.tv189.com/' > /tmp/list_fresh.txt
        cat /tmp/list_tmp | sed 's/^/http:\/\/ltetp3.tv189.com/' >> /tmp/list_fresh.txt
        /sbin/ifconfig tun0 |head -2|tail -1 |awk -F':| ' '{print $13}' >>  /tmp/list_remove.txt
        str=`date +'%M%y%m%d%H'`
        mv /tmp/list_remove.txt /tmp/${str}.txt
			#服务器自动remove对应文件
        ./scpexpect.exp ${str}
        wait
        nc -l 7979 || exit 79
        echo "mv complete,start refresh"
        bline=1 && eline=1000
        allline=`cat /tmp/list_fresh.txt | wc -l`
        echo -n "" > /tmp/refreshcdn.log
        while [[ -s /tmp/list_eachtime ]]
        do
            sed -n "${bline},${eline}p" /tmp/list_fresh.txt > /tmp/list_eachtime
            #request
            /usr/bin/python2.7 txcdnurl.py RefreshCdnUrl --urls-from "/tmp/list_eachtime" && echo "__________${eline}/${allline} refresh ok！logpath：/tmp/refreshcdn.log"
            wait
            let bline=bline+1000 && let eline=eline+1000
        done
        ;;

    tm)
        echo -n "" > /tmp/list_fresh_s.txt
        echo -n "" > /tmp/list_fresh.txt
        echo -n "" > /tmp/list_remove.txt
        curl "http://hlive.tv189.cn/tm-${m3u8head}-512k.m3u8?playseek=${time_refresh}&videotype=2&isdebug=csml" |awk -F'?' '{print $1}'|grep 'tm-' |tee -a /tmp/list_fresh_s.txt|sed '/tm-/s/^/\/data\/tmlive\/ts/' > /tmp/list_remove.txt
        curl "http://hlive.tv189.cn/tm-${m3u8head}-800k.m3u8?playseek=${time_refresh}&videotype=2&isdebug=csml" |awk -F'?' '{print $1}'|grep 'tm-' |tee -a /tmp/list_fresh_s.txt|sed '/tm-/s/^/\/data\/tmlive\/ts/' >> /tmp/list_remove.txt
        sed  's/^/http:\/\/live3.nty.tv189.com/' /tmp/list_fresh_s.txt > /tmp/list_fresh.txt
        sed 's/^/http:\/\/ltetp3.tv189.com/' /tmp/list_fresh_s.txt >> /tmp/list_fresh.txt

        /sbin/ifconfig tun0 |head -2|tail -1 |awk -F':| ' '{print $13}' >>  /tmp/list_remove.txt

		str=`date +'%M%y%m%d%H'`
        mv /tmp/list_remove.txt /tmp/${str}.txt
        
        #服务器自动remove对应文件
        ./scpexpect.exp ${str}
		wait              
        nc -l 7979
        echo "mv complete,start refresh"
        bline=1 && eline=1000
        allline=`cat /tmp/list_fresh.txt | wc -l`
        echo -n "" > /tmp/refreshcdn.log
        while [[ -s /tmp/list_eachtime ]]
        do                                             
            sed -n "${bline},${eline}p" /tmp/list_fresh.txt > /tmp/list_eachtime
            #request                                   
            /usr/bin/python2.7 txcdnurl.py RefreshCdnUrl --urls-from "/tmp/list_eachtime" && echo "__________${eline}/${allline} refresh ok！logpath：/tmp/refreshcdn.log"
            wait
            sleep 2
            let bline=bline+1000 && let eline=eline+1000
        done   
        ;;
    *)
        echo "输入错误" && exit
        ;;
esac
exit

