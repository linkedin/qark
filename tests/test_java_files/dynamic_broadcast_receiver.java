class RegisterReceiver {
  public void Test(Context context, Calendar c) {
    final String SOME_ACTION = "com.android.action.MyAction.SomeAction";
    IntentFilter intentFilter = new IntentFilter(SOME_ACTION);
    Receiver mReceiver = new Receiver();
    context.registerReceiver(mReceiver, intentFilter);
  }
}
