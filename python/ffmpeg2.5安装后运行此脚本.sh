#!/bin/bash
ln -s /usr/local/ffmpeg2/bin/ffprobe /usr/bin/ffprobe
ln -s /usr/local/ffmpeg2/bin/ffprobe /usr/bin/ffserver
ln -s /usr/local/ffmpeg2/bin/ffprobe /usr/bin/ffmpeg
echo "/usr/local/ffmpeg2/lib
/usr/local/lib">/etc/ld.so.conf.d/ffmpeg2.conf && ldconfig

rm /lib/libglib-2.0.so.0 -rf && ln -s /lib/libglib-2.0.so.0.2200.5 /lib/libglib-2.0.so.0
rm /lib/libgio-2.0.so.0 -rf && ln -s /lib/libgio-2.0.so.0.2200.5 /lib/libgio-2.0.so.0
rm /lib/libgobject-2.0.so.0 -rf && ln -s /lib/libgobject-2.0.so.0.2200.5  /lib/libgobject-2.0.so.0
rm /lib/libgthread-2.0.so.0 -rf && ln -s /lib/libgthread-2.0.so.0.2200.5 /lib/libgthread-2.0.so.0
rm /lib/ld-linux.so.2 -rf && ln -s /lib/ld-2.12.so /lib/ld-linux.so.2
rm /lib/libuuid.so.1 -rf && ln -s /lib/libuuid.so.1.3.0 /lib/libuuid.so.1
rm /lib/libgmodule-2.0.so.0 -rf && ln -s /lib/libgmodule-2.0.so.0.2200.5 /lib/libgmodule-2.0.so.0
ldconfig
