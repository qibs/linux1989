#-*- encoding: utf-8 -*-

import os
import sys
import traceback
import time
import shutil

import psutil

import config
from helper import date_helper, http_helper, str_helper, log_helper


def logger(log):
    log_helper.get_logger(config.heart_log_file).info(log)

def heart(serverCode, heartInfo):
    url = config.task_heart_url
    params = {
        'serverCode' : serverCode,
        'time' : date_helper.get_now_datetimestr3(),
    }
    data = {'tasks':str_helper.json_encode(heartInfo)}
    re = http_helper.post(url= url, params = params, data = data)
    if 200 == re.status_code:
        re.encoding = 'utf-8'
        log = 'result_task_url:%s,data:%s;result:%s' % (re.url, str_helper.json_encode(data), re.text)        
        logger(log)
        return str_helper.json_decode(re.text)

    log = 'result_task_url:%s;data:%s;resultcode:%s' % (re.url, str_helper.json_encode(data), re.status_code)
    logger(log)
    return None
    

def get_tasks_by_process():
    cmd = config.cut_select_cmd
    pss = os.popen(cmd).readlines()

    prefix = '%s%s%s%s' % (config.cut_temp_path, os.sep, config.server_code, os.sep)
    tasks = {}

    for l in pss:
        line = l.strip()
        lss = line.split('____')
        
        if len(lss) != 3:
            continue

        ls = lss[1].split('___')
        if '0' == ls[0]:
            ls[0] = ''
        tasks[ls[1]] = {
                'vId' : ls[0],
                'taskId' : ls[1],
                'code' : ls[2],
                'status' : 1,
                'startTime' : ls[3],
                'path' : prefix + ls[1],
            }    

    return tasks.values()

def read_all_lines_file(filePath, method = 'r'):
    if not os.path.isfile(filePath):
        return None
    fh = open(filePath, method)
    try:
        c = fh.readlines()
        return c
    finally:
        fh.close()

def read_all_file(filePath, method = 'r'):
    if not os.path.isfile(filePath):
        return None
    fh = open(filePath, method)
    try:
        c = fh.read()
        return c
    finally:
        fh.close()

def get_task_info(taskInfo):
    return {
        'taskId' : taskInfo['taskId'],
        'vId' : taskInfo['vId'],
        'status' : taskInfo['status'],
        'startTime' : taskInfo['startTime'],
    }
    



def check_heart():
    
    heartInfo = {}
    heartInfo['tasks'] = []
    if not os.path.exists(config.cut_test_file):
        heartInfo['status'] = 2
        heartInfo['msg'] = 'storage visit error..'
    else:
        heartInfo['status'] = 1
        heartInfo['msg'] = 'ok.'

    tasks = get_tasks_by_process()
    print tasks
    if len(tasks) <= 0:
        heart(config.server_code, heartInfo)
        return


    for task in tasks:
        heartInfo['tasks'].append(get_task_info(task))

    # print heartInfo
    result = heart(config.server_code, heartInfo)
    if None == result:
        return

    if 2 == result['info']['isStop'] or len(result['info'].get('tasks', [])) <= 0:
        return

    #  不考虑停止任务
    # if 1 == result['info']['isStop'] :
    #     for t in result['info']['tasks']:
    #         serverPath = '%s%s%s' % (config.cut_temp_path,os.sep, config.server_code)
    #         basePath = '%s%s%s' % (serverPath, os.sep, t['taskId'])
    #         transPidPath = '%s%s%s' % (basePath, os.sep, config.cut_pid_txt)
    #         pid = read_all_file().strip()
    #         if str_helper.is_null_or_empty(pid):
    #             logger('cut process pid file not exists. taskId:'+t['taskId'])
    #             continue
    #         try:
    #             os.remove(transPidPath)
    #             p = psutil.Process(pid)
    #             if None == p:
    #                 continue
    #             p.kill()
    #         except Exception, e:
    #             logger(traceback.format_exc())
    #         finally:
    #             pass
    #         shutil.rmtree(basePath)










def run():
    logger('monitor_record start....')
    while True:
        time.sleep(config.heart_interval)
        try:
            #验证当前切片任务
            check_heart()

        except Exception, e:
            logger(traceback.format_exc())

        logger('monitor_record sleep....')
        


if __name__ == '__main__':
    run()
    # check_heart()
    # print get_record_by_status(config.server_code, 2)








