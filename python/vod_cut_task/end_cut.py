#-*- encoding: utf-8 -*-

import os
import sys
import traceback
from datetime import date, datetime, timedelta
import time
import shutil

import psutil

import config
from helper import date_helper, http_helper, str_helper, log_helper


def logger(log):
    log_helper.get_logger(config.end_log_file).info(log)

def logger_error(log):
    log_helper.get_logger(config.end_log_file).error(log)

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

def remove_path(path):
    try:
        shutil.rmtree(path)
    except Exception, e:
        logger(traceback.format_exc())

def get_folder_son(path):
    if not os.path.isdir(path):
        return []

    paths = os.listdir(path)
    pps = []
    for s in paths:
        p = '%s%s%s' % (path, os.sep, s)
        pps.append(p)
    return pps

def get_now_datestr():
    return datetime.now().strftime('%Y'+os.sep+'%m'+os.sep+'%d')

def get_tasks_by_folder(serverCode):
    ps =get_folder_son('%s%s%s' % (config.cut_temp_path, os.sep, serverCode))
    tasks = {
        'ok' : [],
        'fail' : [],
        'run' : [],
    }
    for f in ps:
        if os.path.isfile(f):
            continue

        resultPath = os.path.join(f, config.cut_result_txt)

        if not os.path.exists(resultPath):            
            continue

        result = read_all_file(resultPath).strip()
        log = 'cut_result:%s;result:%s' % (resultPath, result)
        logger(log)
        if 'fail' == result:
            tasks['fail'].append(f)
            continue
        if 'ok' == result:
            tasks['ok'].append(f)
            continue
        if 'run' == result:
            tasks['run'].append(f)
            continue

    return tasks

def get_over_tasks():
    tasks = get_tasks_by_folder(config.server_code)
    return tasks

def result_task(serverCode, taskInfo):
    url = config.task_result_url
    params = {
        'serverCode' : serverCode,
        'time' : date_helper.get_now_datetimestr3(),
        'taskId' : taskInfo['taskId'],
    }
    data = {
        'result' : str_helper.json_encode(taskInfo),
    }

    re = http_helper.post(url, params = params, data = data)
    if 200 == re.status_code:
        re.encoding = 'utf-8'
        log = 'result_task_url:%s;data:%s;result:%s' % (re.url, str_helper.json_encode(data), re.text)
        # print log
        logger(log)
        return str_helper.json_decode(re.text)

    log = 'result_task_url:%s;data:%s;resultcode:%s' % (re.url, str_helper.json_encode(data), re.status_code)
    # print log
    logger(log)
    return None


def get_file_md5(path):
    cmd = 'md5sum %s ' % (path)
    # print cmd
    md5s = os.popen(cmd).readlines()    
    # print md5s
    for m in md5s:
        l = m.strip()
        ls = l.split('  ')
        if len(ls) != 2:
            continue

        return ls[0].strip()

def get_folder_sizes(taskPath):
    cmd = 'du -sb %s/*' % (taskPath)

    pss = os.popen(cmd).readlines()

    fileSizes = {}
    for l in pss:
        ll = l.strip().split('\t')
        size = int(ll[0])
        code = ll[1].replace(taskPath+'/', '')
        fileSizes[code] = size

    return fileSizes


