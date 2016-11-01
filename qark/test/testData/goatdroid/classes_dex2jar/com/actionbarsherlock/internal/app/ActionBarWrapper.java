package com.actionbarsherlock.internal.app;

import android.app.Activity;
import android.content.Context;
import android.graphics.drawable.Drawable;
import android.support.v4.app.FragmentManager;
import android.view.View;
import android.widget.SpinnerAdapter;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class ActionBarWrapper
  extends com.actionbarsherlock.app.ActionBar
  implements android.app.ActionBar.OnNavigationListener, android.app.ActionBar.OnMenuVisibilityListener
{
  private final android.app.ActionBar mActionBar;
  private final Activity mActivity;
  private android.support.v4.app.FragmentTransaction mFragmentTransaction;
  private Set<com.actionbarsherlock.app.ActionBar.OnMenuVisibilityListener> mMenuVisibilityListeners = new HashSet(1);
  private com.actionbarsherlock.app.ActionBar.OnNavigationListener mNavigationListener;
  
  public ActionBarWrapper(Activity paramActivity)
  {
    this.mActivity = paramActivity;
    this.mActionBar = paramActivity.getActionBar();
    if (this.mActionBar != null) {
      this.mActionBar.addOnMenuVisibilityListener(this);
    }
  }
  
  public void addOnMenuVisibilityListener(com.actionbarsherlock.app.ActionBar.OnMenuVisibilityListener paramOnMenuVisibilityListener)
  {
    this.mMenuVisibilityListeners.add(paramOnMenuVisibilityListener);
  }
  
  public void addTab(com.actionbarsherlock.app.ActionBar.Tab paramTab)
  {
    this.mActionBar.addTab(((TabWrapper)paramTab).mNativeTab);
  }
  
  public void addTab(com.actionbarsherlock.app.ActionBar.Tab paramTab, int paramInt)
  {
    this.mActionBar.addTab(((TabWrapper)paramTab).mNativeTab, paramInt);
  }
  
  public void addTab(com.actionbarsherlock.app.ActionBar.Tab paramTab, int paramInt, boolean paramBoolean)
  {
    this.mActionBar.addTab(((TabWrapper)paramTab).mNativeTab, paramInt, paramBoolean);
  }
  
  public void addTab(com.actionbarsherlock.app.ActionBar.Tab paramTab, boolean paramBoolean)
  {
    this.mActionBar.addTab(((TabWrapper)paramTab).mNativeTab, paramBoolean);
  }
  
  public View getCustomView()
  {
    return this.mActionBar.getCustomView();
  }
  
  public int getDisplayOptions()
  {
    return this.mActionBar.getDisplayOptions();
  }
  
  public int getHeight()
  {
    return this.mActionBar.getHeight();
  }
  
  public int getNavigationItemCount()
  {
    return this.mActionBar.getNavigationItemCount();
  }
  
  public int getNavigationMode()
  {
    return this.mActionBar.getNavigationMode();
  }
  
  public int getSelectedNavigationIndex()
  {
    return this.mActionBar.getSelectedNavigationIndex();
  }
  
  public com.actionbarsherlock.app.ActionBar.Tab getSelectedTab()
  {
    android.app.ActionBar.Tab localTab = this.mActionBar.getSelectedTab();
    if (localTab != null) {
      return (com.actionbarsherlock.app.ActionBar.Tab)localTab.getTag();
    }
    return null;
  }
  
  public CharSequence getSubtitle()
  {
    return this.mActionBar.getSubtitle();
  }
  
  public com.actionbarsherlock.app.ActionBar.Tab getTabAt(int paramInt)
  {
    android.app.ActionBar.Tab localTab = this.mActionBar.getTabAt(paramInt);
    if (localTab != null) {
      return (com.actionbarsherlock.app.ActionBar.Tab)localTab.getTag();
    }
    return null;
  }
  
  public int getTabCount()
  {
    return this.mActionBar.getTabCount();
  }
  
  public Context getThemedContext()
  {
    return this.mActionBar.getThemedContext();
  }
  
  public CharSequence getTitle()
  {
    return this.mActionBar.getTitle();
  }
  
  public void hide()
  {
    this.mActionBar.hide();
  }
  
  public boolean isShowing()
  {
    return this.mActionBar.isShowing();
  }
  
  public com.actionbarsherlock.app.ActionBar.Tab newTab()
  {
    return new TabWrapper(this.mActionBar.newTab());
  }
  
  public void onMenuVisibilityChanged(boolean paramBoolean)
  {
    Iterator localIterator = this.mMenuVisibilityListeners.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      ((com.actionbarsherlock.app.ActionBar.OnMenuVisibilityListener)localIterator.next()).onMenuVisibilityChanged(paramBoolean);
    }
  }
  
  public boolean onNavigationItemSelected(int paramInt, long paramLong)
  {
    return this.mNavigationListener.onNavigationItemSelected(paramInt, paramLong);
  }
  
  public void removeAllTabs()
  {
    this.mActionBar.removeAllTabs();
  }
  
  public void removeOnMenuVisibilityListener(com.actionbarsherlock.app.ActionBar.OnMenuVisibilityListener paramOnMenuVisibilityListener)
  {
    this.mMenuVisibilityListeners.remove(paramOnMenuVisibilityListener);
  }
  
  public void removeTab(com.actionbarsherlock.app.ActionBar.Tab paramTab)
  {
    this.mActionBar.removeTab(((TabWrapper)paramTab).mNativeTab);
  }
  
  public void removeTabAt(int paramInt)
  {
    this.mActionBar.removeTabAt(paramInt);
  }
  
  public void selectTab(com.actionbarsherlock.app.ActionBar.Tab paramTab)
  {
    this.mActionBar.selectTab(((TabWrapper)paramTab).mNativeTab);
  }
  
  public void setBackgroundDrawable(Drawable paramDrawable)
  {
    this.mActionBar.setBackgroundDrawable(paramDrawable);
  }
  
  public void setCustomView(int paramInt)
  {
    this.mActionBar.setCustomView(paramInt);
  }
  
  public void setCustomView(View paramView)
  {
    this.mActionBar.setCustomView(paramView);
  }
  
  public void setCustomView(View paramView, com.actionbarsherlock.app.ActionBar.LayoutParams paramLayoutParams)
  {
    android.app.ActionBar.LayoutParams localLayoutParams = new android.app.ActionBar.LayoutParams(paramLayoutParams);
    localLayoutParams.gravity = paramLayoutParams.gravity;
    localLayoutParams.bottomMargin = paramLayoutParams.bottomMargin;
    localLayoutParams.topMargin = paramLayoutParams.topMargin;
    localLayoutParams.leftMargin = paramLayoutParams.leftMargin;
    localLayoutParams.rightMargin = paramLayoutParams.rightMargin;
    this.mActionBar.setCustomView(paramView, localLayoutParams);
  }
  
  public void setDisplayHomeAsUpEnabled(boolean paramBoolean)
  {
    this.mActionBar.setDisplayHomeAsUpEnabled(paramBoolean);
  }
  
  public void setDisplayOptions(int paramInt)
  {
    this.mActionBar.setDisplayOptions(paramInt);
  }
  
  public void setDisplayOptions(int paramInt1, int paramInt2)
  {
    this.mActionBar.setDisplayOptions(paramInt1, paramInt2);
  }
  
  public void setDisplayShowCustomEnabled(boolean paramBoolean)
  {
    this.mActionBar.setDisplayShowCustomEnabled(paramBoolean);
  }
  
  public void setDisplayShowHomeEnabled(boolean paramBoolean)
  {
    this.mActionBar.setDisplayShowHomeEnabled(paramBoolean);
  }
  
  public void setDisplayShowTitleEnabled(boolean paramBoolean)
  {
    this.mActionBar.setDisplayShowTitleEnabled(paramBoolean);
  }
  
  public void setDisplayUseLogoEnabled(boolean paramBoolean)
  {
    this.mActionBar.setDisplayUseLogoEnabled(paramBoolean);
  }
  
  public void setHomeButtonEnabled(boolean paramBoolean)
  {
    this.mActionBar.setHomeButtonEnabled(paramBoolean);
  }
  
  public void setIcon(int paramInt)
  {
    this.mActionBar.setIcon(paramInt);
  }
  
  public void setIcon(Drawable paramDrawable)
  {
    this.mActionBar.setIcon(paramDrawable);
  }
  
  public void setListNavigationCallbacks(SpinnerAdapter paramSpinnerAdapter, com.actionbarsherlock.app.ActionBar.OnNavigationListener paramOnNavigationListener)
  {
    this.mNavigationListener = paramOnNavigationListener;
    android.app.ActionBar localActionBar = this.mActionBar;
    if (paramOnNavigationListener != null) {}
    for (;;)
    {
      localActionBar.setListNavigationCallbacks(paramSpinnerAdapter, this);
      return;
      this = null;
    }
  }
  
  public void setLogo(int paramInt)
  {
    this.mActionBar.setLogo(paramInt);
  }
  
  public void setLogo(Drawable paramDrawable)
  {
    this.mActionBar.setLogo(paramDrawable);
  }
  
  public void setNavigationMode(int paramInt)
  {
    this.mActionBar.setNavigationMode(paramInt);
  }
  
  public void setSelectedNavigationItem(int paramInt)
  {
    this.mActionBar.setSelectedNavigationItem(paramInt);
  }
  
  public void setSplitBackgroundDrawable(Drawable paramDrawable)
  {
    this.mActionBar.setSplitBackgroundDrawable(paramDrawable);
  }
  
  public void setStackedBackgroundDrawable(Drawable paramDrawable)
  {
    this.mActionBar.setStackedBackgroundDrawable(paramDrawable);
  }
  
  public void setSubtitle(int paramInt)
  {
    this.mActionBar.setSubtitle(paramInt);
  }
  
  public void setSubtitle(CharSequence paramCharSequence)
  {
    this.mActionBar.setSubtitle(paramCharSequence);
  }
  
  public void setTitle(int paramInt)
  {
    this.mActionBar.setTitle(paramInt);
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    this.mActionBar.setTitle(paramCharSequence);
  }
  
  public void show()
  {
    this.mActionBar.show();
  }
  
  public class TabWrapper
    extends com.actionbarsherlock.app.ActionBar.Tab
    implements android.app.ActionBar.TabListener
  {
    private com.actionbarsherlock.app.ActionBar.TabListener mListener;
    final android.app.ActionBar.Tab mNativeTab;
    private Object mTag;
    
    public TabWrapper(android.app.ActionBar.Tab paramTab)
    {
      this.mNativeTab = paramTab;
      this.mNativeTab.setTag(this);
    }
    
    public CharSequence getContentDescription()
    {
      return this.mNativeTab.getContentDescription();
    }
    
    public View getCustomView()
    {
      return this.mNativeTab.getCustomView();
    }
    
    public Drawable getIcon()
    {
      return this.mNativeTab.getIcon();
    }
    
    public int getPosition()
    {
      return this.mNativeTab.getPosition();
    }
    
    public Object getTag()
    {
      return this.mTag;
    }
    
    public CharSequence getText()
    {
      return this.mNativeTab.getText();
    }
    
    public void onTabReselected(android.app.ActionBar.Tab paramTab, android.app.FragmentTransaction paramFragmentTransaction)
    {
      if (this.mListener != null)
      {
        boolean bool = ActionBarWrapper.this.mActivity instanceof SherlockFragmentActivity;
        android.support.v4.app.FragmentTransaction localFragmentTransaction = null;
        if (bool) {
          localFragmentTransaction = ((SherlockFragmentActivity)ActionBarWrapper.this.mActivity).getSupportFragmentManager().beginTransaction().disallowAddToBackStack();
        }
        this.mListener.onTabReselected(this, localFragmentTransaction);
        if ((localFragmentTransaction != null) && (!localFragmentTransaction.isEmpty())) {
          localFragmentTransaction.commit();
        }
      }
    }
    
    public void onTabSelected(android.app.ActionBar.Tab paramTab, android.app.FragmentTransaction paramFragmentTransaction)
    {
      if (this.mListener != null)
      {
        if ((ActionBarWrapper.this.mFragmentTransaction == null) && ((ActionBarWrapper.this.mActivity instanceof SherlockFragmentActivity))) {
          ActionBarWrapper.this.mFragmentTransaction = ((SherlockFragmentActivity)ActionBarWrapper.this.mActivity).getSupportFragmentManager().beginTransaction().disallowAddToBackStack();
        }
        this.mListener.onTabSelected(this, ActionBarWrapper.this.mFragmentTransaction);
        if (ActionBarWrapper.this.mFragmentTransaction != null)
        {
          if (!ActionBarWrapper.this.mFragmentTransaction.isEmpty()) {
            ActionBarWrapper.this.mFragmentTransaction.commit();
          }
          ActionBarWrapper.this.mFragmentTransaction = null;
        }
      }
    }
    
    public void onTabUnselected(android.app.ActionBar.Tab paramTab, android.app.FragmentTransaction paramFragmentTransaction)
    {
      if (this.mListener != null)
      {
        boolean bool = ActionBarWrapper.this.mActivity instanceof SherlockFragmentActivity;
        android.support.v4.app.FragmentTransaction localFragmentTransaction = null;
        if (bool)
        {
          localFragmentTransaction = ((SherlockFragmentActivity)ActionBarWrapper.this.mActivity).getSupportFragmentManager().beginTransaction().disallowAddToBackStack();
          ActionBarWrapper.this.mFragmentTransaction = localFragmentTransaction;
        }
        this.mListener.onTabUnselected(this, localFragmentTransaction);
      }
    }
    
    public void select()
    {
      this.mNativeTab.select();
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setContentDescription(int paramInt)
    {
      this.mNativeTab.setContentDescription(paramInt);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setContentDescription(CharSequence paramCharSequence)
    {
      this.mNativeTab.setContentDescription(paramCharSequence);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setCustomView(int paramInt)
    {
      this.mNativeTab.setCustomView(paramInt);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setCustomView(View paramView)
    {
      this.mNativeTab.setCustomView(paramView);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setIcon(int paramInt)
    {
      this.mNativeTab.setIcon(paramInt);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setIcon(Drawable paramDrawable)
    {
      this.mNativeTab.setIcon(paramDrawable);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setTabListener(com.actionbarsherlock.app.ActionBar.TabListener paramTabListener)
    {
      android.app.ActionBar.Tab localTab = this.mNativeTab;
      if (paramTabListener != null) {}
      for (TabWrapper localTabWrapper = this;; localTabWrapper = null)
      {
        localTab.setTabListener(localTabWrapper);
        this.mListener = paramTabListener;
        return this;
      }
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setTag(Object paramObject)
    {
      this.mTag = paramObject;
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setText(int paramInt)
    {
      this.mNativeTab.setText(paramInt);
      return this;
    }
    
    public com.actionbarsherlock.app.ActionBar.Tab setText(CharSequence paramCharSequence)
    {
      this.mNativeTab.setText(paramCharSequence);
      return this;
    }
  }
}
