#!/bin/bash
ipad()
{
WORK_DIR=~
cd ${WORK_DIR}
PACKAGES_DIR=${WORK_DIR}/war/$(date +'%Y%m%d')
CONFIGS_DIR=${WORK_DIR}/conf/ipad
WEB_ROOT=${WORK_DIR}/deploy/ipad
CLASSPATH=${WEB_ROOT}/WEB-INF/classes
CONFIGPATH=${WEB_ROOT}/WEB-INF/conf
backup_dir=${WORK_DIR}/backup/$(date +'%Y-%m-%d')
date=$(date +'%Y%m%d%H%M%S')

if [ ! -d ${PACKAGES_DIR} ];then
echo "当天发布包文件夹不存在，请检查"
exit 1
fi

TOMCAT_NAME=tomcat-ipad-9323

WAR_FILE=`ls ${PACKAGES_DIR} -1 -t | grep ipad.*war$ | awk '{print $1}' | head -1`
echo "WAR_FILE: $WAR_FILE"
if [ -z "$WAR_FILE" ]; then
        echo "error: war file [ipad.*war] not exist!"
        exit 1
fi

TOMCAT_HOME=${WORK_DIR}/tomcat/${TOMCAT_NAME}
echo "TOMCAT_HOME: $TOMCAT_HOME"

pid=`ps -ef | grep $TOMCAT_HOME/bin | grep -v grep | awk '{print $2}'`
echo "pid: $pid"
if [ -n "$pid" ]; then
       echo "stop tomcat [$pid]..."
       kill -9 $pid
       sleep 5s
fi

if [ -d "${backup_dir}" ]; then
        echo "当月备份文件夹已存在"
        else mkdir -p ${backup_dir}
fi

if [ -d "${WEB_ROOT}" ]; then
        echo "backup [${WEB_ROOT}]"
        mv ${WEB_ROOT} ${WEB_ROOT}-${date}
        mv -f ${WEB_ROOT}-${date} ${backup_dir}/
#	sh ~/maomao_script/fabu_upftp.sh
        sleep 5s
fi

mkdir ${WEB_ROOT}
echo "unzip ${PACKAGES_DIR}/${WAR_FILE} to [${WEB_ROOT}]"
unzip -q ${PACKAGES_DIR}/${WAR_FILE} -d ${WEB_ROOT}
chmod -R 755 ${WEB_ROOT}

if [ -d "${CONFIGS_DIR}" ]; then
	cd ${CONFIGPATH}
        echo "begin copy config files from ${CONFIGPATH}!"
        if [ -f "${CONFIGS_DIR}/cache.properties" ]; then
        echo "copy ${CONFIGS_DIR}/cache.properties to ${CONFIGPATH}/cache.properties"
        cp -rf ${CONFIGS_DIR}/cache.properties .
        else
        echo "error: cache config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

        if [ -f "${CONFIGS_DIR}/server.properties" ]; then
        echo "copy ${CONFIGS_DIR}/server.properties to ${CONFIGPATH}/server.properties"
	cp -rf ${CONFIGS_DIR}/server.properties .
        else
        echo "error: server config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi
	 if [ -f "${CONFIGS_DIR}/bank-config-beans.xml" ]; then
        echo "copy ${CONFIGS_DIR}/bank-config-beans.xml to ${CONFIGPATH}/bank-config-beans.xml"
        cp -rf ${CONFIGS_DIR}/bank-config-beans.xml .
        else
        echo "error: server config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi


        if [ -f "${CONFIGS_DIR}/log4j.properties" ]; then
        echo "copy ${CONFIGS_DIR}/log4j.properties to ${CONFIGPATH}/log4j.properties"
	cp -rf  ${CONFIGS_DIR}/log4j.properties .
        else
        echo "error: log4j config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

        if [ -f "${CONFIGS_DIR}/quartz.properties" ]; then
	cd ${CLASSPATH}
        echo "copy ${CONFIGS_DIR}/quartz.properties to ${CLASSPATH}/quartz.properties"
	cp -rf ${CONFIGS_DIR}/quartz.properties .
        else
        echo "error:quartz config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi
else
        echo "config dir not exists, skip config files copy!"
fi
rm -rf ${WORK_DIR}/tomcat/tomcat-ipad-9323/work/Catalina/*
echo "startup tomcat..."
sh ${TOMCAT_HOME}/bin/startup.sh
echo "[ipad] app published successfully!"
}

portal()
{
WORK_DIR=~
cd ${WORK_DIR}
PACKAGES_DIR=${WORK_DIR}/war/$(date +'%Y%m%d')
CONFIGS_DIR=${WORK_DIR}/conf/portal
WEB_ROOT=${WORK_DIR}/deploy/portal
CLASSPATH=${WEB_ROOT}/WEB-INF/classes
CONFIGPATH=${WEB_ROOT}/WEB-INF/conf
backup_dir=${WORK_DIR}/backup/$(date +'%Y-%m-%d')
date=$(date +'%Y%m%d%H%M%S')

if [ ! -d ${PACKAGES_DIR} ];then
echo "当天发布包文件夹不存在，请检查"
exit 1
fi


TOMCAT_NAME=tomcat-portal-9322

WAR_FILE=`ls ${PACKAGES_DIR} -1 -t | grep portal.*war$ | awk '{print $1}' | head -1`
echo "WAR_FILE: $WAR_FILE"
if [ -z "$WAR_FILE" ]; then
        echo "error: war file [portal.*war] not exist!"
        exit 1
fi

TOMCAT_HOME=${WORK_DIR}/tomcat/${TOMCAT_NAME}
echo "TOMCAT_HOME: $TOMCAT_HOME"

pid=`ps -ef | grep $TOMCAT_HOME/bin | grep -v grep | awk '{print $2}'`
echo "pid: $pid"
if [ -n "$pid" ]; then
       echo "stop tomcat [$pid]..."
       kill -9 $pid
       sleep 5s
fi

if [ -d "${backup_dir}" ]; then
        echo "当月备份文件夹已存在"
        else mkdir -p ${backup_dir}
fi

if [ -d "${WEB_ROOT}" ]; then
        echo "backup [${WEB_ROOT}]"
        mv ${WEB_ROOT} ${WEB_ROOT}-${date}
        mv -f ${WEB_ROOT}-${date} ${backup_dir}/
	sh ~/maomao_script/fabu_upftp.sh
        sleep 5s
fi

mkdir ${WEB_ROOT}
echo "unzip ${PACKAGES_DIR}/${WAR_FILE} to [${WEB_ROOT}]"
unzip -q ${PACKAGES_DIR}/${WAR_FILE} -d ${WEB_ROOT}/
chmod -R 755 ${WEB_ROOT}
if [ -d "${CONFIGPATH}" ]; then

	cd ${CONFIGPATH}
        echo "begin copy config files from ${CONFIGPATH}!"
        if [ -f "${CONFIGS_DIR}/cache.properties" ]; then
        echo "copy ${CONFIGS_DIR}/cache.properties to ${CONFIGPATH}/cache.properties"
        cp -rf ${CONFIGS_DIR}/cache.properties .
        else
        echo "error:cache config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

        if [ -f "${CONFIGS_DIR}/server.properties" ]; then
        echo "copy ${CONFIGS_DIR}/server.properties to ${CONFIGPATH}/server.properties"
	cp -rf ${CONFIGS_DIR}/server.properties .
        else
        echo "error:server config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

        if [ -f "${CONFIGS_DIR}/log4j.properties" ]; then
        echo "copy ${CONFIGS_DIR}/log4j.properties to ${CONFIGPATH}/log4j.properties"
	cp -rf  ${CONFIGS_DIR}/log4j.properties .
        else
        echo "error:log4j config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

        if [ -f "${CONFIGS_DIR}/quartz.properties" ]; then
	cd ${CLASSPATH}
        echo "copy ${CONFIGS_DIR}/quartz.properties to ${CLASSPATH}/quartz.properties"
	cp -rf  ${CONFIGS_DIR}/quartz.properties .
        else
        echo "error:quartz config file is not exist,please copy config file to $CONFIGS_DIR !"
        exit 1
        fi

else
        echo "config dir not exists, skip config files copy!"
fi
rm -rf ${WORK_DIR}/tomcat/tomcat-portal-9322/work/Catalina/*
echo "startup tomcat..."
sh ${TOMCAT_HOME}/bin/startup.sh
echo "[portal] app published !"
}

read -p "请问你要发布ipad,还是portal？:" target
if [ "$target" = ipad ];then
ipad
elif [ $target = portal ];then
portal
else
echo "请选择ipad或者portal！！"
fi