def over_task(path, isOk):
    ''' 完成任务 
    info.txt
    0       201512151318004da492ffdc424a9ca6        Q200_2014348086 /201512151318004da492ffdc424a9ca6/Q200_2014348086/Q200_2014348086.3gp.m3u8      /st02/2015/12/10/Q200_2014348086.3gp
    vId     taskId  fileName              path             vPath
    '''
    basePath = '%s%s%s' % (config.cut_temp_path,os.sep, config.server_code)
    taskPath = path
    infoPath = '%s%s%s' % (taskPath, os.sep, config.cut_info_txt)
    pidPath =  '%s%s%s' % (taskPath, os.sep, config.cut_pid_txt)
    resultPath =  '%s%s%s' % (taskPath, os.sep, config.cut_result_txt)

    infos = read_all_lines_file(infoPath)

    # logger(infoPath+":"+('None' if None == infos else ''.join(infos)))
    
    task = {
        'taskId' : '',
        'vId' : '',
        'path' : '',
        'md5' : '',
        'fileSize' : 0,
        'status' : 0,
        'msg' : 0,
    }

    if None == infos or [] == infos:
        logger(infoPath+":"+'None')
        remove_path(taskPath)
        task['msg'] = 'cut fail'
        task['status'] = 2
        return task


    fileName = ''
    vPath = ''
    for i in infos:
        ls = i.strip().split('\t')
        if len(ls) < 5:
            continue
        task['vId'] = ls[0]
        task['taskId'] = ls[1]
        fileName = ls[2]
        vPath = ls[4]
    
    # print infoPath
    # print infos
    if '' == task['taskId']:
        return task

    if False == isOk:
        #切片失败     
        task['msg'] = 'cut fail'
        task['status'] = 2
        logger('cat_fail:'+task['taskId']+';path:'+taskPath)
        remove_path(taskPath)
        return task

    #切片成功
    fileSizes = get_folder_sizes(taskPath)
    # print fileSizes
    for i in infos:
        ls = i.strip().split('\t')
        if len(ls) < 5:
            continue
        vId = ls[0]
        taskId = ls[1]
        name = ls[2]
        path = ls[3]

        tmpFilePath = '%s%s' % (basePath, path)
        #要mv的临时目录
        tmpFileFolder = os.path.dirname(tmpFilePath)

        if os.path.isfile(tmpFilePath):

            md5 = get_file_md5(tmpFilePath)

            # datenow = get_now_datestr()
            if 'TVM' in vPath:
                prefix = '/'.join(vPath.split('/')[4:10])
            else:
                prefix = '/'.join(vPath.split('/')[2:5])

            #mv的目标目录
            targetFolder = '%s%s%s' % (config.cut_final_path, os.sep, prefix)

            #分发的url
            targetUrl = '%s%s%s' % (config.cut_url_prefix, prefix, path.replace(os.sep+taskId,''))

            try:
                logger(tmpFileFolder)
                logger(targetFolder)
                # print tmpFileFolder
                # print targetFolder

                tfolder = os.path.join(targetFolder, fileName)
                if os.path.exists(tfolder):
                    logger('path_exists_remove_path:' + tfolder)
                    remove_path(tfolder)

                if not os.path.exists(targetFolder):
                    os.makedirs(targetFolder)

                m3u8Path = os.path.join(os.path.join(tmpFileFolder, os.path.basename(targetUrl)))

                files = get_folder_son(tmpFileFolder)                
                tss = read_all_lines_file(m3u8Path)

                tscount = 0
                for tsss in tss:
                    if '.ts' in tsss:
                        tscount += 1

                logger('tmppath:%s;files:%s;tscount:%s' % (tmpFileFolder, str(len(files)), str(tscount)))

                if tscount != len(files)-1:
                    raise NameError

                # else:
                #     remove_path(targetFolder)
                #     os.makedirs(targetFolder)
                shutil.move(tmpFileFolder, targetFolder)
                task['path'] = targetUrl
                task['status'] = 1
                task['msg'] = 'cut ok'
                task['md5'] = md5
                task['fileSize'] = fileSizes.get(fileName, 0)
            except NameError, e:
                logger_error(traceback.format_exc())
                task['path'] = ''
                task['status'] = 5
                task['msg'] = 'cut fail ts count error'
                task['md5'] = ''
                task['fileSize'] = fileSizes.get(fileName, 0)
            except Exception, e:
                logger_error(traceback.format_exc())
                task['path'] = ''
                task['status'] = 2
                task['msg'] = 'cut fail'
                task['md5'] = ''
                task['fileSize'] = fileSizes.get(fileName, 0)
                
        else:
            task['path'] = ''
            task['status'] = 2
            task['msg'] = 'cut fail'
            task['md5'] = ''
            task['fileSize'] = fileSizes.get(fileName, 0)

    #删除临时转码任务目录
    shutil.rmtree(taskPath)
    return task


