#! /bin/sh
# /etc/init.d/dump1090

### BEGIN INIT INFO
# Provides:          dump1090
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start the dump1090 receiver.
# Description:       Starts and Stops dump1090 (ADSB)
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting dump1090"
    # run application you want to start
    start-stop-daemon --start --background --chdir /home/jeff/dev/dump1090 --exec dump1090 -- --net --modeac --fix --enable-agc
    ;;
  stop)
    echo "Stopping dump1090"
    # kill application you want to stop
    killall dump1090
    ;;
  *)
    echo "Usage: /etc/init.d/dump1090 {start|stop}"
    exit 1
    ;;
esac

exit 0