package com.actionbarsherlock.internal.widget;

import android.view.View;

final class IcsView
{
  private IcsView() {}
  
  public static int getMeasuredStateInt(View paramView)
  {
    return 0xFF000000 & paramView.getMeasuredWidth() | 0xFF00 & paramView.getMeasuredHeight() >> 16;
  }
}
