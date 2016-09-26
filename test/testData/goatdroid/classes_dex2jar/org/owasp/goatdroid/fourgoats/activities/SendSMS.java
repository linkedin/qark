package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.misc.Utils;

public class SendSMS
  extends BaseActivity
{
  Bundle bundle;
  Context context;
  EditText phoneNumberEditText;
  EditText smsMessageEditText;
  
  public SendSMS() {}
  
  public boolean areFieldsCompleted()
  {
    return (!this.phoneNumberEditText.getText().toString().equals("")) && (!this.smsMessageEditText.getText().toString().equals(""));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903092);
    this.context = getApplicationContext();
    this.bundle = getIntent().getExtras();
    this.phoneNumberEditText = ((EditText)findViewById(2130968675));
    this.smsMessageEditText = ((EditText)findViewById(2130968676));
    this.smsMessageEditText.setText("I checked in at " + this.bundle.getString("venueName") + " on " + this.bundle.getString("dateTime"));
  }
  
  public void sendSMS(View paramView)
  {
    SmsManager localSmsManager = SmsManager.getDefault();
    if (areFieldsCompleted())
    {
      localSmsManager.sendTextMessage(this.phoneNumberEditText.getText().toString(), null, this.smsMessageEditText.getText().toString(), null, null);
      Utils.makeToast(this.context, "Your text message has been sent!", 1);
      return;
    }
    Utils.makeToast(this.context, "All fields are required", 1);
  }
}
