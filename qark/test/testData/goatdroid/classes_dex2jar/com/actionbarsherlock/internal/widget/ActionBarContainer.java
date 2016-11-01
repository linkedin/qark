package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.ViewGroup.LayoutParams;
import android.widget.FrameLayout.LayoutParams;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.R.styleable;
import com.actionbarsherlock.internal.nineoldandroids.widget.NineFrameLayout;

public class ActionBarContainer
  extends NineFrameLayout
{
  private ActionBarView mActionBarView;
  private Drawable mBackground;
  private boolean mIsSplit;
  private boolean mIsStacked;
  private boolean mIsTransitioning;
  private Drawable mSplitBackground;
  private Drawable mStackedBackground;
  private View mTabContainer;
  
  public ActionBarContainer(Context paramContext)
  {
    this(paramContext, null);
  }
  
  public ActionBarContainer(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    setBackgroundDrawable(null);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockActionBar);
    this.mBackground = localTypedArray.getDrawable(2);
    this.mStackedBackground = localTypedArray.getDrawable(12);
    if (getId() == R.id.abs__split_action_bar)
    {
      this.mIsSplit = bool;
      this.mSplitBackground = localTypedArray.getDrawable(3);
    }
    localTypedArray.recycle();
    if (this.mIsSplit) {
      if (this.mSplitBackground != null) {}
    }
    for (;;)
    {
      setWillNotDraw(bool);
      return;
      bool = false;
      continue;
      if ((this.mBackground != null) || (this.mStackedBackground != null)) {
        bool = false;
      }
    }
  }
  
  public View getTabContainer()
  {
    return this.mTabContainer;
  }
  
  public void onDraw(Canvas paramCanvas)
  {
    if ((getWidth() == 0) || (getHeight() == 0)) {}
    do
    {
      do
      {
        return;
        if (!this.mIsSplit) {
          break;
        }
      } while (this.mSplitBackground == null);
      this.mSplitBackground.draw(paramCanvas);
      return;
      if (this.mBackground != null) {
        this.mBackground.draw(paramCanvas);
      }
    } while ((this.mStackedBackground == null) || (!this.mIsStacked));
    this.mStackedBackground.draw(paramCanvas);
  }
  
  public void onFinishInflate()
  {
    super.onFinishInflate();
    this.mActionBarView = ((ActionBarView)findViewById(R.id.abs__action_bar));
  }
  
  public boolean onHoverEvent(MotionEvent paramMotionEvent)
  {
    super.onHoverEvent(paramMotionEvent);
    return true;
  }
  
  public boolean onInterceptTouchEvent(MotionEvent paramMotionEvent)
  {
    return (this.mIsTransitioning) || (super.onInterceptTouchEvent(paramMotionEvent));
  }
  
  public void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    super.onLayout(paramBoolean, paramInt1, paramInt2, paramInt3, paramInt4);
    int i;
    int k;
    int m;
    int i1;
    if ((this.mTabContainer != null) && (this.mTabContainer.getVisibility() != 8))
    {
      i = 1;
      if ((this.mTabContainer != null) && (this.mTabContainer.getVisibility() != 8))
      {
        k = getMeasuredHeight();
        m = this.mTabContainer.getMeasuredHeight();
        if ((0x2 & this.mActionBarView.getDisplayOptions()) != 0) {
          break label208;
        }
        int n = getChildCount();
        i1 = 0;
        if (i1 < n) {
          break label165;
        }
        this.mTabContainer.layout(paramInt1, 0, paramInt3, m);
      }
    }
    for (;;)
    {
      if (!this.mIsSplit) {
        break label228;
      }
      Drawable localDrawable2 = this.mSplitBackground;
      j = 0;
      if (localDrawable2 != null)
      {
        this.mSplitBackground.setBounds(0, 0, getMeasuredWidth(), getMeasuredHeight());
        j = 1;
      }
      if (j != 0) {
        invalidate();
      }
      return;
      i = 0;
      break;
      label165:
      View localView = getChildAt(i1);
      if (localView == this.mTabContainer) {}
      for (;;)
      {
        i1++;
        break;
        if (!this.mActionBarView.isCollapsed()) {
          localView.offsetTopAndBottom(m);
        }
      }
      label208:
      this.mTabContainer.layout(paramInt1, k - m, paramInt3, k);
    }
    label228:
    Drawable localDrawable1 = this.mBackground;
    int j = 0;
    if (localDrawable1 != null)
    {
      this.mBackground.setBounds(this.mActionBarView.getLeft(), this.mActionBarView.getTop(), this.mActionBarView.getRight(), this.mActionBarView.getBottom());
      j = 1;
    }
    if ((i != 0) && (this.mStackedBackground != null)) {}
    for (boolean bool = true;; bool = false)
    {
      this.mIsStacked = bool;
      if (!bool) {
        break;
      }
      this.mStackedBackground.setBounds(this.mTabContainer.getLeft(), this.mTabContainer.getTop(), this.mTabContainer.getRight(), this.mTabContainer.getBottom());
      j = 1;
      break;
    }
  }
  
  public void onMeasure(int paramInt1, int paramInt2)
  {
    super.onMeasure(paramInt1, paramInt2);
    if (this.mActionBarView == null) {}
    for (;;)
    {
      return;
      FrameLayout.LayoutParams localLayoutParams = (FrameLayout.LayoutParams)this.mActionBarView.getLayoutParams();
      if (this.mActionBarView.isCollapsed()) {}
      for (int i = 0; (this.mTabContainer != null) && (this.mTabContainer.getVisibility() != 8) && (View.MeasureSpec.getMode(paramInt2) == Integer.MIN_VALUE); i = this.mActionBarView.getMeasuredHeight() + localLayoutParams.topMargin + localLayoutParams.bottomMargin)
      {
        int j = View.MeasureSpec.getSize(paramInt2);
        setMeasuredDimension(getMeasuredWidth(), Math.min(i + this.mTabContainer.getMeasuredHeight(), j));
        return;
      }
    }
  }
  
  public boolean onTouchEvent(MotionEvent paramMotionEvent)
  {
    super.onTouchEvent(paramMotionEvent);
    return true;
  }
  
  public void setPrimaryBackground(Drawable paramDrawable)
  {
    this.mBackground = paramDrawable;
    invalidate();
  }
  
  public void setSplitBackground(Drawable paramDrawable)
  {
    this.mSplitBackground = paramDrawable;
    invalidate();
  }
  
  public void setStackedBackground(Drawable paramDrawable)
  {
    this.mStackedBackground = paramDrawable;
    invalidate();
  }
  
  public void setTabContainer(ScrollingTabContainerView paramScrollingTabContainerView)
  {
    if (this.mTabContainer != null) {
      removeView(this.mTabContainer);
    }
    this.mTabContainer = paramScrollingTabContainerView;
    if (paramScrollingTabContainerView != null)
    {
      addView(paramScrollingTabContainerView);
      ViewGroup.LayoutParams localLayoutParams = paramScrollingTabContainerView.getLayoutParams();
      localLayoutParams.width = -1;
      localLayoutParams.height = -2;
      paramScrollingTabContainerView.setAllowCollapse(false);
    }
  }
  
  public void setTransitioning(boolean paramBoolean)
  {
    this.mIsTransitioning = paramBoolean;
    if (paramBoolean) {}
    for (int i = 393216;; i = 262144)
    {
      setDescendantFocusability(i);
      return;
    }
  }
}
