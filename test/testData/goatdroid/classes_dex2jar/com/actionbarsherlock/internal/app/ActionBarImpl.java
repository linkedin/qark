package com.actionbarsherlock.internal.app;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.res.Configuration;
import android.content.res.Resources;
import android.content.res.Resources.Theme;
import android.graphics.drawable.Drawable;
import android.os.Build.VERSION;
import android.os.Handler;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.util.TypedValue;
import android.view.ContextThemeWrapper;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Window;
import android.widget.SpinnerAdapter;
import com.actionbarsherlock.R.attr;
import com.actionbarsherlock.R.bool;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.LayoutParams;
import com.actionbarsherlock.app.ActionBar.OnMenuVisibilityListener;
import com.actionbarsherlock.app.ActionBar.OnNavigationListener;
import com.actionbarsherlock.app.ActionBar.Tab;
import com.actionbarsherlock.app.ActionBar.TabListener;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.internal.ResourcesCompat;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator.AnimatorListener;
import com.actionbarsherlock.internal.nineoldandroids.animation.AnimatorListenerAdapter;
import com.actionbarsherlock.internal.nineoldandroids.animation.AnimatorSet;
import com.actionbarsherlock.internal.nineoldandroids.animation.AnimatorSet.Builder;
import com.actionbarsherlock.internal.nineoldandroids.animation.ObjectAnimator;
import com.actionbarsherlock.internal.nineoldandroids.widget.NineFrameLayout;
import com.actionbarsherlock.internal.view.menu.MenuBuilder;
import com.actionbarsherlock.internal.view.menu.MenuBuilder.Callback;
import com.actionbarsherlock.internal.view.menu.MenuPopupHelper;
import com.actionbarsherlock.internal.view.menu.SubMenuBuilder;
import com.actionbarsherlock.internal.widget.ActionBarContainer;
import com.actionbarsherlock.internal.widget.ActionBarContextView;
import com.actionbarsherlock.internal.widget.ActionBarView;
import com.actionbarsherlock.internal.widget.ScrollingTabContainerView;
import com.actionbarsherlock.view.ActionMode;
import com.actionbarsherlock.view.ActionMode.Callback;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuInflater;
import com.actionbarsherlock.view.MenuItem;
import java.lang.ref.WeakReference;
import java.util.ArrayList;

