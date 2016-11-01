package android.support.v4.content;

public class IntentCompat
{
  public static final String ACTION_EXTERNAL_APPLICATIONS_AVAILABLE = "android.intent.action.EXTERNAL_APPLICATIONS_AVAILABLE";
  public static final String ACTION_EXTERNAL_APPLICATIONS_UNAVAILABLE = "android.intent.action.EXTERNAL_APPLICATIONS_UNAVAILABLE";
  public static final String EXTRA_CHANGED_PACKAGE_LIST = "android.intent.extra.changed_package_list";
  public static final String EXTRA_CHANGED_UID_LIST = "android.intent.extra.changed_uid_list";
  public static final int FLAG_ACTIVITY_CLEAR_TASK = 32768;
  public static final int FLAG_ACTIVITY_TASK_ON_HOME = 16384;
  
  private IntentCompat() {}
}
