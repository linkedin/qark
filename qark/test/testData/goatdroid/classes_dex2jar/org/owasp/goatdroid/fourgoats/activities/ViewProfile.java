package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.friends.FriendRequest;

public class ViewProfile
  extends BaseActivity
{
  private Bundle bundle;
  private Context context;
  private TextView lastCheckinTextView;
  private TextView nameTextView;
  private TextView userNameTextView;
  
  public ViewProfile() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903086);
    this.context = getApplicationContext();
    this.bundle = getIntent().getExtras();
    this.userNameTextView = ((TextView)findViewById(2130968640));
    this.nameTextView = ((TextView)findViewById(2130968662));
    this.lastCheckinTextView = ((TextView)findViewById(2130968663));
    new GetProfileInfo(null).execute(new Void[] { null, null });
  }
  
  public void requestAsFriend(View paramView)
  {
    new RequestFriendAsyncTask(null).execute(new Void[] { null, null });
  }
  
  public void viewUserCheckinHistory(View paramView)
  {
    Intent localIntent = new Intent(this.context, History.class);
    localIntent.putExtras(this.bundle);
    startActivity(localIntent);
  }
  
  private class GetProfileInfo
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private GetProfileInfo() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      localHashMap = new HashMap();
      localUserInfoDBHelper = new UserInfoDBHelper(ViewProfile.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      FriendRequest localFriendRequest = new FriendRequest(ViewProfile.this.context);
      try
      {
        if (!str.equals("")) {
          break label83;
        }
        localHashMap.put("errors", "Invalid session");
        localHashMap.put("success", "false");
      }
      catch (Exception localException)
      {
        for (;;)
        {
          label83:
          boolean bool;
          localHashMap.put("errors", localException.getMessage());
          localHashMap.put("success", "false");
          localUserInfoDBHelper.close();
        }
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
      return localHashMap;
      localHashMap = localFriendRequest.getProfile(str, ViewProfile.this.bundle.getString("userName"));
      bool = ((String)localHashMap.get("success")).equals("true");
      if (bool)
      {
        localUserInfoDBHelper.close();
        return localHashMap;
      }
      localUserInfoDBHelper.close();
      return localHashMap;
    }
    
    public void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        ViewProfile.this.userNameTextView.setText(ViewProfile.this.bundle.getString("userName"));
        ViewProfile.this.nameTextView.setText((String)paramHashMap.get("firstName") + " " + (String)paramHashMap.get("lastName"));
        if (((String)paramHashMap.get("lastCheckinTime")).equals(""))
        {
          ViewProfile.this.lastCheckinTextView.setText("User has never checked in");
          return;
        }
        String[] arrayOfString = ((String)paramHashMap.get("lastCheckinTime")).split(" ");
        ViewProfile.this.lastCheckinTextView.setText("Date: " + arrayOfString[0] + "\nTime: " + arrayOfString[1] + "\nLatitude: " + (String)paramHashMap.get("lastLatitude") + "\nLongitude: " + (String)paramHashMap.get("lastLongitude"));
        return;
      }
      Utils.makeToast(ViewProfile.this.context, "Something weird happened", 1);
    }
  }
  
  private class RequestFriendAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private RequestFriendAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      FriendRequest localFriendRequest = new FriendRequest(ViewProfile.this.context);
      HashMap localHashMap1 = new HashMap();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(ViewProfile.this.context);
      try
      {
        HashMap localHashMap2 = localFriendRequest.doFriendRequest(localUserInfoDBHelper.getSessionToken(), ViewProfile.this.bundle.getString("userName"));
        return localHashMap2;
      }
      catch (Exception localException)
      {
        localHashMap1.put("errors", localException.getMessage());
        localHashMap1.put("success", "false");
        return localHashMap1;
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
        Utils.makeToast(ViewProfile.this.context, "Friend request sent!", 1);
        return;
      }
      Utils.makeToast(ViewProfile.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
