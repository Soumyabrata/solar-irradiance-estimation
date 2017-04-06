import numpy as np
import csv
import datetime
from pysolar.solar import *
from SG_solarmodel import *


def import_WS_CI(CSV_file):
	
	lat = 1.3429943
	longitude = 103.6810899

	# Weather station data
	# read the input file
	with open(CSV_file) as f: #f is a file header
		reader = csv.reader(f, delimiter=",")
		d = list(reader) # d is a list of list here.
	
	d_data = d[1:len(d)]

	date_item = d_data[10][0]
	time_item = d_data[10][1]

	daterange = []
	datetime_range = []
	solar_range = []
	clearsky_range = []
	clearindex_range = []
	rainfall_range = []

	wrong_index = []

	for i in range(0,len(d_data)):
		date_item = d_data[i][0]
		DD = int(date_item[0:2])
		MM = int(date_item[3:5])
		YY = int(date_item[6:10])
		

		time_item = d_data[i][1]
		
		HH = int(time_item[0:2])
		MIN = int(time_item[3:5])
		SEC = int(time_item[6:8])
		

		sw = datetime.datetime(YY,MM,DD,HH,MIN,SEC)
		datetime_range.append(sw)


		# Adding only the date part, with no time information.
		sw2 = datetime.date(YY,MM,DD)
		daterange.append(sw2)

		solar_range.append(d_data[i][9])
		rainfall_range.append(d_data[i][8])
		
		
		date_part = datetime.datetime(YY, MM, DD, HH, MIN, SEC)

		clear_sky_rad = SG_model(date_part)
		if (clear_sky_rad==0):
			clearness_index = 0
		else:
			clearness_index = float(d_data[i][9])/float(clear_sky_rad)




		clearsky_range.append(clear_sky_rad)
		clearindex_range.append(clearness_index)

		
	return(daterange,datetime_range,solar_range,clearsky_range,clearindex_range,rainfall_range)
