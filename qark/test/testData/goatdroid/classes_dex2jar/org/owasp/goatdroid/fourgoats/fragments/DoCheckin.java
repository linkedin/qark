package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.activities.AddVenue;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.activities.ViewCheckin;
import org.owasp.goatdroid.fourgoats.db.CheckinDBHelper;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.checkin.CheckinRequest;

public class DoCheckin
  extends SherlockFragment
{
  Context context;
  TextView gpsCoordsText;
  String latitude;
  String longitude;
  Button sendCheckin;
  
  public DoCheckin() {}
  
  public void getLocation()
  {
    ((LocationManager)this.context.getSystemService("location")).requestLocationUpdates("gps", 0L, 0.0F, new MyLocationListener(null));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    this.context = getActivity().getApplicationContext();
    getLocation();
  }
  
  public View onCreateView(LayoutInflater paramLayoutInflater, ViewGroup paramViewGroup, Bundle paramBundle)
  {
    View localView = paramLayoutInflater.inflate(2130903071, paramViewGroup, false);
    this.gpsCoordsText = ((TextView)localView.findViewById(2130968638));
    this.sendCheckin = ((Button)localView.findViewById(2130968623));
    this.sendCheckin.setOnClickListener(new View.OnClickListener()
    {
      public void onClick(View paramAnonymousView)
      {
        DoCheckin.this.sendCheckin(paramAnonymousView);
      }
    });
    return localView;
  }
  
  public void sendCheckin(View paramView)
  {
    if (this.gpsCoordsText.getText().toString().startsWith("Getting your location"))
    {
      Utils.makeToast(this.context, "I don't know where you are. I need your location", 1);
      return;
    }
    new DoCheckinAsyncTask(null).execute(new Void[] { null, null });
  }
  
  private class DoCheckinAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private DoCheckinAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(DoCheckin.this.context);
      HashMap localHashMap = new HashMap();
      String str = localUserInfoDBHelper.getSessionToken();
      CheckinRequest localCheckinRequest = new CheckinRequest(DoCheckin.this.context);
      try
      {
        localHashMap = localCheckinRequest.doCheckin(str, DoCheckin.this.latitude, DoCheckin.this.longitude);
        if (((String)localHashMap.get("success")).equals("true"))
        {
          CheckinDBHelper localCheckinDBHelper = new CheckinDBHelper(DoCheckin.this.context);
          localHashMap.put("latitude", DoCheckin.this.latitude);
          localHashMap.put("longitude", DoCheckin.this.longitude);
          localCheckinDBHelper.insertCheckin(localHashMap);
        }
        return localHashMap;
      }
      catch (Exception localException)
      {
        localHashMap.put("errors", localException.getMessage());
        return localHashMap;
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void launchAddVenue(Bundle paramBundle)
    {
      Intent localIntent = new Intent(DoCheckin.this.context, AddVenue.class);
      localIntent.putExtras(paramBundle);
      DoCheckin.this.startActivity(localIntent);
    }
    
    public void launchViewCheckin(Bundle paramBundle)
    {
      Intent localIntent = new Intent(DoCheckin.this.context, ViewCheckin.class);
      localIntent.putExtras(paramBundle);
      DoCheckin.this.startActivity(localIntent);
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        if (paramHashMap.size() == 4) {
          Utils.makeToast(DoCheckin.this.context, "Checkin complete, great success!", 1);
        }
        for (;;)
        {
          Bundle localBundle2 = new Bundle();
          localBundle2.putString("checkinID", (String)paramHashMap.get("checkinID"));
          localBundle2.putString("venueName", (String)paramHashMap.get("venueName"));
          localBundle2.putString("venueWebsite", (String)paramHashMap.get("venueWebsite"));
          localBundle2.putString("dateTime", (String)paramHashMap.get("dateTime"));
          localBundle2.putString("latitude", DoCheckin.this.latitude);
          localBundle2.putString("longitude", DoCheckin.this.longitude);
          launchViewCheckin(localBundle2);
          CheckinDBHelper localCheckinDBHelper = new CheckinDBHelper(DoCheckin.this.context);
          paramHashMap.put("latitude", DoCheckin.this.latitude);
          paramHashMap.put("longitude", DoCheckin.this.longitude);
          localCheckinDBHelper.insertCheckin(paramHashMap);
          return;
          String str = "You've earned a reward:  " + (String)paramHashMap.get("rewardName");
          Utils.makeToast(DoCheckin.this.context, str, 1);
        }
      }
      if (((String)paramHashMap.get("errors")).equals("Venue does not exist"))
      {
        Utils.makeToast(DoCheckin.this.context, "Venue does not exist", 1);
        Bundle localBundle1 = new Bundle();
        localBundle1.putString("latitude", DoCheckin.this.latitude);
        localBundle1.putString("longitude", DoCheckin.this.longitude);
        launchAddVenue(localBundle1);
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        Utils.makeToast(DoCheckin.this.context, "Invalid session", 1);
        Intent localIntent = new Intent(DoCheckin.this.context, Login.class);
        DoCheckin.this.startActivity(localIntent);
        return;
      }
      Utils.makeToast(DoCheckin.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
  
  private class MyLocationListener
    implements LocationListener
  {
    private MyLocationListener() {}
    
    public void onLocationChanged(Location paramLocation)
    {
      DoCheckin.this.latitude = Double.toString(paramLocation.getLatitude());
      DoCheckin.this.longitude = Double.toString(paramLocation.getLongitude());
      DoCheckin.this.gpsCoordsText.setText("Latitude: " + DoCheckin.this.latitude + "\n\nLongitude: " + DoCheckin.this.longitude);
    }
    
    public void onProviderDisabled(String paramString) {}
    
    public void onProviderEnabled(String paramString) {}
    
    public void onStatusChanged(String paramString, int paramInt, Bundle paramBundle) {}
  }
}
