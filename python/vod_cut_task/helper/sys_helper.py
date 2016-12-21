#-*- encoding: utf-8 -*-

import sys
import os
import commands
import time

import platform




def add_path(path):
    '''
        将path追加入系统PATH
    '''
    sys.path.append(path)


def run_sys_cmd(cmd):
    '''
        系统命令，没有返回
    '''
    os.system(cmd)

def run_sys_cmd_result(cmd):
    '''
        系统命令，返回输出，返回file对象，可以使用read()或readlines()读取信息
    '''
    return os.popen(cmd)


def run_sys_cmd_status_output(cmd):
    '''
        系统命令，返回输出，获得到返回值和输出，输出为(status, output)。
    '''
    return commands.getstatusoutput(cmd)


def wait_input(prompt = ''):
    '''
        系统命令，返回输出，获得到返回值和输出，输出为(status, output)。
    '''
    a = raw_input('%s:' % prompt)
    return a


Windows = 'Windows'
Linux = 'Linux'

def get_os_platform():
    global Windows
    global Linux
    if Windows in platform.platform():
        return Windows

    if Linux in platform.platform():
        return Linux
    return None


def get_local_ip():  
    global Linux
    if Linux == get_os_platform():
        return os.popen("ifconfig|grep 'inet '|grep -v '127.0'|xargs|awk -F '[ :]' '{print $3}'").readline().rstrip()
    return None


if __name__ == '__main__':
    print platform.architecture()
    print platform.platform()
