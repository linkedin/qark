package com.actionbarsherlock.internal.view.menu;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.res.Configuration;
import android.content.res.Resources;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Parcelable;
import android.util.SparseArray;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.KeyCharacterMap.KeyData;
import android.view.KeyEvent;
import android.view.MenuItem.OnMenuItemClickListener;
import android.view.View;
import com.actionbarsherlock.R.bool;
import com.actionbarsherlock.view.ActionProvider;
import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class MenuBuilder
  implements com.actionbarsherlock.view.Menu
{
  private static final String ACTION_VIEW_STATES_KEY = "android:menu:actionviewstates";
  private static final String EXPANDED_ACTION_VIEW_ID = "android:menu:expandedactionview";
  private static final String PRESENTER_KEY = "android:menu:presenters";
  private static final int[] sCategoryToOrder;
  private ArrayList<MenuItemImpl> mActionItems;
  private Callback mCallback;
  private final Context mContext;
  private ContextMenu.ContextMenuInfo mCurrentMenuInfo;
  private int mDefaultShowAsAction = 0;
  private MenuItemImpl mExpandedItem;
  Drawable mHeaderIcon;
  CharSequence mHeaderTitle;
  View mHeaderView;
  private boolean mIsActionItemsStale;
  private boolean mIsClosing = false;
  private boolean mIsVisibleItemsStale;
  private ArrayList<MenuItemImpl> mItems;
  private boolean mItemsChangedWhileDispatchPrevented = false;
  private ArrayList<MenuItemImpl> mNonActionItems;
  private boolean mOptionalIconsVisible = false;
  private CopyOnWriteArrayList<WeakReference<MenuPresenter>> mPresenters = new CopyOnWriteArrayList();
  private boolean mPreventDispatchingItemsChanged = false;
  private boolean mQwertyMode;
  private final Resources mResources;
  private boolean mShortcutsVisible;
  private ArrayList<MenuItemImpl> mTempShortcutItemList = new ArrayList();
  private ArrayList<MenuItemImpl> mVisibleItems;
  
  static
  {
    int[] arrayOfInt = new int[6];
    arrayOfInt[0] = 1;
    arrayOfInt[1] = 4;
    arrayOfInt[2] = 5;
    arrayOfInt[3] = 3;
    arrayOfInt[4] = 2;
    sCategoryToOrder = arrayOfInt;
  }
  
  public MenuBuilder(Context paramContext)
  {
    this.mContext = paramContext;
    this.mResources = paramContext.getResources();
    this.mItems = new ArrayList();
    this.mVisibleItems = new ArrayList();
    this.mIsVisibleItemsStale = true;
    this.mActionItems = new ArrayList();
    this.mNonActionItems = new ArrayList();
    this.mIsActionItemsStale = true;
    setShortcutsVisibleInner(true);
  }
  
  private com.actionbarsherlock.view.MenuItem addInternal(int paramInt1, int paramInt2, int paramInt3, CharSequence paramCharSequence)
  {
    int i = getOrdering(paramInt3);
    MenuItemImpl localMenuItemImpl = new MenuItemImpl(this, paramInt1, paramInt2, paramInt3, i, paramCharSequence, this.mDefaultShowAsAction);
    if (this.mCurrentMenuInfo != null) {
      localMenuItemImpl.setMenuInfo(this.mCurrentMenuInfo);
    }
    this.mItems.add(findInsertIndex(this.mItems, i), localMenuItemImpl);
    onItemsChanged(true);
    return localMenuItemImpl;
  }
  
  private void dispatchPresenterUpdate(boolean paramBoolean)
  {
    if (this.mPresenters.isEmpty()) {
      return;
    }
    stopDispatchingItemsChanged();
    Iterator localIterator = this.mPresenters.iterator();
    for (;;)
    {
      if (!localIterator.hasNext())
      {
        startDispatchingItemsChanged();
        return;
      }
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null) {
        this.mPresenters.remove(localWeakReference);
      } else {
        localMenuPresenter.updateMenuView(paramBoolean);
      }
    }
  }
  
  private void dispatchRestoreInstanceState(Bundle paramBundle)
  {
    SparseArray localSparseArray = paramBundle.getSparseParcelableArray("android:menu:presenters");
    if ((localSparseArray == null) || (this.mPresenters.isEmpty())) {}
    for (;;)
    {
      return;
      Iterator localIterator = this.mPresenters.iterator();
      while (localIterator.hasNext())
      {
        WeakReference localWeakReference = (WeakReference)localIterator.next();
        MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
        if (localMenuPresenter == null)
        {
          this.mPresenters.remove(localWeakReference);
        }
        else
        {
          int i = localMenuPresenter.getId();
          if (i > 0)
          {
            Parcelable localParcelable = (Parcelable)localSparseArray.get(i);
            if (localParcelable != null) {
              localMenuPresenter.onRestoreInstanceState(localParcelable);
            }
          }
        }
      }
    }
  }
  
  private void dispatchSaveInstanceState(Bundle paramBundle)
  {
    if (this.mPresenters.isEmpty()) {
      return;
    }
    SparseArray localSparseArray = new SparseArray();
    Iterator localIterator = this.mPresenters.iterator();
    for (;;)
    {
      if (!localIterator.hasNext())
      {
        paramBundle.putSparseParcelableArray("android:menu:presenters", localSparseArray);
        return;
      }
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null)
      {
        this.mPresenters.remove(localWeakReference);
      }
      else
      {
        int i = localMenuPresenter.getId();
        if (i > 0)
        {
          Parcelable localParcelable = localMenuPresenter.onSaveInstanceState();
          if (localParcelable != null) {
            localSparseArray.put(i, localParcelable);
          }
        }
      }
    }
  }
  
  private boolean dispatchSubMenuSelected(SubMenuBuilder paramSubMenuBuilder)
  {
    boolean bool;
    if (this.mPresenters.isEmpty()) {
      bool = false;
    }
    for (;;)
    {
      return bool;
      bool = false;
      Iterator localIterator = this.mPresenters.iterator();
      while (localIterator.hasNext())
      {
        WeakReference localWeakReference = (WeakReference)localIterator.next();
        MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
        if (localMenuPresenter == null) {
          this.mPresenters.remove(localWeakReference);
        } else if (!bool) {
          bool = localMenuPresenter.onSubMenuSelected(paramSubMenuBuilder);
        }
      }
    }
  }
  
  private static int findInsertIndex(ArrayList<MenuItemImpl> paramArrayList, int paramInt)
  {
    for (int i = -1 + paramArrayList.size();; i--)
    {
      if (i < 0) {
        return 0;
      }
      if (((MenuItemImpl)paramArrayList.get(i)).getOrdering() <= paramInt) {
        return i + 1;
      }
    }
  }
  
  private static int getOrdering(int paramInt)
  {
    int i = (0xFFFF0000 & paramInt) >> 16;
    if ((i < 0) || (i >= sCategoryToOrder.length)) {
      throw new IllegalArgumentException("order does not contain a valid category.");
    }
    return sCategoryToOrder[i] << 16 | 0xFFFF & paramInt;
  }
  
  private void removeItemAtInt(int paramInt, boolean paramBoolean)
  {
    if ((paramInt < 0) || (paramInt >= this.mItems.size())) {}
    do
    {
      return;
      this.mItems.remove(paramInt);
    } while (!paramBoolean);
    onItemsChanged(true);
  }
  
  private void setHeaderInternal(int paramInt1, CharSequence paramCharSequence, int paramInt2, Drawable paramDrawable, View paramView)
  {
    Resources localResources = getResources();
    if (paramView != null)
    {
      this.mHeaderView = paramView;
      this.mHeaderTitle = null;
      this.mHeaderIcon = null;
      onItemsChanged(false);
      return;
    }
    if (paramInt1 > 0)
    {
      this.mHeaderTitle = localResources.getText(paramInt1);
      label47:
      if (paramInt2 <= 0) {
        break label81;
      }
      this.mHeaderIcon = localResources.getDrawable(paramInt2);
    }
    for (;;)
    {
      this.mHeaderView = null;
      break;
      if (paramCharSequence == null) {
        break label47;
      }
      this.mHeaderTitle = paramCharSequence;
      break label47;
      label81:
      if (paramDrawable != null) {
        this.mHeaderIcon = paramDrawable;
      }
    }
  }
  
  private void setShortcutsVisibleInner(boolean paramBoolean)
  {
    int i = 1;
    if ((paramBoolean) && (this.mResources.getConfiguration().keyboard != i) && (this.mResources.getBoolean(R.bool.abs__config_showMenuShortcutsWhenKeyboardPresent))) {}
    for (;;)
    {
      this.mShortcutsVisible = i;
      return;
      i = 0;
    }
  }
  
  public com.actionbarsherlock.view.MenuItem add(int paramInt)
  {
    return addInternal(0, 0, 0, this.mResources.getString(paramInt));
  }
  
  public com.actionbarsherlock.view.MenuItem add(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    return addInternal(paramInt1, paramInt2, paramInt3, this.mResources.getString(paramInt4));
  }
  
  public com.actionbarsherlock.view.MenuItem add(int paramInt1, int paramInt2, int paramInt3, CharSequence paramCharSequence)
  {
    return addInternal(paramInt1, paramInt2, paramInt3, paramCharSequence);
  }
  
  public com.actionbarsherlock.view.MenuItem add(CharSequence paramCharSequence)
  {
    return addInternal(0, 0, 0, paramCharSequence);
  }
  
  public int addIntentOptions(int paramInt1, int paramInt2, int paramInt3, ComponentName paramComponentName, Intent[] paramArrayOfIntent, Intent paramIntent, int paramInt4, com.actionbarsherlock.view.MenuItem[] paramArrayOfMenuItem)
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
      com.actionbarsherlock.view.MenuItem localMenuItem = add(paramInt1, paramInt2, paramInt3, localResolveInfo.loadLabel(localPackageManager)).setIcon(localResolveInfo.loadIcon(localPackageManager)).setIntent(localIntent2);
      if ((paramArrayOfMenuItem != null) && (localResolveInfo.specificIndex >= 0)) {
        paramArrayOfMenuItem[localResolveInfo.specificIndex] = localMenuItem;
      }
      j++;
      break;
    }
  }
  
  public void addMenuPresenter(MenuPresenter paramMenuPresenter)
  {
    this.mPresenters.add(new WeakReference(paramMenuPresenter));
    paramMenuPresenter.initForMenu(this.mContext, this);
    this.mIsActionItemsStale = true;
  }
  
  public com.actionbarsherlock.view.SubMenu addSubMenu(int paramInt)
  {
    return addSubMenu(0, 0, 0, this.mResources.getString(paramInt));
  }
  
  public com.actionbarsherlock.view.SubMenu addSubMenu(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    return addSubMenu(paramInt1, paramInt2, paramInt3, this.mResources.getString(paramInt4));
  }
  
  public com.actionbarsherlock.view.SubMenu addSubMenu(int paramInt1, int paramInt2, int paramInt3, CharSequence paramCharSequence)
  {
    MenuItemImpl localMenuItemImpl = (MenuItemImpl)addInternal(paramInt1, paramInt2, paramInt3, paramCharSequence);
    SubMenuBuilder localSubMenuBuilder = new SubMenuBuilder(this.mContext, this, localMenuItemImpl);
    localMenuItemImpl.setSubMenu(localSubMenuBuilder);
    return localSubMenuBuilder;
  }
  
  public com.actionbarsherlock.view.SubMenu addSubMenu(CharSequence paramCharSequence)
  {
    return addSubMenu(0, 0, 0, paramCharSequence);
  }
  
  public boolean bindNativeOverflow(android.view.Menu paramMenu, MenuItem.OnMenuItemClickListener paramOnMenuItemClickListener, HashMap<android.view.MenuItem, MenuItemImpl> paramHashMap)
  {
    ArrayList localArrayList = getNonActionItems();
    if ((localArrayList == null) || (localArrayList.size() == 0))
    {
      bool = false;
      return bool;
    }
    boolean bool = false;
    paramMenu.clear();
    Iterator localIterator1 = localArrayList.iterator();
    label45:
    MenuItemImpl localMenuItemImpl1;
    android.view.SubMenu localSubMenu;
    Iterator localIterator2;
    while (localIterator1.hasNext())
    {
      localMenuItemImpl1 = (MenuItemImpl)localIterator1.next();
      if (localMenuItemImpl1.isVisible())
      {
        bool = true;
        if (!localMenuItemImpl1.hasSubMenu()) {
          break label483;
        }
        localSubMenu = paramMenu.addSubMenu(localMenuItemImpl1.getGroupId(), localMenuItemImpl1.getItemId(), localMenuItemImpl1.getOrder(), localMenuItemImpl1.getTitle());
        localIterator2 = ((SubMenuBuilder)localMenuItemImpl1.getSubMenu()).getVisibleItems().iterator();
        label130:
        if (localIterator2.hasNext()) {
          break label295;
        }
      }
    }
    label295:
    label483:
    for (android.view.MenuItem localMenuItem1 = localSubMenu.getItem();; localMenuItem1 = paramMenu.add(localMenuItemImpl1.getGroupId(), localMenuItemImpl1.getItemId(), localMenuItemImpl1.getOrder(), localMenuItemImpl1.getTitle()))
    {
      localMenuItem1.setIcon(localMenuItemImpl1.getIcon());
      localMenuItem1.setOnMenuItemClickListener(paramOnMenuItemClickListener);
      localMenuItem1.setEnabled(localMenuItemImpl1.isEnabled());
      localMenuItem1.setIntent(localMenuItemImpl1.getIntent());
      localMenuItem1.setNumericShortcut(localMenuItemImpl1.getNumericShortcut());
      localMenuItem1.setAlphabeticShortcut(localMenuItemImpl1.getAlphabeticShortcut());
      localMenuItem1.setTitleCondensed(localMenuItemImpl1.getTitleCondensed());
      localMenuItem1.setCheckable(localMenuItemImpl1.isCheckable());
      localMenuItem1.setChecked(localMenuItemImpl1.isChecked());
      if (localMenuItemImpl1.isExclusiveCheckable()) {
        paramMenu.setGroupCheckable(localMenuItemImpl1.getGroupId(), true, true);
      }
      paramHashMap.put(localMenuItem1, localMenuItemImpl1);
      break label45;
      break;
      MenuItemImpl localMenuItemImpl2 = (MenuItemImpl)localIterator2.next();
      android.view.MenuItem localMenuItem2 = localSubMenu.add(localMenuItemImpl2.getGroupId(), localMenuItemImpl2.getItemId(), localMenuItemImpl2.getOrder(), localMenuItemImpl2.getTitle());
      localMenuItem2.setIcon(localMenuItemImpl2.getIcon());
      localMenuItem2.setOnMenuItemClickListener(paramOnMenuItemClickListener);
      localMenuItem2.setEnabled(localMenuItemImpl2.isEnabled());
      localMenuItem2.setIntent(localMenuItemImpl2.getIntent());
      localMenuItem2.setNumericShortcut(localMenuItemImpl2.getNumericShortcut());
      localMenuItem2.setAlphabeticShortcut(localMenuItemImpl2.getAlphabeticShortcut());
      localMenuItem2.setTitleCondensed(localMenuItemImpl2.getTitleCondensed());
      localMenuItem2.setCheckable(localMenuItemImpl2.isCheckable());
      localMenuItem2.setChecked(localMenuItemImpl2.isChecked());
      if (localMenuItemImpl2.isExclusiveCheckable()) {
        localSubMenu.setGroupCheckable(localMenuItemImpl2.getGroupId(), true, true);
      }
      paramHashMap.put(localMenuItem2, localMenuItemImpl2);
      break label130;
    }
  }
  
  public void changeMenuMode()
  {
    if (this.mCallback != null) {
      this.mCallback.onMenuModeChange(this);
    }
  }
  
  public void clear()
  {
    if (this.mExpandedItem != null) {
      collapseItemActionView(this.mExpandedItem);
    }
    this.mItems.clear();
    onItemsChanged(true);
  }
  
  public void clearAll()
  {
    this.mPreventDispatchingItemsChanged = true;
    clear();
    clearHeader();
    this.mPreventDispatchingItemsChanged = false;
    this.mItemsChangedWhileDispatchPrevented = false;
    onItemsChanged(true);
  }
  
  public void clearHeader()
  {
    this.mHeaderIcon = null;
    this.mHeaderTitle = null;
    this.mHeaderView = null;
    onItemsChanged(false);
  }
  
  public void close()
  {
    close(true);
  }
  
  final void close(boolean paramBoolean)
  {
    if (this.mIsClosing) {
      return;
    }
    this.mIsClosing = true;
    Iterator localIterator = this.mPresenters.iterator();
    for (;;)
    {
      if (!localIterator.hasNext())
      {
        this.mIsClosing = false;
        return;
      }
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null) {
        this.mPresenters.remove(localWeakReference);
      } else {
        localMenuPresenter.onCloseMenu(this, paramBoolean);
      }
    }
  }
  
  public boolean collapseItemActionView(MenuItemImpl paramMenuItemImpl)
  {
    if ((this.mPresenters.isEmpty()) || (this.mExpandedItem != paramMenuItemImpl))
    {
      bool = false;
      return bool;
    }
    boolean bool = false;
    stopDispatchingItemsChanged();
    Iterator localIterator = this.mPresenters.iterator();
    label36:
    if (!localIterator.hasNext()) {}
    for (;;)
    {
      startDispatchingItemsChanged();
      if (!bool) {
        break;
      }
      this.mExpandedItem = null;
      return bool;
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null)
      {
        this.mPresenters.remove(localWeakReference);
        break label36;
      }
      bool = localMenuPresenter.collapseItemActionView(this, paramMenuItemImpl);
      if (!bool) {
        break label36;
      }
    }
  }
  
  boolean dispatchMenuItemSelected(MenuBuilder paramMenuBuilder, com.actionbarsherlock.view.MenuItem paramMenuItem)
  {
    return (this.mCallback != null) && (this.mCallback.onMenuItemSelected(paramMenuBuilder, paramMenuItem));
  }
  
  public boolean expandItemActionView(MenuItemImpl paramMenuItemImpl)
  {
    if (this.mPresenters.isEmpty())
    {
      bool = false;
      return bool;
    }
    boolean bool = false;
    stopDispatchingItemsChanged();
    Iterator localIterator = this.mPresenters.iterator();
    label28:
    if (!localIterator.hasNext()) {}
    for (;;)
    {
      startDispatchingItemsChanged();
      if (!bool) {
        break;
      }
      this.mExpandedItem = paramMenuItemImpl;
      return bool;
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null)
      {
        this.mPresenters.remove(localWeakReference);
        break label28;
      }
      bool = localMenuPresenter.expandItemActionView(this, paramMenuItemImpl);
      if (!bool) {
        break label28;
      }
    }
  }
  
  public int findGroupIndex(int paramInt)
  {
    return findGroupIndex(paramInt, 0);
  }
  
  public int findGroupIndex(int paramInt1, int paramInt2)
  {
    int i = size();
    if (paramInt2 < 0) {
      paramInt2 = 0;
    }
    for (int j = paramInt2;; j++)
    {
      if (j >= i) {
        j = -1;
      }
      while (((MenuItemImpl)this.mItems.get(j)).getGroupId() == paramInt1) {
        return j;
      }
    }
  }
  
  public com.actionbarsherlock.view.MenuItem findItem(int paramInt)
  {
    int i = size();
    for (int j = 0;; j++)
    {
      Object localObject;
      if (j >= i) {
        localObject = null;
      }
      do
      {
        return localObject;
        localObject = (MenuItemImpl)this.mItems.get(j);
      } while (((MenuItemImpl)localObject).getItemId() == paramInt);
      if (((MenuItemImpl)localObject).hasSubMenu())
      {
        com.actionbarsherlock.view.MenuItem localMenuItem = ((MenuItemImpl)localObject).getSubMenu().findItem(paramInt);
        if (localMenuItem != null) {
          return localMenuItem;
        }
      }
    }
  }
  
  public int findItemIndex(int paramInt)
  {
    int i = size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        j = -1;
      }
      while (((MenuItemImpl)this.mItems.get(j)).getItemId() == paramInt) {
        return j;
      }
    }
  }
  
  MenuItemImpl findItemWithShortcutForKey(int paramInt, KeyEvent paramKeyEvent)
  {
    ArrayList localArrayList = this.mTempShortcutItemList;
    localArrayList.clear();
    findItemsWithShortcutForKey(localArrayList, paramInt, paramKeyEvent);
    if (localArrayList.isEmpty()) {}
    for (;;)
    {
      return null;
      int i = paramKeyEvent.getMetaState();
      KeyCharacterMap.KeyData localKeyData = new KeyCharacterMap.KeyData();
      paramKeyEvent.getKeyData(localKeyData);
      int j = localArrayList.size();
      if (j == 1) {
        return (MenuItemImpl)localArrayList.get(0);
      }
      boolean bool = isQwertyMode();
      for (int k = 0; k < j; k++)
      {
        MenuItemImpl localMenuItemImpl = (MenuItemImpl)localArrayList.get(k);
        if (bool) {}
        for (int m = localMenuItemImpl.getAlphabeticShortcut(); ((m == localKeyData.meta[0]) && ((i & 0x2) == 0)) || ((m == localKeyData.meta[2]) && ((i & 0x2) != 0)) || ((bool) && (m == 8) && (paramInt == 67)); m = localMenuItemImpl.getNumericShortcut()) {
          return localMenuItemImpl;
        }
      }
    }
  }
  
  void findItemsWithShortcutForKey(List<MenuItemImpl> paramList, int paramInt, KeyEvent paramKeyEvent)
  {
    boolean bool = isQwertyMode();
    int i = paramKeyEvent.getMetaState();
    KeyCharacterMap.KeyData localKeyData = new KeyCharacterMap.KeyData();
    if ((!paramKeyEvent.getKeyData(localKeyData)) && (paramInt != 67)) {
      return;
    }
    int j = this.mItems.size();
    int k = 0;
    label49:
    MenuItemImpl localMenuItemImpl;
    if (k < j)
    {
      localMenuItemImpl = (MenuItemImpl)this.mItems.get(k);
      if (localMenuItemImpl.hasSubMenu()) {
        ((MenuBuilder)localMenuItemImpl.getSubMenu()).findItemsWithShortcutForKey(paramList, paramInt, paramKeyEvent);
      }
      if (!bool) {
        break label181;
      }
    }
    label181:
    for (int m = localMenuItemImpl.getAlphabeticShortcut();; m = localMenuItemImpl.getNumericShortcut())
    {
      if (((i & 0x5) == 0) && (m != 0) && ((m == localKeyData.meta[0]) || (m == localKeyData.meta[2]) || ((bool) && (m == 8) && (paramInt == 67))) && (localMenuItemImpl.isEnabled())) {
        paramList.add(localMenuItemImpl);
      }
      k++;
      break label49;
      break;
    }
  }
  
  public void flagActionItems()
  {
    if (!this.mIsActionItemsStale) {
      return;
    }
    boolean bool = false;
    Iterator localIterator = this.mPresenters.iterator();
    ArrayList localArrayList;
    int j;
    if (!localIterator.hasNext())
    {
      if (!bool) {
        break label172;
      }
      this.mActionItems.clear();
      this.mNonActionItems.clear();
      localArrayList = getVisibleItems();
      int i = localArrayList.size();
      j = 0;
      if (j < i) {
        break label123;
      }
    }
    for (;;)
    {
      this.mIsActionItemsStale = false;
      return;
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if (localMenuPresenter == null)
      {
        this.mPresenters.remove(localWeakReference);
        break;
      }
      bool |= localMenuPresenter.flagActionItems();
      break;
      label123:
      MenuItemImpl localMenuItemImpl = (MenuItemImpl)localArrayList.get(j);
      if (localMenuItemImpl.isActionButton()) {
        this.mActionItems.add(localMenuItemImpl);
      }
      for (;;)
      {
        j++;
        break;
        this.mNonActionItems.add(localMenuItemImpl);
      }
      label172:
      this.mActionItems.clear();
      this.mNonActionItems.clear();
      this.mNonActionItems.addAll(getVisibleItems());
    }
  }
  
  ArrayList<MenuItemImpl> getActionItems()
  {
    flagActionItems();
    return this.mActionItems;
  }
  
  protected String getActionViewStatesKey()
  {
    return "android:menu:actionviewstates";
  }
  
  public Context getContext()
  {
    return this.mContext;
  }
  
  public MenuItemImpl getExpandedItem()
  {
    return this.mExpandedItem;
  }
  
  public Drawable getHeaderIcon()
  {
    return this.mHeaderIcon;
  }
  
  public CharSequence getHeaderTitle()
  {
    return this.mHeaderTitle;
  }
  
  public View getHeaderView()
  {
    return this.mHeaderView;
  }
  
  public com.actionbarsherlock.view.MenuItem getItem(int paramInt)
  {
    return (com.actionbarsherlock.view.MenuItem)this.mItems.get(paramInt);
  }
  
  ArrayList<MenuItemImpl> getNonActionItems()
  {
    flagActionItems();
    return this.mNonActionItems;
  }
  
  boolean getOptionalIconsVisible()
  {
    return this.mOptionalIconsVisible;
  }
  
  Resources getResources()
  {
    return this.mResources;
  }
  
  public MenuBuilder getRootMenu()
  {
    return this;
  }
  
  ArrayList<MenuItemImpl> getVisibleItems()
  {
    if (!this.mIsVisibleItemsStale) {
      return this.mVisibleItems;
    }
    this.mVisibleItems.clear();
    int i = this.mItems.size();
    for (int j = 0;; j++)
    {
      if (j >= i)
      {
        this.mIsVisibleItemsStale = false;
        this.mIsActionItemsStale = true;
        return this.mVisibleItems;
      }
      MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mItems.get(j);
      if (localMenuItemImpl.isVisible()) {
        this.mVisibleItems.add(localMenuItemImpl);
      }
    }
  }
  
  public boolean hasVisibleItems()
  {
    int i = size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return false;
      }
      if (((MenuItemImpl)this.mItems.get(j)).isVisible()) {
        return true;
      }
    }
  }
  
  boolean isQwertyMode()
  {
    return this.mQwertyMode;
  }
  
  public boolean isShortcutKey(int paramInt, KeyEvent paramKeyEvent)
  {
    return findItemWithShortcutForKey(paramInt, paramKeyEvent) != null;
  }
  
  public boolean isShortcutsVisible()
  {
    return this.mShortcutsVisible;
  }
  
  void onItemActionRequestChanged(MenuItemImpl paramMenuItemImpl)
  {
    this.mIsActionItemsStale = true;
    onItemsChanged(true);
  }
  
  void onItemVisibleChanged(MenuItemImpl paramMenuItemImpl)
  {
    this.mIsVisibleItemsStale = true;
    onItemsChanged(true);
  }
  
  void onItemsChanged(boolean paramBoolean)
  {
    if (!this.mPreventDispatchingItemsChanged)
    {
      if (paramBoolean)
      {
        this.mIsVisibleItemsStale = true;
        this.mIsActionItemsStale = true;
      }
      dispatchPresenterUpdate(paramBoolean);
      return;
    }
    this.mItemsChangedWhileDispatchPrevented = true;
  }
  
  public boolean performIdentifierAction(int paramInt1, int paramInt2)
  {
    return performItemAction(findItem(paramInt1), paramInt2);
  }
  
  public boolean performItemAction(com.actionbarsherlock.view.MenuItem paramMenuItem, int paramInt)
  {
    MenuItemImpl localMenuItemImpl = (MenuItemImpl)paramMenuItem;
    boolean bool;
    if ((localMenuItemImpl == null) || (!localMenuItemImpl.isEnabled())) {
      bool = false;
    }
    do
    {
      do
      {
        do
        {
          return bool;
          bool = localMenuItemImpl.invoke();
          if (!localMenuItemImpl.hasCollapsibleActionView()) {
            break;
          }
          bool |= localMenuItemImpl.expandActionView();
        } while (!bool);
        close(true);
        return bool;
        if (!paramMenuItem.hasSubMenu()) {
          break;
        }
        close(false);
        SubMenuBuilder localSubMenuBuilder = (SubMenuBuilder)paramMenuItem.getSubMenu();
        ActionProvider localActionProvider = paramMenuItem.getActionProvider();
        if ((localActionProvider != null) && (localActionProvider.hasSubMenu())) {
          localActionProvider.onPrepareSubMenu(localSubMenuBuilder);
        }
        bool |= dispatchSubMenuSelected(localSubMenuBuilder);
      } while (bool);
      close(true);
      return bool;
    } while ((paramInt & 0x1) != 0);
    close(true);
    return bool;
  }
  
  public boolean performShortcut(int paramInt1, KeyEvent paramKeyEvent, int paramInt2)
  {
    MenuItemImpl localMenuItemImpl = findItemWithShortcutForKey(paramInt1, paramKeyEvent);
    boolean bool = false;
    if (localMenuItemImpl != null) {
      bool = performItemAction(localMenuItemImpl, paramInt2);
    }
    if ((paramInt2 & 0x2) != 0) {
      close(true);
    }
    return bool;
  }
  
  public void removeGroup(int paramInt)
  {
    int i = findGroupIndex(paramInt);
    int j;
    if (i >= 0) {
      j = this.mItems.size() - i;
    }
    int m;
    for (int k = 0;; k = m)
    {
      m = k + 1;
      if ((k >= j) || (((MenuItemImpl)this.mItems.get(i)).getGroupId() != paramInt))
      {
        onItemsChanged(true);
        return;
      }
      removeItemAtInt(i, false);
    }
  }
  
  public void removeItem(int paramInt)
  {
    removeItemAtInt(findItemIndex(paramInt), true);
  }
  
  public void removeItemAt(int paramInt)
  {
    removeItemAtInt(paramInt, true);
  }
  
  public void removeMenuPresenter(MenuPresenter paramMenuPresenter)
  {
    Iterator localIterator = this.mPresenters.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return;
      }
      WeakReference localWeakReference = (WeakReference)localIterator.next();
      MenuPresenter localMenuPresenter = (MenuPresenter)localWeakReference.get();
      if ((localMenuPresenter == null) || (localMenuPresenter == paramMenuPresenter)) {
        this.mPresenters.remove(localWeakReference);
      }
    }
  }
  
  public void restoreActionViewStates(Bundle paramBundle)
  {
    if (paramBundle == null) {
      return;
    }
    SparseArray localSparseArray = paramBundle.getSparseParcelableArray(getActionViewStatesKey());
    int i = size();
    for (int j = 0;; j++)
    {
      if (j >= i)
      {
        int k = paramBundle.getInt("android:menu:expandedactionview");
        if (k <= 0) {
          break;
        }
        com.actionbarsherlock.view.MenuItem localMenuItem2 = findItem(k);
        if (localMenuItem2 == null) {
          break;
        }
        localMenuItem2.expandActionView();
        return;
      }
      com.actionbarsherlock.view.MenuItem localMenuItem1 = getItem(j);
      View localView = localMenuItem1.getActionView();
      if ((localView != null) && (localView.getId() != -1)) {
        localView.restoreHierarchyState(localSparseArray);
      }
      if (localMenuItem1.hasSubMenu()) {
        ((SubMenuBuilder)localMenuItem1.getSubMenu()).restoreActionViewStates(paramBundle);
      }
    }
  }
  
  public void restorePresenterStates(Bundle paramBundle)
  {
    dispatchRestoreInstanceState(paramBundle);
  }
  
  public void saveActionViewStates(Bundle paramBundle)
  {
    SparseArray localSparseArray = null;
    int i = size();
    for (int j = 0;; j++)
    {
      if (j >= i)
      {
        if (localSparseArray != null) {
          paramBundle.putSparseParcelableArray(getActionViewStatesKey(), localSparseArray);
        }
        return;
      }
      com.actionbarsherlock.view.MenuItem localMenuItem = getItem(j);
      View localView = localMenuItem.getActionView();
      if ((localView != null) && (localView.getId() != -1))
      {
        if (localSparseArray == null) {
          localSparseArray = new SparseArray();
        }
        localView.saveHierarchyState(localSparseArray);
        if (localMenuItem.isActionViewExpanded()) {
          paramBundle.putInt("android:menu:expandedactionview", localMenuItem.getItemId());
        }
      }
      if (localMenuItem.hasSubMenu()) {
        ((SubMenuBuilder)localMenuItem.getSubMenu()).saveActionViewStates(paramBundle);
      }
    }
  }
  
  public void savePresenterStates(Bundle paramBundle)
  {
    dispatchSaveInstanceState(paramBundle);
  }
  
  public void setCallback(Callback paramCallback)
  {
    this.mCallback = paramCallback;
  }
  
  public void setCurrentMenuInfo(ContextMenu.ContextMenuInfo paramContextMenuInfo)
  {
    this.mCurrentMenuInfo = paramContextMenuInfo;
  }
  
  public MenuBuilder setDefaultShowAsAction(int paramInt)
  {
    this.mDefaultShowAsAction = paramInt;
    return this;
  }
  
  void setExclusiveItemChecked(com.actionbarsherlock.view.MenuItem paramMenuItem)
  {
    int i = paramMenuItem.getGroupId();
    int j = this.mItems.size();
    int k = 0;
    if (k >= j) {
      return;
    }
    MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mItems.get(k);
    if ((localMenuItemImpl.getGroupId() != i) || (!localMenuItemImpl.isExclusiveCheckable())) {}
    while (!localMenuItemImpl.isCheckable())
    {
      k++;
      break;
    }
    if (localMenuItemImpl == paramMenuItem) {}
    for (boolean bool = true;; bool = false)
    {
      localMenuItemImpl.setCheckedInt(bool);
      break;
    }
  }
  
  public void setGroupCheckable(int paramInt, boolean paramBoolean1, boolean paramBoolean2)
  {
    int i = this.mItems.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mItems.get(j);
      if (localMenuItemImpl.getGroupId() == paramInt)
      {
        localMenuItemImpl.setExclusiveCheckable(paramBoolean2);
        localMenuItemImpl.setCheckable(paramBoolean1);
      }
    }
  }
  
  public void setGroupEnabled(int paramInt, boolean paramBoolean)
  {
    int i = this.mItems.size();
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mItems.get(j);
      if (localMenuItemImpl.getGroupId() == paramInt) {
        localMenuItemImpl.setEnabled(paramBoolean);
      }
    }
  }
  
  public void setGroupVisible(int paramInt, boolean paramBoolean)
  {
    int i = this.mItems.size();
    int j = 0;
    for (int k = 0;; k++)
    {
      if (k >= i)
      {
        if (j != 0) {
          onItemsChanged(true);
        }
        return;
      }
      MenuItemImpl localMenuItemImpl = (MenuItemImpl)this.mItems.get(k);
      if ((localMenuItemImpl.getGroupId() == paramInt) && (localMenuItemImpl.setVisibleInt(paramBoolean))) {
        j = 1;
      }
    }
  }
  
  protected MenuBuilder setHeaderIconInt(int paramInt)
  {
    setHeaderInternal(0, null, paramInt, null, null);
    return this;
  }
  
  protected MenuBuilder setHeaderIconInt(Drawable paramDrawable)
  {
    setHeaderInternal(0, null, 0, paramDrawable, null);
    return this;
  }
  
  protected MenuBuilder setHeaderTitleInt(int paramInt)
  {
    setHeaderInternal(paramInt, null, 0, null, null);
    return this;
  }
  
  protected MenuBuilder setHeaderTitleInt(CharSequence paramCharSequence)
  {
    setHeaderInternal(0, paramCharSequence, 0, null, null);
    return this;
  }
  
  protected MenuBuilder setHeaderViewInt(View paramView)
  {
    setHeaderInternal(0, null, 0, null, paramView);
    return this;
  }
  
  void setOptionalIconsVisible(boolean paramBoolean)
  {
    this.mOptionalIconsVisible = paramBoolean;
  }
  
  public void setQwertyMode(boolean paramBoolean)
  {
    this.mQwertyMode = paramBoolean;
    onItemsChanged(false);
  }
  
  public void setShortcutsVisible(boolean paramBoolean)
  {
    if (this.mShortcutsVisible == paramBoolean) {
      return;
    }
    setShortcutsVisibleInner(paramBoolean);
    onItemsChanged(false);
  }
  
  public int size()
  {
    return this.mItems.size();
  }
  
  public void startDispatchingItemsChanged()
  {
    this.mPreventDispatchingItemsChanged = false;
    if (this.mItemsChangedWhileDispatchPrevented)
    {
      this.mItemsChangedWhileDispatchPrevented = false;
      onItemsChanged(true);
    }
  }
  
  public void stopDispatchingItemsChanged()
  {
    if (!this.mPreventDispatchingItemsChanged)
    {
      this.mPreventDispatchingItemsChanged = true;
      this.mItemsChangedWhileDispatchPrevented = false;
    }
  }
  
  public static abstract interface Callback
  {
    public abstract boolean onMenuItemSelected(MenuBuilder paramMenuBuilder, com.actionbarsherlock.view.MenuItem paramMenuItem);
    
    public abstract void onMenuModeChange(MenuBuilder paramMenuBuilder);
  }
  
  public static abstract interface ItemInvoker
  {
    public abstract boolean invokeItem(MenuItemImpl paramMenuItemImpl);
  }
}
