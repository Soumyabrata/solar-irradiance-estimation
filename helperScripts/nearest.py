import numpy as np
import bisect



def nearest(ts,s):

	# Given a presorted list of timestamps:  s = sorted(index)
	i = bisect.bisect_left(s, ts)
	nearest_timestamp = min(s[max(0, i-1): i+2], key=lambda t: abs(ts - t))
	diff_timestamps = (nearest_timestamp - ts).total_seconds()
	return (nearest_timestamp,diff_timestamps)
	
	
	
def find_nearest_rainevent(time1_index, rain_array):
	# time1_index is the index of the time series (not the datetime object)
	# rain_array is the actual array containing the rain measurements.
	
	rain_points = np.where(rain_array!= 0)[0]
	idx = np.argmin(np.abs(rain_points - time1_index))
	time2_index = rain_points[idx]
	return (time2_index)
