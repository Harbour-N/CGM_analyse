//
// Copyright (C) 2023 by Discretize Designs Ltd.
//

using Toybox.Graphics as GFX;
//using Toybox.Math     as Math;
//using Toybox.Sensor   as Sensor;
using Toybox.Time     as Time;
using Toybox.Timer    as Timer;
using Toybox.WatchUi  as UI;
//using Toybox.System as Sys;
//using Toybox.Lang   as Lang;

class DataShellView
  extends UI.View
{
    var r = 10;
    var s = 0;

    var dataTimer;

    var x;
    var y;

    var width;
    var height;
    var ox;
    var oy;
    var xx;
    var yy;

    var heartInfo = null;

    function initialize()
    {
        View.initialize();
    }

    // Load your resources here.
    function onLayout(dc)
    {
        width  = dc.getWidth();
        height = dc.getHeight();

        ox = width  / 2;
        oy = height / 2;

        xx = ox / 4;
        yy = oy / 4;

        x = ox;
        y = oy;

        // Note: here a callback delay of 1000 = 1 sec.
        dataTimer = new Timer.Timer();
        dataTimer.start(method(:timerCallback), 100, true);
    }

    // Restore the state of the app and prepare the view to be shown.
    function onShow()
    {
    }

    // Update the view.
    function onUpdate(dc)
    {
        var ds = 90.0 / (r + 1.0);
        if (ds < 1.0)
        {
            ds = 1;
        }

        s = s + ds;
        if (s > r)
        {
            s = 1;
        }

        dc.setColor(GFX.COLOR_WHITE, GFX.COLOR_BLACK);
        dc.clear();

     // dc.setColor(GFX.COLOR_RED, GFX.COLOR_RED);
        dc.setColor(GFX.COLOR_RED, GFX.COLOR_TRANSPARENT);
        dc.fillCircle(x.toNumber(), y.toNumber(), r);

        dc.setColor(GFX.COLOR_GREEN, GFX.COLOR_TRANSPARENT);
        dc.drawCircle(x.toNumber(), y.toNumber(), s);

        // (Re)Set default background colour, etc.
        dc.setColor(GFX.COLOR_YELLOW, GFX.COLOR_TRANSPARENT);
        dc.drawText(ox, oy - 40, GFX.FONT_SMALL, "Position disabled", GFX.TEXT_JUSTIFY_CENTER);

        // (Re)Set default background colour, etc.
        dc.setColor(GFX.COLOR_WHITE, GFX.COLOR_TRANSPARENT);
        if (heartInfo != null)
        {
            var string;

            string = "<" + heartInfo.toString() + " BPM>";
            dc.drawText(ox, (oy - 10), GFX.FONT_SMALL, string, GFX.TEXT_JUSTIFY_CENTER);

            dc.setColor(GFX.COLOR_LT_GRAY, GFX.COLOR_TRANSPARENT);
            dc.drawText(ox, (oy + 15), GFX.FONT_SMALL, "CGM mmol/L", GFX.TEXT_JUSTIFY_CENTER);
        }
        else
        {
            dc.drawText(ox, oy - 15, GFX.FONT_SMALL, "No heart info", GFX.TEXT_JUSTIFY_CENTER);
        }
    }

    function timerCallback()
    {
        UI.requestUpdate();
    }

    function setHeartRate(heartRate)
    {
        heartInfo = heartRate;
        if (heartInfo != null)
        {
            r = heartInfo / 2.0;
        }

        UI.requestUpdate();
    }

    function markEvent()
    {
    }

    // Called when this View is removed from the screen.
    // Save the state of your app here.
    function onHide()
    {
    }
}