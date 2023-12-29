# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:13:33 2023

@author: nicho
"""

import pandas as pd

import json

 

#from datetime import datetime, timezone

from datetime import datetime

 

#def utc_to_local(utc_dt):

#    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

 

#def aslocaltimestr(utc_dt):

#    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

 

def jsonparse(filename):
    times = []
    heart = []

    with open(filename) as fit:
        data = json.load(fit)
  # print(data)

    for entry in data['heartRateValues']:
        times.append(datetime.fromtimestamp(entry[0] / 1000))
        heart.append(entry[1])

    heartrate = pd.DataFrame(list(zip(times, heart)),
                columns =['timestamp', 'heart'])
    heartrate.attrs['userProfilePK'] = data['userProfilePK']
    heartrate.attrs['calendarDate'] = data['calendarDate']
    heartrate.attrs['startTimestampGMT'] = data['startTimestampGMT']
    heartrate.attrs['endTimestampGMT'] = data['endTimestampGMT']
    heartrate.attrs['startTimestampLocal'] = data['startTimestampLocal']
    heartrate.attrs['endTimestampLocal'] = data['endTimestampLocal']
    heartrate.attrs['maxHeartRate'] = data['maxHeartRate']
    heartrate.attrs['minHeartRate'] = data['minHeartRate']
    heartrate.attrs['restingHeartRate'] = data['restingHeartRate']
    heartrate.attrs['lastSevenDaysAvgRestingHeartRate'] = data['lastSevenDaysAvgRestingHeartRate']
  # print(heartrate)

    return heartrate

 

 

# ##################

# Let's get started!

# ##################

 

garmin = jsonparse('HR_data/garmin_HR_data_23_09_01.json')

print(garmin)

 

garmin.plot(

    kind='line',

    legend=True,

    lw=0.5,

    rot=30,

    title='Garmin Heart Rate FIT data',

    x='timestamp',

    xlabel='date',

    y='heart',

    ylabel='rate (BPM)')

 

# #################

# That's all Folks!

# #################

print(end='\a')