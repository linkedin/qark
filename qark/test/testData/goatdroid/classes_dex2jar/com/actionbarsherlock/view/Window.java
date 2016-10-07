package com.actionbarsherlock.view;

import android.content.Context;

public abstract class Window
  extends android.view.Window
{
  public static final long FEATURE_ACTION_BAR = 8L;
  public static final long FEATURE_ACTION_BAR_OVERLAY = 9L;
  public static final long FEATURE_ACTION_MODE_OVERLAY = 10L;
  public static final long FEATURE_INDETERMINATE_PROGRESS = 5L;
  public static final long FEATURE_NO_TITLE = 1L;
  public static final long FEATURE_PROGRESS = 2L;
  
  private Window(Context paramContext)
  {
    super(paramContext);
  }
  
  public static abstract interface Callback
  {
    public abstract boolean onMenuItemSelected(int paramInt, MenuItem paramMenuItem);
  }
}
