package com.actionbarsherlock.internal.view.menu;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.View;
import com.actionbarsherlock.internal.view.ActionProviderWrapper;
import com.actionbarsherlock.view.SubMenu;

public class MenuItemWrapper
  implements com.actionbarsherlock.view.MenuItem, android.view.MenuItem.OnMenuItemClickListener
{
  private com.actionbarsherlock.view.MenuItem.OnActionExpandListener mActionExpandListener = null;
  private com.actionbarsherlock.view.MenuItem.OnMenuItemClickListener mMenuItemClickListener = null;
  private android.view.MenuItem.OnActionExpandListener mNativeActionExpandListener = null;
  private final android.view.MenuItem mNativeItem;
  private SubMenu mSubMenu = null;
  
  public MenuItemWrapper(android.view.MenuItem paramMenuItem)
  {
    if (paramMenuItem == null) {
      throw new IllegalStateException("Wrapped menu item cannot be null.");
    }
    this.mNativeItem = paramMenuItem;
  }
  
  public boolean collapseActionView()
  {
    return this.mNativeItem.collapseActionView();
  }
  
  public boolean expandActionView()
  {
    return this.mNativeItem.expandActionView();
  }
  
  public com.actionbarsherlock.view.ActionProvider getActionProvider()
  {
    android.view.ActionProvider localActionProvider = this.mNativeItem.getActionProvider();
    if ((localActionProvider != null) && ((localActionProvider instanceof ActionProviderWrapper))) {
      return ((ActionProviderWrapper)localActionProvider).unwrap();
    }
    return null;
  }
  
  public View getActionView()
  {
    return this.mNativeItem.getActionView();
  }
  
  public char getAlphabeticShortcut()
  {
    return this.mNativeItem.getAlphabeticShortcut();
  }
  
  public int getGroupId()
  {
    return this.mNativeItem.getGroupId();
  }
  
  public Drawable getIcon()
  {
    return this.mNativeItem.getIcon();
  }
  
  public Intent getIntent()
  {
    return this.mNativeItem.getIntent();
  }
  
  public int getItemId()
  {
    return this.mNativeItem.getItemId();
  }
  
  public ContextMenu.ContextMenuInfo getMenuInfo()
  {
    return this.mNativeItem.getMenuInfo();
  }
  
  public char getNumericShortcut()
  {
    return this.mNativeItem.getNumericShortcut();
  }
  
  public int getOrder()
  {
    return this.mNativeItem.getOrder();
  }
  
  public SubMenu getSubMenu()
  {
    if ((hasSubMenu()) && (this.mSubMenu == null)) {
      this.mSubMenu = new SubMenuWrapper(this.mNativeItem.getSubMenu());
    }
    return this.mSubMenu;
  }
  
  public CharSequence getTitle()
  {
    return this.mNativeItem.getTitle();
  }
  
  public CharSequence getTitleCondensed()
  {
    return this.mNativeItem.getTitleCondensed();
  }
  
  public boolean hasSubMenu()
  {
    return this.mNativeItem.hasSubMenu();
  }
  
  public boolean isActionViewExpanded()
  {
    return this.mNativeItem.isActionViewExpanded();
  }
  
  public boolean isCheckable()
  {
    return this.mNativeItem.isCheckable();
  }
  
  public boolean isChecked()
  {
    return this.mNativeItem.isChecked();
  }
  
  public boolean isEnabled()
  {
    return this.mNativeItem.isEnabled();
  }
  
  public boolean isVisible()
  {
    return this.mNativeItem.isVisible();
  }
  
  public boolean onMenuItemClick(android.view.MenuItem paramMenuItem)
  {
    if (this.mMenuItemClickListener != null) {
      return this.mMenuItemClickListener.onMenuItemClick(this);
    }
    return false;
  }
  
  public com.actionbarsherlock.view.MenuItem setActionProvider(com.actionbarsherlock.view.ActionProvider paramActionProvider)
  {
    this.mNativeItem.setActionProvider(new ActionProviderWrapper(paramActionProvider));
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setActionView(int paramInt)
  {
    this.mNativeItem.setActionView(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setActionView(View paramView)
  {
    this.mNativeItem.setActionView(paramView);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setAlphabeticShortcut(char paramChar)
  {
    this.mNativeItem.setAlphabeticShortcut(paramChar);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setCheckable(boolean paramBoolean)
  {
    this.mNativeItem.setCheckable(paramBoolean);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setChecked(boolean paramBoolean)
  {
    this.mNativeItem.setChecked(paramBoolean);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setEnabled(boolean paramBoolean)
  {
    this.mNativeItem.setEnabled(paramBoolean);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setIcon(int paramInt)
  {
    this.mNativeItem.setIcon(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setIcon(Drawable paramDrawable)
  {
    this.mNativeItem.setIcon(paramDrawable);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setIntent(Intent paramIntent)
  {
    this.mNativeItem.setIntent(paramIntent);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setNumericShortcut(char paramChar)
  {
    this.mNativeItem.setNumericShortcut(paramChar);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setOnActionExpandListener(com.actionbarsherlock.view.MenuItem.OnActionExpandListener paramOnActionExpandListener)
  {
    this.mActionExpandListener = paramOnActionExpandListener;
    if (this.mNativeActionExpandListener == null)
    {
      this.mNativeActionExpandListener = new android.view.MenuItem.OnActionExpandListener()
      {
        public boolean onMenuItemActionCollapse(android.view.MenuItem paramAnonymousMenuItem)
        {
          if (MenuItemWrapper.this.mActionExpandListener != null) {
            return MenuItemWrapper.this.mActionExpandListener.onMenuItemActionCollapse(MenuItemWrapper.this);
          }
          return false;
        }
        
        public boolean onMenuItemActionExpand(android.view.MenuItem paramAnonymousMenuItem)
        {
          if (MenuItemWrapper.this.mActionExpandListener != null) {
            return MenuItemWrapper.this.mActionExpandListener.onMenuItemActionExpand(MenuItemWrapper.this);
          }
          return false;
        }
      };
      this.mNativeItem.setOnActionExpandListener(this.mNativeActionExpandListener);
    }
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setOnMenuItemClickListener(com.actionbarsherlock.view.MenuItem.OnMenuItemClickListener paramOnMenuItemClickListener)
  {
    this.mMenuItemClickListener = paramOnMenuItemClickListener;
    this.mNativeItem.setOnMenuItemClickListener(this);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setShortcut(char paramChar1, char paramChar2)
  {
    this.mNativeItem.setShortcut(paramChar1, paramChar2);
    return this;
  }
  
  public void setShowAsAction(int paramInt)
  {
    this.mNativeItem.setShowAsAction(paramInt);
  }
  
  public com.actionbarsherlock.view.MenuItem setShowAsActionFlags(int paramInt)
  {
    this.mNativeItem.setShowAsActionFlags(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setTitle(int paramInt)
  {
    this.mNativeItem.setTitle(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setTitle(CharSequence paramCharSequence)
  {
    this.mNativeItem.setTitle(paramCharSequence);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setTitleCondensed(CharSequence paramCharSequence)
  {
    this.mNativeItem.setTitleCondensed(paramCharSequence);
    return this;
  }
  
  public com.actionbarsherlock.view.MenuItem setVisible(boolean paramBoolean)
  {
    this.mNativeItem.setVisible(paramBoolean);
    return this;
  }
}
