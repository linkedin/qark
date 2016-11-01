package android.support.v4.app;

import android.app.Activity;
import android.content.Intent;
import android.os.Build.VERSION;

public class ActivityCompat
{
  public ActivityCompat() {}
  
  public static boolean invalidateOptionsMenu(Activity paramActivity)
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      ActivityCompatHoneycomb.invalidateOptionsMenu(paramActivity);
      return true;
    }
    return false;
  }
  
  public static boolean startActivities(Activity paramActivity, Intent[] paramArrayOfIntent)
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      ActivityCompatHoneycomb.startActivities(paramActivity, paramArrayOfIntent);
      return true;
    }
    return false;
  }
}
