package com.actionbarsherlock.internal.view.menu;

import android.graphics.drawable.Drawable;
import android.view.View;
import com.actionbarsherlock.view.MenuItem;

public class SubMenuWrapper
  extends MenuWrapper
  implements com.actionbarsherlock.view.SubMenu
{
  private MenuItem mItem = null;
  private final android.view.SubMenu mNativeSubMenu;
  
  public SubMenuWrapper(android.view.SubMenu paramSubMenu)
  {
    super(paramSubMenu);
    this.mNativeSubMenu = paramSubMenu;
  }
  
  public void clearHeader()
  {
    this.mNativeSubMenu.clearHeader();
  }
  
  public MenuItem getItem()
  {
    if (this.mItem == null) {
      this.mItem = new MenuItemWrapper(this.mNativeSubMenu.getItem());
    }
    return this.mItem;
  }
  
  public com.actionbarsherlock.view.SubMenu setHeaderIcon(int paramInt)
  {
    this.mNativeSubMenu.setHeaderIcon(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setHeaderIcon(Drawable paramDrawable)
  {
    this.mNativeSubMenu.setHeaderIcon(paramDrawable);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setHeaderTitle(int paramInt)
  {
    this.mNativeSubMenu.setHeaderTitle(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setHeaderTitle(CharSequence paramCharSequence)
  {
    this.mNativeSubMenu.setHeaderTitle(paramCharSequence);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setHeaderView(View paramView)
  {
    this.mNativeSubMenu.setHeaderView(paramView);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setIcon(int paramInt)
  {
    this.mNativeSubMenu.setIcon(paramInt);
    return this;
  }
  
  public com.actionbarsherlock.view.SubMenu setIcon(Drawable paramDrawable)
  {
    this.mNativeSubMenu.setIcon(paramDrawable);
    return this;
  }
}
