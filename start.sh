#!/bin/bash

start() {
    echo "Starting mpcwalletplugin..."
    python /home/ec2-user/app/mpcwalletplugin/main.py >/dev/null 2>&1 &
    echo "Python mpcwalletplugin started."
}

stop() {
    echo "Stopping mpcwalletplugin..."
    # 查找正在运行的Python程序的进程ID
    pid=$(pgrep -f "/home/ec2-user/app/mpcwalletplugin/main.py")
    if [ -n "$pid" ]; then
        # 终止进程
        kill "$pid"
        echo "mpcwalletplugin stopped."
    else
        echo "mpcwalletplugin is not running."
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
