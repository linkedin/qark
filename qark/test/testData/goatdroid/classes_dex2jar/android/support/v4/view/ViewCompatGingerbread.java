package android.support.v4.view;

import android.view.View;

class ViewCompatGingerbread
{
  ViewCompatGingerbread() {}
  
  public static int getOverScrollMode(View paramView)
  {
    return paramView.getOverScrollMode();
  }
  
  public static void setOverScrollMode(View paramView, int paramInt)
  {
    paramView.setOverScrollMode(paramInt);
  }
}
