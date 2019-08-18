#! /usr/bin/python
 
from gps import *
import time
import requests
import sys
import logging
import argparse
import os

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

def parseConfig():
	# parse program arguments
	parser = argparse.ArgumentParser(description='Read from GPSd, forward to REST API.')
	parser.add_argument('--settings-file', action='store', required=True, help='Config file to load API settings.')
	args  = parser.parse_args()

	# Overwrite defaults if settings file is provided
	if args and args.settings_file:
		if os.path.isfile(args.settings_file): 
			try:
				with open(args.settings_file) as json_file:
					data = json.load(json_file)
					if "MDROID" in data:
						# Setup MDroid API
						if "MDROID_HOST" in data["MDROID"]:
							return data["MDROID"]["MDROID_HOST"]
						else:
							logging.debug("MDROID_HOST not found in config file, not using MDroid API.")

			except IOError as e:
				logging.error("Failed to open settings file:"+args.settings_file)
				logging.error(e)
		else:
			logging.error("Could not load settings from file"+str(args.settings_file))
	return False
   
try:
	# Read shared config file first
	LOGGING_ADDRESS = parseConfig()
	
	if LOGGING_ADDRESS:
                print("Using "+LOGGING_ADDRESS)
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
					r = requests.post(LOGGING_ADDRESS+"/session/gps", json = postdata, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
				except Exception as e:
					print "Error in request: "+str(e)
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
	print "Done.\nExiting."
