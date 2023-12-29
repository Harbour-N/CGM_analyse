# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 23:55:10 2023

@author: nicho
"""

from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

basal = [0.875, 0.875, 0.95, 0.975, 0.95, 0.9, 0.8, 0.825]
times = [datetime(2022,7,6,0,0,0), datetime(2022,7,6,4,30,0), datetime(2022,7,6,6,0,0), datetime(2022,7,6,9,0,0), datetime(2022,7,6,12,0,0), datetime(2022,7,6,19,0,0), datetime(2022,7,6,23,0,0),datetime(2022,7,7,0,0,0) ]  

f = plt.figure()
f.set_size_inches(10,5)
plt.step(times,basal)
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
plt.show()


"""
Function to generate basal insulin patter for given start and end dates
"""
def basal_insulin(start_t, end_t):
    # start_t = time to start basal, datetime object
    # end_t = end time of sensor data to calculate basal till
    
    basal = 1
    
    
    return basal

