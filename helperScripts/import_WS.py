import numpy as np
import csv
import datetime


def import_WS(CSV_file):

	# Weather station data
	# read the input file
	with open(CSV_file) as f: #f is a file header
		reader = csv.reader(f, delimiter=",")
		d = list(reader) # d is a list of list here.
	
	d_data = d[1:len(d)]

	date_item = d_data[10][0]
	time_item = d_data[10][1]

	time_range = []
	solar_range = []

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
		time_range.append(sw)

		solar_range.append(d_data[i][9])


	return(time_range,solar_range)
	
	
	
	
	
	
	
	
	
def import_WS_w_rain(CSV_file):

	# Weather station data
	# read the input file
	with open(CSV_file) as f: #f is a file header
		reader = csv.reader(f, delimiter=",")
		d = list(reader) # d is a list of list here.
	
	d_data = d[1:len(d)]

	date_item = d_data[10][0]
	time_item = d_data[10][1]

	time_range = []
	solar_range = []
	rainfall_range = []

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
		time_range.append(sw)

		solar_range.append(d_data[i][9])
		
		
		rainfall_range.append(d_data[i][8])


	return(time_range,solar_range,rainfall_range)
