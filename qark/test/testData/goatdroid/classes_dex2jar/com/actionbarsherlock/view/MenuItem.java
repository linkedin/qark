package com.actionbarsherlock.view;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.View;

public abstract interface MenuItem
{
  public static final int SHOW_AS_ACTION_ALWAYS = 2;
  public static final int SHOW_AS_ACTION_COLLAPSE_ACTION_VIEW = 8;
  public static final int SHOW_AS_ACTION_IF_ROOM = 1;
  public static final int SHOW_AS_ACTION_NEVER = 0;
  public static final int SHOW_AS_ACTION_WITH_TEXT = 4;
  
  public abstract boolean collapseActionView();
  
  public abstract boolean expandActionView();
  
  public abstract ActionProvider getActionProvider();
  
  public abstract View getActionView();
  
  public abstract char getAlphabeticShortcut();
  
  public abstract int getGroupId();
  
  public abstract Drawable getIcon();
  
  public abstract Intent getIntent();
  
  public abstract int getItemId();
  
  public abstract ContextMenu.ContextMenuInfo getMenuInfo();
  
  public abstract char getNumericShortcut();
  
  public abstract int getOrder();
  
  public abstract SubMenu getSubMenu();
  
  public abstract CharSequence getTitle();
  
  public abstract CharSequence getTitleCondensed();
  
  public abstract boolean hasSubMenu();
  
  public abstract boolean isActionViewExpanded();
  
  public abstract boolean isCheckable();
  
  public abstract boolean isChecked();
  
  public abstract boolean isEnabled();
  
  public abstract boolean isVisible();
  
  public abstract MenuItem setActionProvider(ActionProvider paramActionProvider);
  
  public abstract MenuItem setActionView(int paramInt);
  
  public abstract MenuItem setActionView(View paramView);
  
  public abstract MenuItem setAlphabeticShortcut(char paramChar);
  
  public abstract MenuItem setCheckable(boolean paramBoolean);
  
  public abstract MenuItem setChecked(boolean paramBoolean);
  
  public abstract MenuItem setEnabled(boolean paramBoolean);
  
  public abstract MenuItem setIcon(int paramInt);
  
  public abstract MenuItem setIcon(Drawable paramDrawable);
  
  public abstract MenuItem setIntent(Intent paramIntent);
  
  public abstract MenuItem setNumericShortcut(char paramChar);
  
  public abstract MenuItem setOnActionExpandListener(OnActionExpandListener paramOnActionExpandListener);
  
  public abstract MenuItem setOnMenuItemClickListener(OnMenuItemClickListener paramOnMenuItemClickListener);
  
  public abstract MenuItem setShortcut(char paramChar1, char paramChar2);
  
  public abstract void setShowAsAction(int paramInt);
  
  public abstract MenuItem setShowAsActionFlags(int paramInt);
  
  public abstract MenuItem setTitle(int paramInt);
  
  public abstract MenuItem setTitle(CharSequence paramCharSequence);
  
  public abstract MenuItem setTitleCondensed(CharSequence paramCharSequence);
  
  public abstract MenuItem setVisible(boolean paramBoolean);
  
  public static abstract interface OnActionExpandListener
  {
    public abstract boolean onMenuItemActionCollapse(MenuItem paramMenuItem);
    
    public abstract boolean onMenuItemActionExpand(MenuItem paramMenuItem);
  }
  
  public static abstract interface OnMenuItemClickListener
  {
    public abstract boolean onMenuItemClick(MenuItem paramMenuItem);
  }
}
