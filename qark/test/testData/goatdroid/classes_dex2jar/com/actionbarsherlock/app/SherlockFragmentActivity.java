package com.actionbarsherlock.app;

import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app._ActionBarSherlockTrojanHorse;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup.LayoutParams;
import com.actionbarsherlock.ActionBarSherlock;
import com.actionbarsherlock.ActionBarSherlock.OnActionModeFinishedListener;
import com.actionbarsherlock.ActionBarSherlock.OnActionModeStartedListener;
import com.actionbarsherlock.view.ActionMode;
import com.actionbarsherlock.view.ActionMode.Callback;
import com.actionbarsherlock.view.MenuInflater;

public class SherlockFragmentActivity
  extends _ActionBarSherlockTrojanHorse
  implements ActionBarSherlock.OnActionModeStartedListener, ActionBarSherlock.OnActionModeFinishedListener
{
  private static final boolean DEBUG = false;
  private static final String TAG = "SherlockFragmentActivity";
  private boolean mIgnoreNativeCreate = false;
  private boolean mIgnoreNativePrepare = false;
  private boolean mIgnoreNativeSelected = false;
  private ActionBarSherlock mSherlock;
  
  public SherlockFragmentActivity() {}
  
  public void addContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    getSherlock().addContentView(paramView, paramLayoutParams);
  }
  
  public void closeOptionsMenu()
  {
    if (!getSherlock().dispatchCloseOptionsMenu()) {
      super.closeOptionsMenu();
    }
  }
  
  public boolean dispatchKeyEvent(KeyEvent paramKeyEvent)
  {
    if (getSherlock().dispatchKeyEvent(paramKeyEvent)) {
      return true;
    }
    return super.dispatchKeyEvent(paramKeyEvent);
  }
  
  protected final ActionBarSherlock getSherlock()
  {
    if (this.mSherlock == null) {
      this.mSherlock = ActionBarSherlock.wrap(this, 1);
    }
    return this.mSherlock;
  }
  
  public ActionBar getSupportActionBar()
  {
    return getSherlock().getActionBar();
  }
  
  public MenuInflater getSupportMenuInflater()
  {
    return getSherlock().getMenuInflater();
  }
  
  public void invalidateOptionsMenu()
  {
    getSherlock().dispatchInvalidateOptionsMenu();
  }
  
  public void onActionModeFinished(ActionMode paramActionMode) {}
  
  public void onActionModeStarted(ActionMode paramActionMode) {}
  
  public void onConfigurationChanged(Configuration paramConfiguration)
  {
    super.onConfigurationChanged(paramConfiguration);
    getSherlock().dispatchConfigurationChanged(paramConfiguration);
  }
  
  public final boolean onCreateOptionsMenu(android.view.Menu paramMenu)
  {
    return true;
  }
  
  public boolean onCreateOptionsMenu(com.actionbarsherlock.view.Menu paramMenu)
  {
    return true;
  }
  
  public final boolean onCreatePanelMenu(int paramInt, android.view.Menu paramMenu)
  {
    if ((paramInt == 0) && (!this.mIgnoreNativeCreate))
    {
      this.mIgnoreNativeCreate = true;
      boolean bool = getSherlock().dispatchCreateOptionsMenu(paramMenu);
      this.mIgnoreNativeCreate = false;
      return bool;
    }
    return super.onCreatePanelMenu(paramInt, paramMenu);
  }
  
  protected void onDestroy()
  {
    getSherlock().dispatchDestroy();
    super.onDestroy();
  }
  
  public final boolean onMenuItemSelected(int paramInt, android.view.MenuItem paramMenuItem)
  {
    if ((paramInt == 0) && (!this.mIgnoreNativeSelected))
    {
      this.mIgnoreNativeSelected = true;
      boolean bool = getSherlock().dispatchOptionsItemSelected(paramMenuItem);
      this.mIgnoreNativeSelected = false;
      return bool;
    }
    return super.onMenuItemSelected(paramInt, paramMenuItem);
  }
  
  public final boolean onMenuOpened(int paramInt, android.view.Menu paramMenu)
  {
    if (getSherlock().dispatchMenuOpened(paramInt, paramMenu)) {
      return true;
    }
    return super.onMenuOpened(paramInt, paramMenu);
  }
  
  public final boolean onOptionsItemSelected(android.view.MenuItem paramMenuItem)
  {
    return false;
  }
  
  public boolean onOptionsItemSelected(com.actionbarsherlock.view.MenuItem paramMenuItem)
  {
    return false;
  }
  
  public void onPanelClosed(int paramInt, android.view.Menu paramMenu)
  {
    getSherlock().dispatchPanelClosed(paramInt, paramMenu);
    super.onPanelClosed(paramInt, paramMenu);
  }
  
  protected void onPause()
  {
    getSherlock().dispatchPause();
    super.onPause();
  }
  
  protected void onPostCreate(Bundle paramBundle)
  {
    getSherlock().dispatchPostCreate(paramBundle);
    super.onPostCreate(paramBundle);
  }
  
  protected void onPostResume()
  {
    super.onPostResume();
    getSherlock().dispatchPostResume();
  }
  
  public final boolean onPrepareOptionsMenu(android.view.Menu paramMenu)
  {
    return true;
  }
  
  public boolean onPrepareOptionsMenu(com.actionbarsherlock.view.Menu paramMenu)
  {
    return true;
  }
  
  public final boolean onPreparePanel(int paramInt, View paramView, android.view.Menu paramMenu)
  {
    if ((paramInt == 0) && (!this.mIgnoreNativePrepare))
    {
      this.mIgnoreNativePrepare = true;
      boolean bool = getSherlock().dispatchPrepareOptionsMenu(paramMenu);
      this.mIgnoreNativePrepare = false;
      return bool;
    }
    return super.onPreparePanel(paramInt, paramView, paramMenu);
  }
  
  protected void onStop()
  {
    getSherlock().dispatchStop();
    super.onStop();
  }
  
  protected void onTitleChanged(CharSequence paramCharSequence, int paramInt)
  {
    getSherlock().dispatchTitleChanged(paramCharSequence, paramInt);
    super.onTitleChanged(paramCharSequence, paramInt);
  }
  
  public void openOptionsMenu()
  {
    if (!getSherlock().dispatchOpenOptionsMenu()) {
      super.openOptionsMenu();
    }
  }
  
  public void requestWindowFeature(long paramLong)
  {
    getSherlock().requestFeature((int)paramLong);
  }
  
  public void setContentView(int paramInt)
  {
    getSherlock().setContentView(paramInt);
  }
  
  public void setContentView(View paramView)
  {
    getSherlock().setContentView(paramView);
  }
  
  public void setContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    getSherlock().setContentView(paramView, paramLayoutParams);
  }
  
  public void setSupportProgress(int paramInt)
  {
    getSherlock().setProgress(paramInt);
  }
  
  public void setSupportProgressBarIndeterminate(boolean paramBoolean)
  {
    getSherlock().setProgressBarIndeterminate(paramBoolean);
  }
  
  public void setSupportProgressBarIndeterminateVisibility(boolean paramBoolean)
  {
    getSherlock().setProgressBarIndeterminateVisibility(paramBoolean);
  }
  
  public void setSupportProgressBarVisibility(boolean paramBoolean)
  {
    getSherlock().setProgressBarVisibility(paramBoolean);
  }
  
  public void setSupportSecondaryProgress(int paramInt)
  {
    getSherlock().setSecondaryProgress(paramInt);
  }
  
  public ActionMode startActionMode(ActionMode.Callback paramCallback)
  {
    return getSherlock().startActionMode(paramCallback);
  }
  
  public void supportInvalidateOptionsMenu()
  {
    invalidateOptionsMenu();
  }
}
