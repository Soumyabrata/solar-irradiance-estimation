import os
from glob import glob
from normalize_array import *
from CalculateLuminance import *  
from sun_positions_day_files import *
from import_WS import *
from nearest import *
from SG_solarmodel import *

def findCorrelation(crop_dim,dt,date_now,selected_files,unik_dates,time_range,solar_range):

    print ('Crop Dimension= ',crop_dim)
    found = []
    for particular_file in selected_files:
        if date_now in particular_file:
            found.append(particular_file)
            # Found is the list of files for a single day

    # And now calculating for a Single Day
    YY = date_now[0:4]
    MON = date_now[5:7]
    DD = date_now[8:10]
    print ('Computing for ',YY,MON,DD)


    (sun_x_list, sun_y_list,select_images) = sun_positions_day_files(YY,MON,DD,found)
    # The output "select_images" contain those images between 8 hours and 18 hours.
    if (len(sun_x_list)==0 or len(sun_y_list)==0):
        print ('Skipping for ',YY,MON,DD, ' because sun could not be located')
        print ('Luminance TXT file not generated')
        


    YY = str(YY)
    MON = str(MON)
    DD = str(DD)
    if len(MON)==1:
        MON = str(0)+MON
    if len(DD)==1:
        DD = str(0)+DD
    match_string = YY + '-' + MON + '-' + DD




    LuminanceSeries = []
    img_date = []
    img_time = []
    # Calculation of luminance for all images in a single day.
    for i,low_LDR_path in enumerate(select_images):

        sun_x = sun_x_list[i]
        sun_y = sun_y_list[i]

        # low LDR
        LDR_path = low_LDR_path
        (date,time,LDRLuminance) = LuminanceSquareCrop(LDR_path,sun_x,sun_y,crop_dim)
        LuminanceSeries.append(LDRLuminance)
        img_date.append(date)
        img_time.append(time)


    print ('LDR luminance computed for crop size ',crop_dim)


    time_datapoints = []


    for i in range(0,len(img_date)):
        YY = int(img_date[i][0:4])
        MON = int(img_date[i][5:7])
        DD = int(img_date[i][8:10])
        HH = int(img_time[i][0:2])
        MM = int(img_time[i][3:5])
        SS = int(img_time[i][6:8])

        sw = datetime.datetime(YY,MON,DD,HH,MM,SS)

        time_datapoints.append(sw)


    match_string = str(YY) + '-' + str(MON) + '-' + str(DD)



    # Pick the Weather Station data corresponding to image
    WS_timestamp = time_range
    WS_solar_rad = solar_range
    image_timestamp = time_datapoints



    common_timestamps = []
    WS_datapoints = []
    img_datapoints = []

    # Check wrt to image datapoints.
    for i,check_time in enumerate(image_timestamp):

        (time_found,diff_ts) = nearest(check_time,WS_timestamp)
        #print ('Check time is ',check_time,'and found time is ',time_found, 'Difference = ' , diff_ts)

        if np.abs(diff_ts)<10:

            common_timestamps.append(check_time)
            img_datapoints.append(LuminanceSeries[i])

            # Check the corresponding index of WS data
            i2 = WS_timestamp.index(time_found)
            WS_datapoints.append(WS_solar_rad[i2])
            



    print ('Total weather station data points = ', len(WS_datapoints))
    if len(WS_datapoints)<50:
        print ('Not enough weather station datapoints to perform computation')
        print ('Correlation not computed for ',match_string)
        #continue


    WS_dtp = np.zeros(len(WS_datapoints))
    for i,qaz in enumerate(WS_datapoints):
        WS_dtp[i] = float(qaz)





    # Calculate the clear sky radiation
    latitude = 1.3429943
    longitude = 103.6810899
    clear_sky_rad = []
    for date_part in common_timestamps:


        CSR = SG_model(date_part)
        clear_sky_rad.append(CSR)

    clear_sky_rad = np.array(clear_sky_rad)

    MaxClearSky = np.max(clear_sky_rad[10:-10])
    MinClearSky = np.min(clear_sky_rad[10:-10])
    MinWS = np.min(WS_dtp[10:-10])
    MaxWS = np.max(WS_dtp[10:-10])
    MinSolar = np.min([MaxClearSky , MinWS])
    MaxSolar = np.min([MaxClearSky , MaxWS])


    # *********************************

    img_datapoints = np.asarray(img_datapoints)
    WS_dtp = np.asarray(WS_dtp)

    x_vect = normalize_array(img_datapoints[10:-10])
    y_vect = normalize_array(WS_dtp[10:-10])
    z_vect = normalize_array(clear_sky_rad[10:-10])
    time_vect = common_timestamps[10:-10]


    # Different normalization technique
    normCSR = normalize_arrayWRT(clear_sky_rad[10:-10] , MinSolar, MaxSolar)
    normLuminance = normalize_array(img_datapoints[10:-10] )
    normWS = normalize_arrayWRT(WS_dtp[10:-10], MinSolar , MaxSolar)



    r = np.corrcoef(normLuminance, normWS)
    r = r[0][1]
     
     
    return(r)
