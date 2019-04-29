#! /usr/bin/python
 
from gps import *
import time
import requests
import sys

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
   
try:
 
    if(len(sys.argv) < 2):
        print("Provide the URL to HTTP POST GPS data to.")
    else:
        while True:
            report = gpsd.next() #
            if report['class'] == 'TPV':
                postdata = {
                    "latitude": str(getattr(report,'lat','')),
                    "longitude": str(getattr(report,'lon','')),
                    "altitude": getattr(report,'alt',None),
                    "speed": getattr(report,'speed',None),
                    "climb": getattr(report,'climb',None),
                    "epv": getattr(report,'epv',None),
                    "ept": getattr(report,'ept',None),
                    "time": str(getattr(report,'time',''))
                }

                print(postdata)

                try:
                    r = requests.post(sys.argv[1], json = postdata, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
                except Exception as e:
                    print "Error in request: "+str(e)
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "Done.\nExiting."