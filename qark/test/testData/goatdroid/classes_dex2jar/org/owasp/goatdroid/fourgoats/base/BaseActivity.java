package org.owasp.goatdroid.fourgoats.base;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build.VERSION;
import android.os.Bundle;
import com.actionbarsherlock.app.SherlockActivity;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuInflater;
import com.actionbarsherlock.view.MenuItem;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.activities.About;
import org.owasp.goatdroid.fourgoats.activities.AdminHome;
import org.owasp.goatdroid.fourgoats.activities.Home;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.activities.Preferences;
import org.owasp.goatdroid.fourgoats.activities.ViewProfile;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.login.LoginRequest;

public class BaseActivity
  extends SherlockActivity
{
  protected Context context;
  
  public BaseActivity() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    getSupportActionBar().setIcon(2130837628);
    if ((!(this instanceof Home)) && (!(this instanceof AdminHome)))
    {
      if (Build.VERSION.SDK_INT >= 14)
      {
        getActionBar().setHomeButtonEnabled(true);
        getActionBar().setDisplayHomeAsUpEnabled(true);
      }
    }
    else {
      return;
    }
    getSupportActionBar().setHomeButtonEnabled(true);
    getSupportActionBar().setDisplayHomeAsUpEnabled(true);
  }
  
  public boolean onCreateOptionsMenu(Menu paramMenu)
  {
    getSupportMenuInflater().inflate(2131492865, paramMenu);
    this.context = getApplicationContext();
    return super.onCreateOptionsMenu(paramMenu);
  }
  
  public boolean onOptionsItemSelected(MenuItem paramMenuItem)
  {
    int i = paramMenuItem.getItemId();
    if (i == 16908332) {
      finish();
    }
    do
    {
      return true;
      if (i == 2130968680)
      {
        startActivity(new Intent(this, Preferences.class));
        return true;
      }
      if (i == 2130968681)
      {
        Intent localIntent = new Intent(this, ViewProfile.class);
        Bundle localBundle = new Bundle();
        UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(this.context);
        String str = localUserInfoDBHelper.getUserName();
        localUserInfoDBHelper.close();
        localBundle.putString("userName", str);
        localIntent.putExtras(localBundle);
        startActivity(localIntent);
        return true;
      }
      if (i == 2130968683)
      {
        new LogOutAsyncTask().execute(new Void[] { null, null });
        return true;
      }
    } while (i != 2130968682);
    startActivity(new Intent(this, About.class));
    return true;
  }
  
  public class LogOutAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    public LogOutAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      LoginRequest localLoginRequest = new LoginRequest(BaseActivity.this.context);
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(BaseActivity.this.context);
      HashMap localHashMap = new HashMap();
      try
      {
        localHashMap = localLoginRequest.logOut(localUserInfoDBHelper.getSessionToken());
        localUserInfoDBHelper.deleteInfo();
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
        Intent localIntent1 = new Intent(BaseActivity.this.context, Login.class);
        BaseActivity.this.startActivity(localIntent1);
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        Utils.makeToast(BaseActivity.this.context, "Invalid session", 1);
        Intent localIntent2 = new Intent(BaseActivity.this.context, Login.class);
        BaseActivity.this.startActivity(localIntent2);
        return;
      }
      Utils.makeToast(BaseActivity.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
