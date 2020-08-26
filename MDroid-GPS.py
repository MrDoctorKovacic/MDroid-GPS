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

def postGPSFix(key, value):
	try:
		r = requests.post(LOGGING_ADDRESS+"/session/gps."+key, json = { "value": value }, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
	except Exception as e:
		print("Error in request: "+str(e))

try:
	# Read shared config file first
	#config = mdroidconfig.readConfig('{"MDROID": {"MDROID_HOST"}}')
	#if config is None:
	#	exit("Failed to parse config.")
	LOGGING_ADDRESS = "http://localhost:5353"

	if LOGGING_ADDRESS:
		print("Using "+LOGGING_ADDRESS)
		while True:
			try:
				report = gpsd.next() #
				if report['class'] == 'TPV':
					postGPSFix("latitude", str(getattr(report,'lat','')))
					postGPSFix("longitude", str(getattr(report,'lon','')))
					postGPSFix("altitude", (getattr(report,'alt',None)))
					postGPSFix("speed", (getattr(report,'speed',None)))
					postGPSFix("climb", (getattr(report,'climb',None)))
					postGPSFix("epv", (getattr(report,'epv',None)))
					postGPSFix("ept", (getattr(report,'ept',None)))
					#postGPSFix("time", str(getattr(report,'time','')))

			except Exception as e:
				print("GPSD error: "+str(e))

except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
	print("Done.\nExiting.")
