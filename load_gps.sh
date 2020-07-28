#!/bin/bash

/usr/bin/python ~/MDroid/gps/loadgps.py
GPSDEV=`readlink -f /dev/serial/by-id/usb-Android_Android-if01-port0`

systemctl stop gpsd gpsd.socket
rm /var/run/gpsd.sock
/usr/bin/pkill gpsd

#until ! [ $(lsof $GPSDEV | wc -l) -gt 0] 
while :
do
	if ! [[ `lsof $GPSDEV | wc -l` -gt 0 ]]
	then
		break
	fi
	sleep 1
	echo "Waiting for $GPSDEV to be released..."
done

echo "Device released, starting GPSD..."
lsof $GPSDEV
/usr/sbin/gpsd -n $GPSDEV
#/usr/bin/python /home/pi/MDroid/MDroid-GPS/MDroid-GPS.py --settings-file /home/pi/MDroid/config.json | tee /home/pi/MDroid/logs/gps/gps.log