public class ActionBarImpl
  extends ActionBar
{
  private static final int CONTEXT_DISPLAY_NORMAL = 0;
  private static final int CONTEXT_DISPLAY_SPLIT = 1;
  private static final int INVALID_POSITION = -1;
  ActionModeImpl mActionMode;
  private ActionBarView mActionView;
  private Activity mActivity;
  private ActionBarContainer mContainerView;
  private NineFrameLayout mContentView;
  private Context mContext;
  private int mContextDisplayMode;
  private ActionBarContextView mContextView;
  private Animator mCurrentModeAnim;
  private Animator mCurrentShowAnim;
  ActionMode mDeferredDestroyActionMode;
  ActionMode.Callback mDeferredModeDestroyCallback;
  final Handler mHandler = new Handler();
  private boolean mHasEmbeddedTabs;
  final Animator.AnimatorListener mHideListener = new AnimatorListenerAdapter()
  {
    public void onAnimationEnd(Animator paramAnonymousAnimator)
    {
      if (ActionBarImpl.this.mContentView != null)
      {
        ActionBarImpl.this.mContentView.setTranslationY(0.0F);
        ActionBarImpl.this.mContainerView.setTranslationY(0.0F);
      }
      if ((ActionBarImpl.this.mSplitView != null) && (ActionBarImpl.this.mContextDisplayMode == 1)) {
        ActionBarImpl.this.mSplitView.setVisibility(8);
      }
      ActionBarImpl.this.mContainerView.setVisibility(8);
      ActionBarImpl.this.mContainerView.setTransitioning(false);
      ActionBarImpl.this.mCurrentShowAnim = null;
      ActionBarImpl.this.completeDeferredDestroyActionMode();
    }
  };
  private boolean mLastMenuVisibility;
  private ArrayList<ActionBar.OnMenuVisibilityListener> mMenuVisibilityListeners = new ArrayList();
  private int mSavedTabPosition = -1;
  private TabImpl mSelectedTab;
  private boolean mShowHideAnimationEnabled;
  final Animator.AnimatorListener mShowListener = new AnimatorListenerAdapter()
  {
    public void onAnimationEnd(Animator paramAnonymousAnimator)
    {
      ActionBarImpl.this.mCurrentShowAnim = null;
      ActionBarImpl.this.mContainerView.requestLayout();
    }
  };
  private ActionBarContainer mSplitView;
  private ScrollingTabContainerView mTabScrollView;
  Runnable mTabSelector;
  private ArrayList<TabImpl> mTabs = new ArrayList();
  private Context mThemedContext;
  boolean mWasHiddenBeforeMode;
  
  public ActionBarImpl(Activity paramActivity, int paramInt)
  {
    this.mActivity = paramActivity;
    View localView = paramActivity.getWindow().getDecorView();
    init(localView);
    if ((paramInt & 0x200) == 0) {
      this.mContentView = ((NineFrameLayout)localView.findViewById(16908290));
    }
  }
  
  public ActionBarImpl(Dialog paramDialog)
  {
    init(paramDialog.getWindow().getDecorView());
  }
  
  private void cleanupTabs()
  {
    if (this.mSelectedTab != null) {
      selectTab(null);
    }
    this.mTabs.clear();
    if (this.mTabScrollView != null) {
      this.mTabScrollView.removeAllTabs();
    }
    this.mSavedTabPosition = -1;
  }
  
  private void configureTab(ActionBar.Tab paramTab, int paramInt)
  {
    TabImpl localTabImpl = (TabImpl)paramTab;
    if (localTabImpl.getCallback() == null) {
      throw new IllegalStateException("Action Bar Tab must have a Callback");
    }
    localTabImpl.setPosition(paramInt);
    this.mTabs.add(paramInt, localTabImpl);
    int i = this.mTabs.size();
    for (int j = paramInt + 1;; j++)
    {
      if (j >= i) {
        return;
      }
      ((TabImpl)this.mTabs.get(j)).setPosition(j);
    }
  }
  
  private void ensureTabsExist()
  {
    if (this.mTabScrollView != null) {
      return;
    }
    ScrollingTabContainerView localScrollingTabContainerView = new ScrollingTabContainerView(this.mContext);
    if (this.mHasEmbeddedTabs)
    {
      localScrollingTabContainerView.setVisibility(0);
      this.mActionView.setEmbeddedTabView(localScrollingTabContainerView);
      this.mTabScrollView = localScrollingTabContainerView;
      return;
    }
    int i = getNavigationMode();
    int j = 0;
    if (i == 2) {}
    for (;;)
    {
      localScrollingTabContainerView.setVisibility(j);
      this.mContainerView.setTabContainer(localScrollingTabContainerView);
      break;
      j = 8;
    }
  }
  
  private void init(View paramView)
  {
    int i = 1;
    this.mContext = paramView.getContext();
    this.mActionView = ((ActionBarView)paramView.findViewById(R.id.abs__action_bar));
    this.mContextView = ((ActionBarContextView)paramView.findViewById(R.id.abs__action_context_bar));
    this.mContainerView = ((ActionBarContainer)paramView.findViewById(R.id.abs__action_bar_container));
    this.mSplitView = ((ActionBarContainer)paramView.findViewById(R.id.abs__split_action_bar));
    if ((this.mActionView == null) || (this.mContextView == null) || (this.mContainerView == null)) {
      throw new IllegalStateException(getClass().getSimpleName() + " can only be used " + "with a compatible window decor layout");
    }
    this.mActionView.setContextView(this.mContextView);
    int j;
    if (this.mActionView.isSplitActionBar())
    {
      j = i;
      this.mContextDisplayMode = j;
      if (this.mContext.getApplicationInfo().targetSdkVersion >= 14) {
        break label195;
      }
    }
    for (;;)
    {
      setHomeButtonEnabled(i);
      setHasEmbeddedTabs(ResourcesCompat.getResources_getBoolean(this.mContext, R.bool.abs__action_bar_embed_tabs));
      return;
      j = 0;
      break;
      label195:
      i = 0;
    }
  }
  
  private void setHasEmbeddedTabs(boolean paramBoolean)
  {
    boolean bool1 = true;
    this.mHasEmbeddedTabs = paramBoolean;
    boolean bool2;
    label43:
    int i;
    label63:
    ActionBarView localActionBarView;
    if (!this.mHasEmbeddedTabs)
    {
      this.mActionView.setEmbeddedTabView(null);
      this.mContainerView.setTabContainer(this.mTabScrollView);
      if (getNavigationMode() != 2) {
        break label116;
      }
      bool2 = bool1;
      if (this.mTabScrollView != null)
      {
        ScrollingTabContainerView localScrollingTabContainerView = this.mTabScrollView;
        if (!bool2) {
          break label121;
        }
        i = 0;
        localScrollingTabContainerView.setVisibility(i);
      }
      localActionBarView = this.mActionView;
      if ((this.mHasEmbeddedTabs) || (!bool2)) {
        break label128;
      }
    }
    for (;;)
    {
      localActionBarView.setCollapsable(bool1);
      return;
      this.mContainerView.setTabContainer(null);
      this.mActionView.setEmbeddedTabView(this.mTabScrollView);
      break;
      label116:
      bool2 = false;
      break label43;
      label121:
      i = 8;
      break label63;
      label128:
      bool1 = false;
    }
  }
  
  public void addOnMenuVisibilityListener(ActionBar.OnMenuVisibilityListener paramOnMenuVisibilityListener)
  {
    this.mMenuVisibilityListeners.add(paramOnMenuVisibilityListener);
  }
  
  public void addTab(ActionBar.Tab paramTab)
  {
    addTab(paramTab, this.mTabs.isEmpty());
  }
  
  public void addTab(ActionBar.Tab paramTab, int paramInt)
  {
    addTab(paramTab, paramInt, this.mTabs.isEmpty());
  }
  
  public void addTab(ActionBar.Tab paramTab, int paramInt, boolean paramBoolean)
  {
    ensureTabsExist();
    this.mTabScrollView.addTab(paramTab, paramInt, paramBoolean);
    configureTab(paramTab, paramInt);
    if (paramBoolean) {
      selectTab(paramTab);
    }
  }
  
  public void addTab(ActionBar.Tab paramTab, boolean paramBoolean)
  {
    ensureTabsExist();
    this.mTabScrollView.addTab(paramTab, paramBoolean);
    configureTab(paramTab, this.mTabs.size());
    if (paramBoolean) {
      selectTab(paramTab);
    }
  }
  
  void animateToMode(boolean paramBoolean)
  {
    int i = 8;
    if (paramBoolean) {
      show(false);
    }
    if (this.mCurrentModeAnim != null) {
      this.mCurrentModeAnim.end();
    }
    ActionBarView localActionBarView = this.mActionView;
    int j;
    int k;
    label57:
    ScrollingTabContainerView localScrollingTabContainerView;
    if (paramBoolean)
    {
      j = i;
      localActionBarView.animateToVisibility(j);
      ActionBarContextView localActionBarContextView = this.mContextView;
      if (!paramBoolean) {
        break label114;
      }
      k = 0;
      localActionBarContextView.animateToVisibility(k);
      if ((this.mTabScrollView != null) && (!this.mActionView.hasEmbeddedTabs()) && (this.mActionView.isCollapsed()))
      {
        localScrollingTabContainerView = this.mTabScrollView;
        if (!paramBoolean) {
          break label120;
        }
      }
    }
    for (;;)
    {
      localScrollingTabContainerView.animateToVisibility(i);
      return;
      j = 0;
      break;
      label114:
      k = i;
      break label57;
      label120:
      i = 0;
    }
  }
  
  void completeDeferredDestroyActionMode()
  {
    if (this.mDeferredModeDestroyCallback != null)
    {
      this.mDeferredModeDestroyCallback.onDestroyActionMode(this.mDeferredDestroyActionMode);
      this.mDeferredDestroyActionMode = null;
      this.mDeferredModeDestroyCallback = null;
    }
  }
  
  public void dispatchMenuVisibilityChanged(boolean paramBoolean)
  {
    if (paramBoolean == this.mLastMenuVisibility) {}
    for (;;)
    {
      return;
      this.mLastMenuVisibility = paramBoolean;
      int i = this.mMenuVisibilityListeners.size();
      for (int j = 0; j < i; j++) {
        ((ActionBar.OnMenuVisibilityListener)this.mMenuVisibilityListeners.get(j)).onMenuVisibilityChanged(paramBoolean);
      }
    }
  }
  
  public View getCustomView()
  {
    return this.mActionView.getCustomNavigationView();
  }
  
  public int getDisplayOptions()
  {
    return this.mActionView.getDisplayOptions();
  }
  
  public int getHeight()
  {
    return this.mContainerView.getHeight();
  }
  
  public int getNavigationItemCount()
  {
    switch (this.mActionView.getNavigationMode())
    {
    }
    SpinnerAdapter localSpinnerAdapter;
    do
    {
      return 0;
      return this.mTabs.size();
      localSpinnerAdapter = this.mActionView.getDropdownAdapter();
    } while (localSpinnerAdapter == null);
    return localSpinnerAdapter.getCount();
  }
  
  public int getNavigationMode()
  {
    return this.mActionView.getNavigationMode();
  }
  
  public int getSelectedNavigationIndex()
  {
    switch (this.mActionView.getNavigationMode())
    {
    default: 
    case 2: 
      do
      {
        return -1;
      } while (this.mSelectedTab == null);
      return this.mSelectedTab.getPosition();
    }
    return this.mActionView.getDropdownSelectedPosition();
  }
  
  public ActionBar.Tab getSelectedTab()
  {
    return this.mSelectedTab;
  }
  
  public CharSequence getSubtitle()
  {
    return this.mActionView.getSubtitle();
  }
  
  public ActionBar.Tab getTabAt(int paramInt)
  {
    return (ActionBar.Tab)this.mTabs.get(paramInt);
  }
  
  public int getTabCount()
  {
    return this.mTabs.size();
  }
  
  public Context getThemedContext()
  {
    int i;
    if (this.mThemedContext == null)
    {
      TypedValue localTypedValue = new TypedValue();
      this.mContext.getTheme().resolveAttribute(R.attr.actionBarWidgetTheme, localTypedValue, true);
      i = localTypedValue.resourceId;
      if (i == 0) {
        break label61;
      }
    }
    label61:
    for (this.mThemedContext = new ContextThemeWrapper(this.mContext, i);; this.mThemedContext = this.mContext) {
      return this.mThemedContext;
    }
  }
  
  public CharSequence getTitle()
  {
    return this.mActionView.getTitle();
  }
  
  public void hide()
  {
    if (this.mCurrentShowAnim != null) {
      this.mCurrentShowAnim.end();
    }
    if (this.mContainerView.getVisibility() == 8) {
      return;
    }
    if (this.mShowHideAnimationEnabled)
    {
      this.mContainerView.setAlpha(1.0F);
      this.mContainerView.setTransitioning(true);
      AnimatorSet localAnimatorSet = new AnimatorSet();
      AnimatorSet.Builder localBuilder = localAnimatorSet.play(ObjectAnimator.ofFloat(this.mContainerView, "alpha", new float[] { 0.0F }));
      if (this.mContentView != null)
      {
        NineFrameLayout localNineFrameLayout = this.mContentView;
        float[] arrayOfFloat1 = new float[2];
        arrayOfFloat1[0] = 0.0F;
        arrayOfFloat1[1] = (-this.mContainerView.getHeight());
        localBuilder.with(ObjectAnimator.ofFloat(localNineFrameLayout, "translationY", arrayOfFloat1));
        ActionBarContainer localActionBarContainer = this.mContainerView;
        float[] arrayOfFloat2 = new float[1];
        arrayOfFloat2[0] = (-this.mContainerView.getHeight());
        localBuilder.with(ObjectAnimator.ofFloat(localActionBarContainer, "translationY", arrayOfFloat2));
      }
      if ((this.mSplitView != null) && (this.mSplitView.getVisibility() == 0))
      {
        this.mSplitView.setAlpha(1.0F);
        localBuilder.with(ObjectAnimator.ofFloat(this.mSplitView, "alpha", new float[] { 0.0F }));
      }
      localAnimatorSet.addListener(this.mHideListener);
      this.mCurrentShowAnim = localAnimatorSet;
      localAnimatorSet.start();
      return;
    }
    this.mHideListener.onAnimationEnd(null);
  }
  
  public boolean isShowing()
  {
    return this.mContainerView.getVisibility() == 0;
  }
  
  public ActionBar.Tab newTab()
  {
    return new TabImpl();
  }
  
  public void onConfigurationChanged(Configuration paramConfiguration)
  {
    setHasEmbeddedTabs(ResourcesCompat.getResources_getBoolean(this.mContext, R.bool.abs__action_bar_embed_tabs));
    if (Build.VERSION.SDK_INT < 8)
    {
      this.mActionView.onConfigurationChanged(paramConfiguration);
      if (this.mContextView != null) {
        this.mContextView.onConfigurationChanged(paramConfiguration);
      }
    }
  }
  
  public void removeAllTabs()
  {
    cleanupTabs();
  }
  
  public void removeOnMenuVisibilityListener(ActionBar.OnMenuVisibilityListener paramOnMenuVisibilityListener)
  {
    this.mMenuVisibilityListeners.remove(paramOnMenuVisibilityListener);
  }
  
  public void removeTab(ActionBar.Tab paramTab)
  {
    removeTabAt(paramTab.getPosition());
  }
  
  public void removeTabAt(int paramInt)
  {
    if (this.mTabScrollView == null) {}
    int i;
    int k;
    label64:
    do
    {
      return;
      if (this.mSelectedTab == null) {
        break;
      }
      i = this.mSelectedTab.getPosition();
      this.mTabScrollView.removeTabAt(paramInt);
      TabImpl localTabImpl = (TabImpl)this.mTabs.remove(paramInt);
      if (localTabImpl != null) {
        localTabImpl.setPosition(-1);
      }
      int j = this.mTabs.size();
      k = paramInt;
      if (k < j) {
        break label104;
      }
    } while (i != paramInt);
    if (this.mTabs.isEmpty()) {}
    for (Object localObject = null;; localObject = (TabImpl)this.mTabs.get(Math.max(0, paramInt - 1)))
    {
      selectTab((ActionBar.Tab)localObject);
      return;
      i = this.mSavedTabPosition;
      break;
      label104:
      ((TabImpl)this.mTabs.get(k)).setPosition(k);
      k++;
      break label64;
    }
  }
  
  public void selectTab(ActionBar.Tab paramTab)
  {
    int i = -1;
    int j;
    if (getNavigationMode() != 2) {
      if (paramTab != null)
      {
        j = paramTab.getPosition();
        this.mSavedTabPosition = j;
      }
    }
    for (;;)
    {
      return;
      j = i;
      break;
      boolean bool = this.mActivity instanceof SherlockFragmentActivity;
      FragmentTransaction localFragmentTransaction = null;
      if (bool) {
        localFragmentTransaction = ((SherlockFragmentActivity)this.mActivity).getSupportFragmentManager().beginTransaction().disallowAddToBackStack();
      }
      if (this.mSelectedTab == paramTab) {
        if (this.mSelectedTab != null)
        {
          this.mSelectedTab.getCallback().onTabReselected(this.mSelectedTab, localFragmentTransaction);
          this.mTabScrollView.animateToTab(paramTab.getPosition());
        }
      }
      while ((localFragmentTransaction != null) && (!localFragmentTransaction.isEmpty()))
      {
        localFragmentTransaction.commit();
        return;
        ScrollingTabContainerView localScrollingTabContainerView = this.mTabScrollView;
        if (paramTab != null) {
          i = paramTab.getPosition();
        }
        localScrollingTabContainerView.setTabSelected(i);
        if (this.mSelectedTab != null) {
          this.mSelectedTab.getCallback().onTabUnselected(this.mSelectedTab, localFragmentTransaction);
        }
        this.mSelectedTab = ((TabImpl)paramTab);
        if (this.mSelectedTab != null) {
          this.mSelectedTab.getCallback().onTabSelected(this.mSelectedTab, localFragmentTransaction);
        }
      }
    }
  }
  
  public void setBackgroundDrawable(Drawable paramDrawable)
  {
    this.mContainerView.setPrimaryBackground(paramDrawable);
  }
  
  public void setCustomView(int paramInt)
  {
    setCustomView(LayoutInflater.from(getThemedContext()).inflate(paramInt, this.mActionView, false));
  }
  
  public void setCustomView(View paramView)
  {
    this.mActionView.setCustomNavigationView(paramView);
  }
  
  public void setCustomView(View paramView, ActionBar.LayoutParams paramLayoutParams)
  {
    paramView.setLayoutParams(paramLayoutParams);
    this.mActionView.setCustomNavigationView(paramView);
  }
  
  public void setDisplayHomeAsUpEnabled(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = 4;; i = 0)
    {
      setDisplayOptions(i, 4);
      return;
    }
  }
  
  public void setDisplayOptions(int paramInt)
  {
    this.mActionView.setDisplayOptions(paramInt);
  }
  
  public void setDisplayOptions(int paramInt1, int paramInt2)
  {
    int i = this.mActionView.getDisplayOptions();
    this.mActionView.setDisplayOptions(paramInt1 & paramInt2 | i & (paramInt2 ^ 0xFFFFFFFF));
  }
  
  public void setDisplayShowCustomEnabled(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = 16;; i = 0)
    {
      setDisplayOptions(i, 16);
      return;
    }
  }
  
  public void setDisplayShowHomeEnabled(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = 2;; i = 0)
    {
      setDisplayOptions(i, 2);
      return;
    }
  }
  
  public void setDisplayShowTitleEnabled(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = 8;; i = 0)
    {
      setDisplayOptions(i, 8);
      return;
    }
  }
  
  public void setDisplayUseLogoEnabled(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = 1;; i = 0)
    {
      setDisplayOptions(i, 1);
      return;
    }
  }
  
  public void setHomeButtonEnabled(boolean paramBoolean)
  {
    this.mActionView.setHomeButtonEnabled(paramBoolean);
  }
  
  public void setIcon(int paramInt)
  {
    this.mActionView.setIcon(paramInt);
  }
  
  public void setIcon(Drawable paramDrawable)
  {
    this.mActionView.setIcon(paramDrawable);
  }
  
  public void setListNavigationCallbacks(SpinnerAdapter paramSpinnerAdapter, ActionBar.OnNavigationListener paramOnNavigationListener)
  {
    this.mActionView.setDropdownAdapter(paramSpinnerAdapter);
    this.mActionView.setCallback(paramOnNavigationListener);
  }
  
  public void setLogo(int paramInt)
  {
    this.mActionView.setLogo(paramInt);
  }
  
  public void setLogo(Drawable paramDrawable)
  {
    this.mActionView.setLogo(paramDrawable);
  }
  
  public void setNavigationMode(int paramInt)
  {
    switch (this.mActionView.getNavigationMode())
    {
    default: 
      this.mActionView.setNavigationMode(paramInt);
      switch (paramInt)
      {
      }
      break;
    }
    for (;;)
    {
      ActionBarView localActionBarView = this.mActionView;
      boolean bool1 = false;
      if (paramInt == 2)
      {
        boolean bool2 = this.mHasEmbeddedTabs;
        bool1 = false;
        if (!bool2) {
          bool1 = true;
        }
      }
      localActionBarView.setCollapsable(bool1);
      return;
      this.mSavedTabPosition = getSelectedNavigationIndex();
      selectTab(null);
      this.mTabScrollView.setVisibility(8);
      break;
      ensureTabsExist();
      this.mTabScrollView.setVisibility(0);
      if (this.mSavedTabPosition != -1)
      {
        setSelectedNavigationItem(this.mSavedTabPosition);
        this.mSavedTabPosition = -1;
      }
    }
  }
  
  public void setSelectedNavigationItem(int paramInt)
  {
    switch (this.mActionView.getNavigationMode())
    {
    default: 
      throw new IllegalStateException("setSelectedNavigationIndex not valid for current navigation mode");
    case 2: 
      selectTab((ActionBar.Tab)this.mTabs.get(paramInt));
      return;
    }
    this.mActionView.setDropdownSelectedPosition(paramInt);
  }
  
  public void setShowHideAnimationEnabled(boolean paramBoolean)
  {
    this.mShowHideAnimationEnabled = paramBoolean;
    if ((!paramBoolean) && (this.mCurrentShowAnim != null)) {
      this.mCurrentShowAnim.end();
    }
  }
  
  public void setSplitBackgroundDrawable(Drawable paramDrawable)
  {
    if (this.mSplitView != null) {
      this.mSplitView.setSplitBackground(paramDrawable);
    }
  }
  
  public void setStackedBackgroundDrawable(Drawable paramDrawable)
  {
    this.mContainerView.setStackedBackground(paramDrawable);
  }
  
  public void setSubtitle(int paramInt)
  {
    setSubtitle(this.mContext.getString(paramInt));
  }
  
  public void setSubtitle(CharSequence paramCharSequence)
  {
    this.mActionView.setSubtitle(paramCharSequence);
  }
  
  public void setTitle(int paramInt)
  {
    setTitle(this.mContext.getString(paramInt));
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    this.mActionView.setTitle(paramCharSequence);
  }
  
  public void show()
  {
    show(true);
  }
  
  void show(boolean paramBoolean)
  {
    if (this.mCurrentShowAnim != null) {
      this.mCurrentShowAnim.end();
    }
    if (this.mContainerView.getVisibility() == 0)
    {
      if (paramBoolean) {
        this.mWasHiddenBeforeMode = false;
      }
      return;
    }
    this.mContainerView.setVisibility(0);
    if (this.mShowHideAnimationEnabled)
    {
      this.mContainerView.setAlpha(0.0F);
      AnimatorSet localAnimatorSet = new AnimatorSet();
      AnimatorSet.Builder localBuilder = localAnimatorSet.play(ObjectAnimator.ofFloat(this.mContainerView, "alpha", new float[] { 1.0F }));
      if (this.mContentView != null)
      {
        NineFrameLayout localNineFrameLayout = this.mContentView;
        float[] arrayOfFloat = new float[2];
        arrayOfFloat[0] = (-this.mContainerView.getHeight());
        arrayOfFloat[1] = 0.0F;
        localBuilder.with(ObjectAnimator.ofFloat(localNineFrameLayout, "translationY", arrayOfFloat));
        this.mContainerView.setTranslationY(-this.mContainerView.getHeight());
        localBuilder.with(ObjectAnimator.ofFloat(this.mContainerView, "translationY", new float[] { 0.0F }));
      }
      if ((this.mSplitView != null) && (this.mContextDisplayMode == 1))
      {
        this.mSplitView.setAlpha(0.0F);
        this.mSplitView.setVisibility(0);
        localBuilder.with(ObjectAnimator.ofFloat(this.mSplitView, "alpha", new float[] { 1.0F }));
      }
      localAnimatorSet.addListener(this.mShowListener);
      this.mCurrentShowAnim = localAnimatorSet;
      localAnimatorSet.start();
      return;
    }
    this.mContainerView.setAlpha(1.0F);
    this.mContainerView.setTranslationY(0.0F);
    this.mShowListener.onAnimationEnd(null);
  }
  
  public ActionMode startActionMode(ActionMode.Callback paramCallback)
  {
    ActionModeImpl localActionModeImpl1 = this.mActionMode;
    boolean bool1 = false;
    if (localActionModeImpl1 != null)
    {
      bool1 = this.mWasHiddenBeforeMode;
      this.mActionMode.finish();
    }
    this.mContextView.killMode();
    ActionModeImpl localActionModeImpl2 = new ActionModeImpl(paramCallback);
    if (localActionModeImpl2.dispatchOnCreate())
    {
      if ((isShowing()) && (!bool1)) {}
      for (boolean bool2 = false;; bool2 = true)
      {
        this.mWasHiddenBeforeMode = bool2;
        localActionModeImpl2.invalidate();
        this.mContextView.initForMode(localActionModeImpl2);
        animateToMode(true);
        if ((this.mSplitView != null) && (this.mContextDisplayMode == 1)) {
          this.mSplitView.setVisibility(0);
        }
        this.mContextView.sendAccessibilityEvent(32);
        this.mActionMode = localActionModeImpl2;
        return localActionModeImpl2;
      }
    }
    return null;
  }
  
  public class ActionModeImpl
    extends ActionMode
    implements MenuBuilder.Callback
  {
    private ActionMode.Callback mCallback;
    private WeakReference<View> mCustomView;
    private MenuBuilder mMenu;
    
    public ActionModeImpl(ActionMode.Callback paramCallback)
    {
      this.mCallback = paramCallback;
      this.mMenu = new MenuBuilder(ActionBarImpl.this.getThemedContext()).setDefaultShowAsAction(1);
      this.mMenu.setCallback(this);
    }
    
    public boolean dispatchOnCreate()
    {
      this.mMenu.stopDispatchingItemsChanged();
      try
      {
        boolean bool = this.mCallback.onCreateActionMode(this, this.mMenu);
        return bool;
      }
      finally
      {
        this.mMenu.startDispatchingItemsChanged();
      }
    }
    
    public void finish()
    {
      if (ActionBarImpl.this.mActionMode != this) {
        return;
      }
      if (ActionBarImpl.this.mWasHiddenBeforeMode)
      {
        ActionBarImpl.this.mDeferredDestroyActionMode = this;
        ActionBarImpl.this.mDeferredModeDestroyCallback = this.mCallback;
      }
      for (;;)
      {
        this.mCallback = null;
        ActionBarImpl.this.animateToMode(false);
        ActionBarImpl.this.mContextView.closeMode();
        ActionBarImpl.this.mActionView.sendAccessibilityEvent(32);
        ActionBarImpl.this.mActionMode = null;
        if (!ActionBarImpl.this.mWasHiddenBeforeMode) {
          break;
        }
        ActionBarImpl.this.hide();
        return;
        this.mCallback.onDestroyActionMode(this);
      }
    }
    
    public View getCustomView()
    {
      if (this.mCustomView != null) {
        return (View)this.mCustomView.get();
      }
      return null;
    }
    
    public Menu getMenu()
    {
      return this.mMenu;
    }
    
    public MenuInflater getMenuInflater()
    {
      return new MenuInflater(ActionBarImpl.this.getThemedContext());
    }
    
    public CharSequence getSubtitle()
    {
      return ActionBarImpl.this.mContextView.getSubtitle();
    }
    
    public CharSequence getTitle()
    {
      return ActionBarImpl.this.mContextView.getTitle();
    }
    
    public void invalidate()
    {
      this.mMenu.stopDispatchingItemsChanged();
      try
      {
        this.mCallback.onPrepareActionMode(this, this.mMenu);
        return;
      }
      finally
      {
        this.mMenu.startDispatchingItemsChanged();
      }
    }
    
    public void onCloseMenu(MenuBuilder paramMenuBuilder, boolean paramBoolean) {}
    
    public void onCloseSubMenu(SubMenuBuilder paramSubMenuBuilder) {}
    
    public boolean onMenuItemSelected(MenuBuilder paramMenuBuilder, MenuItem paramMenuItem)
    {
      if (this.mCallback != null) {
        return this.mCallback.onActionItemClicked(this, paramMenuItem);
      }
      return false;
    }
    
    public void onMenuModeChange(MenuBuilder paramMenuBuilder)
    {
      if (this.mCallback == null) {
        return;
      }
      invalidate();
      ActionBarImpl.this.mContextView.showOverflowMenu();
    }
    
    public boolean onSubMenuSelected(SubMenuBuilder paramSubMenuBuilder)
    {
      boolean bool = true;
      if (this.mCallback == null) {
        bool = false;
      }
      while (!paramSubMenuBuilder.hasVisibleItems()) {
        return bool;
      }
      new MenuPopupHelper(ActionBarImpl.this.getThemedContext(), paramSubMenuBuilder).show();
      return bool;
    }
    
    public void setCustomView(View paramView)
    {
      ActionBarImpl.this.mContextView.setCustomView(paramView);
      this.mCustomView = new WeakReference(paramView);
    }
    
    public void setSubtitle(int paramInt)
    {
      setSubtitle(ActionBarImpl.this.mContext.getResources().getString(paramInt));
    }
    
    public void setSubtitle(CharSequence paramCharSequence)
    {
      ActionBarImpl.this.mContextView.setSubtitle(paramCharSequence);
    }
    
    public void setTitle(int paramInt)
    {
      setTitle(ActionBarImpl.this.mContext.getResources().getString(paramInt));
    }
    
    public void setTitle(CharSequence paramCharSequence)
    {
      ActionBarImpl.this.mContextView.setTitle(paramCharSequence);
    }
  }
  
  public class TabImpl
    extends ActionBar.Tab
  {
    private ActionBar.TabListener mCallback;
    private CharSequence mContentDesc;
    private View mCustomView;
    private Drawable mIcon;
    private int mPosition = -1;
    private Object mTag;
    private CharSequence mText;
    
    public TabImpl() {}
    
    public ActionBar.TabListener getCallback()
    {
      return this.mCallback;
    }
    
    public CharSequence getContentDescription()
    {
      return this.mContentDesc;
    }
    
    public View getCustomView()
    {
      return this.mCustomView;
    }
    
    public Drawable getIcon()
    {
      return this.mIcon;
    }
    
    public int getPosition()
    {
      return this.mPosition;
    }
    
    public Object getTag()
    {
      return this.mTag;
    }
    
    public CharSequence getText()
    {
      return this.mText;
    }
    
    public void select()
    {
      ActionBarImpl.this.selectTab(this);
    }
    
    public ActionBar.Tab setContentDescription(int paramInt)
    {
      return setContentDescription(ActionBarImpl.this.mContext.getResources().getText(paramInt));
    }
    
    public ActionBar.Tab setContentDescription(CharSequence paramCharSequence)
    {
      this.mContentDesc = paramCharSequence;
      if (this.mPosition >= 0) {
        ActionBarImpl.this.mTabScrollView.updateTab(this.mPosition);
      }
      return this;
    }
    
    public ActionBar.Tab setCustomView(int paramInt)
    {
      return setCustomView(LayoutInflater.from(ActionBarImpl.this.getThemedContext()).inflate(paramInt, null));
    }
    
    public ActionBar.Tab setCustomView(View paramView)
    {
      this.mCustomView = paramView;
      if (this.mPosition >= 0) {
        ActionBarImpl.this.mTabScrollView.updateTab(this.mPosition);
      }
      return this;
    }
    
    public ActionBar.Tab setIcon(int paramInt)
    {
      return setIcon(ActionBarImpl.this.mContext.getResources().getDrawable(paramInt));
    }
    
    public ActionBar.Tab setIcon(Drawable paramDrawable)
    {
      this.mIcon = paramDrawable;
      if (this.mPosition >= 0) {
        ActionBarImpl.this.mTabScrollView.updateTab(this.mPosition);
      }
      return this;
    }
    
    public void setPosition(int paramInt)
    {
      this.mPosition = paramInt;
    }
    
    public ActionBar.Tab setTabListener(ActionBar.TabListener paramTabListener)
    {
      this.mCallback = paramTabListener;
      return this;
    }
    
    public ActionBar.Tab setTag(Object paramObject)
    {
      this.mTag = paramObject;
      return this;
    }
    
    public ActionBar.Tab setText(int paramInt)
    {
      return setText(ActionBarImpl.this.mContext.getResources().getText(paramInt));
    }
    
    public ActionBar.Tab setText(CharSequence paramCharSequence)
    {
      this.mText = paramCharSequence;
      if (this.mPosition >= 0) {
        ActionBarImpl.this.mTabScrollView.updateTab(this.mPosition);
      }
      return this;
    }
  }
}
