class ExampleReadable{
  public static void main(){
    SharedPreferences preference = context.getContext()
        .getSharedPreferences(Context.MODE_WORLD_READABLE);
  }
}
class ExampleWritable{
  public static void main(){
    SharedPreferences preference = context.getContext()
        .getSharedPreferences(Context.MODE_WORLD_WRITEABLE);
  }
}
class ExampleNonVulnerable{
  public static void main(){
    SharedPreferences preference = context.getContext()
        .getSharedPreferences(Context.MODE_WRITEABLE);
  }
}
class ExampleCommented{
  public static void main(){
    /* SharedPreferences preference = context.getContext()
        .getSharedPreferences(Context.MODE_WRITEABLE);
    */
  }
}
