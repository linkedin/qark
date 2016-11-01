package com.actionbarsherlock.internal;

import android.app.Activity;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.res.AssetManager;
import android.content.res.Configuration;
import android.content.res.Resources.Theme;
import android.content.res.TypedArray;
import android.content.res.XmlResourceParser;
import android.os.Bundle;
import android.util.AndroidRuntimeException;
import android.util.Log;
import android.util.TypedValue;
import android.view.ContextThemeWrapper;
import android.view.KeyCharacterMap;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.MenuItem.OnMenuItemClickListener;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.ViewStub;
import android.view.Window;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.FrameLayout;
import android.widget.TextView;
import com.actionbarsherlock.ActionBarSherlock;
import com.actionbarsherlock.ActionBarSherlock.Implementation;
import com.actionbarsherlock.ActionBarSherlock.OnActionModeFinishedListener;
import com.actionbarsherlock.ActionBarSherlock.OnActionModeStartedListener;
import com.actionbarsherlock.R.attr;
import com.actionbarsherlock.R.bool;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.R.layout;
import com.actionbarsherlock.R.styleable;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.internal.app.ActionBarImpl;
import com.actionbarsherlock.internal.view.StandaloneActionMode;
import com.actionbarsherlock.internal.view.menu.ActionMenuPresenter;
import com.actionbarsherlock.internal.view.menu.MenuBuilder;
import com.actionbarsherlock.internal.view.menu.MenuBuilder.Callback;
import com.actionbarsherlock.internal.view.menu.MenuItemImpl;
import com.actionbarsherlock.internal.view.menu.MenuPresenter.Callback;
import com.actionbarsherlock.internal.widget.ActionBarContainer;
import com.actionbarsherlock.internal.widget.ActionBarContextView;
import com.actionbarsherlock.internal.widget.ActionBarView;
import com.actionbarsherlock.internal.widget.IcsProgressBar;
import com.actionbarsherlock.view.ActionMode;
import com.actionbarsherlock.view.ActionMode.Callback;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

