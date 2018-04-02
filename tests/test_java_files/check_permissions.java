import android.content.Context;

class Test {
  public static void Test(Context context) {
    context.checkCallingOrSelfPermission();
    context.enforceCallingOrSelfPermission();
  }
}