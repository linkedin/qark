package com.actionbarsherlock.internal;

import android.app.Activity;
import android.content.Context;
import android.content.res.Resources.Theme;
import android.util.TypedValue;
import android.view.ContextThemeWrapper;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import android.view.Window;
import com.actionbarsherlock.ActionBarSherlock;
import com.actionbarsherlock.ActionBarSherlock.Implementation;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.internal.app.ActionBarWrapper;
import com.actionbarsherlock.internal.view.menu.MenuWrapper;
import com.actionbarsherlock.view.MenuInflater;

@ActionBarSherlock.Implementation(api=14)
public class ActionBarSherlockNative
  extends ActionBarSherlock
{
  private ActionBarWrapper mActionBar;
  private ActionModeWrapper mActionMode;
  private MenuWrapper mMenu;
  
  public ActionBarSherlockNative(Activity paramActivity, int paramInt)
  {
    super(paramActivity, paramInt);
  }
  
  private void initActionBar()
  {
    if ((this.mActionBar != null) || (this.mActivity.getActionBar() == null)) {
      return;
    }
    this.mActionBar = new ActionBarWrapper(this.mActivity);
  }
  
  public void addContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    this.mActivity.getWindow().addContentView(paramView, paramLayoutParams);
    initActionBar();
  }
  
  public boolean dispatchCreateOptionsMenu(Menu paramMenu)
  {
    if ((this.mMenu == null) || (paramMenu != this.mMenu.unwrap())) {
      this.mMenu = new MenuWrapper(paramMenu);
    }
    return callbackCreateOptionsMenu(this.mMenu);
  }
  
  public void dispatchInvalidateOptionsMenu()
  {
    this.mActivity.getWindow().invalidatePanelMenu(0);
  }
  
  public boolean dispatchOptionsItemSelected(MenuItem paramMenuItem)
  {
    return callbackOptionsItemSelected(this.mMenu.findItem(paramMenuItem));
  }
  
  public boolean dispatchPrepareOptionsMenu(Menu paramMenu)
  {
    return callbackPrepareOptionsMenu(this.mMenu);
  }
  
  public ActionBar getActionBar()
  {
    initActionBar();
    return this.mActionBar;
  }
  
  protected Context getThemedContext()
  {
    Object localObject = this.mActivity;
    TypedValue localTypedValue = new TypedValue();
    this.mActivity.getTheme().resolveAttribute(16843671, localTypedValue, true);
    if (localTypedValue.resourceId != 0) {
      localObject = new ContextThemeWrapper((Context)localObject, localTypedValue.resourceId);
    }
    return localObject;
  }
  
  public boolean hasFeature(int paramInt)
  {
    return this.mActivity.getWindow().hasFeature(paramInt);
  }
  
  public boolean requestFeature(int paramInt)
  {
    return this.mActivity.getWindow().requestFeature(paramInt);
  }
  
  public void setContentView(int paramInt)
  {
    this.mActivity.getWindow().setContentView(paramInt);
    initActionBar();
  }
  
  public void setContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    this.mActivity.getWindow().setContentView(paramView, paramLayoutParams);
    initActionBar();
  }
  
  public void setProgress(int paramInt)
  {
    this.mActivity.setProgress(paramInt);
  }
  
  public void setProgressBarIndeterminate(boolean paramBoolean)
  {
    this.mActivity.setProgressBarIndeterminate(paramBoolean);
  }
  
  public void setProgressBarIndeterminateVisibility(boolean paramBoolean)
  {
    this.mActivity.setProgressBarIndeterminateVisibility(paramBoolean);
  }
  
  public void setProgressBarVisibility(boolean paramBoolean)
  {
    this.mActivity.setProgressBarVisibility(paramBoolean);
  }
  
  public void setSecondaryProgress(int paramInt)
  {
    this.mActivity.setSecondaryProgress(paramInt);
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    this.mActivity.getWindow().setTitle(paramCharSequence);
  }
  
  public void setUiOptions(int paramInt)
  {
    this.mActivity.getWindow().setUiOptions(paramInt);
  }
  
  public void setUiOptions(int paramInt1, int paramInt2)
  {
    this.mActivity.getWindow().setUiOptions(paramInt1, paramInt2);
  }
  
  public com.actionbarsherlock.view.ActionMode startActionMode(com.actionbarsherlock.view.ActionMode.Callback paramCallback)
  {
    if (this.mActionMode != null) {
      this.mActionMode.finish();
    }
    ActionModeCallbackWrapper localActionModeCallbackWrapper = null;
    if (paramCallback != null) {
      localActionModeCallbackWrapper = new ActionModeCallbackWrapper(paramCallback);
    }
    this.mActivity.startActionMode(localActionModeCallbackWrapper);
    return this.mActionMode;
  }
  
  private class ActionModeCallbackWrapper
    implements android.view.ActionMode.Callback
  {
    private final com.actionbarsherlock.view.ActionMode.Callback mCallback;
    
    public ActionModeCallbackWrapper(com.actionbarsherlock.view.ActionMode.Callback paramCallback)
    {
      this.mCallback = paramCallback;
    }
    
    public boolean onActionItemClicked(android.view.ActionMode paramActionMode, MenuItem paramMenuItem)
    {
      return this.mCallback.onActionItemClicked(ActionBarSherlockNative.this.mActionMode, ActionBarSherlockNative.this.mActionMode.getMenu().findItem(paramMenuItem));
    }
    
    public boolean onCreateActionMode(android.view.ActionMode paramActionMode, Menu paramMenu)
    {
      ActionBarSherlockNative.this.mActionMode = new ActionBarSherlockNative.ActionModeWrapper(ActionBarSherlockNative.this, paramActionMode);
      return this.mCallback.onCreateActionMode(ActionBarSherlockNative.this.mActionMode, ActionBarSherlockNative.this.mActionMode.getMenu());
    }
    
    public void onDestroyActionMode(android.view.ActionMode paramActionMode)
    {
      this.mCallback.onDestroyActionMode(ActionBarSherlockNative.this.mActionMode);
    }
    
    public boolean onPrepareActionMode(android.view.ActionMode paramActionMode, Menu paramMenu)
    {
      return this.mCallback.onPrepareActionMode(ActionBarSherlockNative.this.mActionMode, ActionBarSherlockNative.this.mActionMode.getMenu());
    }
  }
  
  private class ActionModeWrapper
    extends com.actionbarsherlock.view.ActionMode
  {
    private final android.view.ActionMode mActionMode;
    private MenuWrapper mMenu = null;
    
    ActionModeWrapper(android.view.ActionMode paramActionMode)
    {
      this.mActionMode = paramActionMode;
    }
    
    public void finish()
    {
      this.mActionMode.finish();
    }
    
    public View getCustomView()
    {
      return this.mActionMode.getCustomView();
    }
    
    public MenuWrapper getMenu()
    {
      if (this.mMenu == null) {
        this.mMenu = new MenuWrapper(this.mActionMode.getMenu());
      }
      return this.mMenu;
    }
    
    public MenuInflater getMenuInflater()
    {
      return ActionBarSherlockNative.this.getMenuInflater();
    }
    
    public CharSequence getSubtitle()
    {
      return this.mActionMode.getSubtitle();
    }
    
    public Object getTag()
    {
      return this.mActionMode.getTag();
    }
    
    public CharSequence getTitle()
    {
      return this.mActionMode.getTitle();
    }
    
    public void invalidate()
    {
      this.mActionMode.invalidate();
    }
    
    public void setCustomView(View paramView)
    {
      this.mActionMode.setCustomView(paramView);
    }
    
    public void setSubtitle(int paramInt)
    {
      this.mActionMode.setSubtitle(paramInt);
    }
    
    public void setSubtitle(CharSequence paramCharSequence)
    {
      this.mActionMode.setSubtitle(paramCharSequence);
    }
    
    public void setTag(Object paramObject)
    {
      this.mActionMode.setTag(paramObject);
    }
    
    public void setTitle(int paramInt)
    {
      this.mActionMode.setTitle(paramInt);
    }
    
    public void setTitle(CharSequence paramCharSequence)
    {
      this.mActionMode.setTitle(paramCharSequence);
    }
  }
}
