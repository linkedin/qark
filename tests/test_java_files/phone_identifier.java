import android.telephony.TelephonyManager;

class Test {
  public static void Test(Context context) {
    TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);

    //Calling the methods of TelephonyManager the returns the information
    String IMEINumber=tm.getDeviceId();
  }
}