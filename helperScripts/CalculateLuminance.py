import numpy as np
import exifread
import cv2
import datetime
import re
from scipy import ndimage

# User defined functions
from cmask import *

def LuminanceSquareCrop(LDR_path,sun_x,sun_y,crop_dim):

	
	# LDR images
	image_path1 = LDR_path
	
	#print ('Processing ', image_path1)
	f1 = open(image_path1, 'rb')
	im1 = cv2.imread(image_path1)
	
	# Rotate to correct positions if required
	lx, ly, dummy = im1.shape
	if lx>ly:
		#print ('Rotating')
		im1 = ndimage.rotate(im1, -90)
		
	tags = exifread.process_file(f1)
	date_time = tags["EXIF DateTimeDigitized"].values
	im_date = date_time[0:10]
	im_time = date_time[11:20]
	exp_time = tags["EXIF ExposureTime"].values
	exp_time1 = exp_time[0].num / exp_time[0].den
	

	centroid_x = sun_x
	centroid_y = sun_y
	
	around_sun = im1[(int(centroid_x - crop_dim/2)):(int(centroid_x + crop_dim/2)),(int(centroid_y - crop_dim/2)):(int(centroid_y + crop_dim/2))]

	lum = 0.2126*around_sun[:,:,0] + 0.7152*around_sun[:,:,1] + 0.0722*around_sun[:,:,2]
	lum = np.mean(lum)

	date = im_date
	time = im_time
	
	LDRLuminance = lum/exp_time1
	
	return(date,time,LDRLuminance)
	
