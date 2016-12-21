#-*- encoding: utf-8 -*-

import os


#接口地址配置
#task_path='http://192.168.23.250:9983/stream/vod/cut/task'
task_path='http://192.168.45.72:9983/stream/vod/cut/task'
#获取任务接口地址
task_get_url='%s/get' % (task_path)
#获取任务接口地址
task_push_url='%s/push' % (task_path)
#获取任务接口地址
task_heart_url='%s/heart' % (task_path)
#完成任务接口地址
task_result_url='%s/result' % (task_path)


#获取任务时间间隔
task_interval = 5
#心跳间隔
heart_interval = 5
#验证任务完毕间隔
end_check_interval = 5

#日志路径
log_path='/data/log/vod_cut'
#record日志路径
log_cut_path='%s%scut' % (log_path, os.sep)
#运行日志路径
log_file='%s/vod_cut_run.log' % (log_path)
#运行日志路径
end_log_file='%s/end_cut_run.log' % (log_path)
#心跳日志
heart_log_file='%s/heart_cut_run.log' % (log_path)


#服务器编号
server_code = '01'

#录制文件存放路径
cut_temp_path = '/data/vod_cut/tmp'
#切片信息保存文件
cut_info_txt = 'info.txt'
#切片pid保存文件
cut_pid_txt = 'pid.pid'
#切片状态文件
cut_result_txt = 'result.txt'
#切片目标路径
#cut_final_path = '/data/vod_cut/final'
cut_final_path = '/vod/vodhls/ts01/st05'
#存储发布地址前缀
cut_url_prefix = '/ts01/st05/'

#源视频存储路径
store_path = {
    '1' : '/vod/vodhls', #龙存
    '2' : '/vod/vod3gp', #Dell
}

#录制存储测试文件路径
cut_test_file = '%s' % (cut_final_path)



#收录切片程序路径
cut_bin_path = '/opt/shell/tysx_vod_cut/tysx_vod'

#获取当前切片命令
cut_select_cmd = ' ps aux | grep [t]ysx_vod '


