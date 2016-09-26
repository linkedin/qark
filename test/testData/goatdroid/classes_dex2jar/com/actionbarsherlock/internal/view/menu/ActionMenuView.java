package com.actionbarsherlock.internal.view.menu;

import android.content.Context;
import android.content.res.Configuration;
import android.content.res.Resources;
import android.graphics.Canvas;
import android.os.Build.VERSION;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.ViewGroup.LayoutParams;
import android.view.accessibility.AccessibilityEvent;
import android.widget.LinearLayout.LayoutParams;
import com.actionbarsherlock.internal.widget.IcsLinearLayout;

public class ActionMenuView
  extends IcsLinearLayout
  implements MenuBuilder.ItemInvoker, MenuView
{
  static final int GENERATED_ITEM_PADDING = 4;
  private static final boolean IS_FROYO = false;
  static final int MIN_CELL_SIZE = 56;
  private boolean mFirst = true;
  private boolean mFormatItems;
  private int mFormatItemsWidth;
  private int mGeneratedItemPadding;
  private MenuBuilder mMenu;
  private int mMinCellSize;
  private ActionMenuPresenter mPresenter;
  private boolean mReserveOverflow;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 8) {}
    for (boolean bool = true;; bool = false)
    {
      IS_FROYO = bool;
      return;
    }
  }
  
  public ActionMenuView(Context paramContext)
  {
    this(paramContext, null);
  }
  
  public ActionMenuView(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    setBaselineAligned(false);
    float f = paramContext.getResources().getDisplayMetrics().density;
    this.mMinCellSize = ((int)(56.0F * f));
    this.mGeneratedItemPadding = ((int)(4.0F * f));
  }
  
  static int measureChildForCells(View paramView, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    LayoutParams localLayoutParams = (LayoutParams)paramView.getLayoutParams();
    int i = View.MeasureSpec.makeMeasureSpec(View.MeasureSpec.getSize(paramInt3) - paramInt4, View.MeasureSpec.getMode(paramInt3));
    int j = 0;
    if (paramInt2 > 0)
    {
      paramView.measure(View.MeasureSpec.makeMeasureSpec(paramInt1 * paramInt2, Integer.MIN_VALUE), i);
      int k = paramView.getMeasuredWidth();
      j = k / paramInt1;
      if (k % paramInt1 != 0) {
        j++;
      }
    }
    ActionMenuItemView localActionMenuItemView;
    if ((paramView instanceof ActionMenuItemView))
    {
      localActionMenuItemView = (ActionMenuItemView)paramView;
      if ((localLayoutParams.isOverflowButton) || (localActionMenuItemView == null) || (!localActionMenuItemView.hasText())) {
        break label143;
      }
    }
    label143:
    for (boolean bool = true;; bool = false)
    {
      localLayoutParams.expandable = bool;
      localLayoutParams.cellsUsed = j;
      paramView.measure(View.MeasureSpec.makeMeasureSpec(j * paramInt1, 1073741824), i);
      return j;
      localActionMenuItemView = null;
      break;
    }
  }
  
  private void onMeasureExactFormat(int paramInt1, int paramInt2)
  {
    int i = View.MeasureSpec.getMode(paramInt2);
    int j = View.MeasureSpec.getSize(paramInt1);
    int k = View.MeasureSpec.getSize(paramInt2);
    int m = getPaddingLeft() + getPaddingRight();
    int n = getPaddingTop() + getPaddingBottom();
    int i1 = j - m;
    int i2 = i1 / this.mMinCellSize;
    int i3 = i1 % this.mMinCellSize;
    if (i2 == 0)
    {
      setMeasuredDimension(i1, 0);
      return;
    }
    int i4 = this.mMinCellSize + i3 / i2;
    int i5 = i2;
    int i6 = 0;
    int i7 = 0;
    int i8 = 0;
    int i9 = 0;
    int i10 = 0;
    long l1 = 0L;
    int i11 = getChildCount();
    int i12 = 0;
    int i16;
    label141:
    int i17;
    label144:
    label154:
    int i18;
    label168:
    float f;
    if (i12 >= i11)
    {
      if ((i10 == 0) || (i9 != 2)) {
        break label599;
      }
      i16 = 1;
      i17 = 0;
      if ((i8 > 0) && (i5 > 0)) {
        break label605;
      }
      if ((i10 != 0) || (i9 != 1)) {
        break label863;
      }
      i18 = 1;
      if ((i5 > 0) && (l1 != 0L) && ((i5 < i9 - 1) || (i18 != 0) || (i7 > 1)))
      {
        f = Long.bitCount(l1);
        if (i18 == 0)
        {
          if (((1L & l1) != 0L) && (!((LayoutParams)getChildAt(0).getLayoutParams()).preventEdgeOffset)) {
            f -= 0.5F;
          }
          if (((l1 & 1 << i11 - 1) != 0L) && (!((LayoutParams)getChildAt(i11 - 1).getLayoutParams()).preventEdgeOffset)) {
            f -= 0.5F;
          }
        }
        if (f <= 0.0F) {
          break label869;
        }
      }
    }
    int i22;
    int i19;
    int i20;
    label481:
    label592:
    label599:
    label605:
    label745:
    label863:
    label869:
    for (int i21 = (int)(i5 * i4 / f);; i21 = 0)
    {
      i22 = 0;
      if (i22 < i11) {
        break label875;
      }
      if (i17 != 0)
      {
        i19 = View.MeasureSpec.makeMeasureSpec(k - n, i);
        i20 = 0;
        if (i20 < i11) {
          break label1038;
        }
      }
      if (i != 1073741824) {
        k = i6;
      }
      setMeasuredDimension(i1, k);
      return;
      View localView1 = getChildAt(i12);
      if (localView1.getVisibility() == 8)
      {
        i12++;
        break;
      }
      boolean bool1 = localView1 instanceof ActionMenuItemView;
      i9++;
      if (bool1) {
        localView1.setPadding(this.mGeneratedItemPadding, 0, this.mGeneratedItemPadding, 0);
      }
      LayoutParams localLayoutParams1 = (LayoutParams)localView1.getLayoutParams();
      localLayoutParams1.expanded = false;
      localLayoutParams1.extraPixels = 0;
      localLayoutParams1.cellsUsed = 0;
      localLayoutParams1.expandable = false;
      localLayoutParams1.leftMargin = 0;
      localLayoutParams1.rightMargin = 0;
      boolean bool2;
      if ((bool1) && (((ActionMenuItemView)localView1).hasText()))
      {
        bool2 = true;
        localLayoutParams1.preventEdgeOffset = bool2;
        if (!localLayoutParams1.isOverflowButton) {
          break label592;
        }
      }
      for (int i13 = 1;; i13 = i5)
      {
        int i14 = measureChildForCells(localView1, i4, i13, paramInt2, n);
        i7 = Math.max(i7, i14);
        if (localLayoutParams1.expandable) {
          i8++;
        }
        if (localLayoutParams1.isOverflowButton) {
          i10 = 1;
        }
        i5 -= i14;
        int i15 = localView1.getMeasuredHeight();
        i6 = Math.max(i6, i15);
        if (i14 != 1) {
          break;
        }
        l1 |= 1 << i12;
        break;
        bool2 = false;
        break label481;
      }
      i16 = 0;
      break label141;
      int i24 = Integer.MAX_VALUE;
      long l2 = 0L;
      int i25 = 0;
      int i26 = 0;
      int i27;
      int i28;
      if (i26 >= i11)
      {
        l1 |= l2;
        if (i25 > i5) {
          break label154;
        }
        i27 = i24 + 1;
        i28 = 0;
        if (i28 < i11) {
          break label745;
        }
        i17 = 1;
        break label144;
      }
      LayoutParams localLayoutParams4 = (LayoutParams)getChildAt(i26).getLayoutParams();
      if (!localLayoutParams4.expandable) {}
      for (;;)
      {
        i26++;
        break;
        if (localLayoutParams4.cellsUsed < i24)
        {
          i24 = localLayoutParams4.cellsUsed;
          l2 = 1 << i26;
          i25 = 1;
        }
        else if (localLayoutParams4.cellsUsed == i24)
        {
          l2 |= 1 << i26;
          i25++;
        }
      }
      View localView4 = getChildAt(i28);
      LayoutParams localLayoutParams5 = (LayoutParams)localView4.getLayoutParams();
      if ((l2 & 1 << i28) == 0L) {
        if (localLayoutParams5.cellsUsed == i27) {
          l1 |= 1 << i28;
        }
      }
      for (;;)
      {
        i28++;
        break;
        if ((i16 != 0) && (localLayoutParams5.preventEdgeOffset) && (i5 == 1)) {
          localView4.setPadding(i4 + this.mGeneratedItemPadding, 0, this.mGeneratedItemPadding, 0);
        }
        localLayoutParams5.cellsUsed = (1 + localLayoutParams5.cellsUsed);
        localLayoutParams5.expanded = true;
        i5--;
      }
      i18 = 0;
      break label168;
    }
    label875:
    if ((l1 & 1 << i22) == 0L) {}
    for (;;)
    {
      i22++;
      break;
      View localView3 = getChildAt(i22);
      LayoutParams localLayoutParams3 = (LayoutParams)localView3.getLayoutParams();
      if ((localView3 instanceof ActionMenuItemView))
      {
        localLayoutParams3.extraPixels = i21;
        localLayoutParams3.expanded = true;
        if ((i22 == 0) && (!localLayoutParams3.preventEdgeOffset)) {
          localLayoutParams3.leftMargin = (-i21 / 2);
        }
        i17 = 1;
      }
      else if (localLayoutParams3.isOverflowButton)
      {
        localLayoutParams3.extraPixels = i21;
        localLayoutParams3.expanded = true;
        localLayoutParams3.rightMargin = (-i21 / 2);
        i17 = 1;
      }
      else
      {
        if (i22 != 0) {
          localLayoutParams3.leftMargin = (i21 / 2);
        }
        int i23 = i11 - 1;
        if (i22 != i23) {
          localLayoutParams3.rightMargin = (i21 / 2);
        }
      }
    }
    label1038:
    View localView2 = getChildAt(i20);
    LayoutParams localLayoutParams2 = (LayoutParams)localView2.getLayoutParams();
    if (!localLayoutParams2.expanded) {}
    for (;;)
    {
      i20++;
      break;
      localView2.measure(View.MeasureSpec.makeMeasureSpec(i4 * localLayoutParams2.cellsUsed + localLayoutParams2.extraPixels, 1073741824), i19);
    }
  }
  
  protected boolean checkLayoutParams(ViewGroup.LayoutParams paramLayoutParams)
  {
    return (paramLayoutParams != null) && ((paramLayoutParams instanceof LayoutParams));
  }
  
  public boolean dispatchPopulateAccessibilityEvent(AccessibilityEvent paramAccessibilityEvent)
  {
    return false;
  }
  
  protected LayoutParams generateDefaultLayoutParams()
  {
    LayoutParams localLayoutParams = new LayoutParams(-2, -2);
    localLayoutParams.gravity = 16;
    return localLayoutParams;
  }
  
  public LayoutParams generateLayoutParams(AttributeSet paramAttributeSet)
  {
    return new LayoutParams(getContext(), paramAttributeSet);
  }
  
  protected LayoutParams generateLayoutParams(ViewGroup.LayoutParams paramLayoutParams)
  {
    if ((paramLayoutParams instanceof LayoutParams))
    {
      LayoutParams localLayoutParams = new LayoutParams((LayoutParams)paramLayoutParams);
      if (localLayoutParams.gravity <= 0) {
        localLayoutParams.gravity = 16;
      }
      return localLayoutParams;
    }
    return generateDefaultLayoutParams();
  }
  
  public LayoutParams generateOverflowButtonLayoutParams()
  {
    LayoutParams localLayoutParams = generateDefaultLayoutParams();
    localLayoutParams.isOverflowButton = true;
    return localLayoutParams;
  }
  
  public int getWindowAnimations()
  {
    return 0;
  }
  
  protected boolean hasDividerBeforeChildAt(int paramInt)
  {
    View localView1 = getChildAt(paramInt - 1);
    View localView2 = getChildAt(paramInt);
    int i = getChildCount();
    boolean bool1 = false;
    if (paramInt < i)
    {
      boolean bool2 = localView1 instanceof ActionMenuChildView;
      bool1 = false;
      if (bool2) {
        bool1 = false | ((ActionMenuChildView)localView1).needsDividerAfter();
      }
    }
    if ((paramInt > 0) && ((localView2 instanceof ActionMenuChildView))) {
      bool1 |= ((ActionMenuChildView)localView2).needsDividerBefore();
    }
    return bool1;
  }
  
  public void initialize(MenuBuilder paramMenuBuilder)
  {
    this.mMenu = paramMenuBuilder;
  }
  
  public boolean invokeItem(MenuItemImpl paramMenuItemImpl)
  {
    return this.mMenu.performItemAction(paramMenuItemImpl, 0);
  }
  
  public boolean isExpandedFormat()
  {
    return this.mFormatItems;
  }
  
  public boolean isOverflowReserved()
  {
    return this.mReserveOverflow;
  }
  
  public void onConfigurationChanged(Configuration paramConfiguration)
  {
    if (IS_FROYO) {
      super.onConfigurationChanged(paramConfiguration);
    }
    this.mPresenter.updateMenuView(false);
    if ((this.mPresenter != null) && (this.mPresenter.isOverflowMenuShowing()))
    {
      this.mPresenter.hideOverflowMenu();
      this.mPresenter.showOverflowMenu();
    }
  }
  
  public void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    this.mPresenter.dismissPopupMenus();
  }
  
  protected void onDraw(Canvas paramCanvas)
  {
    if ((!IS_FROYO) && (this.mFirst))
    {
      this.mFirst = false;
      requestLayout();
      return;
    }
    super.onDraw(paramCanvas);
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    if (!this.mFormatItems)
    {
      super.onLayout(paramBoolean, paramInt1, paramInt2, paramInt3, paramInt4);
      return;
    }
    int i = getChildCount();
    int j = (paramInt2 + paramInt4) / 2;
    int k = 0;
    int m = paramInt3 - paramInt1 - getPaddingRight() - getPaddingLeft();
    int n = 0;
    int i1 = 0;
    if (i1 >= i)
    {
      if ((i == 1) && (n == 0))
      {
        View localView3 = getChildAt(0);
        int i17 = localView3.getMeasuredWidth();
        int i18 = localView3.getMeasuredHeight();
        int i19 = (paramInt3 - paramInt1) / 2 - i17 / 2;
        int i20 = j - i18 / 2;
        localView3.layout(i19, i20, i19 + i17, i20 + i18);
      }
    }
    else
    {
      View localView1 = getChildAt(i1);
      if (localView1.getVisibility() == 8) {}
      for (;;)
      {
        i1++;
        break;
        LayoutParams localLayoutParams1 = (LayoutParams)localView1.getLayoutParams();
        if (localLayoutParams1.isOverflowButton)
        {
          int i2 = localView1.getMeasuredWidth();
          if (hasDividerBeforeChildAt(i1)) {
            i2 += 0;
          }
          int i3 = localView1.getMeasuredHeight();
          int i4 = getWidth() - getPaddingRight() - localLayoutParams1.rightMargin;
          int i5 = i4 - i2;
          int i6 = j - i3 / 2;
          localView1.layout(i5, i6, i4, i6 + i3);
          m -= i2;
          n = 1;
        }
        else
        {
          m -= localView1.getMeasuredWidth() + localLayoutParams1.leftMargin + localLayoutParams1.rightMargin;
          k++;
        }
      }
    }
    int i7;
    label305:
    int i9;
    label324:
    int i10;
    int i11;
    int i12;
    label341:
    View localView2;
    LayoutParams localLayoutParams2;
    if (n != 0)
    {
      i7 = 0;
      int i8 = k - i7;
      if (i8 <= 0) {
        break label396;
      }
      i9 = m / i8;
      i10 = Math.max(0, i9);
      i11 = getPaddingLeft();
      i12 = 0;
      if (i12 < i)
      {
        localView2 = getChildAt(i12);
        localLayoutParams2 = (LayoutParams)localView2.getLayoutParams();
        if ((localView2.getVisibility() != 8) && (!localLayoutParams2.isOverflowButton)) {
          break label402;
        }
      }
    }
    for (;;)
    {
      i12++;
      break label341;
      break;
      i7 = 1;
      break label305;
      label396:
      i9 = 0;
      break label324;
      label402:
      int i13 = i11 + localLayoutParams2.leftMargin;
      int i14 = localView2.getMeasuredWidth();
      int i15 = localView2.getMeasuredHeight();
      int i16 = j - i15 / 2;
      localView2.layout(i13, i16, i13 + i14, i16 + i15);
      i11 = i13 + (i10 + (i14 + localLayoutParams2.rightMargin));
    }
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    boolean bool1 = this.mFormatItems;
    if (View.MeasureSpec.getMode(paramInt1) == 1073741824) {}
    for (boolean bool2 = true;; bool2 = false)
    {
      this.mFormatItems = bool2;
      if (bool1 != this.mFormatItems) {
        this.mFormatItemsWidth = 0;
      }
      int i = View.MeasureSpec.getMode(paramInt1);
      if ((this.mFormatItems) && (this.mMenu != null) && (i != this.mFormatItemsWidth))
      {
        this.mFormatItemsWidth = i;
        this.mMenu.onItemsChanged(true);
      }
      if (!this.mFormatItems) {
        break;
      }
      onMeasureExactFormat(paramInt1, paramInt2);
      return;
    }
    super.onMeasure(paramInt1, paramInt2);
  }
  
  public void setOverflowReserved(boolean paramBoolean)
  {
    this.mReserveOverflow = paramBoolean;
  }
  
  public void setPresenter(ActionMenuPresenter paramActionMenuPresenter)
  {
    this.mPresenter = paramActionMenuPresenter;
  }
  
  public static abstract interface ActionMenuChildView
  {
    public abstract boolean needsDividerAfter();
    
    public abstract boolean needsDividerBefore();
  }
  
  public static class LayoutParams
    extends LinearLayout.LayoutParams
  {
    public int cellsUsed;
    public boolean expandable;
    public boolean expanded;
    public int extraPixels;
    public boolean isOverflowButton;
    public boolean preventEdgeOffset;
    
    public LayoutParams(int paramInt1, int paramInt2)
    {
      super(paramInt2);
      this.isOverflowButton = false;
    }
    
    public LayoutParams(int paramInt1, int paramInt2, boolean paramBoolean)
    {
      super(paramInt2);
      this.isOverflowButton = paramBoolean;
    }
    
    public LayoutParams(Context paramContext, AttributeSet paramAttributeSet)
    {
      super(paramAttributeSet);
    }
    
    public LayoutParams(LayoutParams paramLayoutParams)
    {
      super();
      this.isOverflowButton = paramLayoutParams.isOverflowButton;
    }
  }
}