def check_run_task(path):
    ''' 完成任务 
    info.txt
    0       201512151318004da492ffdc424a9ca6        Q200_2014348086 /201512151318004da492ffdc424a9ca6/Q200_2014348086/Q200_2014348086.3gp.m3u8      /st02/2015/12/10/Q200_2014348086.3gp
    vId     taskId  fileName              path             vPath
    '''
    basePath = '%s%s%s' % (config.cut_temp_path, os.sep, config.server_code)
    taskPath = path
    infoPath = '%s%s%s' % (taskPath, os.sep, config.cut_info_txt)
    pidPath =  '%s%s%s' % (taskPath, os.sep, config.cut_pid_txt)
    resultPath =  '%s%s%s' % (taskPath, os.sep, config.cut_result_txt)

    infos = read_all_lines_file(infoPath)

    # logger(infoPath+":"+('None' if None == infos else ''.join(infos)))
    
    task = {
        'taskId' : '',
        'vId' : '',
        'path' : '',
        'md5' : '',
        'fileSize' : 0,
        'status' : 0,
        'msg' : 0,
    }

    if None == infos or [] == infos:
        logger(infoPath+":"+'None')
        remove_path(taskPath)
        task['msg'] = 'cut fail'
        task['status'] = 2
        return task

    fileName = ''
    vPath = ''
    taskTime = 0
    for i in infos:
        ls = i.strip().split('\t')
        if len(ls) < 5:
            continue
        task['vId'] = ls[0]
        task['taskId'] = ls[1]
        fileName = ls[2]
        vPath = ls[4]
        if len(ls) > 5:
            taskTime = int(ls[5])

    tasklimit = int(time.time()) - (60 * 60 * 24) 
    if 0 == taskTime or taskTime > tasklimit:
        return None
    #超过时限的异常run任务，清除
    remove_path(taskPath)
    task['msg'] = 'cut task run fail'
    task['status'] = 2
    return task




def check_record():
    ''' 验证是否有完成的任务 '''
    tasks = get_over_tasks()
    print tasks

    for t in tasks['fail']:
        taskInfo = over_task(t, False)
        if None == taskInfo:
            continue
        result_task(config.server_code, taskInfo)

    for t in tasks['ok']:
        taskInfo = over_task(t, True)
        print taskInfo
        if None == taskInfo:
            continue
        result_task(config.server_code, taskInfo)

    for t in tasks['run']:
        taskInfo = check_run_task(t)
        if None == taskInfo:
            continue
        result_task(config.server_code, taskInfo)

        


def run():
    logger('end_cut start....')
    while True:
        try:
            time.sleep(config.end_check_interval)
            check_record()
        except Exception, e:
            logger(traceback.format_exc())

        logger('end_cut sleep....')


if __name__ == '__main__':
    run()

    # print os.path.basename('/data/vod_cut/tmp/01/2015121529cc7dc8e0e34ce1863fbd86/Q600_2024462791')

    # vPath = '/TVM/video/3gp/TVM/CCTVNEWS/2015/09/13/a771646c-51f0-46fe-8220-5a93acb5075c/Q600/Q600.3gp'

    # print '/'.join(vPath.split('/')[4:10])
    # print 'xxx.FLV'[-4:].lower()

    # check_record()

    # data = {"ovId": "2015061311365018beb7ace5584dd381", "tasks": {"600k_3gp": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/600k_3gp/2015061311365018beb7ace5584dd381_600k_3gp.3gp", "code": "600k_3gp", "msg": "transcode ok", "md5": ""}, "350k_3gp": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/350k_3gp/2015061311365018beb7ace5584dd381_350k_3gp.3gp", "code": "350k_3gp", "msg": "transcode ok", "md5": ""}, "600k_hls": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/600k_hls/2015061311365018beb7ace5584dd381_600k_hls.m3u8", "code": "600k_hls", "msg": "transcode ok", "md5": ""}, "4m_flv": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/4m_flv/2015061311365018beb7ace5584dd381_4m_flv.flv", "code": "4m_flv", "msg": "transcode ok", "md5": ""}, "1m2_3gp": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/1m2_3gp/2015061311365018beb7ace5584dd381_1m2_3gp.3gp", "code": "1m2_3gp", "msg": "transcode ok", "md5": ""}, "1m2_flv": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/1m2_flv/2015061311365018beb7ace5584dd381_1m2_flv.flv", "code": "1m2_flv", "msg": "transcode ok", "md5": ""}, "200k_3gp": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/200k_3gp/2015061311365018beb7ace5584dd381_200k_3gp.3gp", "code": "200k_3gp", "msg": "transcode ok", "md5": ""}, "450k_hls": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/450k_hls/2015061311365018beb7ace5584dd381_450k_hls.m3u8", "code": "450k_hls", "msg": "transcode ok", "md5": ""}, "512k_flv": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/512k_flv/2015061311365018beb7ace5584dd381_512k_flv.flv", "code": "512k_flv", "msg": "transcode ok", "md5": ""}, "100k_3gp": {"status": 1, "path": "/2015/06/16/2015061311365018beb7ace5584dd381/100k_3gp/2015061311365018beb7ace5584dd381_100k_3gp.3gp", "code": "100k_3gp", "msg": "transcode ok", "md5": ""}}, "taskId": "20150613113651414c1b4903c446238b"}
    # result_task(config.server_code, "20150613113651414c1b4903c446238b", data)

    # shutil.rmtree('D:\\ttt.txt')



