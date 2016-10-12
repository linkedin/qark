package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseUnauthenticatedActivity;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.register.RegisterRequest;

public class Register
  extends BaseUnauthenticatedActivity
{
  Context context;
  
  public Register() {}
  
  public boolean allFieldsCompleted(String paramString1, String paramString2, String paramString3, String paramString4)
  {
    return (!paramString1.equals("")) && (!paramString2.equals("")) && (!paramString3.equals("")) && (!paramString4.equals(""));
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903087);
    this.context = getApplicationContext();
  }
  
  public void submitRegistration(View paramView)
  {
    new RegisterAsyncTask(this).execute(new Void[] { null, null });
  }
  
  private class RegisterAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    Register mActivity;
    
    public RegisterAsyncTask(Register paramRegister)
    {
      this.mActivity = paramRegister;
    }
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      RegisterRequest localRegisterRequest = new RegisterRequest(Register.this.context);
      EditText localEditText1 = (EditText)Register.this.findViewById(2130968665);
      EditText localEditText2 = (EditText)Register.this.findViewById(2130968667);
      EditText localEditText3 = (EditText)Register.this.findViewById(2130968668);
      EditText localEditText4 = (EditText)Register.this.findViewById(2130968669);
      EditText localEditText5 = (EditText)Register.this.findViewById(2130968671);
      String str1 = localEditText1.getText().toString();
      String str2 = localEditText2.getText().toString();
      String str3 = localEditText3.getText().toString();
      String str4 = localEditText4.getText().toString();
      String str5 = localEditText5.getText().toString();
      HashMap localHashMap = new HashMap();
      try
      {
        if (str4.equals(str5))
        {
          if (Register.this.allFieldsCompleted(str1, str2, str3, str4)) {
            return localRegisterRequest.validateRegistration(str1, str2, str3, str4);
          }
          localHashMap.put("errors", "All fields are required");
          localHashMap.put("success", "false");
          return localHashMap;
        }
      }
      catch (Exception localException)
      {
        localHashMap.put("errors", "Could not contact the remote service");
        localHashMap.put("success", "false");
        return localHashMap;
      }
      localHashMap.put("errors", "Passwords didn't match");
      localHashMap.put("success", "false");
      return localHashMap;
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        Utils.makeToast(Register.this.context, "Registration complete!", 1);
        Register.this.launchLogin();
        return;
      }
      Utils.makeToast(this.mActivity, (String)paramHashMap.get("errors"), 1);
    }
  }
}
