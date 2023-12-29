//
// Copyright (C) 2023 by Discretize Designs Ltd.
//

using Toybox.Application as App;
using Toybox.Sensor      as Sensor;

//using Toybox.Lang;
using Toybox.System;
using Toybox.SensorHistory;
using Toybox.Time;

class DataShellApp
  extends App.AppBase
{
    const oneHour = new Time.Duration(3600);

    var mainView;

    function initialize()
    {
        AppBase.initialize();
    }

    // Here 'onStart()' is called on application start-up.
    function onStart(state)
    {
        Sensor.setEnabledSensors([Sensor.SENSOR_HEARTRATE]);
        Sensor.enableSensorEvents(method(:onSensor));
    }

    // Here 'onStop()' is called when your application is exiting.
    function onStop(state)
    {
     // Position.enableLocationEvents(Position.LOCATION_DISABLE, method(:onPosition));
        Sensor.enableSensorEvents();
    }

    function onSensor(sensorInfo)
    {
     // System.println("sensorInfo: " + sensorInfo);
     // System.println("Heart Rate: " + sensorInfo.heartRate);
        mainView.setHeartRate(sensorInfo.heartRate);
/*
        // Store the iterator info in a variable.
        // The options are 'null' in this case so the entire available history is returned
        // with the newest samples returned first.
        var sensorIter = getIterator();

        // Print out the next entry in the iterator
        if (sensorIter != null)
        {
         // System.println((sensorIter.next()).data);
            var item = sensorIter.next();
            while (item != null) 
            {
             // if (item != null)
             // {
                    System.println(item.when.value());
                    System.println(item.data);
             // }

                item = sensorIter.next();
            }
        }
        System.println("data end");
*/
    }

    // Return the initial view of your application here.
    function getInitialView()
    {
        mainView = new DataShellView();
        var viewDelegate = new DataShellDelegate(mainView);
        return [mainView, viewDelegate];
    }

    // Create a method to get the SensorHistoryIterator object
    function getIterator()
    {
        // Check device for SensorHistory compatibility.
        if ((Toybox has :SensorHistory) && (Toybox.SensorHistory has :getHeartRateHistory))
        {
            return Toybox.SensorHistory.getHeartRateHistory({ :period => oneHour, :order => SensorHistory.ORDER_OLDEST_FIRST });
        }

        return null;
    }
}