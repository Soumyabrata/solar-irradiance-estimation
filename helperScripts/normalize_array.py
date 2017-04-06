import numpy as np

def normalize_array( a ):
	
	min_value = np.amin(a)
	max_value = np.amax(a)
	
	norm_array = [None]*len(a)
	
	
	for i in range(0,len(a)):
		
		norm_array[i] = (a[i]-min_value)/(max_value - min_value)
	
	return(norm_array)

def normalize_arrayWRT( a, MinWRT, MaxWRT):
	
	min_value = MinWRT
	max_value = MaxWRT
	
	norm_array = [None]*len(a)
	
	for i in range(0,len(a)):
		
		norm_array[i] = (a[i]-min_value)/(max_value - min_value)
	
	return(norm_array)
