#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 08 14:58:11 2023

@author: nickharbour
"""
        
import csv

import matplotlib.pyplot as plt
import os

import pandas as pd

from datetime import datetime, timezone

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

#from garmin_fit_sdk import Decoder, Profile, Stream
from garmin_fit_sdk import Decoder, Stream

def fitparse(filename):
    stream = Stream.from_file(filename)
    decoder = Decoder(stream)

  # record_fields = set()
  # def mesg_listener(mesg_num, message):
  #     if mesg_num == Profile['mesg_num']['RECORD']:
  #         for field in message:
  #           # print(field)
  #             if field == 'timestamp':
  #                 record_fields.add(field)
  #             if field == 'timestamp_16':
  #                 record_fields.add(field)
  #             if field == 'heart_rate':
  #                 record_fields.add(field)
  #             if field == 'activity_type':
  #                 record_fields.add(field)
  #             if field == 'intensity':
  #                 record_fields.add(field)
  #             if field == '????':
  #                 record_fields.add(field)

    messages, errors = decoder.read(
      # convert_datetimes_to_dates = True,
      # convert_types_to_strings = True,
      # merge_heart_rates = True,
      # mesg_listener = mesg_listener
        )

  # print(record_fields)

  # print(errors)
  # print(messages)

    monitor = True

    if "monitoring_mesgs" in messages:
        records = messages['monitoring_mesgs']
        monitor = True

    if "record_mesgs" in messages:
        records = messages['record_mesgs']
        monitor = False

  # print(records)

    times = []
    heart = []
    power = []
    types = []

    color = []
    marks = []

    # Look to assign these to various filled Markers.
    # @see https://forums.garmin.com/developer/fit-sdk/f/discussion/287708/what-does-intensity-in-fit-monitoring-mean
    activity = "generic"
    activities = {
       "generic":           's',  # 0,
       "running":           '^',  # 1,
       "cycling":           '.',  # 2,
       "transition":        'v',  # 3,
       "fitness_equipment": '>',  # 4,
       "swimming":          '<',  # 5,
       "walking":           '8',  # 6,
       "sedentary":         'o'   # 7
    }

    # Assign these to various colours.
    # @see https://forums.garmin.com/developer/fit-sdk/f/discussion/287708/what-does-intensity-in-fit-monitoring-mean
    intensity = 6
    intensities = {
        0: 'red',    # active,
        1: 'green',  # rest,
        2: 'pink',   # warmup,
        3: 'blue',   # cooldown,
        4: 'black',  # recovery,
        5: 'cyan',   # interval,
        6: 'brown'   # other
    }

    for field in records:
      # print(field)
      # print()

        if "activity_type" in field:
            activity = field['activity_type']

        if "intensity" in field:
            intensity = field['intensity']

        if "timestamp" in field:
            timestamp = field['timestamp']

        if "heart_rate" in field:
            rate = field['heart_rate']
            # We assume zero entries are system mis-reads (outliers),
            # but keep all-data if needed to track (heart) anomalies.
            if rate > 0.0:
                tick = timestamp

                # Local timestamp-offset correction for Monitor files.
                # @see https://stackoverflow.com/questions/57774180/how-to-handle-timestamp-16-in-garmin-devices
                if monitor == True:
                    # Take the 'special' Garmin epoch into account,
                    # it's 631065600 seconds later than the Unix timestamp epoch.
                    # Hence calculations should happen in 'special time'.
                    garmintime = int(timestamp.timestamp()) - 631065600
                    garmintick = (garmintime & 0xffff0000) | field['timestamp_16']
                    if garmintick < garmintime:
                        garmintick += 0x10000
                    tick = datetime.fromtimestamp(garmintick + 631065600)

              # times.append(aslocaltimestr(tick))
                times.append(tick)
                heart.append(rate)

                if activity:
                  # print("activity = " + str(activity))
                    types.append(activity)
                    if activity in activities:
                        marks.append(activities[activity])
                    else:
                        marks.append('o')

                # Note: intensity may be 0 :(.
              # if intensity:
                if True:
                  # print("intensity = " + str(intensity))
                    power.append(intensity)
                    if intensity in intensities:
                        color.append(intensities[intensity])
                    else:
                        color.append('orange')

    fit = []

    if heart:
      # print()
      # print("heart")
      # print(heart)

      # print()
      # print("times")
      # print(times)

      # print()
      # print("power")
      # print(power)

      # print()
      # print("types")
      # print(types)

      # print()
      # print("color")
      # print(color)

      # print()
      # print("marks")
      # print(marks)

        # Switching to Pandas Dataframe and plots.
    # # plt.plot_date(times, heart, color=color)
    #   plt.scatter(times, heart, color=color)
    #   plt.plot(times, heart)
    # # ax = plt.subplot(111)
    # # ax.bar(times, heart)
    # # ax.xaxis_date()
    #   plt.xticks(rotation=90, ha='right')
    #   plt.xlabel("date")
    #   plt.ylabel("rate (BPM)")
    #   plt.title(min(times).strftime("%m/%d/%Y, %H:%M:%S") + " - " + max(times).strftime("%m/%d/%Y, %H:%M:%S"))
    #   plt.suptitle(filename)
    #   plt.show()

        fit = pd.DataFrame(list(zip(times, heart, power, types)),
            columns =['timestamp', 'heartrate', 'intensity', 'activity'])

        # Associate relevant metadata to this DataFrame.
        if len(times):
            fit.attrs['max'] = max(times)
            fit.attrs['min'] = min(times)
            fit.attrs['label'] = fit.attrs['min'].strftime("%m/%d/%Y, %H:%M:%S") + "$\endash$" + fit.attrs['max'].strftime("%m/%d/%Y, %H:%M:%S")

        fit.attrs['title'] = filename
        fit.attrs['color'] = color
        fit.attrs['marks'] = marks

        print(filename)
        print(fit)

    return fit

def fitplot(fit, gca = []):
    plot = []

    if len(fit) != 0:

        if gca:
            axes = fit.plot(
                ax=gca,
                kind='line',
                color='lightgray',
                label=fit.attrs['label'],
                legend=True,
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='heartrate',
                ylabel='rate (BPM)')
        else:
            axes = fit.plot(
                kind='line',
                color='lightgray',
                label=fit.attrs['label'],
                legend=True,
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='heartrate',
                ylabel='rate (BPM)')

        plot = fit.plot(
            ax=axes,
            kind='scatter',
            color=fit.attrs['color'],
            legend=False,
          # marker=fit.attrs['marks'],
            rot=30,
            title=fit.attrs['title'],
            x='timestamp',
            xlabel='date',
            y='heartrate',
            ylabel='rate (BPM)')

        plt.show()

    return plot

def intplot(fit, gca = []):
    plot = []

    if len(fit) != 0:

        if gca:
            axes = fit.plot(
                ax=gca,
                kind='area',
                color='yellow',
                label=fit.attrs['label'],
                legend=False,
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='intensity',
                ylabel='intensity')
        else:
            axes = fit.plot(
                kind='area',
                color='yellow',
                label=fit.attrs['label'],
                legend=False,
                lw=0.5,
                x='timestamp',
                xlabel='date',
                y='intensity',
                ylabel='intensity')

        plot = fit.plot(
            ax=axes,
            kind='scatter',
            color='yellow',
          # color=fit.attrs['color'],
            legend=False,
          # marker=fit.attrs['marks'],
            rot=30,
            title=fit.attrs['title'],
            x='timestamp',
            xlabel='date',
            y='intensity',
            ylabel='intensity')

      # plt.show()

    return plot

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
                legend=True,
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
            marker='*',
            rot=30,
            title=cgm.attrs['title'],
            x='timestamp',
            xlabel='date',
            y='glucose',
            ylabel='glucose (mmol/L)')

      # plt.show()

    return plot

# ##################
# Let's get started!
# ##################

cgm_filename = 'LibreView/NicholasHarbour_glucose_9-12-2023.csv'

start = datetime(2023,12,8,14,30,0,0)
end   = datetime(2023,12,9,0,0,0,0)

cgm = cgmparse(cgm_filename, start, end)

if len(cgm) != 0:
    cgmplot(cgm)
    plt.show()

# Support a combined plot.

cgm_times = cgm['timestamp'].tolist()
cgm_value = cgm['glucose'].tolist()

#plt.plot_date(cgm_times, cgm_value, color='orange', marker='*')
##plt.scatter(cgm_times, cgm_value, color='orange', marker='*')
#plt.plot(cgm_times, cgm_value, color='orange')
##ax = plt.subplot(111)
##ax.bar(cgm_times, cgm_value)
##ax.xaxis_date()
#plt.xticks(rotation=90, ha='right')
#plt.xlabel("date")
#plt.ylabel("glucose (mmol/L)")
#plt.title(min(cgm_times).strftime("%m/%d/%Y, %H:%M:%S") + " - " + max(cgm_times).strftime("%m/%d/%Y, %H:%M:%S"))
#plt.suptitle(cgm_filename)
#plt.show()

#plt.plot_date(cgm_times, cgm_value, color='orange', fmt='*')
##plt.scatter(cgm_times, cgm_value, color='orange', marker='*')
#plt.plot(cgm_times, cgm_value, color='orange')
##ax = plt.subplot(111)
##ax.bar(cgm_times, cgm_value)
##ax.xaxis_date()
#plt.xticks(rotation=30, ha='right')
#plt.xlabel("date")
#plt.ylabel("glucose (mmol/L)")
#plt.suptitle(cgm_filename)
#ax = (plt.gca()).twinx()


print()
print()
print()


#fit = fitparse("Garmin/DEVICE.fit")
#fit = fitparse("Garmin/Records/RECORDS.fit")
#fit = fitparse("Garmin//Seg_List/SEG_LIST.fit")
#fit = fitparse("Garmin/Totals/TOTALS.fit")
#fit = fitparse("2023-01-29-15-47-38.fit")

# List all files in a directory using 'os.listdir'.
#basepath = 'Garmin/Activity'
basepath = 'Garmin/Monitor'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
      # print(entry)
        fit = fitparse(basepath + '/' + entry)
        print()

        if len(fit) != 0:
            start = fit.attrs['min']
            end = fit.attrs['max']
            print(start)
            print(end)
            if start and end:
                cgm = cgmparse(cgm_filename, start, end)
                print(start)
                print(end)
                print(cgm)
                if len(cgm) != 0:

                    cgm_times = cgm['timestamp'].tolist()
                    cgm_value = cgm['glucose'].tolist()

                  # cgmplot(cgm)
                    plt.plot_date(cgm_times, cgm_value, color='orange', fmt='*')
                  # plt.scatter(cgm_times, cgm_value, color='orange', marker='*')
                    plt.plot(cgm_times, cgm_value, color='orange')
                  # ax = plt.subplot(111)
                  # ax.bar(cgm_times, cgm_value)
                  # ax.xaxis_date()
                    plt.xticks(rotation=30, ha='right')
                    plt.xlabel("date")
                    plt.ylabel("glucose (mmol/L)")
                    plt.suptitle(cgm_filename)
                  # ax = (plt.gca()).twinx()
                    ax = (plt.gca()).twinx()

            intplot(fit, ax)
            ax = (plt.gca()).twinx()
            fitplot(fit, ax)
            plt.show()
            ax = []

# #################
# That's all Folks!
# #################
print(end='\a')
