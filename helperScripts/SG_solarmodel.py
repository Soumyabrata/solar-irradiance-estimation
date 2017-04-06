import numpy as np
import math
import datetime
from pysolar.solar import *



def SG_model(datetime_date):
	latitude = 1.3429943
	longitude = 103.6810899
	
	date_part = datetime_date
	altitude_deg = get_altitude(latitude, longitude, date_part)
	
	# Singapore model
	elevation_angle = get_altitude(latitude, longitude, date_part)
	zenith_angle=90-elevation_angle
	theta = ((np.pi)/180)*zenith_angle

	day_of_year = (date_part - datetime.datetime(date_part.year, 1, 1)).days + 1
	tau = 2*(np.pi)*(day_of_year - 1)/365
	E0 = 1.00011 + 0.034221*np.cos(tau) + 0.001280*np.sin(tau) + 0.000719*np.cos(2*tau) + 0.000077*np.sin(2*tau)
	Isc = 1366.1

	try:
		f1 = math.pow(np.cos(theta), 1.3644)
		f2 = math.pow(np.e, (-0.0013 * (90 - zenith_angle)))
		Gc = 0.8277*E0*Isc*f1*f2
	except:
		Gc=0
	
	return (Gc)
