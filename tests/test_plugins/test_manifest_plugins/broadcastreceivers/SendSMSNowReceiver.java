package test_plugins.test_manifest_plugins.broadcastreceivers;

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
    paramContext = SmsManager.getDefault();
    paramIntent = paramIntent.getExtras();
    paramContext.sendTextMessage(paramIntent.getString("phoneNumber"), null, paramIntent.getString("message"), null, null);
    Utils.makeToast(this.context, "Your text message has been sent!", 1);
  }
}