@ActionBarSherlock.Implementation(api=7)
public class ActionBarSherlockCompat
  extends ActionBarSherlock
  implements MenuBuilder.Callback, com.actionbarsherlock.view.Window.Callback, MenuPresenter.Callback, MenuItem.OnMenuItemClickListener
{
  protected static final int DEFAULT_FEATURES;
  private ActionBarImpl aActionBar;
  private ActionMode mActionMode;
  private ActionBarContextView mActionModeView;
  private IcsProgressBar mCircularProgressBar;
  private boolean mClosingActionMenu;
  private ViewGroup mContentParent;
  private ViewGroup mDecor;
  private int mFeatures = 0;
  private IcsProgressBar mHorizontalProgressBar;
  private boolean mIsDestroyed = false;
  private boolean mIsFloating;
  private boolean mIsTitleReady = false;
  private MenuBuilder mMenu;
  private Bundle mMenuFrozenActionViewState;
  private boolean mMenuIsPrepared;
  private boolean mMenuKeyIsLongPress = false;
  private boolean mMenuRefreshContent;
  protected HashMap<android.view.MenuItem, MenuItemImpl> mNativeItemMap;
  private boolean mReserveOverflow;
  private boolean mReserveOverflowSet = false;
  private CharSequence mTitle = null;
  private TextView mTitleView;
  private int mUiOptions = 0;
  private ActionBarView wActionBar;
  
  public ActionBarSherlockCompat(Activity paramActivity, int paramInt)
  {
    super(paramActivity, paramInt);
  }
  
  public static String cleanActivityName(String paramString1, String paramString2)
  {
    if (paramString2.charAt(0) == '.') {
      paramString2 = paramString1 + paramString2;
    }
    while (paramString2.indexOf('.', 1) != -1) {
      return paramString2;
    }
    return paramString1 + "." + paramString2;
  }
  
  private ViewGroup generateLayout()
  {
    TypedArray localTypedArray = this.mActivity.getTheme().obtainStyledAttributes(R.styleable.SherlockTheme);
    this.mIsFloating = localTypedArray.getBoolean(0, false);
    if (!localTypedArray.hasValue(45)) {
      throw new IllegalStateException("You must use Theme.Sherlock, Theme.Sherlock.Light, Theme.Sherlock.Light.DarkActionBar, or a derivative.");
    }
    int i;
    if (localTypedArray.getBoolean(44, false))
    {
      requestFeature(1);
      if (localTypedArray.getBoolean(46, false)) {
        requestFeature(9);
      }
      if (localTypedArray.getBoolean(47, false)) {
        requestFeature(10);
      }
      localTypedArray.recycle();
      if (hasFeature(1)) {
        break label242;
      }
      if (!this.mIsFloating) {
        break label219;
      }
      this.mDecor = ((ViewGroup)this.mDecor.getParent());
      this.mDecor.removeAllViews();
      i = R.layout.abs__dialog_title_holo;
    }
    ViewGroup localViewGroup;
    for (;;)
    {
      View localView = this.mActivity.getLayoutInflater().inflate(i, null);
      this.mDecor.addView(localView, new ViewGroup.LayoutParams(-1, -1));
      localViewGroup = (ViewGroup)this.mDecor.findViewById(R.id.abs__content);
      if (localViewGroup != null) {
        break label273;
      }
      throw new RuntimeException("Couldn't find content container view");
      if (!localTypedArray.getBoolean(45, false)) {
        break;
      }
      requestFeature(8);
      break;
      label219:
      if (hasFeature(9))
      {
        i = R.layout.abs__screen_action_bar_overlay;
      }
      else
      {
        i = R.layout.abs__screen_action_bar;
        continue;
        label242:
        if ((hasFeature(10)) && (!hasFeature(1))) {
          i = R.layout.abs__screen_simple_overlay_action_mode;
        } else {
          i = R.layout.abs__screen_simple;
        }
      }
    }
    label273:
    this.mDecor.setId(-1);
    localViewGroup.setId(16908290);
    if (hasFeature(5))
    {
      IcsProgressBar localIcsProgressBar = getCircularProgressBar(false);
      if (localIcsProgressBar != null) {
        localIcsProgressBar.setIndeterminate(true);
      }
    }
    return localViewGroup;
  }
  
  private IcsProgressBar getCircularProgressBar(boolean paramBoolean)
  {
    if (this.mCircularProgressBar != null) {
      return this.mCircularProgressBar;
    }
    if ((this.mContentParent == null) && (paramBoolean)) {
      installDecor();
    }
    this.mCircularProgressBar = ((IcsProgressBar)this.mDecor.findViewById(R.id.abs__progress_circular));
    if (this.mCircularProgressBar != null) {
      this.mCircularProgressBar.setVisibility(4);
    }
    return this.mCircularProgressBar;
  }
  
  private int getFeatures()
  {
    return this.mFeatures;
  }
  
  private IcsProgressBar getHorizontalProgressBar(boolean paramBoolean)
  {
    if (this.mHorizontalProgressBar != null) {
      return this.mHorizontalProgressBar;
    }
    if ((this.mContentParent == null) && (paramBoolean)) {
      installDecor();
    }
    this.mHorizontalProgressBar = ((IcsProgressBar)this.mDecor.findViewById(R.id.abs__progress_horizontal));
    if (this.mHorizontalProgressBar != null) {
      this.mHorizontalProgressBar.setVisibility(4);
    }
    return this.mHorizontalProgressBar;
  }
  
  private void hideProgressBars(IcsProgressBar paramIcsProgressBar1, IcsProgressBar paramIcsProgressBar2)
  {
    int i = this.mFeatures;
    Animation localAnimation = AnimationUtils.loadAnimation(this.mActivity, 17432577);
    localAnimation.setDuration(1000L);
    if (((i & 0x20) != 0) && (paramIcsProgressBar2.getVisibility() == 0))
    {
      paramIcsProgressBar2.startAnimation(localAnimation);
      paramIcsProgressBar2.setVisibility(4);
    }
    if (((i & 0x4) != 0) && (paramIcsProgressBar1.getVisibility() == 0))
    {
      paramIcsProgressBar1.startAnimation(localAnimation);
      paramIcsProgressBar1.setVisibility(4);
    }
  }
  
  private void initActionBar()
  {
    if (this.mDecor == null) {
      installDecor();
    }
    if ((this.aActionBar != null) || (!hasFeature(8)) || (hasFeature(1)) || (this.mActivity.isChild())) {}
    do
    {
      return;
      this.aActionBar = new ActionBarImpl(this.mActivity, this.mFeatures);
    } while (this.mIsDelegate);
    this.wActionBar.setWindowTitle(this.mActivity.getTitle());
  }
  
  private boolean initializePanelMenu()
  {
    Object localObject = this.mActivity;
    if (this.wActionBar != null)
    {
      TypedValue localTypedValue = new TypedValue();
      ((Context)localObject).getTheme().resolveAttribute(R.attr.actionBarWidgetTheme, localTypedValue, true);
      int i = localTypedValue.resourceId;
      if (i != 0) {
        localObject = new ContextThemeWrapper((Context)localObject, i);
      }
    }
    this.mMenu = new MenuBuilder((Context)localObject);
    this.mMenu.setCallback(this);
    return true;
  }
  
  private void installDecor()
  {
    int i = 1;
    if (this.mDecor == null) {
      this.mDecor = ((ViewGroup)this.mActivity.getWindow().getDecorView().findViewById(16908290));
    }
    ArrayList localArrayList;
    int m;
    Iterator localIterator;
    if (this.mContentParent == null)
    {
      int k = this.mDecor.getChildCount();
      localArrayList = null;
      if (k > 0)
      {
        localArrayList = new ArrayList(i);
        m = 0;
        int n = this.mDecor.getChildCount();
        if (m < n) {
          break label173;
        }
      }
      this.mContentParent = generateLayout();
      if (localArrayList != null)
      {
        localIterator = localArrayList.iterator();
        label100:
        if (localIterator.hasNext()) {
          break label207;
        }
      }
      this.mTitleView = ((TextView)this.mDecor.findViewById(16908310));
      if (this.mTitleView == null) {
        break label243;
      }
      if (!hasFeature(i)) {
        break label231;
      }
      this.mTitleView.setVisibility(8);
      if ((this.mContentParent instanceof FrameLayout)) {
        ((FrameLayout)this.mContentParent).setForeground(null);
      }
    }
    label173:
    label207:
    label231:
    label243:
    do
    {
      return;
      View localView1 = this.mDecor.getChildAt(0);
      this.mDecor.removeView(localView1);
      localArrayList.add(localView1);
      m++;
      break;
      View localView2 = (View)localIterator.next();
      this.mContentParent.addView(localView2);
      break label100;
      this.mTitleView.setText(this.mTitle);
      return;
      this.wActionBar = ((ActionBarView)this.mDecor.findViewById(R.id.abs__action_bar));
    } while (this.wActionBar == null);
    this.wActionBar.setWindowCallback(this);
    if (this.wActionBar.getTitle() == null) {
      this.wActionBar.setWindowTitle(this.mActivity.getTitle());
    }
    if (hasFeature(2)) {
      this.wActionBar.initProgress();
    }
    if (hasFeature(5)) {
      this.wActionBar.initIndeterminateProgress();
    }
    int i1 = loadUiOptionsFromManifest(this.mActivity);
    if (i1 != 0) {
      this.mUiOptions = i1;
    }
    boolean bool;
    if ((0x1 & this.mUiOptions) != 0)
    {
      if (i == 0) {
        break label485;
      }
      bool = ResourcesCompat.getResources_getBoolean(this.mActivity, R.bool.abs__split_action_bar_is_narrow);
      label374:
      ActionBarContainer localActionBarContainer = (ActionBarContainer)this.mDecor.findViewById(R.id.abs__split_action_bar);
      if (localActionBarContainer == null) {
        break label509;
      }
      this.wActionBar.setSplitView(localActionBarContainer);
      this.wActionBar.setSplitActionBar(bool);
      this.wActionBar.setSplitWhenNarrow(i);
      this.mActionModeView = ((ActionBarContextView)this.mDecor.findViewById(R.id.abs__action_context_bar));
      this.mActionModeView.setSplitView(localActionBarContainer);
      this.mActionModeView.setSplitActionBar(bool);
      this.mActionModeView.setSplitWhenNarrow(i);
    }
    for (;;)
    {
      this.mDecor.post(new Runnable()
      {
        public void run()
        {
          if ((!ActionBarSherlockCompat.this.mIsDestroyed) && (!ActionBarSherlockCompat.this.mActivity.isFinishing()) && (ActionBarSherlockCompat.this.mMenu == null)) {
            ActionBarSherlockCompat.this.dispatchInvalidateOptionsMenu();
          }
        }
      });
      return;
      int j = 0;
      break;
      label485:
      bool = this.mActivity.getTheme().obtainStyledAttributes(R.styleable.SherlockTheme).getBoolean(48, false);
      break label374;
      label509:
      if (bool) {
        Log.e("ActionBarSherlock", "Requested split action bar with incompatible window decor! Ignoring request.");
      }
    }
  }
  
  private boolean isReservingOverflow()
  {
    if (!this.mReserveOverflowSet)
    {
      this.mReserveOverflow = ActionMenuPresenter.reserveOverflow(this.mActivity);
      this.mReserveOverflowSet = true;
    }
    return this.mReserveOverflow;
  }
  
  private static int loadUiOptionsFromManifest(Activity paramActivity)
  {
    int i = 0;
    int j;
    int n;
    try
    {
      str1 = paramActivity.getClass().getName();
      str2 = paramActivity.getApplicationInfo().packageName;
      localXmlResourceParser = paramActivity.createPackageContext(str2, 0).getAssets().openXmlResourceParser("AndroidManifest.xml");
      j = localXmlResourceParser.getEventType();
      i = 0;
    }
    catch (Exception localException)
    {
      String str1;
      String str2;
      XmlResourceParser localXmlResourceParser;
      String str3;
      String str4;
      Integer localInteger;
      localException.printStackTrace();
      return i;
    }
    if (j == 2)
    {
      str3 = localXmlResourceParser.getName();
      if (!"application".equals(str3)) {
        break label135;
      }
      n = -1 + localXmlResourceParser.getAttributeCount();
      break label286;
    }
    label103:
    label135:
    while (!"activity".equals(str3)) {
      for (;;)
      {
        j = localXmlResourceParser.nextToken();
        break;
        if (!"uiOptions".equals(localXmlResourceParser.getAttributeName(n))) {
          break label294;
        }
        i = localXmlResourceParser.getAttributeIntValue(n, 0);
      }
    }
    int k = -1 + localXmlResourceParser.getAttributeCount();
    str4 = null;
    localInteger = null;
    int m = 0;
    label286:
    label294:
    label298:
    label312:
    label316:
    for (;;)
    {
      String str5 = localXmlResourceParser.getAttributeName(k);
      if ("uiOptions".equals(str5)) {
        localInteger = Integer.valueOf(localXmlResourceParser.getAttributeIntValue(k, 0));
      }
      for (;;)
      {
        if ((localInteger != null) && (str4 != null))
        {
          i = localInteger.intValue();
          break label312;
          if ("name".equals(str5))
          {
            str4 = cleanActivityName(str2, localXmlResourceParser.getAttributeValue(k));
            boolean bool = str1.equals(str4);
            if (bool)
            {
              m = 1;
              continue;
              if (j != 1) {
                break;
              }
              return i;
              for (;;)
              {
                if (n >= 0) {
                  break label298;
                }
                break;
                n--;
              }
              break label103;
            }
          }
        }
      }
      for (;;)
      {
        if (k >= 0) {
          break label316;
        }
        if (m == 0) {
          break;
        }
        return i;
        k--;
      }
    }
  }
  
  private void onIntChanged(int paramInt1, int paramInt2)
  {
    if ((paramInt1 == 2) || (paramInt1 == 5)) {
      updateProgressBars(paramInt2);
    }
  }
  
  private boolean preparePanel()
  {
    boolean bool2;
    if (this.mMenuIsPrepared) {
      bool2 = true;
    }
    ActionBarView localActionBarView;
    do
    {
      MenuBuilder localMenuBuilder2;
      do
      {
        boolean bool3;
        do
        {
          return bool2;
          if ((this.mMenu != null) && (!this.mMenuRefreshContent)) {
            break label134;
          }
          if (this.mMenu != null) {
            break;
          }
          bool3 = initializePanelMenu();
          bool2 = false;
        } while (!bool3);
        localMenuBuilder2 = this.mMenu;
        bool2 = false;
      } while (localMenuBuilder2 == null);
      if (this.wActionBar != null) {
        this.wActionBar.setMenu(this.mMenu, this);
      }
      this.mMenu.stopDispatchingItemsChanged();
      if (callbackCreateOptionsMenu(this.mMenu)) {
        break;
      }
      this.mMenu = null;
      localActionBarView = this.wActionBar;
      bool2 = false;
    } while (localActionBarView == null);
    this.wActionBar.setMenu(null, this);
    return false;
    this.mMenuRefreshContent = false;
    label134:
    this.mMenu.stopDispatchingItemsChanged();
    if (this.mMenuFrozenActionViewState != null)
    {
      this.mMenu.restoreActionViewStates(this.mMenuFrozenActionViewState);
      this.mMenuFrozenActionViewState = null;
    }
    if (!callbackPrepareOptionsMenu(this.mMenu))
    {
      if (this.wActionBar != null) {
        this.wActionBar.setMenu(null, this);
      }
      this.mMenu.startDispatchingItemsChanged();
      return false;
    }
    KeyCharacterMap localKeyCharacterMap = KeyCharacterMap.load(-1);
    MenuBuilder localMenuBuilder1 = this.mMenu;
    int i = localKeyCharacterMap.getKeyboardType();
    boolean bool1 = false;
    if (i != 1) {
      bool1 = true;
    }
    localMenuBuilder1.setQwertyMode(bool1);
    this.mMenu.startDispatchingItemsChanged();
    this.mMenuIsPrepared = true;
    return true;
  }
  
  private void reopenMenu(boolean paramBoolean)
  {
    if ((this.wActionBar != null) && (this.wActionBar.isOverflowReserved()))
    {
      if ((this.wActionBar.isOverflowMenuShowing()) && (paramBoolean)) {
        break label61;
      }
      if ((this.wActionBar.getVisibility() == 0) && (callbackPrepareOptionsMenu(this.mMenu))) {
        this.wActionBar.showOverflowMenu();
      }
    }
    return;
    label61:
    this.wActionBar.hideOverflowMenu();
  }
  
  private void setFeatureInt(int paramInt1, int paramInt2)
  {
    updateInt(paramInt1, paramInt2, false);
  }
  
  private void showProgressBars(IcsProgressBar paramIcsProgressBar1, IcsProgressBar paramIcsProgressBar2)
  {
    int i = this.mFeatures;
    if (((i & 0x20) != 0) && (paramIcsProgressBar2.getVisibility() == 4)) {
      paramIcsProgressBar2.setVisibility(0);
    }
    if (((i & 0x4) != 0) && (paramIcsProgressBar1.getProgress() < 10000)) {
      paramIcsProgressBar1.setVisibility(0);
    }
  }
  
  private void updateInt(int paramInt1, int paramInt2, boolean paramBoolean)
  {
    if (this.mContentParent == null) {}
    while (((1 << paramInt1 & getFeatures()) == 0) && (!paramBoolean)) {
      return;
    }
    onIntChanged(paramInt1, paramInt2);
  }
  
  private void updateProgressBars(int paramInt)
  {
    IcsProgressBar localIcsProgressBar1 = getCircularProgressBar(true);
    IcsProgressBar localIcsProgressBar2 = getHorizontalProgressBar(true);
    int i = this.mFeatures;
    int k;
    if (paramInt == -1) {
      if ((i & 0x4) != 0)
      {
        int j = localIcsProgressBar2.getProgress();
        if ((localIcsProgressBar2.isIndeterminate()) || (j < 10000))
        {
          k = 0;
          localIcsProgressBar2.setVisibility(k);
        }
      }
      else if ((i & 0x20) != 0)
      {
        localIcsProgressBar1.setVisibility(0);
      }
    }
    label114:
    do
    {
      do
      {
        return;
        k = 4;
        break;
        if (paramInt != -2) {
          break label114;
        }
        if ((i & 0x4) != 0) {
          localIcsProgressBar2.setVisibility(8);
        }
      } while ((i & 0x20) == 0);
      localIcsProgressBar1.setVisibility(8);
      return;
      if (paramInt == -3)
      {
        localIcsProgressBar2.setIndeterminate(true);
        return;
      }
      if (paramInt == -4)
      {
        localIcsProgressBar2.setIndeterminate(false);
        return;
      }
      if ((paramInt >= 0) && (paramInt <= 10000))
      {
        localIcsProgressBar2.setProgress(paramInt + 0);
        if (paramInt < 10000)
        {
          showProgressBars(localIcsProgressBar2, localIcsProgressBar1);
          return;
        }
        hideProgressBars(localIcsProgressBar2, localIcsProgressBar1);
        return;
      }
    } while ((20000 > paramInt) || (paramInt > 30000));
    localIcsProgressBar2.setSecondaryProgress(paramInt - 20000);
    showProgressBars(localIcsProgressBar2, localIcsProgressBar1);
  }
  
  public void addContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    if (this.mContentParent == null) {
      installDecor();
    }
    this.mContentParent.addView(paramView, paramLayoutParams);
    initActionBar();
  }
  
  void checkCloseActionMenu(com.actionbarsherlock.view.Menu paramMenu)
  {
    if (this.mClosingActionMenu) {
      return;
    }
    this.mClosingActionMenu = true;
    this.wActionBar.dismissPopupMenus();
    this.mClosingActionMenu = false;
  }
  
  public boolean dispatchCloseOptionsMenu()
  {
    if (!isReservingOverflow()) {
      return false;
    }
    return this.wActionBar.hideOverflowMenu();
  }
  
  public void dispatchConfigurationChanged(Configuration paramConfiguration)
  {
    if (this.aActionBar != null) {
      this.aActionBar.onConfigurationChanged(paramConfiguration);
    }
  }
  
  public boolean dispatchCreateOptionsMenu(android.view.Menu paramMenu)
  {
    return true;
  }
  
  public void dispatchDestroy()
  {
    this.mIsDestroyed = true;
  }
  
  public void dispatchInvalidateOptionsMenu()
  {
    if (this.mMenu != null)
    {
      Bundle localBundle = new Bundle();
      this.mMenu.saveActionViewStates(localBundle);
      if (localBundle.size() > 0) {
        this.mMenuFrozenActionViewState = localBundle;
      }
      this.mMenu.stopDispatchingItemsChanged();
      this.mMenu.clear();
    }
    this.mMenuRefreshContent = true;
    if (this.wActionBar != null)
    {
      this.mMenuIsPrepared = false;
      preparePanel();
    }
  }
  
  public boolean dispatchKeyEvent(KeyEvent paramKeyEvent)
  {
    int i = paramKeyEvent.getKeyCode();
    int k;
    boolean bool1;
    if (i == 4)
    {
      k = paramKeyEvent.getAction();
      if (this.mActionMode != null)
      {
        if (k == 1) {
          this.mActionMode.finish();
        }
        bool1 = true;
      }
    }
    int j;
    do
    {
      boolean bool2;
      do
      {
        do
        {
          return bool1;
          if ((this.wActionBar != null) && (this.wActionBar.hasExpandedActionView()))
          {
            if (k == 1) {
              this.wActionBar.collapseActionView();
            }
            return true;
          }
          bool1 = false;
        } while (i != 82);
        bool2 = isReservingOverflow();
        bool1 = false;
      } while (!bool2);
      if ((paramKeyEvent.getAction() == 0) && (paramKeyEvent.isLongPress()))
      {
        this.mMenuKeyIsLongPress = true;
        return false;
      }
      j = paramKeyEvent.getAction();
      bool1 = false;
    } while (j != 1);
    boolean bool3 = this.mMenuKeyIsLongPress;
    boolean bool4 = false;
    if (!bool3) {
      if ((this.mActionMode == null) && (this.wActionBar != null))
      {
        if (!this.wActionBar.isOverflowMenuShowing()) {
          break label185;
        }
        this.wActionBar.hideOverflowMenu();
      }
    }
    for (;;)
    {
      bool4 = true;
      this.mMenuKeyIsLongPress = false;
      return bool4;
      label185:
      this.wActionBar.showOverflowMenu();
    }
  }
  
  public boolean dispatchMenuOpened(int paramInt, android.view.Menu paramMenu)
  {
    if ((paramInt == 8) || (paramInt == 0))
    {
      if (this.aActionBar != null) {
        this.aActionBar.dispatchMenuVisibilityChanged(true);
      }
      return true;
    }
    return false;
  }
  
  public boolean dispatchOpenOptionsMenu()
  {
    if (!isReservingOverflow()) {
      return false;
    }
    return this.wActionBar.showOverflowMenu();
  }
  
  public boolean dispatchOptionsItemSelected(android.view.MenuItem paramMenuItem)
  {
    throw new IllegalStateException("Native callback invoked. Create a test case and report!");
  }
  
  public void dispatchPanelClosed(int paramInt, android.view.Menu paramMenu)
  {
    if (((paramInt == 8) || (paramInt == 0)) && (this.aActionBar != null)) {
      this.aActionBar.dispatchMenuVisibilityChanged(false);
    }
  }
  
  public void dispatchPause()
  {
    if ((this.wActionBar != null) && (this.wActionBar.isOverflowMenuShowing())) {
      this.wActionBar.hideOverflowMenu();
    }
  }
  
  public void dispatchPostCreate(Bundle paramBundle)
  {
    if (this.mIsDelegate) {
      this.mIsTitleReady = true;
    }
    if (this.mDecor == null) {
      initActionBar();
    }
  }
  
  public void dispatchPostResume()
  {
    if (this.aActionBar != null) {
      this.aActionBar.setShowHideAnimationEnabled(true);
    }
  }
  
  public boolean dispatchPrepareOptionsMenu(android.view.Menu paramMenu)
  {
    if (this.mActionMode != null) {}
    for (;;)
    {
      return false;
      this.mMenuIsPrepared = false;
      if ((preparePanel()) && (!isReservingOverflow()))
      {
        if (this.mNativeItemMap == null) {
          this.mNativeItemMap = new HashMap();
        }
        while (this.mMenu != null)
        {
          return this.mMenu.bindNativeOverflow(paramMenu, this, this.mNativeItemMap);
          this.mNativeItemMap.clear();
        }
      }
    }
  }
  
  public void dispatchStop()
  {
    if (this.aActionBar != null) {
      this.aActionBar.setShowHideAnimationEnabled(false);
    }
  }
  
  public void dispatchTitleChanged(CharSequence paramCharSequence, int paramInt)
  {
    if ((!this.mIsDelegate) || (this.mIsTitleReady))
    {
      if (this.mTitleView == null) {
        break label35;
      }
      this.mTitleView.setText(paramCharSequence);
    }
    for (;;)
    {
      this.mTitle = paramCharSequence;
      return;
      label35:
      if (this.wActionBar != null) {
        this.wActionBar.setWindowTitle(paramCharSequence);
      }
    }
  }
  
  public ActionBar getActionBar()
  {
    initActionBar();
    return this.aActionBar;
  }
  
  protected Context getThemedContext()
  {
    return this.aActionBar.getThemedContext();
  }
  
  public boolean hasFeature(int paramInt)
  {
    return (this.mFeatures & 1 << paramInt) != 0;
  }
  
  public void onCloseMenu(MenuBuilder paramMenuBuilder, boolean paramBoolean)
  {
    checkCloseActionMenu(paramMenuBuilder);
  }
  
  public boolean onMenuItemClick(android.view.MenuItem paramMenuItem)
  {
    MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mNativeItemMap.get(paramMenuItem);
    if (localMenuItemImpl != null) {
      localMenuItemImpl.invoke();
    }
    for (;;)
    {
      return true;
      Log.e("ActionBarSherlock", "Options item \"" + paramMenuItem + "\" not found in mapping");
    }
  }
  
  public boolean onMenuItemSelected(int paramInt, com.actionbarsherlock.view.MenuItem paramMenuItem)
  {
    return callbackOptionsItemSelected(paramMenuItem);
  }
  
  public boolean onMenuItemSelected(MenuBuilder paramMenuBuilder, com.actionbarsherlock.view.MenuItem paramMenuItem)
  {
    return callbackOptionsItemSelected(paramMenuItem);
  }
  
  public void onMenuModeChange(MenuBuilder paramMenuBuilder)
  {
    reopenMenu(true);
  }
  
  public boolean onOpenSubMenu(MenuBuilder paramMenuBuilder)
  {
    return true;
  }
  
  public boolean requestFeature(int paramInt)
  {
    if (this.mContentParent != null) {
      throw new AndroidRuntimeException("requestFeature() must be called before adding content");
    }
    switch (paramInt)
    {
    case 3: 
    case 4: 
    case 6: 
    case 7: 
    default: 
      return false;
    }
    this.mFeatures |= 1 << paramInt;
    return true;
  }
  
  public void setContentView(int paramInt)
  {
    if (this.mContentParent == null) {
      installDecor();
    }
    for (;;)
    {
      this.mActivity.getLayoutInflater().inflate(paramInt, this.mContentParent);
      android.view.Window.Callback localCallback = this.mActivity.getWindow().getCallback();
      if (localCallback != null) {
        localCallback.onContentChanged();
      }
      initActionBar();
      return;
      this.mContentParent.removeAllViews();
    }
  }
  
  public void setContentView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    if (this.mContentParent == null) {
      installDecor();
    }
    for (;;)
    {
      this.mContentParent.addView(paramView, paramLayoutParams);
      android.view.Window.Callback localCallback = this.mActivity.getWindow().getCallback();
      if (localCallback != null) {
        localCallback.onContentChanged();
      }
      initActionBar();
      return;
      this.mContentParent.removeAllViews();
    }
  }
  
  public void setProgress(int paramInt)
  {
    setFeatureInt(2, paramInt + 0);
  }
  
  public void setProgressBarIndeterminate(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = -3;; i = -4)
    {
      setFeatureInt(2, i);
      return;
    }
  }
  
  public void setProgressBarIndeterminateVisibility(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = -1;; i = -2)
    {
      setFeatureInt(5, i);
      return;
    }
  }
  
  public void setProgressBarVisibility(boolean paramBoolean)
  {
    if (paramBoolean) {}
    for (int i = -1;; i = -2)
    {
      setFeatureInt(2, i);
      return;
    }
  }
  
  public void setSecondaryProgress(int paramInt)
  {
    setFeatureInt(2, paramInt + 20000);
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    dispatchTitleChanged(paramCharSequence, 0);
  }
  
  public void setUiOptions(int paramInt)
  {
    this.mUiOptions = paramInt;
  }
  
  public void setUiOptions(int paramInt1, int paramInt2)
  {
    this.mUiOptions = (this.mUiOptions & (paramInt2 ^ 0xFFFFFFFF) | paramInt1 & paramInt2);
  }
  
  public ActionMode startActionMode(ActionMode.Callback paramCallback)
  {
    if (this.mActionMode != null) {
      this.mActionMode.finish();
    }
    ActionModeCallbackWrapper localActionModeCallbackWrapper = new ActionModeCallbackWrapper(paramCallback);
    initActionBar();
    ActionBarImpl localActionBarImpl = this.aActionBar;
    ActionMode localActionMode = null;
    if (localActionBarImpl != null) {
      localActionMode = this.aActionBar.startActionMode(localActionModeCallbackWrapper);
    }
    if (localActionMode != null) {
      this.mActionMode = localActionMode;
    }
    for (;;)
    {
      if ((this.mActionMode != null) && ((this.mActivity instanceof ActionBarSherlock.OnActionModeStartedListener))) {
        ((ActionBarSherlock.OnActionModeStartedListener)this.mActivity).onActionModeStarted(this.mActionMode);
      }
      return this.mActionMode;
      if (this.mActionModeView == null)
      {
        ViewStub localViewStub = (ViewStub)this.mDecor.findViewById(R.id.abs__action_mode_bar_stub);
        if (localViewStub != null) {
          this.mActionModeView = ((ActionBarContextView)localViewStub.inflate());
        }
      }
      if (this.mActionModeView != null)
      {
        this.mActionModeView.killMode();
        StandaloneActionMode localStandaloneActionMode = new StandaloneActionMode(this.mActivity, this.mActionModeView, localActionModeCallbackWrapper, true);
        if (paramCallback.onCreateActionMode(localStandaloneActionMode, localStandaloneActionMode.getMenu()))
        {
          localStandaloneActionMode.invalidate();
          this.mActionModeView.initForMode(localStandaloneActionMode);
          this.mActionModeView.setVisibility(0);
          this.mActionMode = localStandaloneActionMode;
          this.mActionModeView.sendAccessibilityEvent(32);
        }
        else
        {
          this.mActionMode = null;
        }
      }
    }
  }
  
  private class ActionModeCallbackWrapper
    implements ActionMode.Callback
  {
    private final ActionMode.Callback mWrapped;
    
    public ActionModeCallbackWrapper(ActionMode.Callback paramCallback)
    {
      this.mWrapped = paramCallback;
    }
    
    public boolean onActionItemClicked(ActionMode paramActionMode, com.actionbarsherlock.view.MenuItem paramMenuItem)
    {
      return this.mWrapped.onActionItemClicked(paramActionMode, paramMenuItem);
    }
    
    public boolean onCreateActionMode(ActionMode paramActionMode, com.actionbarsherlock.view.Menu paramMenu)
    {
      return this.mWrapped.onCreateActionMode(paramActionMode, paramMenu);
    }
    
    public void onDestroyActionMode(ActionMode paramActionMode)
    {
      this.mWrapped.onDestroyActionMode(paramActionMode);
      if (ActionBarSherlockCompat.this.mActionModeView != null)
      {
        ActionBarSherlockCompat.this.mActionModeView.setVisibility(8);
        ActionBarSherlockCompat.this.mActionModeView.removeAllViews();
      }
      if ((ActionBarSherlockCompat.this.mActivity instanceof ActionBarSherlock.OnActionModeFinishedListener)) {
        ((ActionBarSherlock.OnActionModeFinishedListener)ActionBarSherlockCompat.this.mActivity).onActionModeFinished(ActionBarSherlockCompat.this.mActionMode);
      }
      ActionBarSherlockCompat.this.mActionMode = null;
    }
    
    public boolean onPrepareActionMode(ActionMode paramActionMode, com.actionbarsherlock.view.Menu paramMenu)
    {
      return this.mWrapped.onPrepareActionMode(paramActionMode, paramMenu);
    }
  }
}
