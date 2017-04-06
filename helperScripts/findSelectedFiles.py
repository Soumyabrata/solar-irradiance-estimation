import os
from glob import glob

def findSelectedFiles(start_dir):

	global_files = []
	
	# Check for all JPEG images if any.
	pattern  = "*.jpg"
	for direc,_,_ in os.walk(start_dir):
		global_files.extend(glob(os.path.join(direc,pattern)))

	# Check for LDR image patterns in this list
	pattern1  = "low.jpg"
	pattern2  = "med.jpg"
	pattern3  = "high.jpg"

	files_low = []
	files_single = []

	for particular_file in global_files:
		if pattern1 in particular_file:
			files_low.append(particular_file)

		if (pattern1 not in particular_file) and (pattern2 not in particular_file) and (pattern3 not in particular_file):
			files_single.append(particular_file)


	selected_files = files_low
	selected_files.extend(files_single)
	selected_files = sorted(selected_files)
	
	return(selected_files)
	
