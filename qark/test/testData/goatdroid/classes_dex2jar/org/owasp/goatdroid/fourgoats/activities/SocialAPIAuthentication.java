package org.owasp.goatdroid.fourgoats.activities;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.login.LoginRequest;

public class SocialAPIAuthentication
  extends Activity
{
  Context context;
  boolean isAuthenticated;
  EditText passwordEditText;
  String sessionToken;
  EditText userNameEditText;
  
  public SocialAPIAuthentication() {}
  
  public boolean allFieldsCompleted(String paramString1, String paramString2)
  {
    return (!paramString1.equals("")) && (!paramString2.equals(""));
  }
  
  public void doAuthenticateAPI(View paramView)
  {
    new AuthenticateAsyncTask(null).execute(new Void[] { null, null });
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903095);
    this.userNameEditText = ((EditText)findViewById(2130968646));
    this.passwordEditText = ((EditText)findViewById(2130968652));
    this.context = getApplicationContext();
    this.sessionToken = "";
  }
  
  private class AuthenticateAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private AuthenticateAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      LoginRequest localLoginRequest = new LoginRequest(SocialAPIAuthentication.this.context);
      str1 = SocialAPIAuthentication.this.userNameEditText.getText().toString();
      str2 = SocialAPIAuthentication.this.passwordEditText.getText().toString();
      localHashMap = new HashMap();
      localUserInfoDBHelper = new UserInfoDBHelper(SocialAPIAuthentication.this.context);
      for (;;)
      {
        try
        {
          SocialAPIAuthentication.this.sessionToken = localUserInfoDBHelper.getSessionToken();
          if (!SocialAPIAuthentication.this.allFieldsCompleted(str1, str2)) {
            continue;
          }
          if ((!SocialAPIAuthentication.this.sessionToken.isEmpty()) && (SocialAPIAuthentication.this.sessionToken != null)) {
            continue;
          }
          localHashMap.put("errors", "Invalid session");
          localHashMap.put("success", "false");
        }
        catch (Exception localException)
        {
          localHashMap.put("errors", localException.getMessage());
          localHashMap.put("success", "false");
          Log.w("Failed login", "Login with " + str1 + " " + str2 + " failed");
          return localHashMap;
          localHashMap.put("success", "false");
          localHashMap.put("errors", "Invalid session");
          continue;
        }
        finally
        {
          localUserInfoDBHelper.close();
        }
        localUserInfoDBHelper.close();
        return localHashMap;
        localHashMap = localLoginRequest.validateCredentialsAPI(str1, str2);
        continue;
        if (SocialAPIAuthentication.this.sessionToken == null) {
          continue;
        }
        SocialAPIAuthentication.this.isAuthenticated = true;
        localHashMap.put("success", "true");
      }
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      Intent localIntent;
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        Utils.makeToast(SocialAPIAuthentication.this.context, "You have successfully authenticated.", 1);
        SocialAPIAuthentication.this.sessionToken = ((String)paramHashMap.get("sessionToken"));
        localIntent = new Intent();
        localIntent.putExtra("sessionToken", SocialAPIAuthentication.this.sessionToken);
        if (SocialAPIAuthentication.this.getParent() != null) {
          break label158;
        }
        SocialAPIAuthentication.this.setResult(-1, localIntent);
      }
      for (;;)
      {
        SocialAPIAuthentication.this.finish();
        return;
        if (((String)paramHashMap.get("errors")).equals("Invalid session"))
        {
          Utils.makeToast(SocialAPIAuthentication.this.context, "Invalid session", 1);
          SocialAPIAuthentication.this.launchLogin();
          break;
        }
        Utils.makeToast(SocialAPIAuthentication.this.getApplicationContext(), (String)paramHashMap.get("errors"), 0);
        break;
        label158:
        SocialAPIAuthentication.this.getParent().setResult(-1, localIntent);
      }
    }
  }
}
