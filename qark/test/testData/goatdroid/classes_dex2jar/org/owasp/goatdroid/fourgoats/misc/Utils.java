package org.owasp.goatdroid.fourgoats.misc;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.widget.Toast;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.HashMap;

public class Utils
{
  public Utils() {}
  
  public static String getCurrentDateTime()
  {
    Calendar localCalendar = Calendar.getInstance();
    return new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(localCalendar.getTime());
  }
  
  public static String getDestinationInfo(Context paramContext)
  {
    SharedPreferences localSharedPreferences = paramContext.getSharedPreferences("destination_info", 1);
    return new StringBuilder(String.valueOf(new StringBuilder(String.valueOf("")).append(localSharedPreferences.getString("host", "")).toString())).append(":").toString() + localSharedPreferences.getString("port", "");
  }
  
  public static HashMap<String, String> getDestinationInfoMap(Context paramContext)
  {
    HashMap localHashMap = new HashMap();
    SharedPreferences localSharedPreferences = paramContext.getSharedPreferences("destination_info", 1);
    localHashMap.put("host", localSharedPreferences.getString("host", ""));
    localHashMap.put("port", localSharedPreferences.getString("port", ""));
    return localHashMap;
  }
  
  public static HashMap<String, String> getProxyMap(Context paramContext)
  {
    HashMap localHashMap = new HashMap();
    SharedPreferences localSharedPreferences = paramContext.getSharedPreferences("proxy_info", 1);
    localHashMap.put("proxyHost", localSharedPreferences.getString("proxyHost", ""));
    localHashMap.put("proxyPort", localSharedPreferences.getString("proxyPort", ""));
    return localHashMap;
  }
  
  public static void makeToast(Context paramContext, String paramString, int paramInt)
  {
    Toast.makeText(paramContext, paramString, paramInt).show();
  }
  
  public static void writeDestinationInfo(Context paramContext, String paramString1, String paramString2)
  {
    SharedPreferences.Editor localEditor = paramContext.getSharedPreferences("destination_info", 1).edit();
    localEditor.putString("host", paramString1);
    localEditor.putString("port", paramString2);
    localEditor.commit();
  }
  
  public static void writeProxyInfo(Context paramContext, String paramString1, String paramString2)
  {
    SharedPreferences.Editor localEditor = paramContext.getSharedPreferences("proxy_info", 1).edit();
    localEditor.putString("proxyHost", paramString1);
    localEditor.putString("proxyPort", paramString2);
    localEditor.commit();
  }
}
