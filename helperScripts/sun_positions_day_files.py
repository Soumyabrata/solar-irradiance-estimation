import cv2
import numpy as np
import glob
import exifread
import pandas as pd
import re
import datetime
from scipy import ndimage


def sun_positions_day_files(YY,MON,DD,global_images):
	
	# Find the matching string for the particular date
	YY = str(YY)
	MON = str(MON)
	DD = str(DD)
	if len(MON)==1:
		MON = str(0)+MON
	if len(DD)==1:
		DD = str(0)+DD
	match_string = YY + '-' + MON + '-' + DD


	# File location
	global_images = sorted(global_images)
	

	start_time = datetime.datetime(int(YY),int(MON),int(DD),7,0,0)
	end_time = datetime.datetime(int(YY),int(MON),int(DD),19,0,0)
	all_images = []
	
	# Select images from a time range
	for image_path in global_images:
		f = open(image_path, 'rb')
		try:
			tags = exifread.process_file(f)
			# To check if there are no EXIF information in the images.

			date_time = tags["EXIF DateTimeDigitized"].values
			im_date = date_time[0:10]
			im_time = date_time[11:20]
			
			
			time_components = im_time.split(":")
			hour = time_components[0]
			mint = time_components[1]
			sec = time_components[2]
			

			time_now = datetime.datetime(int(YY),int(MON),int(DD),int(hour),int(mint),int(sec))
			
			if time_now > start_time and time_now<end_time :
				all_images.append(image_path)
				#print ('Added time ', time_now)
			
		
		except:
			continue
			
	print ('Number of images added between 7 am and 7 pm = ', str(len(all_images)))
	
	if len(all_images)==0:
		complete_x = []
		complete_y = []
		all_images = []
	else:
		
		
		sun_CX = np.zeros(len(all_images))
		sun_CY = np.zeros(len(all_images))
		
		print ('Now computing sun position in images for different hours of the day.')
		# Pass 1: If sun can be seen in images
		# Extract information from Low LDR images
		for i in range(0,len(all_images)):
			image_path = all_images[i]
			#print ('Calculating for ',image_path)
			f = open(image_path, 'rb')
			im = cv2.imread(all_images[i])
			
			
			# Rotate to correct positions if required
			lx, ly, dummy = im.shape
			if lx>ly:
				#print ('Rotating')
				im = ndimage.rotate(im, -90)
		
		
			tags = exifread.process_file(f)
			date_time = tags["EXIF DateTimeDigitized"].values
			im_date = date_time[0:10]
			im_time = date_time[11:20]
			
			
			time_components = im_time.split(":")
			hour = time_components[0]
			mint = time_components[1]
			sec = time_components[2]
			

				
			exp_time = tags["EXIF ExposureTime"].values
			exp_time = exp_time[0].num / exp_time[0].den
			
			
			# Finding the centroid of sun position polygon
			threshold_value = 240
			red = im[:,:,2]
			green = im[:,:,1]
			blue = im[:,:,0]
			all_coord = np.where( red > threshold_value )
			all_coord = np.asarray(all_coord)
			length = np.shape(all_coord)[1]
			sum_x = np.sum(all_coord[0,:])
			sum_y = np.sum(all_coord[1,:])
			
			if (sum_x == 0 or sum_y == 0):
				centroid_x = np.nan
				centroid_y = np.nan
			else:
				centroid_x = int(sum_x/length)
				centroid_y = int(sum_y/length)
					
			sun_CX[i] = centroid_x
			sun_CY[i] = centroid_y
			
			
		print ('Task completed.')
		
		

		
		# Interpolate the sun's location in the missing places
		s1 = pd.Series(sun_CX)
		s2 = pd.Series(sun_CY)
		
		
		
		complete_x = s1.interpolate()
		complete_y = s2.interpolate()
		
		
		# All computed values are NaN
		if (np.isnan(complete_x).any()) or (np.isnan(complete_y).any()):
			#print ('Skipping for ', match_string)
			complete_x = np.array([])
			complete_y = np.array([])
		else:
			# Replacing NaN s in the beginning with closest non-NaN value
			# For x co-orinate
			a = complete_x
			ind = np.where(~np.isnan(a))[0]
			first, last = ind[0], ind[-1]
			a[:first] = a[first]
			a[last + 1:] = a[last]
			
			# For y co-orinate
			a = complete_y
			ind = np.where(~np.isnan(a))[0]
			first, last = ind[0], ind[-1]
			a[:first] = a[first]
			a[last + 1:] = a[last]
			
		
			print ('All sun locations for different time stamps are successfully computed.')
	
	
	return(complete_x,complete_y,all_images)
	
