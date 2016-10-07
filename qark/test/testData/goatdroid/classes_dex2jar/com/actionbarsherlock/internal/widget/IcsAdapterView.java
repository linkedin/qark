package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.database.DataSetObserver;
import android.os.Parcelable;
import android.os.SystemClock;
import android.util.AttributeSet;
import android.util.SparseArray;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewDebug.CapturedViewProperty;
import android.view.ViewDebug.ExportedProperty;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;
import android.widget.Adapter;
import android.widget.AdapterView.OnItemClickListener;

public abstract class IcsAdapterView<T extends Adapter>
  extends ViewGroup
{
  public static final int INVALID_POSITION = -1;
  public static final long INVALID_ROW_ID = Long.MIN_VALUE;
  public static final int ITEM_VIEW_TYPE_HEADER_OR_FOOTER = -2;
  public static final int ITEM_VIEW_TYPE_IGNORE = -1;
  static final int SYNC_FIRST_POSITION = 1;
  static final int SYNC_MAX_DURATION_MILLIS = 100;
  static final int SYNC_SELECTED_POSITION;
  boolean mBlockLayoutRequests = false;
  boolean mDataChanged;
  private boolean mDesiredFocusableInTouchModeState;
  private boolean mDesiredFocusableState;
  private View mEmptyView;
  @ViewDebug.ExportedProperty(category="scrolling")
  int mFirstPosition = 0;
  boolean mInLayout = false;
  @ViewDebug.ExportedProperty(category="list")
  int mItemCount;
  private int mLayoutHeight;
  boolean mNeedSync = false;
  @ViewDebug.ExportedProperty(category="list")
  int mNextSelectedPosition = -1;
  long mNextSelectedRowId = Long.MIN_VALUE;
  int mOldItemCount;
  int mOldSelectedPosition = -1;
  long mOldSelectedRowId = Long.MIN_VALUE;
  AdapterView.OnItemClickListener mOnItemClickListener;
  OnItemLongClickListener mOnItemLongClickListener;
  OnItemSelectedListener mOnItemSelectedListener;
  @ViewDebug.ExportedProperty(category="list")
  int mSelectedPosition = -1;
  long mSelectedRowId = Long.MIN_VALUE;
  private IcsAdapterView<T>.SelectionNotifier mSelectionNotifier;
  int mSpecificTop;
  long mSyncHeight;
  int mSyncMode;
  int mSyncPosition;
  long mSyncRowId = Long.MIN_VALUE;
  
  public IcsAdapterView(Context paramContext)
  {
    super(paramContext);
  }
  
  public IcsAdapterView(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
  }
  
  public IcsAdapterView(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
  }
  
  private void fireOnSelected()
  {
    if (this.mOnItemSelectedListener == null) {
      return;
    }
    int i = getSelectedItemPosition();
    if (i >= 0)
    {
      View localView = getSelectedView();
      this.mOnItemSelectedListener.onItemSelected(this, localView, i, getAdapter().getItemId(i));
      return;
    }
    this.mOnItemSelectedListener.onNothingSelected(this);
  }
  
  private boolean isScrollableForAccessibility()
  {
    Adapter localAdapter = getAdapter();
    boolean bool = false;
    if (localAdapter != null)
    {
      int i = localAdapter.getCount();
      bool = false;
      if (i > 0) {
        if (getFirstVisiblePosition() <= 0)
        {
          int j = getLastVisiblePosition();
          int k = i - 1;
          bool = false;
          if (j >= k) {}
        }
        else
        {
          bool = true;
        }
      }
    }
    return bool;
  }
  
  private void updateEmptyStatus(boolean paramBoolean)
  {
    if (isInFilterMode()) {
      paramBoolean = false;
    }
    if (paramBoolean)
    {
      if (this.mEmptyView != null)
      {
        this.mEmptyView.setVisibility(0);
        setVisibility(8);
      }
      for (;;)
      {
        if (this.mDataChanged) {
          onLayout(false, getLeft(), getTop(), getRight(), getBottom());
        }
        return;
        setVisibility(0);
      }
    }
    if (this.mEmptyView != null) {
      this.mEmptyView.setVisibility(8);
    }
    setVisibility(0);
  }
  
  public void addView(View paramView)
  {
    throw new UnsupportedOperationException("addView(View) is not supported in AdapterView");
  }
  
  public void addView(View paramView, int paramInt)
  {
    throw new UnsupportedOperationException("addView(View, int) is not supported in AdapterView");
  }
  
  public void addView(View paramView, int paramInt, ViewGroup.LayoutParams paramLayoutParams)
  {
    throw new UnsupportedOperationException("addView(View, int, LayoutParams) is not supported in AdapterView");
  }
  
  public void addView(View paramView, ViewGroup.LayoutParams paramLayoutParams)
  {
    throw new UnsupportedOperationException("addView(View, LayoutParams) is not supported in AdapterView");
  }
  
  protected boolean canAnimate()
  {
    return (super.canAnimate()) && (this.mItemCount > 0);
  }
  
  void checkFocus()
  {
    Adapter localAdapter = getAdapter();
    int i;
    int j;
    label33:
    boolean bool1;
    label47:
    boolean bool2;
    label67:
    boolean bool3;
    if ((localAdapter != null) && (localAdapter.getCount() != 0))
    {
      i = 0;
      if ((i == 0) || (isInFilterMode())) {
        break label112;
      }
      j = 0;
      if ((j == 0) || (!this.mDesiredFocusableInTouchModeState)) {
        break label117;
      }
      bool1 = true;
      super.setFocusableInTouchMode(bool1);
      if ((j == 0) || (!this.mDesiredFocusableState)) {
        break label123;
      }
      bool2 = true;
      super.setFocusable(bool2);
      if (this.mEmptyView != null)
      {
        if (localAdapter == null) {
          break label129;
        }
        boolean bool4 = localAdapter.isEmpty();
        bool3 = false;
        if (bool4) {
          break label129;
        }
      }
    }
    for (;;)
    {
      updateEmptyStatus(bool3);
      return;
      i = 1;
      break;
      label112:
      j = 1;
      break label33;
      label117:
      bool1 = false;
      break label47;
      label123:
      bool2 = false;
      break label67;
      label129:
      bool3 = true;
    }
  }
  
  void checkSelectionChanged()
  {
    if ((this.mSelectedPosition != this.mOldSelectedPosition) || (this.mSelectedRowId != this.mOldSelectedRowId))
    {
      selectionChanged();
      this.mOldSelectedPosition = this.mSelectedPosition;
      this.mOldSelectedRowId = this.mSelectedRowId;
    }
  }
  
  public boolean dispatchPopulateAccessibilityEvent(AccessibilityEvent paramAccessibilityEvent)
  {
    View localView = getSelectedView();
    return (localView != null) && (localView.getVisibility() == 0) && (localView.dispatchPopulateAccessibilityEvent(paramAccessibilityEvent));
  }
  
  protected void dispatchRestoreInstanceState(SparseArray<Parcelable> paramSparseArray)
  {
    dispatchThawSelfOnly(paramSparseArray);
  }
  
  protected void dispatchSaveInstanceState(SparseArray<Parcelable> paramSparseArray)
  {
    dispatchFreezeSelfOnly(paramSparseArray);
  }
  
  int findSyncPosition()
  {
    int i = this.mItemCount;
    if (i == 0)
    {
      m = -1;
      return m;
    }
    long l1 = this.mSyncRowId;
    int j = this.mSyncPosition;
    if (l1 == Long.MIN_VALUE) {
      return -1;
    }
    int k = Math.max(0, j);
    int m = Math.min(i - 1, k);
    long l2 = 100L + SystemClock.uptimeMillis();
    int n = m;
    int i1 = m;
    Adapter localAdapter = getAdapter();
    int i2 = 0;
    if (localAdapter == null) {
      return -1;
    }
    label138:
    label144:
    label207:
    while (localAdapter.getItemId(m) != l1)
    {
      int i3;
      if (i1 == i - 1)
      {
        i3 = 1;
        if (n != 0) {
          break label138;
        }
      }
      for (int i4 = 1;; i4 = 0)
      {
        if ((i3 == 0) || (i4 == 0)) {
          break label144;
        }
        return -1;
        i3 = 0;
        break;
      }
      if ((i4 != 0) || ((i2 != 0) && (i3 == 0)))
      {
        i1++;
        m = i1;
      }
      for (i2 = 0;; i2 = 1)
      {
        do
        {
          if (SystemClock.uptimeMillis() <= l2) {
            break label207;
          }
          break;
        } while ((i3 == 0) && ((i2 != 0) || (i4 != 0)));
        n--;
        m = n;
      }
    }
  }
  
  public abstract T getAdapter();
  
  @ViewDebug.CapturedViewProperty
  public int getCount()
  {
    return this.mItemCount;
  }
  
  public View getEmptyView()
  {
    return this.mEmptyView;
  }
  
  public int getFirstVisiblePosition()
  {
    return this.mFirstPosition;
  }
  
  public Object getItemAtPosition(int paramInt)
  {
    Adapter localAdapter = getAdapter();
    if ((localAdapter == null) || (paramInt < 0)) {
      return null;
    }
    return localAdapter.getItem(paramInt);
  }
  
  public long getItemIdAtPosition(int paramInt)
  {
    Adapter localAdapter = getAdapter();
    if ((localAdapter == null) || (paramInt < 0)) {
      return Long.MIN_VALUE;
    }
    return localAdapter.getItemId(paramInt);
  }
  
  public int getLastVisiblePosition()
  {
    return -1 + (this.mFirstPosition + getChildCount());
  }
  
  public final AdapterView.OnItemClickListener getOnItemClickListener()
  {
    return this.mOnItemClickListener;
  }
  
  public final OnItemLongClickListener getOnItemLongClickListener()
  {
    return this.mOnItemLongClickListener;
  }
  
  public final OnItemSelectedListener getOnItemSelectedListener()
  {
    return this.mOnItemSelectedListener;
  }
  
  public int getPositionForView(View paramView)
  {
    Object localObject = paramView;
    for (;;)
    {
      int j;
      try
      {
        View localView = (View)((View)localObject).getParent();
        boolean bool = localView.equals(this);
        if (bool)
        {
          int i = getChildCount();
          j = 0;
          if (j >= i) {
            return -1;
          }
        }
        else
        {
          localObject = localView;
          continue;
        }
        if (!getChildAt(j).equals(localObject)) {
          break label72;
        }
      }
      catch (ClassCastException localClassCastException)
      {
        return -1;
      }
      return j + this.mFirstPosition;
      label72:
      j++;
    }
  }
  
  public Object getSelectedItem()
  {
    Adapter localAdapter = getAdapter();
    int i = getSelectedItemPosition();
    if ((localAdapter != null) && (localAdapter.getCount() > 0) && (i >= 0)) {
      return localAdapter.getItem(i);
    }
    return null;
  }
  
  @ViewDebug.CapturedViewProperty
  public long getSelectedItemId()
  {
    return this.mNextSelectedRowId;
  }
  
  @ViewDebug.CapturedViewProperty
  public int getSelectedItemPosition()
  {
    return this.mNextSelectedPosition;
  }
  
  public abstract View getSelectedView();
  
  void handleDataChanged()
  {
    int i = this.mItemCount;
    int j = 0;
    if (i > 0)
    {
      boolean bool = this.mNeedSync;
      j = 0;
      if (bool)
      {
        this.mNeedSync = false;
        int n = findSyncPosition();
        j = 0;
        if (n >= 0)
        {
          int i1 = lookForSelectablePosition(n, true);
          j = 0;
          if (i1 == n)
          {
            setNextSelectedPositionInt(n);
            j = 1;
          }
        }
      }
      if (j == 0)
      {
        int k = getSelectedItemPosition();
        if (k >= i) {
          k = i - 1;
        }
        if (k < 0) {
          k = 0;
        }
        int m = lookForSelectablePosition(k, true);
        if (m < 0) {
          m = lookForSelectablePosition(k, false);
        }
        if (m >= 0)
        {
          setNextSelectedPositionInt(m);
          checkSelectionChanged();
          j = 1;
        }
      }
    }
    if (j == 0)
    {
      this.mSelectedPosition = -1;
      this.mSelectedRowId = Long.MIN_VALUE;
      this.mNextSelectedPosition = -1;
      this.mNextSelectedRowId = Long.MIN_VALUE;
      this.mNeedSync = false;
      checkSelectionChanged();
    }
  }
  
  boolean isInFilterMode()
  {
    return false;
  }
  
  int lookForSelectablePosition(int paramInt, boolean paramBoolean)
  {
    return paramInt;
  }
  
  protected void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    removeCallbacks(this.mSelectionNotifier);
  }
  
  public void onInitializeAccessibilityEvent(AccessibilityEvent paramAccessibilityEvent)
  {
    super.onInitializeAccessibilityEvent(paramAccessibilityEvent);
    paramAccessibilityEvent.setScrollable(isScrollableForAccessibility());
    View localView = getSelectedView();
    if (localView != null) {
      paramAccessibilityEvent.setEnabled(localView.isEnabled());
    }
    paramAccessibilityEvent.setCurrentItemIndex(getSelectedItemPosition());
    paramAccessibilityEvent.setFromIndex(getFirstVisiblePosition());
    paramAccessibilityEvent.setToIndex(getLastVisiblePosition());
    paramAccessibilityEvent.setItemCount(getCount());
  }
  
  public void onInitializeAccessibilityNodeInfo(AccessibilityNodeInfo paramAccessibilityNodeInfo)
  {
    super.onInitializeAccessibilityNodeInfo(paramAccessibilityNodeInfo);
    paramAccessibilityNodeInfo.setScrollable(isScrollableForAccessibility());
    View localView = getSelectedView();
    if (localView != null) {
      paramAccessibilityNodeInfo.setEnabled(localView.isEnabled());
    }
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    this.mLayoutHeight = getHeight();
  }
  
  public boolean onRequestSendAccessibilityEvent(View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    if (super.onRequestSendAccessibilityEvent(paramView, paramAccessibilityEvent))
    {
      AccessibilityEvent localAccessibilityEvent = AccessibilityEvent.obtain();
      onInitializeAccessibilityEvent(localAccessibilityEvent);
      paramView.dispatchPopulateAccessibilityEvent(localAccessibilityEvent);
      paramAccessibilityEvent.appendRecord(localAccessibilityEvent);
      return true;
    }
    return false;
  }
  
  public boolean performItemClick(View paramView, int paramInt, long paramLong)
  {
    AdapterView.OnItemClickListener localOnItemClickListener = this.mOnItemClickListener;
    boolean bool = false;
    if (localOnItemClickListener != null)
    {
      playSoundEffect(0);
      if (paramView != null) {
        paramView.sendAccessibilityEvent(1);
      }
      this.mOnItemClickListener.onItemClick(null, paramView, paramInt, paramLong);
      bool = true;
    }
    return bool;
  }
  
  void rememberSyncState()
  {
    if (getChildCount() > 0)
    {
      this.mNeedSync = true;
      this.mSyncHeight = this.mLayoutHeight;
      if (this.mSelectedPosition >= 0)
      {
        View localView2 = getChildAt(this.mSelectedPosition - this.mFirstPosition);
        this.mSyncRowId = this.mNextSelectedRowId;
        this.mSyncPosition = this.mNextSelectedPosition;
        if (localView2 != null) {
          this.mSpecificTop = localView2.getTop();
        }
        this.mSyncMode = 0;
      }
    }
    else
    {
      return;
    }
    View localView1 = getChildAt(0);
    Adapter localAdapter = getAdapter();
    if ((this.mFirstPosition >= 0) && (this.mFirstPosition < localAdapter.getCount())) {}
    for (this.mSyncRowId = localAdapter.getItemId(this.mFirstPosition);; this.mSyncRowId = -1L)
    {
      this.mSyncPosition = this.mFirstPosition;
      if (localView1 != null) {
        this.mSpecificTop = localView1.getTop();
      }
      this.mSyncMode = 1;
      return;
    }
  }
  
  public void removeAllViews()
  {
    throw new UnsupportedOperationException("removeAllViews() is not supported in AdapterView");
  }
  
  public void removeView(View paramView)
  {
    throw new UnsupportedOperationException("removeView(View) is not supported in AdapterView");
  }
  
  public void removeViewAt(int paramInt)
  {
    throw new UnsupportedOperationException("removeViewAt(int) is not supported in AdapterView");
  }
  
  void selectionChanged()
  {
    if (this.mOnItemSelectedListener != null)
    {
      if ((!this.mInLayout) && (!this.mBlockLayoutRequests)) {
        break label78;
      }
      if (this.mSelectionNotifier == null) {
        this.mSelectionNotifier = new SelectionNotifier(null);
      }
      post(this.mSelectionNotifier);
    }
    for (;;)
    {
      if ((this.mSelectedPosition != -1) && (isShown()) && (!isInTouchMode())) {
        sendAccessibilityEvent(4);
      }
      return;
      label78:
      fireOnSelected();
    }
  }
  
  public abstract void setAdapter(T paramT);
  
  public void setEmptyView(View paramView)
  {
    this.mEmptyView = paramView;
    Adapter localAdapter = getAdapter();
    if ((localAdapter != null) && (!localAdapter.isEmpty())) {}
    for (boolean bool = false;; bool = true)
    {
      updateEmptyStatus(bool);
      return;
    }
  }
  
  public void setFocusable(boolean paramBoolean)
  {
    boolean bool = true;
    Adapter localAdapter = getAdapter();
    int i;
    if ((localAdapter != null) && (localAdapter.getCount() != 0))
    {
      i = 0;
      this.mDesiredFocusableState = paramBoolean;
      if (!paramBoolean) {
        this.mDesiredFocusableInTouchModeState = false;
      }
      if ((!paramBoolean) || ((i != 0) && (!isInFilterMode()))) {
        break label65;
      }
    }
    for (;;)
    {
      super.setFocusable(bool);
      return;
      i = bool;
      break;
      label65:
      bool = false;
    }
  }
  
  public void setFocusableInTouchMode(boolean paramBoolean)
  {
    boolean bool = true;
    Adapter localAdapter = getAdapter();
    int i;
    if ((localAdapter != null) && (localAdapter.getCount() != 0))
    {
      i = 0;
      this.mDesiredFocusableInTouchModeState = paramBoolean;
      if (paramBoolean) {
        this.mDesiredFocusableState = bool;
      }
      if ((!paramBoolean) || ((i != 0) && (!isInFilterMode()))) {
        break label65;
      }
    }
    for (;;)
    {
      super.setFocusableInTouchMode(bool);
      return;
      i = bool;
      break;
      label65:
      bool = false;
    }
  }
  
  void setNextSelectedPositionInt(int paramInt)
  {
    this.mNextSelectedPosition = paramInt;
    this.mNextSelectedRowId = getItemIdAtPosition(paramInt);
    if ((this.mNeedSync) && (this.mSyncMode == 0) && (paramInt >= 0))
    {
      this.mSyncPosition = paramInt;
      this.mSyncRowId = this.mNextSelectedRowId;
    }
  }
  
  public void setOnClickListener(View.OnClickListener paramOnClickListener)
  {
    throw new RuntimeException("Don't call setOnClickListener for an AdapterView. You probably want setOnItemClickListener instead");
  }
  
  public void setOnItemClickListener(AdapterView.OnItemClickListener paramOnItemClickListener)
  {
    this.mOnItemClickListener = paramOnItemClickListener;
  }
  
  public void setOnItemLongClickListener(OnItemLongClickListener paramOnItemLongClickListener)
  {
    if (!isLongClickable()) {
      setLongClickable(true);
    }
    this.mOnItemLongClickListener = paramOnItemLongClickListener;
  }
  
  public void setOnItemSelectedListener(OnItemSelectedListener paramOnItemSelectedListener)
  {
    this.mOnItemSelectedListener = paramOnItemSelectedListener;
  }
  
  void setSelectedPositionInt(int paramInt)
  {
    this.mSelectedPosition = paramInt;
    this.mSelectedRowId = getItemIdAtPosition(paramInt);
  }
  
  public abstract void setSelection(int paramInt);
  
  public static class AdapterContextMenuInfo
    implements ContextMenu.ContextMenuInfo
  {
    public long id;
    public int position;
    public View targetView;
    
    public AdapterContextMenuInfo(View paramView, int paramInt, long paramLong)
    {
      this.targetView = paramView;
      this.position = paramInt;
      this.id = paramLong;
    }
  }
  
  class AdapterDataSetObserver
    extends DataSetObserver
  {
    private Parcelable mInstanceState = null;
    
    AdapterDataSetObserver() {}
    
    public void clearSavedState()
    {
      this.mInstanceState = null;
    }
    
    public void onChanged()
    {
      IcsAdapterView.this.mDataChanged = true;
      IcsAdapterView.this.mOldItemCount = IcsAdapterView.this.mItemCount;
      IcsAdapterView.this.mItemCount = IcsAdapterView.this.getAdapter().getCount();
      if ((IcsAdapterView.this.getAdapter().hasStableIds()) && (this.mInstanceState != null) && (IcsAdapterView.this.mOldItemCount == 0) && (IcsAdapterView.this.mItemCount > 0))
      {
        IcsAdapterView.this.onRestoreInstanceState(this.mInstanceState);
        this.mInstanceState = null;
      }
      for (;;)
      {
        IcsAdapterView.this.checkFocus();
        IcsAdapterView.this.requestLayout();
        return;
        IcsAdapterView.this.rememberSyncState();
      }
    }
    
    public void onInvalidated()
    {
      IcsAdapterView.this.mDataChanged = true;
      if (IcsAdapterView.this.getAdapter().hasStableIds()) {
        this.mInstanceState = IcsAdapterView.this.onSaveInstanceState();
      }
      IcsAdapterView.this.mOldItemCount = IcsAdapterView.this.mItemCount;
      IcsAdapterView.this.mItemCount = 0;
      IcsAdapterView.this.mSelectedPosition = -1;
      IcsAdapterView.this.mSelectedRowId = Long.MIN_VALUE;
      IcsAdapterView.this.mNextSelectedPosition = -1;
      IcsAdapterView.this.mNextSelectedRowId = Long.MIN_VALUE;
      IcsAdapterView.this.mNeedSync = false;
      IcsAdapterView.this.checkFocus();
      IcsAdapterView.this.requestLayout();
    }
  }
  
  public static abstract interface OnItemLongClickListener
  {
    public abstract boolean onItemLongClick(IcsAdapterView<?> paramIcsAdapterView, View paramView, int paramInt, long paramLong);
  }
  
  public static abstract interface OnItemSelectedListener
  {
    public abstract void onItemSelected(IcsAdapterView<?> paramIcsAdapterView, View paramView, int paramInt, long paramLong);
    
    public abstract void onNothingSelected(IcsAdapterView<?> paramIcsAdapterView);
  }
  
  private class SelectionNotifier
    implements Runnable
  {
    private SelectionNotifier() {}
    
    public void run()
    {
      if (IcsAdapterView.this.mDataChanged)
      {
        if (IcsAdapterView.this.getAdapter() != null) {
          IcsAdapterView.this.post(this);
        }
        return;
      }
      IcsAdapterView.this.fireOnSelected();
    }
  }
}
