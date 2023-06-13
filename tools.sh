#!/bin/bash

debug() {
    python bot.py
}

start() {
    if ps -ef | grep python | grep bot.py > /dev/null
    then
        echo "zbot already start."
    else
        nohup python bot.py >/dev/null 2>&1 &
        echo "start zbot complete."
    fi
}

stop() {
    ps -ef | grep python | grep bot.py | awk '{print $2}' | xargs kill -9
    echo "stop zbot complete."
}

update() {
    stop
    git pull
    start
}

case $1 in
    dg)
        debug
        ;;
    st)
        start
        ;;
    sp)
        stop
        ;;
    rs)
        stop
        start
        ;;
    up)
        stop
        git pull
        start
        ;;
    *)
        echo "
    dg              直接运行
    st              后台启动
    sp              关闭
    rs              重启
    up              更新：关闭 -> git pull -> 后台启动
    "
        ;;
esac
