package org.owasp.goatdroid.fourgoats.services;

import android.app.Service;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.IBinder;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.db.CheckinDBHelper;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;

public class LocationService
  extends Service
{
  String latitude;
  LocationManager locationManager;
  String longitude;
  
  public LocationService() {}
  
  public void getLocation()
  {
    this.locationManager = ((LocationManager)getSystemService("location"));
    MyLocationListener localMyLocationListener = new MyLocationListener(null);
    this.locationManager.requestLocationUpdates("gps", 0L, 0.0F, localMyLocationListener);
  }
  
  public void getLocationLoop()
  {
    new Thread()
    {
      public void run()
      {
        while ((LocationService.this.latitude == null) && (LocationService.this.longitude == null)) {}
        for (;;)
        {
          CheckinDBHelper localCheckinDBHelper = new CheckinDBHelper(LocationService.this.getApplicationContext());
          localCheckinDBHelper.insertAutoCheckin(LocationService.this.latitude, LocationService.this.longitude, Utils.getCurrentDateTime());
          localCheckinDBHelper.close();
          try
          {
            sleep(300000L);
          }
          catch (InterruptedException localInterruptedException) {}
        }
      }
    }.start();
  }
  
  public IBinder onBind(Intent paramIntent)
  {
    return null;
  }
  
  public void onCreate()
  {
    super.onCreate();
    if (((String)new UserInfoDBHelper(getApplicationContext()).getPreferences().get("autoCheckin")).equals("true"))
    {
      getLocation();
      getLocationLoop();
      return;
    }
    stopSelf();
  }
  
  private class MyLocationListener
    implements LocationListener
  {
    private MyLocationListener() {}
    
    public void onLocationChanged(Location paramLocation)
    {
      LocationService.this.latitude = Double.toString(paramLocation.getLatitude());
      LocationService.this.longitude = Double.toString(paramLocation.getLongitude());
    }
    
    public void onProviderDisabled(String paramString) {}
    
    public void onProviderEnabled(String paramString) {}
    
    public void onStatusChanged(String paramString, int paramInt, Bundle paramBundle) {}
  }
}
