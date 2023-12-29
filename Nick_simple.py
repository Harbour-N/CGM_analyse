# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 19:30:10 2023

@author: nicho
"""

import csv
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime, timezone
import numpy as np
import json
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, DayLocator, HourLocator, drange



def cgmparse(filename, start, end):
    times = []
    value = []

    with open(filename) as cgmfile:
        reader = csv.reader(cgmfile, delimiter=',')
        lines = 0
        for row in reader:
            if lines == 1:
                print('Column names:')
                print(f'{", ".join(row)}')

            if lines > 1:
                reading = datetime.strptime(row[2], '%d/%m/%Y %H:%M')
                # Keep amount of data small, plottable.
                # BUT,would be better served by checking for specific-time-intervals.
              # if len(cgm_value) < 256:
                if reading > start and reading < end:
                  # print(f'\t{row[2]} {row[3]} {row[4]}')
                    # We have two CGM colums.
                    # Here 'type' asserts which we can use.
                    type = int(row[3])
                    if type < 1:
                    # For now consider only type 1 readings,
                    # otherwise we need to sort carefully.
                  # if type < 2:
                        times.append(reading);
                        value.append(float(row[4 + type]));
            else:
                print(f'Skipping: {lines}.')            

            lines += 1

        print(f'Processed {lines} lines.')

    print()

  # print()
  # print("times")
  # print(times)

  # print()
  # print("value")
  # print(value)

    cgm = []

    if value:
        cgm = pd.DataFrame(list(zip(times, value)),
            columns =['timestamp', 'glucose'])

        # Associate relevant metadata to this DataFrame.
        if len(times):
            cgm.attrs['max'] = max(times)
            cgm.attrs['min'] = min(times)
            cgm.attrs['label'] = cgm.attrs['min'].strftime("%m/%d/%Y, %H:%M:%S") + "$\endash$" + cgm.attrs['max'].strftime("%m/%d/%Y, %H:%M:%S")

        cgm.attrs['title'] = filename
        cgm.attrs['color'] = 'orange'

        print(filename)
        print(cgm)

    return cgm



def cgmplot(cgm, gca = []):
    plot = []

    if len(cgm) != 0:

        if gca:
            axes = cgm.plot(
                ax=gca,
                kind='line',
                color=cgm.attrs['color'],
                label=cgm.attrs['label'],
                legend=True,
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='glucose',
                ylabel='glucose (mmol/L)')
        else:
            axes = cgm.plot(
                kind='line',
                color=cgm.attrs['color'],
                label=cgm.attrs['label'],
                legend="BG",
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='glucose',
                ylabel='glucose (mmol/L)')

        plot = cgm.plot(
            ax=axes,
            kind='scatter',
            color=cgm.attrs['color'],
            legend=False,
            marker='o',
            rot=30,
            title=cgm.attrs['title'],
            x='timestamp',
            xlabel='date',
            y='glucose',
            ylabel='glucose (mmol/L)')

      # plt.show()

    return plot

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
    # Associate relevant metadata to this DataFrame.
    if len(times):
        heartrate.attrs['max'] = max(times)
        heartrate.attrs['min'] = min(times)
        heartrate.attrs['label'] = heartrate.attrs['min'].strftime("%m/%d/%Y, %H:%M:%S") + "$\endash$" + heartrate.attrs['max'].strftime("%m/%d/%Y, %H:%M:%S")

  # print(heartrate)

    return heartrate


HR_data = jsonparse('HR_data/garmin_HR_data_23_09_01.json')

HR_times = HR_data['timestamp'].tolist()
HR_value = HR_data['heart'].tolist()

cgm_filename = 'LibreView/NicholasHarbour_glucose_9-12-2023.csv'

start = HR_data.attrs["min"]
end   = HR_data.attrs["max"]

cgm = cgmparse(cgm_filename, start, end)

cgm_times = cgm['timestamp'].tolist()
cgm_value = cgm['glucose'].tolist()

#cgm_times = np.array(cgm_times)
#cgm_value = np.array(cgm_value)

#f = plt.figure()
#plt.plot(cgm_times, cgm_value, 'o-', markersize = 3)
#plt.plot(HR_times, HR_value, alpha = 0.3)

# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
fig, ax1 = plt.subplots()


# dont know how to format the title
# start.strftime("%m-%d-%Y") # if want all numerical
#start.strftime("%b %d, %Y") # if want sep 02 23
ax1.set_title(start.strftime("%a, %b %d, %Y"))

color = 'tab:blue'
ax1.set_xlabel('time')
ax1.set_ylabel('BG (mmol/L)', color = color)
ax1.plot(cgm_times, cgm_value, 'o-', markersize = 3, color = color)
ax1.tick_params(axis='y',labelcolor=color)
ax1.axhline(y = 3.9, color ="green", linestyle ="--") 
ax1.axhline(y = 10.0, color ="green", linestyle ="--") 

xformatter = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(xformatter)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:red'
ax2.set_ylabel('HR (BPM)', color = color)  # we already handled the x-label with ax1
ax2.plot(HR_times, HR_value, alpha = 0.3, color = color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()


