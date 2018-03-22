class Test {
  public static File[] Test(Context context) {
    File[] roots = context.getExternalFilesDirs("external");
    File roots = context.getExternalFilesDir("external");
    File roots = context.getExternalMediaDirs("external");
    File roots = context.getExternalStoragePublicDirectory("external");
    return roots;
  }
}