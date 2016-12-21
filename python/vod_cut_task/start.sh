#!/bin/bash

nohup /opt/pro/python279/bin/python-vod-cut-heart /opt/shell/vod_cut_task/monitor_heart.py 2>&1 1>>/data/log/vod_cut/shell_monitor_heart.log &
sleep 2
nohup /opt/pro/python279/bin/python-vod-cut /opt/shell/vod_cut_task/start_cut.py 2>&1 1>>/data/log/vod_cut/shell_start.log &
sleep 2
nohup /opt/pro/python279/bin/python-vod-cut-end /opt/shell/vod_cut_task/end_cut.py 2>&1 1>>/data/log/vod_cut/shell_end.log &
sleep 2
ps aux|grep python-vod-cut
