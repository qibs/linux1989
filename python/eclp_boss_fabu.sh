#!/bin/bash
boss()
{

WORK_DIR=~
cd ${WORK_DIR}
PACKAGES_DIR=${WORK_DIR}/war/$(date +'%Y%m%d')
CONFIGS_DIR=${WORK_DIR}/conf/boss
WEB_ROOT=${WORK_DIR}/deploy/boss
CLASSPATH=${WEB_ROOT}/WEB-INF/classes
CONFIGPATH=${WEB_ROOT}/WEB-INF/conf
backup_dir=${WORK_DIR}/backup/$(date +'%Y%m%d')
date=$(date +'%Y%m%d%H%M%S')

if [ ! -d ${PACKAGES_DIR} ];then
echo "当天发布包文件夹不存在，请检查"
exit 1
fi

TOMCAT_NAME=tomcat-boss-9321

WAR_FILE=`ls ${PACKAGES_DIR} -1 -t | grep boss.*war$ | awk '{print $1}' | head -1`
echo "WAR_FILE: $WAR_FILE"
if [ -z "$WAR_FILE" ]; then
        echo "error: war file [boss.*war] not exist!"
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
        sleep 5s
fi

mkdir ${WEB_ROOT}
echo "unzip ${PACKAGES_DIR}/${WAR_FILE} to [${WEB_ROOT}]"
unzip -q ${PACKAGES_DIR}/${WAR_FILE} -d ${WEB_ROOT}/
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
rm -rf ${WORK_DIR}/tomcat/tomcat-boss-9321/work/Catalina/*
echo "startup tomcat..."
sh ${TOMCAT_HOME}/bin/startup.sh
echo "[boss] app published successfully!"
}


eclp()
{
WORK_DIR=~
cd ${WORK_DIR}
PACKAGES_DIR=${WORK_DIR}/war/$(date +'%Y%m%d')
CONFIGS_DIR=${WORK_DIR}/conf/eclp
WEB_ROOT=${WORK_DIR}/deploy/eclp
CLASSPATH=${WEB_ROOT}/WEB-INF/classes
CONFIGPATH=${WEB_ROOT}/WEB-INF/conf
backup_dir=${WORK_DIR}/backup/$(date +'%Y%m%d')
date=$(date +'%Y%m%d%H%M%S')

if [ ! -d ${PACKAGES_DIR} ];then
echo "当天发布包文件夹不存在，请检查"
exit 1
fi

TOMCAT_NAME=tomcat-eclp-9320

WAR_FILE=`ls ${PACKAGES_DIR} -1 -t | grep eclp.*war$ | awk '{print $1}' | head -1`
echo "WAR_FILE: $WAR_FILE"
if [ -z "$WAR_FILE" ]; then
        echo "error: war file [eclp.*war] not exist!"
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
rm -rf ${WORK_DIR}/tomcat/tomcat-eclp-9320/work/Catalina/*
echo "startup tomcat..."
sh ${TOMCAT_HOME}/bin/startup.sh
echo "[eclp] app published successfully!"
}


if [ $1 = boss ];then
boss
elif [ $1 = eclp ];then
eclp
else
echo "使用方法 sh scriptsname.sh eclp/boss(选一)，或./scriptsname.sh eclp/boss(选一)"
fi
