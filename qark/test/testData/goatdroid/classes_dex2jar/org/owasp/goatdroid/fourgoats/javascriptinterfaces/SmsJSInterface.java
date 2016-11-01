package org.owasp.goatdroid.fourgoats.javascriptinterfaces;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import org.owasp.goatdroid.fourgoats.activities.SendSMS;

public class SmsJSInterface
  implements Cloneable
{
  Context mContext;
  
  public SmsJSInterface(Context paramContext)
  {
    this.mContext = paramContext;
  }
  
  public void launchSendSMSActivity(String paramString1, String paramString2)
  {
    Intent localIntent = new Intent(this.mContext, SendSMS.class);
    Bundle localBundle = new Bundle();
    localBundle.putString("venueName", paramString1);
    localBundle.putString("dateTime", paramString2);
    localIntent.putExtras(localBundle);
    this.mContext.startActivity(localIntent);
  }
  
  public void sendSMS(String paramString1, String paramString2)
  {
    SmsManager.getDefault().sendTextMessage(paramString1, null, paramString2, null, null);
  }
}
