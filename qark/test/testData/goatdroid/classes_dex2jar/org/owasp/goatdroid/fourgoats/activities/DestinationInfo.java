package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseUnauthenticatedActivity;
import org.owasp.goatdroid.fourgoats.misc.Utils;

public class DestinationInfo
  extends BaseUnauthenticatedActivity
{
  CheckBox autoCheckin;
  Context context;
  EditText hostEditText;
  CheckBox isPublic;
  EditText portEditText;
  EditText proxyHostEditText;
  EditText proxyPortEditText;
  
  public DestinationInfo() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903070);
    this.context = getApplicationContext();
    HashMap localHashMap1 = Utils.getDestinationInfoMap(this.context);
    HashMap localHashMap2 = Utils.getProxyMap(this.context);
    this.hostEditText = ((EditText)findViewById(2130968634));
    this.portEditText = ((EditText)findViewById(2130968635));
    this.proxyHostEditText = ((EditText)findViewById(2130968636));
    this.proxyPortEditText = ((EditText)findViewById(2130968637));
    this.hostEditText.setText((CharSequence)localHashMap1.get("host"));
    this.portEditText.setText((CharSequence)localHashMap1.get("port"));
    this.proxyHostEditText.setText((CharSequence)localHashMap2.get("proxyHost"));
    this.proxyPortEditText.setText((CharSequence)localHashMap2.get("proxyPort"));
  }
  
  public void saveDestinationInfo(View paramView)
  {
    if ((this.hostEditText.getText().toString().equals("")) || (this.portEditText.getText().toString().equals("")))
    {
      Utils.makeToast(this.context, "All fields are required", 1);
      return;
    }
    Utils.writeDestinationInfo(this.context, this.hostEditText.getText().toString(), this.portEditText.getText().toString());
    Utils.writeProxyInfo(this.context, this.proxyHostEditText.getText().toString(), this.proxyPortEditText.getText().toString());
    Utils.makeToast(this.context, "Now you are ready to use the app!", 1);
    startActivity(new Intent(this, Login.class));
  }
}
