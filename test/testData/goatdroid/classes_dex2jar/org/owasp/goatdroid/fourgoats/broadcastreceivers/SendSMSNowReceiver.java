package org.owasp.goatdroid.fourgoats.broadcastreceivers;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsManager;
import org.owasp.goatdroid.fourgoats.misc.Utils;

public class SendSMSNowReceiver
  extends BroadcastReceiver
{
  Context context;
  
  public SendSMSNowReceiver() {}
  
  public void onReceive(Context paramContext, Intent paramIntent)
  {
    this.context = paramContext;
    SmsManager localSmsManager = SmsManager.getDefault();
    Bundle localBundle = paramIntent.getExtras();
    localSmsManager.sendTextMessage(localBundle.getString("phoneNumber"), null, localBundle.getString("message"), null, null);
    Utils.makeToast(this.context, "Your text message has been sent!", 1);
  }
}
