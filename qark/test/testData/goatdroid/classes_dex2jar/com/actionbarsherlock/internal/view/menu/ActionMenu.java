package com.actionbarsherlock.internal.view.menu;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.res.Resources;
import android.view.KeyEvent;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuItem;
import com.actionbarsherlock.view.SubMenu;
import java.util.ArrayList;
import java.util.List;

public class ActionMenu
  implements Menu
{
  private Context mContext;
  private boolean mIsQwerty;
  private ArrayList<ActionMenuItem> mItems;
  
  public ActionMenu(Context paramContext)
  {
    this.mContext = paramContext;
    this.mItems = new ArrayList();
  }
  
  private int findItemIndex(int paramInt)
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        j = -1;
      }
      while (((ActionMenuItem)localArrayList.get(j)).getItemId() == paramInt) {
        return j;
      }
    }
  }
  
  private ActionMenuItem findItemWithShortcut(int paramInt, KeyEvent paramKeyEvent)
  {
    boolean bool = this.mIsQwerty;
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    int j = 0;
    ActionMenuItem localActionMenuItem;
    if (j >= i) {
      localActionMenuItem = null;
    }
    label77:
    for (;;)
    {
      return localActionMenuItem;
      localActionMenuItem = (ActionMenuItem)localArrayList.get(j);
      if (bool) {}
      for (int k = localActionMenuItem.getAlphabeticShortcut();; k = localActionMenuItem.getNumericShortcut())
      {
        if (paramInt == k) {
          break label77;
        }
        j++;
        break;
      }
    }
  }
  
  public MenuItem add(int paramInt)
  {
    return add(0, 0, 0, paramInt);
  }
  
  public MenuItem add(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    return add(paramInt1, paramInt2, paramInt3, this.mContext.getResources().getString(paramInt4));
  }
  
  public MenuItem add(int paramInt1, int paramInt2, int paramInt3, CharSequence paramCharSequence)
  {
    ActionMenuItem localActionMenuItem = new ActionMenuItem(getContext(), paramInt1, paramInt2, 0, paramInt3, paramCharSequence);
    this.mItems.add(paramInt3, localActionMenuItem);
    return localActionMenuItem;
  }
  
  public MenuItem add(CharSequence paramCharSequence)
  {
    return add(0, 0, 0, paramCharSequence);
  }
  
  public int addIntentOptions(int paramInt1, int paramInt2, int paramInt3, ComponentName paramComponentName, Intent[] paramArrayOfIntent, Intent paramIntent, int paramInt4, MenuItem[] paramArrayOfMenuItem)
  {
    PackageManager localPackageManager = this.mContext.getPackageManager();
    List localList = localPackageManager.queryIntentActivityOptions(paramComponentName, paramArrayOfIntent, paramIntent, 0);
    if (localList != null) {}
    int j;
    for (int i = localList.size();; i = 0)
    {
      if ((paramInt4 & 0x1) == 0) {
        removeGroup(paramInt1);
      }
      j = 0;
      if (j < i) {
        break;
      }
      return i;
    }
    ResolveInfo localResolveInfo = (ResolveInfo)localList.get(j);
    if (localResolveInfo.specificIndex < 0) {}
    for (Intent localIntent1 = paramIntent;; localIntent1 = paramArrayOfIntent[localResolveInfo.specificIndex])
    {
      Intent localIntent2 = new Intent(localIntent1);
      localIntent2.setComponent(new ComponentName(localResolveInfo.activityInfo.applicationInfo.packageName, localResolveInfo.activityInfo.name));
      MenuItem localMenuItem = add(paramInt1, paramInt2, paramInt3, localResolveInfo.loadLabel(localPackageManager)).setIcon(localResolveInfo.loadIcon(localPackageManager)).setIntent(localIntent2);
      if ((paramArrayOfMenuItem != null) && (localResolveInfo.specificIndex >= 0)) {
        paramArrayOfMenuItem[localResolveInfo.specificIndex] = localMenuItem;
      }
      j++;
      break;
    }
  }
  
  public SubMenu addSubMenu(int paramInt)
  {
    return null;
  }
  
  public SubMenu addSubMenu(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    return null;
  }
  
  public SubMenu addSubMenu(int paramInt1, int paramInt2, int paramInt3, CharSequence paramCharSequence)
  {
    return null;
  }
  
  public SubMenu addSubMenu(CharSequence paramCharSequence)
  {
    return null;
  }
  
  public void clear()
  {
    this.mItems.clear();
  }
  
  public void close() {}
  
  public MenuItem findItem(int paramInt)
  {
    return (MenuItem)this.mItems.get(findItemIndex(paramInt));
  }
  
  public Context getContext()
  {
    return this.mContext;
  }
  
  public MenuItem getItem(int paramInt)
  {
    return (MenuItem)this.mItems.get(paramInt);
  }
  
  public boolean hasVisibleItems()
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return false;
      }
      if (((ActionMenuItem)localArrayList.get(j)).isVisible()) {
        return true;
      }
    }
  }
  
  public boolean isShortcutKey(int paramInt, KeyEvent paramKeyEvent)
  {
    return findItemWithShortcut(paramInt, paramKeyEvent) != null;
  }
  
  public boolean performIdentifierAction(int paramInt1, int paramInt2)
  {
    int i = findItemIndex(paramInt1);
    if (i < 0) {
      return false;
    }
    return ((ActionMenuItem)this.mItems.get(i)).invoke();
  }
  
  public boolean performShortcut(int paramInt1, KeyEvent paramKeyEvent, int paramInt2)
  {
    ActionMenuItem localActionMenuItem = findItemWithShortcut(paramInt1, paramKeyEvent);
    if (localActionMenuItem == null) {
      return false;
    }
    return localActionMenuItem.invoke();
  }
  
  public void removeGroup(int paramInt)
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    int j = 0;
    for (;;)
    {
      if (j >= i) {
        return;
      }
      if (((ActionMenuItem)localArrayList.get(j)).getGroupId() == paramInt)
      {
        localArrayList.remove(j);
        i--;
      }
      else
      {
        j++;
      }
    }
  }
  
  public void removeItem(int paramInt)
  {
    this.mItems.remove(findItemIndex(paramInt));
  }
  
  public void setGroupCheckable(int paramInt, boolean paramBoolean1, boolean paramBoolean2)
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      ActionMenuItem localActionMenuItem = (ActionMenuItem)localArrayList.get(j);
      if (localActionMenuItem.getGroupId() == paramInt)
      {
        localActionMenuItem.setCheckable(paramBoolean1);
        localActionMenuItem.setExclusiveCheckable(paramBoolean2);
      }
    }
  }
  
  public void setGroupEnabled(int paramInt, boolean paramBoolean)
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      ActionMenuItem localActionMenuItem = (ActionMenuItem)localArrayList.get(j);
      if (localActionMenuItem.getGroupId() == paramInt) {
        localActionMenuItem.setEnabled(paramBoolean);
      }
    }
  }
  
  public void setGroupVisible(int paramInt, boolean paramBoolean)
  {
    ArrayList localArrayList = this.mItems;
    int i = localArrayList.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      ActionMenuItem localActionMenuItem = (ActionMenuItem)localArrayList.get(j);
      if (localActionMenuItem.getGroupId() == paramInt) {
        localActionMenuItem.setVisible(paramBoolean);
      }
    }
  }
  
  public void setQwertyMode(boolean paramBoolean)
  {
    this.mIsQwerty = paramBoolean;
  }
  
  public int size()
  {
    return this.mItems.size();
  }
}
