package android.support.v4.view;

import android.os.Build.VERSION;
import android.view.MenuItem;
import android.view.View;

public class MenuItemCompat
{
  static final MenuVersionImpl IMPL = new BaseMenuVersionImpl();
  public static final int SHOW_AS_ACTION_ALWAYS = 2;
  public static final int SHOW_AS_ACTION_COLLAPSE_ACTION_VIEW = 8;
  public static final int SHOW_AS_ACTION_IF_ROOM = 1;
  public static final int SHOW_AS_ACTION_NEVER = 0;
  public static final int SHOW_AS_ACTION_WITH_TEXT = 4;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      IMPL = new HoneycombMenuVersionImpl();
      return;
    }
  }
  
  public MenuItemCompat() {}
  
  public static MenuItem setActionView(MenuItem paramMenuItem, View paramView)
  {
    return IMPL.setActionView(paramMenuItem, paramView);
  }
  
  public static boolean setShowAsAction(MenuItem paramMenuItem, int paramInt)
  {
    return IMPL.setShowAsAction(paramMenuItem, paramInt);
  }
  
  static class BaseMenuVersionImpl
    implements MenuItemCompat.MenuVersionImpl
  {
    BaseMenuVersionImpl() {}
    
    public MenuItem setActionView(MenuItem paramMenuItem, View paramView)
    {
      return paramMenuItem;
    }
    
    public boolean setShowAsAction(MenuItem paramMenuItem, int paramInt)
    {
      return false;
    }
  }
  
  static class HoneycombMenuVersionImpl
    implements MenuItemCompat.MenuVersionImpl
  {
    HoneycombMenuVersionImpl() {}
    
    public MenuItem setActionView(MenuItem paramMenuItem, View paramView)
    {
      return MenuItemCompatHoneycomb.setActionView(paramMenuItem, paramView);
    }
    
    public boolean setShowAsAction(MenuItem paramMenuItem, int paramInt)
    {
      MenuItemCompatHoneycomb.setShowAsAction(paramMenuItem, paramInt);
      return true;
    }
  }
  
  static abstract interface MenuVersionImpl
  {
    public abstract MenuItem setActionView(MenuItem paramMenuItem, View paramView);
    
    public abstract boolean setShowAsAction(MenuItem paramMenuItem, int paramInt);
  }
}
