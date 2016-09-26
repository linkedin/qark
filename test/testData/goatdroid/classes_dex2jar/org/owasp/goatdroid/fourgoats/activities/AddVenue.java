package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.CheckinDBHelper;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.addvenue.AddVenueRequest;
import org.owasp.goatdroid.fourgoats.rest.checkin.CheckinRequest;

public class AddVenue
  extends BaseActivity
{
  Bundle bundle;
  Context context;
  EditText venueNameText;
  EditText venueWebsiteText;
  
  public AddVenue() {}
  
  public void addVenue(View paramView)
  {
    if (!allFieldsCompleted(this.venueNameText.getText().toString(), this.venueWebsiteText.getText().toString()))
    {
      Utils.makeToast(this.context, "All fields are required", 1);
      return;
    }
    new AddVenueAsyncTask(null).execute(new Void[] { null, null });
  }
  
  public boolean allFieldsCompleted(String paramString1, String paramString2)
  {
    return (!paramString1.equals("")) && (!paramString2.equals(""));
  }
  
  public void launchAddVenue()
  {
    Intent localIntent = new Intent(this.context, AddVenue.class);
    localIntent.putExtras(this.bundle);
    startActivity(localIntent);
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void launchViewCheckin()
  {
    Intent localIntent = new Intent(this.context, ViewCheckin.class);
    localIntent.putExtras(this.bundle);
    startActivity(localIntent);
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903061);
    this.context = getApplicationContext();
    this.bundle = getIntent().getExtras();
    this.venueNameText = ((EditText)findViewById(2130968621));
    this.venueWebsiteText = ((EditText)findViewById(2130968622));
  }
  
  private class AddVenueAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private AddVenueAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(AddVenue.this.context);
      CheckinDBHelper localCheckinDBHelper = new CheckinDBHelper(AddVenue.this.context);
      AddVenueRequest localAddVenueRequest = new AddVenueRequest(AddVenue.this.context);
      HashMap localHashMap1 = new HashMap();
      try
      {
        String str = localUserInfoDBHelper.getSessionToken();
        if (str.equals("")) {
          localHashMap1.put("errors", "Invalid session");
        }
        for (;;)
        {
          return localHashMap1;
          localHashMap1 = localAddVenueRequest.doAddVenue(str, AddVenue.this.venueNameText.getText().toString(), AddVenue.this.venueWebsiteText.getText().toString(), AddVenue.this.bundle.getString("latitude"), AddVenue.this.bundle.getString("longitude"));
          if (((String)localHashMap1.get("success")).equals("true"))
          {
            localHashMap2 = new CheckinRequest(AddVenue.this.context).doCheckin(str, AddVenue.this.bundle.getString("latitude"), AddVenue.this.bundle.getString("longitude"));
            if (!((String)localHashMap2.get("success")).equals("true")) {
              break;
            }
            localHashMap2.put("latitude", AddVenue.this.bundle.getString("latitude"));
            localHashMap2.put("longitude", AddVenue.this.bundle.getString("longitude"));
            localCheckinDBHelper.insertCheckin(localHashMap2);
            AddVenue.this.bundle.putString("checkinID", (String)localHashMap2.get("checkinID"));
            AddVenue.this.bundle.putString("dateTime", (String)localHashMap2.get("dateTime"));
          }
        }
      }
      catch (Exception localException)
      {
        for (;;)
        {
          HashMap localHashMap2;
          localHashMap1.put("errors", localException.getMessage());
          return localHashMap1;
          localHashMap1.put("success", "false");
          localHashMap1.put("errors", (String)localHashMap2.get("errors"));
        }
      }
      finally
      {
        localUserInfoDBHelper.close();
        localCheckinDBHelper.close();
      }
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        AddVenue.this.bundle.putString("venueName", AddVenue.this.venueNameText.getText().toString());
        AddVenue.this.bundle.putString("venueWebsite", AddVenue.this.venueWebsiteText.getText().toString());
        AddVenue.this.launchViewCheckin();
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        Utils.makeToast(AddVenue.this.context, "Invalid session", 1);
        AddVenue.this.launchLogin();
        return;
      }
      Utils.makeToast(AddVenue.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
