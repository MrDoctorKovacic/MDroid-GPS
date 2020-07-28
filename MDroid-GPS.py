#! /usr/bin/python
print("Starting GPS logging...")

from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE
import mdroidconfig
import time
import requests
import sys
import logging
import argparse
import os
import json

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

try:
	# Read shared config file first
	config = mdroidconfig.readConfig('{"MDROID": {"MDROID_HOST"}}')
	if config is None:
		exit("Failed to parse config.")
	LOGGING_ADDRESS = config["MDROID"]["MDROID_HOST"]

	if LOGGING_ADDRESS:
		print("Using "+LOGGING_ADDRESS)
		while True:
			report = gpsd.next() #
			if report['class'] == 'TPV':
				postdata = {
					"latitude": str(getattr(report,'lat','')),
					"longitude": str(getattr(report,'lon','')),
					"altitude": str(getattr(report,'alt',None)),
					"speed": str(getattr(report,'speed',None)),
					"climb": str(getattr(report,'climb',None)),
					"epv": str(getattr(report,'epv',None)),
					"ept": str(getattr(report,'ept',None)),
					"time": str(getattr(report,'time',''))
				}

				#print(postdata)

				try:
					r = requests.post(LOGGING_ADDRESS+"/session/gps", json = postdata, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
				except Exception as e:
					print("Error in request: "+str(e))
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
	print("Done.\nExiting.")
