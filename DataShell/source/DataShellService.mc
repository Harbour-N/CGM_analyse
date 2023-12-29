using Toybox.Background;
using Toybox.Communications;
using Toybox.System;

(:background)
class MyServiceDelegate
  extends System.ServiceDelegate
{
    // When a scheduled background event triggers,
    // make a request to a service
    // and handle the response with a callback function,
    // within this delegate.
    function onTemporalEvent()
    {
        System.println("Service Delegate # onTemporalEvent");

        Communications.makeWebRequest(
            "https://nightscout.com",
            {},
            {},
            method(:responseCallback)
        );
    }

    function responseCallback(responseCode, data)
    {
        // Do stuff with the response data here
        // and send the data payload
        // back to the app that originated the background process.
        Background.exit(backgroundData);
        System.println("Service Delegate # responseCallback");
    }
}