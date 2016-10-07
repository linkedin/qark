package org.owasp.goatdroid.fourgoats.base;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build.VERSION;
import android.os.Bundle;
import com.actionbarsherlock.app.SherlockFragmentActivity;
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

public class BaseFragmentActivity
  extends SherlockFragmentActivity
{
  protected Context context;
  
  public BaseFragmentActivity() {}
  
  public void launchHome()
  {
    startActivity(new Intent(this.context, Home.class));
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    getSupportActionBar().setIcon(2130837628);
    if (Build.VERSION.SDK_INT >= 14)
    {
      getActionBar().setHomeButtonEnabled(true);
      getActionBar().setDisplayHomeAsUpEnabled(true);
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
    UserInfoDBHelper localUserInfoDBHelper1;
    if (i == 16908332) {
      localUserInfoDBHelper1 = new UserInfoDBHelper(this.context);
    }
    label102:
    do
    {
      try
      {
        if (localUserInfoDBHelper1.getIsAdmin()) {}
        for (Intent localIntent1 = new Intent(this, AdminHome.class);; localIntent1 = new Intent(this, Home.class))
        {
          localUserInfoDBHelper1.close();
          startActivity(localIntent1);
          return true;
        }
        if (i != 2130968680) {
          break label102;
        }
      }
      finally
      {
        localUserInfoDBHelper1.close();
      }
      startActivity(new Intent(this, Preferences.class));
      return true;
      if (i == 2130968681)
      {
        Intent localIntent2 = new Intent(this, ViewProfile.class);
        Bundle localBundle = new Bundle();
        UserInfoDBHelper localUserInfoDBHelper2 = new UserInfoDBHelper(this.context);
        String str = localUserInfoDBHelper2.getUserName();
        localUserInfoDBHelper2.close();
        localBundle.putString("userName", str);
        localIntent2.putExtras(localBundle);
        startActivity(localIntent2);
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
      LoginRequest localLoginRequest = new LoginRequest(BaseFragmentActivity.this.context);
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(BaseFragmentActivity.this.context);
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
        Intent localIntent1 = new Intent(BaseFragmentActivity.this.context, Login.class);
        BaseFragmentActivity.this.startActivity(localIntent1);
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        Utils.makeToast(BaseFragmentActivity.this.context, "Invalid session", 1);
        Intent localIntent2 = new Intent(BaseFragmentActivity.this.context, Login.class);
        BaseFragmentActivity.this.startActivity(localIntent2);
        return;
      }
      Utils.makeToast(BaseFragmentActivity.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
