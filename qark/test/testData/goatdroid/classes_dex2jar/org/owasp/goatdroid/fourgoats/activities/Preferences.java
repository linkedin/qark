package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.preferences.PreferencesRequest;

public class Preferences
  extends BaseActivity
{
  CheckBox autoCheckin;
  Context context;
  CheckBox isPublic;
  
  public Preferences() {}
  
  public void launchHome(String paramString)
  {
    if (paramString.equals("true")) {}
    for (Intent localIntent = new Intent(this, AdminHome.class);; localIntent = new Intent(this, Home.class))
    {
      startActivity(localIntent);
      return;
    }
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903085);
    this.context = getApplicationContext();
    this.isPublic = ((CheckBox)findViewById(2130968660));
    this.autoCheckin = ((CheckBox)findViewById(2130968661));
    new GetExistingPreferences(null).execute(new Void[] { null, null });
  }
  
  public void submitChanges(View paramView)
  {
    new UpdatePreferencesAsyncTask(null).execute(new Void[] { null, null });
  }
  
  private class GetExistingPreferences
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private GetExistingPreferences() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      new HashMap();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(Preferences.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      HashMap localHashMap = localUserInfoDBHelper.getPreferences();
      localUserInfoDBHelper.close();
      if (str.equals(""))
      {
        localIntent = new Intent(Preferences.this, Login.class);
        Preferences.this.startActivity(localIntent);
      }
      while (localHashMap.size() > 0)
      {
        Intent localIntent;
        return localHashMap;
      }
      Utils.makeToast(Preferences.this.context, "Something weird happened", 1);
      return localHashMap;
    }
    
    public void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("isPublic")).equals("true")) {
        Preferences.this.isPublic.setChecked(true);
      }
      while (((String)paramHashMap.get("autoCheckin")).equals("true"))
      {
        Preferences.this.autoCheckin.setChecked(true);
        return;
        Preferences.this.isPublic.setChecked(false);
      }
      Preferences.this.autoCheckin.setChecked(false);
    }
  }
  
  private class UpdatePreferencesAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private UpdatePreferencesAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(Preferences.this.context);
      localUserInfoDBHelper.updatePreferences(Boolean.toString(Preferences.this.isPublic.isChecked()), Boolean.toString(Preferences.this.autoCheckin.isChecked()));
      PreferencesRequest localPreferencesRequest = new PreferencesRequest(Preferences.this.context);
      HashMap localHashMap = new HashMap();
      try
      {
        localHashMap = localPreferencesRequest.updatePreferences(localUserInfoDBHelper.getSessionToken(), Boolean.toString(Preferences.this.isPublic.isChecked()), Boolean.toString(Preferences.this.autoCheckin.isChecked()));
        localHashMap.put("isAdmin", Boolean.toString(localUserInfoDBHelper.getIsAdmin()));
        return localHashMap;
      }
      catch (Exception localException)
      {
        localHashMap.put("errors", localException.getMessage());
        localHashMap.put("success", "false");
        return localHashMap;
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        Utils.makeToast(Preferences.this.context, "Preferences have been updated!", 1);
        Preferences.this.launchHome((String)paramHashMap.get("isAdmin"));
        return;
      }
      Utils.makeToast(Preferences.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
