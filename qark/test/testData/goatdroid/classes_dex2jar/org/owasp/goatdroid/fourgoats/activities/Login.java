package org.owasp.goatdroid.fourgoats.activities;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.util.Log;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseUnauthenticatedActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.login.LoginRequest;

public class Login
  extends BaseUnauthenticatedActivity
{
  Context context;
  EditText passwordEditText;
  String previousActivity;
  CheckBox rememberMeCheckBox;
  EditText userNameEditText;
  
  public Login() {}
  
  public boolean allFieldsCompleted(String paramString1, String paramString2)
  {
    return (!paramString1.equals("")) && (!paramString2.equals(""));
  }
  
  public void checkCredentials(View paramView)
  {
    if (allFieldsCompleted(this.userNameEditText.getText().toString(), this.passwordEditText.getText().toString()))
    {
      new ValidateCredsAsyncTask(this).execute(new Void[] { null, null });
      return;
    }
    Utils.makeToast(this.context, "All fields are required", 1);
  }
  
  public void launchAdminHome()
  {
    startActivity(new Intent(this, AdminHome.class));
  }
  
  public void launchHome()
  {
    startActivity(new Intent(this, Home.class));
  }
  
  public void launchRegistration(View paramView)
  {
    startActivity(new Intent(this, Register.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903081);
    this.context = getApplicationContext();
    this.userNameEditText = ((EditText)findViewById(2130968646));
    this.passwordEditText = ((EditText)findViewById(2130968652));
    this.rememberMeCheckBox = ((CheckBox)findViewById(2130968653));
    SharedPreferences localSharedPreferences = getSharedPreferences("credentials", 1);
    try
    {
      this.previousActivity = getIntent().getExtras().getString("previousActivity");
      this.userNameEditText.setText(localSharedPreferences.getString("username", ""));
      this.passwordEditText.setText(localSharedPreferences.getString("password", ""));
      if (localSharedPreferences.getBoolean("remember", true))
      {
        this.rememberMeCheckBox.setChecked(true);
        return;
      }
    }
    catch (NullPointerException localNullPointerException)
    {
      for (;;)
      {
        this.previousActivity = "";
      }
      this.rememberMeCheckBox.setChecked(false);
    }
  }
  
  public void saveCredentials(String paramString1, String paramString2)
  {
    SharedPreferences.Editor localEditor = getSharedPreferences("credentials", 1).edit();
    localEditor.putString("username", paramString1);
    localEditor.putString("password", paramString2);
    localEditor.putBoolean("remember", true);
    localEditor.commit();
  }
  
  private class ValidateCredsAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    Login mActivity;
    
    public ValidateCredsAsyncTask(Login paramLogin)
    {
      this.mActivity = paramLogin;
    }
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      LoginRequest localLoginRequest = new LoginRequest(Login.this.context);
      String str1 = Login.this.userNameEditText.getText().toString();
      String str2 = Login.this.passwordEditText.getText().toString();
      boolean bool = Login.this.rememberMeCheckBox.isChecked();
      HashMap localHashMap = new HashMap();
      if (Login.this.allFieldsCompleted(str1, str2))
      {
        UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(Login.this.context);
        try
        {
          localHashMap = localLoginRequest.validateCredentials(str1, str2);
          if (((String)localHashMap.get("success")).equals("false")) {
            localHashMap.put("errors", "Login failed. Try again.");
          }
          for (;;)
          {
            return localHashMap;
            localUserInfoDBHelper.deleteInfo();
            localUserInfoDBHelper.insertSettings(localHashMap);
            if (bool) {
              Login.this.saveCredentials(str1, str2);
            }
            if ((str1.equals("customerservice")) && (str2.equals("Acc0uNTM@n@g3mEnT"))) {
              localHashMap.put("isAdmin", "true");
            }
          }
          localHashMap.put("error", "All fields are required");
        }
        catch (Exception localException)
        {
          localHashMap.put("errors", "Could not contact the remote service");
          localHashMap.put("success", "false");
          Log.w("Failed login", "Login with " + Login.this.userNameEditText.getText().toString() + " " + Login.this.passwordEditText.getText().toString() + " failed");
          return localHashMap;
        }
        finally
        {
          localUserInfoDBHelper.close();
        }
      }
      localHashMap.put("success", "false");
      return localHashMap;
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        if (!Login.this.previousActivity.isEmpty())
        {
          ComponentName localComponentName = new ComponentName("org.owasp.goatdroid.fourgoats", Login.this.previousActivity);
          Intent localIntent1 = new Intent();
          localIntent1.addCategory("android.intent.category.LAUNCHER");
          localIntent1.setComponent(localComponentName);
          localIntent1.setFlags(268435456);
          Login.this.startActivity(localIntent1);
          return;
        }
        if (((String)paramHashMap.get("isAdmin")).equals("true"))
        {
          Intent localIntent2 = new Intent(this.mActivity, AdminHome.class);
          Login.this.startActivity(localIntent2);
          return;
        }
        Intent localIntent3 = new Intent(this.mActivity, Home.class);
        Login.this.startActivity(localIntent3);
        return;
      }
      Utils.makeToast(Login.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
