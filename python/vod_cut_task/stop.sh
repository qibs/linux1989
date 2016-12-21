#!/bin/bash

killall python-vod-cut-heart
sleep 2
killall python-vod-cut
sleep 2
killall python-vod-cut-end
sleep 2
ps aux|grep python-vod-cut
