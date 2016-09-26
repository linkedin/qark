package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.res.TypedArray;
import android.database.DataSetObserver;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.SpinnerAdapter;
import com.actionbarsherlock.R.attr;
import com.actionbarsherlock.R.styleable;

public class IcsSpinner
  extends IcsAbsSpinner
  implements DialogInterface.OnClickListener
{
  private static final int MAX_ITEMS_MEASURED = 15;
  public static final int MODE_DROPDOWN = 1;
  private boolean mDisableChildrenWhenDisabled;
  int mDropDownWidth;
  private int mGravity;
  private SpinnerPopup mPopup;
  private DropDownAdapter mTempAdapter;
  private Rect mTempRect = new Rect();
  
  public IcsSpinner(Context paramContext, AttributeSet paramAttributeSet)
  {
    this(paramContext, paramAttributeSet, R.attr.actionDropDownStyle);
  }
  
  public IcsSpinner(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockSpinner, paramInt, 0);
    DropdownPopup localDropdownPopup = new DropdownPopup(paramContext, paramAttributeSet, paramInt);
    this.mDropDownWidth = localTypedArray.getLayoutDimension(4, -2);
    localDropdownPopup.setBackgroundDrawable(localTypedArray.getDrawable(2));
    int i = localTypedArray.getDimensionPixelOffset(6, 0);
    if (i != 0) {
      localDropdownPopup.setVerticalOffset(i);
    }
    int j = localTypedArray.getDimensionPixelOffset(5, 0);
    if (j != 0) {
      localDropdownPopup.setHorizontalOffset(j);
    }
    this.mPopup = localDropdownPopup;
    this.mGravity = localTypedArray.getInt(0, 17);
    this.mPopup.setPromptText(localTypedArray.getString(3));
    this.mDisableChildrenWhenDisabled = true;
    localTypedArray.recycle();
    if (this.mTempAdapter != null)
    {
      this.mPopup.setAdapter(this.mTempAdapter);
      this.mTempAdapter = null;
    }
  }
  
  private View makeAndAddView(int paramInt)
  {
    if (!this.mDataChanged)
    {
      View localView2 = this.mRecycler.get(paramInt);
      if (localView2 != null)
      {
        setUpChild(localView2);
        return localView2;
      }
    }
    View localView1 = this.mAdapter.getView(paramInt, null, this);
    setUpChild(localView1);
    return localView1;
  }
  
  private void setUpChild(View paramView)
  {
    ViewGroup.LayoutParams localLayoutParams = paramView.getLayoutParams();
    if (localLayoutParams == null) {
      localLayoutParams = generateDefaultLayoutParams();
    }
    addViewInLayout(paramView, 0, localLayoutParams);
    paramView.setSelected(hasFocus());
    if (this.mDisableChildrenWhenDisabled) {
      paramView.setEnabled(isEnabled());
    }
    int i = ViewGroup.getChildMeasureSpec(this.mHeightMeasureSpec, this.mSpinnerPadding.top + this.mSpinnerPadding.bottom, localLayoutParams.height);
    paramView.measure(ViewGroup.getChildMeasureSpec(this.mWidthMeasureSpec, this.mSpinnerPadding.left + this.mSpinnerPadding.right, localLayoutParams.width), i);
    int j = this.mSpinnerPadding.top + (getMeasuredHeight() - this.mSpinnerPadding.bottom - this.mSpinnerPadding.top - paramView.getMeasuredHeight()) / 2;
    int k = j + paramView.getMeasuredHeight();
    paramView.layout(0, j, 0 + paramView.getMeasuredWidth(), k);
  }
  
  public int getBaseline()
  {
    int i = -1;
    View localView;
    if (getChildCount() > 0) {
      localView = getChildAt(0);
    }
    for (;;)
    {
      if (localView != null)
      {
        int k = localView.getBaseline();
        if (k >= 0) {
          i = k + localView.getTop();
        }
      }
      return i;
      SpinnerAdapter localSpinnerAdapter = this.mAdapter;
      localView = null;
      if (localSpinnerAdapter != null)
      {
        int j = this.mAdapter.getCount();
        localView = null;
        if (j > 0)
        {
          localView = makeAndAddView(0);
          this.mRecycler.put(0, localView);
          removeAllViewsInLayout();
        }
      }
    }
  }
  
  public CharSequence getPrompt()
  {
    return this.mPopup.getHintText();
  }
  
  void layout(int paramInt, boolean paramBoolean)
  {
    int i = this.mSpinnerPadding.left;
    int j = getRight() - getLeft() - this.mSpinnerPadding.left - this.mSpinnerPadding.right;
    if (this.mDataChanged) {
      handleDataChanged();
    }
    if (this.mItemCount == 0)
    {
      resetList();
      return;
    }
    if (this.mNextSelectedPosition >= 0) {
      setSelectedPositionInt(this.mNextSelectedPosition);
    }
    recycleAllViews();
    removeAllViewsInLayout();
    this.mFirstPosition = this.mSelectedPosition;
    View localView = makeAndAddView(this.mSelectedPosition);
    int k = localView.getMeasuredWidth();
    int m = i;
    switch (0x7 & this.mGravity)
    {
    }
    for (;;)
    {
      localView.offsetLeftAndRight(m);
      this.mRecycler.clear();
      invalidate();
      checkSelectionChanged();
      this.mDataChanged = false;
      this.mNeedSync = false;
      setNextSelectedPositionInt(this.mSelectedPosition);
      return;
      m = i + j / 2 - k / 2;
      continue;
      m = i + j - k;
    }
  }
  
  int measureContentWidth(SpinnerAdapter paramSpinnerAdapter, Drawable paramDrawable)
  {
    if (paramSpinnerAdapter == null)
    {
      i = 0;
      return i;
    }
    int i = 0;
    View localView = null;
    int j = 0;
    int k = View.MeasureSpec.makeMeasureSpec(0, 0);
    int m = View.MeasureSpec.makeMeasureSpec(0, 0);
    int n = Math.max(0, getSelectedItemPosition());
    int i1 = Math.min(paramSpinnerAdapter.getCount(), n + 15);
    for (int i2 = Math.max(0, n - (15 - (i1 - n)));; i2++)
    {
      if (i2 >= i1)
      {
        if (paramDrawable == null) {
          break;
        }
        paramDrawable.getPadding(this.mTempRect);
        return i + (this.mTempRect.left + this.mTempRect.right);
      }
      int i3 = paramSpinnerAdapter.getItemViewType(i2);
      if (i3 != j)
      {
        j = i3;
        localView = null;
      }
      localView = paramSpinnerAdapter.getView(i2, localView, this);
      if (localView.getLayoutParams() == null) {
        localView.setLayoutParams(new ViewGroup.LayoutParams(-2, -2));
      }
      localView.measure(k, m);
      i = Math.max(i, localView.getMeasuredWidth());
    }
  }
  
  public void onClick(DialogInterface paramDialogInterface, int paramInt)
  {
    setSelection(paramInt);
    paramDialogInterface.dismiss();
  }
  
  protected void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    if ((this.mPopup != null) && (this.mPopup.isShowing())) {
      this.mPopup.dismiss();
    }
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    super.onLayout(paramBoolean, paramInt1, paramInt2, paramInt3, paramInt4);
    this.mInLayout = true;
    layout(0, false);
    this.mInLayout = false;
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    super.onMeasure(paramInt1, paramInt2);
    if ((this.mPopup != null) && (View.MeasureSpec.getMode(paramInt1) == Integer.MIN_VALUE)) {
      setMeasuredDimension(Math.min(Math.max(getMeasuredWidth(), measureContentWidth(getAdapter(), getBackground())), View.MeasureSpec.getSize(paramInt1)), getMeasuredHeight());
    }
  }
  
  public boolean performClick()
  {
    boolean bool = super.performClick();
    if (!bool)
    {
      bool = true;
      if (!this.mPopup.isShowing()) {
        this.mPopup.show();
      }
    }
    return bool;
  }
  
  public void setAdapter(SpinnerAdapter paramSpinnerAdapter)
  {
    super.setAdapter(paramSpinnerAdapter);
    if (this.mPopup != null)
    {
      this.mPopup.setAdapter(new DropDownAdapter(paramSpinnerAdapter));
      return;
    }
    this.mTempAdapter = new DropDownAdapter(paramSpinnerAdapter);
  }
  
  public void setEnabled(boolean paramBoolean)
  {
    super.setEnabled(paramBoolean);
    int i;
    if (this.mDisableChildrenWhenDisabled) {
      i = getChildCount();
    }
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      getChildAt(j).setEnabled(paramBoolean);
    }
  }
  
  public void setGravity(int paramInt)
  {
    if (this.mGravity != paramInt)
    {
      if ((paramInt & 0x7) == 0) {
        paramInt |= 0x3;
      }
      this.mGravity = paramInt;
      requestLayout();
    }
  }
  
  public void setOnItemClickListener(AdapterView.OnItemClickListener paramOnItemClickListener)
  {
    throw new RuntimeException("setOnItemClickListener cannot be used with a spinner.");
  }
  
  public void setPrompt(CharSequence paramCharSequence)
  {
    this.mPopup.setPromptText(paramCharSequence);
  }
  
  public void setPromptId(int paramInt)
  {
    setPrompt(getContext().getText(paramInt));
  }
  
  private static class DropDownAdapter
    implements ListAdapter, SpinnerAdapter
  {
    private SpinnerAdapter mAdapter;
    private ListAdapter mListAdapter;
    
    public DropDownAdapter(SpinnerAdapter paramSpinnerAdapter)
    {
      this.mAdapter = paramSpinnerAdapter;
      if ((paramSpinnerAdapter instanceof ListAdapter)) {
        this.mListAdapter = ((ListAdapter)paramSpinnerAdapter);
      }
    }
    
    public boolean areAllItemsEnabled()
    {
      ListAdapter localListAdapter = this.mListAdapter;
      if (localListAdapter != null) {
        return localListAdapter.areAllItemsEnabled();
      }
      return true;
    }
    
    public int getCount()
    {
      if (this.mAdapter == null) {
        return 0;
      }
      return this.mAdapter.getCount();
    }
    
    public View getDropDownView(int paramInt, View paramView, ViewGroup paramViewGroup)
    {
      if (this.mAdapter == null) {
        return null;
      }
      return this.mAdapter.getDropDownView(paramInt, paramView, paramViewGroup);
    }
    
    public Object getItem(int paramInt)
    {
      if (this.mAdapter == null) {
        return null;
      }
      return this.mAdapter.getItem(paramInt);
    }
    
    public long getItemId(int paramInt)
    {
      if (this.mAdapter == null) {
        return -1L;
      }
      return this.mAdapter.getItemId(paramInt);
    }
    
    public int getItemViewType(int paramInt)
    {
      return 0;
    }
    
    public View getView(int paramInt, View paramView, ViewGroup paramViewGroup)
    {
      return getDropDownView(paramInt, paramView, paramViewGroup);
    }
    
    public int getViewTypeCount()
    {
      return 1;
    }
    
    public boolean hasStableIds()
    {
      return (this.mAdapter != null) && (this.mAdapter.hasStableIds());
    }
    
    public boolean isEmpty()
    {
      return getCount() == 0;
    }
    
    public boolean isEnabled(int paramInt)
    {
      ListAdapter localListAdapter = this.mListAdapter;
      if (localListAdapter != null) {
        return localListAdapter.isEnabled(paramInt);
      }
      return true;
    }
    
    public void registerDataSetObserver(DataSetObserver paramDataSetObserver)
    {
      if (this.mAdapter != null) {
        this.mAdapter.registerDataSetObserver(paramDataSetObserver);
      }
    }
    
    public void unregisterDataSetObserver(DataSetObserver paramDataSetObserver)
    {
      if (this.mAdapter != null) {
        this.mAdapter.unregisterDataSetObserver(paramDataSetObserver);
      }
    }
  }
  
  private class DropdownPopup
    extends IcsListPopupWindow
    implements IcsSpinner.SpinnerPopup
  {
    private ListAdapter mAdapter;
    private CharSequence mHintText;
    
    public DropdownPopup(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
    {
      super(paramAttributeSet, 0, paramInt);
      setAnchorView(IcsSpinner.this);
      setModal(true);
      setPromptPosition(0);
      setOnItemClickListener(new AdapterView.OnItemClickListener()
      {
        public void onItemClick(AdapterView paramAnonymousAdapterView, View paramAnonymousView, int paramAnonymousInt, long paramAnonymousLong)
        {
          IcsSpinner.this.setSelection(paramAnonymousInt);
          IcsSpinner.DropdownPopup.this.dismiss();
        }
      });
    }
    
    public CharSequence getHintText()
    {
      return this.mHintText;
    }
    
    public void setAdapter(ListAdapter paramListAdapter)
    {
      super.setAdapter(paramListAdapter);
      this.mAdapter = paramListAdapter;
    }
    
    public void setPromptText(CharSequence paramCharSequence)
    {
      this.mHintText = paramCharSequence;
    }
    
    public void show()
    {
      int i = IcsSpinner.this.getPaddingLeft();
      if (IcsSpinner.this.mDropDownWidth == -2)
      {
        int n = IcsSpinner.this.getWidth();
        int i1 = IcsSpinner.this.getPaddingRight();
        setContentWidth(Math.max(IcsSpinner.this.measureContentWidth((SpinnerAdapter)this.mAdapter, IcsSpinner.this.getBackground()), n - i - i1));
      }
      for (;;)
      {
        Drawable localDrawable = IcsSpinner.this.getBackground();
        int j = 0;
        if (localDrawable != null)
        {
          localDrawable.getPadding(IcsSpinner.this.mTempRect);
          j = -IcsSpinner.this.mTempRect.left;
        }
        setHorizontalOffset(j + i);
        setInputMethodMode(2);
        super.show();
        getListView().setChoiceMode(1);
        IcsSpinner.this.setSelection(IcsSpinner.this.getSelectedItemPosition());
        return;
        if (IcsSpinner.this.mDropDownWidth == -1)
        {
          int k = IcsSpinner.this.getWidth();
          int m = IcsSpinner.this.getPaddingRight();
          setContentWidth(k - i - m);
        }
        else
        {
          setContentWidth(IcsSpinner.this.mDropDownWidth);
        }
      }
    }
  }
  
  private static abstract interface SpinnerPopup
  {
    public abstract void dismiss();
    
    public abstract CharSequence getHintText();
    
    public abstract boolean isShowing();
    
    public abstract void setAdapter(ListAdapter paramListAdapter);
    
    public abstract void setPromptText(CharSequence paramCharSequence);
    
    public abstract void show();
  }
}
