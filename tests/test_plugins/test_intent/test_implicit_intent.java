package android.support.v4.content;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import java.util.ArrayList;
import java.util.HashMap;


public class VulnerableTest {
  public void vulnerableMethodGetActivity() {
    PendingIntent b = PendingIntent.getActivity("context", "requestcode", new Intent(), "flags");
  }
  public void vulnerableMethodGetActivities() {
    PendingIntent b = PendingIntent.getActivities("context", "requestcode", new Intent[]{new Intent()}, "flags");
  }
  public void vulnerableMethodGetService() {
    PendingIntent b = PendingIntent.getService("context", "requestcode", new Intent(), "flags");
  }
  public void vulnerableMethodGetBroadcast() {
    PendingIntent b = PendingIntent.getBroadcast("context", "requestcode", new Intent(), "flags");
  }
  public void nonVulnerableMethodGetBroadcast() {
    PendingIntent b = PendingIntent.getBroadcast("context", "requestcode", new Intent(this, VulnerableTest.class), "flags");
  }
}