package com.actionbarsherlock.internal.view.menu;

import android.content.Context;
import android.os.Build.VERSION;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import java.util.ArrayList;

public abstract class BaseMenuPresenter
  implements MenuPresenter
{
  private static final boolean IS_HONEYCOMB;
  private MenuPresenter.Callback mCallback;
  protected Context mContext;
  private int mId;
  protected LayoutInflater mInflater;
  private int mItemLayoutRes;
  protected MenuBuilder mMenu;
  private int mMenuLayoutRes;
  protected MenuView mMenuView;
  protected Context mSystemContext;
  protected LayoutInflater mSystemInflater;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11) {}
    for (boolean bool = true;; bool = false)
    {
      IS_HONEYCOMB = bool;
      return;
    }
  }
  
  public BaseMenuPresenter(Context paramContext, int paramInt1, int paramInt2)
  {
    this.mSystemContext = paramContext;
    this.mSystemInflater = LayoutInflater.from(paramContext);
    this.mMenuLayoutRes = paramInt1;
    this.mItemLayoutRes = paramInt2;
  }
  
  protected void addItemView(View paramView, int paramInt)
  {
    ViewGroup localViewGroup = (ViewGroup)paramView.getParent();
    if (localViewGroup != null) {
      localViewGroup.removeView(paramView);
    }
    ((ViewGroup)this.mMenuView).addView(paramView, paramInt);
  }
  
  public abstract void bindItemView(MenuItemImpl paramMenuItemImpl, MenuView.ItemView paramItemView);
  
  public boolean collapseItemActionView(MenuBuilder paramMenuBuilder, MenuItemImpl paramMenuItemImpl)
  {
    return false;
  }
  
  public MenuView.ItemView createItemView(ViewGroup paramViewGroup)
  {
    return (MenuView.ItemView)this.mSystemInflater.inflate(this.mItemLayoutRes, paramViewGroup, false);
  }
  
  public boolean expandItemActionView(MenuBuilder paramMenuBuilder, MenuItemImpl paramMenuItemImpl)
  {
    return false;
  }
  
  protected boolean filterLeftoverView(ViewGroup paramViewGroup, int paramInt)
  {
    paramViewGroup.removeViewAt(paramInt);
    return true;
  }
  
  public boolean flagActionItems()
  {
    return false;
  }
  
  public int getId()
  {
    return this.mId;
  }
  
  public View getItemView(MenuItemImpl paramMenuItemImpl, View paramView, ViewGroup paramViewGroup)
  {
    if ((paramView instanceof MenuView.ItemView)) {}
    for (MenuView.ItemView localItemView = (MenuView.ItemView)paramView;; localItemView = createItemView(paramViewGroup))
    {
      bindItemView(paramMenuItemImpl, localItemView);
      return (View)localItemView;
    }
  }
  
  public MenuView getMenuView(ViewGroup paramViewGroup)
  {
    if (this.mMenuView == null)
    {
      this.mMenuView = ((MenuView)this.mSystemInflater.inflate(this.mMenuLayoutRes, paramViewGroup, false));
      this.mMenuView.initialize(this.mMenu);
      updateMenuView(true);
    }
    return this.mMenuView;
  }
  
  public void initForMenu(Context paramContext, MenuBuilder paramMenuBuilder)
  {
    this.mContext = paramContext;
    this.mInflater = LayoutInflater.from(this.mContext);
    this.mMenu = paramMenuBuilder;
  }
  
  public void onCloseMenu(MenuBuilder paramMenuBuilder, boolean paramBoolean)
  {
    if (this.mCallback != null) {
      this.mCallback.onCloseMenu(paramMenuBuilder, paramBoolean);
    }
  }
  
  public boolean onSubMenuSelected(SubMenuBuilder paramSubMenuBuilder)
  {
    if (this.mCallback != null) {
      return this.mCallback.onOpenSubMenu(paramSubMenuBuilder);
    }
    return false;
  }
  
  public void setCallback(MenuPresenter.Callback paramCallback)
  {
    this.mCallback = paramCallback;
  }
  
  public void setId(int paramInt)
  {
    this.mId = paramInt;
  }
  
  public boolean shouldIncludeItem(int paramInt, MenuItemImpl paramMenuItemImpl)
  {
    return true;
  }
  
  public void updateMenuView(boolean paramBoolean)
  {
    ViewGroup localViewGroup = (ViewGroup)this.mMenuView;
    if (localViewGroup == null) {}
    int i;
    ArrayList localArrayList;
    int k;
    for (;;)
    {
      return;
      MenuBuilder localMenuBuilder = this.mMenu;
      i = 0;
      if (localMenuBuilder != null)
      {
        this.mMenu.flagActionItems();
        localArrayList = this.mMenu.getVisibleItems();
        int j = localArrayList.size();
        k = 0;
        if (k < j) {
          break;
        }
      }
      else
      {
        while (i < localViewGroup.getChildCount()) {
          if (!filterLeftoverView(localViewGroup, i)) {
            i++;
          }
        }
      }
    }
    MenuItemImpl localMenuItemImpl1 = (MenuItemImpl)localArrayList.get(k);
    View localView1;
    if (shouldIncludeItem(i, localMenuItemImpl1))
    {
      localView1 = localViewGroup.getChildAt(i);
      if (!(localView1 instanceof MenuView.ItemView)) {
        break label193;
      }
    }
    label193:
    for (MenuItemImpl localMenuItemImpl2 = ((MenuView.ItemView)localView1).getItemData();; localMenuItemImpl2 = null)
    {
      View localView2 = getItemView(localMenuItemImpl1, localView1, localViewGroup);
      if (localMenuItemImpl1 != localMenuItemImpl2)
      {
        localView2.setPressed(false);
        if (IS_HONEYCOMB) {
          localView2.jumpDrawablesToCurrentState();
        }
      }
      if (localView2 != localView1) {
        addItemView(localView2, i);
      }
      i++;
      k++;
      break;
    }
  }
}
