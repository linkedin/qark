package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.text.TextUtils;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.ViewGroup.MarginLayoutParams;
import android.view.accessibility.AccessibilityEvent;
import android.view.animation.DecelerateInterpolator;
import android.widget.LinearLayout;
import android.widget.TextView;
import com.actionbarsherlock.R.attr;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.R.layout;
import com.actionbarsherlock.R.styleable;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator.AnimatorListener;
import com.actionbarsherlock.internal.nineoldandroids.animation.AnimatorSet;
import com.actionbarsherlock.internal.nineoldandroids.animation.AnimatorSet.Builder;
import com.actionbarsherlock.internal.nineoldandroids.animation.ObjectAnimator;
import com.actionbarsherlock.internal.nineoldandroids.view.animation.AnimatorProxy;
import com.actionbarsherlock.internal.nineoldandroids.widget.NineLinearLayout;
import com.actionbarsherlock.internal.view.menu.ActionMenuPresenter;
import com.actionbarsherlock.internal.view.menu.ActionMenuView;
import com.actionbarsherlock.internal.view.menu.MenuBuilder;
import com.actionbarsherlock.view.ActionMode;

public class ActionBarContextView
  extends AbsActionBarView
  implements Animator.AnimatorListener
{
  private static final int ANIMATE_IDLE = 0;
  private static final int ANIMATE_IN = 1;
  private static final int ANIMATE_OUT = 2;
  private boolean mAnimateInOnLayout;
  private int mAnimationMode;
  private NineLinearLayout mClose;
  private Animator mCurrentAnimation;
  private View mCustomView;
  private Drawable mSplitBackground;
  private CharSequence mSubtitle;
  private int mSubtitleStyleRes;
  private TextView mSubtitleView;
  private CharSequence mTitle;
  private LinearLayout mTitleLayout;
  private int mTitleStyleRes;
  private TextView mTitleView;
  
  public ActionBarContextView(Context paramContext)
  {
    this(paramContext, null);
  }
  
  public ActionBarContextView(Context paramContext, AttributeSet paramAttributeSet)
  {
    this(paramContext, paramAttributeSet, R.attr.actionModeStyle);
  }
  
  public ActionBarContextView(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockActionMode, paramInt, 0);
    setBackgroundDrawable(localTypedArray.getDrawable(2));
    this.mTitleStyleRes = localTypedArray.getResourceId(0, 0);
    this.mSubtitleStyleRes = localTypedArray.getResourceId(1, 0);
    this.mContentHeight = localTypedArray.getLayoutDimension(4, 0);
    this.mSplitBackground = localTypedArray.getDrawable(3);
    localTypedArray.recycle();
  }
  
  private void finishAnimation()
  {
    Animator localAnimator = this.mCurrentAnimation;
    if (localAnimator != null)
    {
      this.mCurrentAnimation = null;
      localAnimator.end();
    }
  }
  
  private void initTitle()
  {
    int i = 8;
    if (this.mTitleLayout == null)
    {
      LayoutInflater.from(getContext()).inflate(R.layout.abs__action_bar_title_item, this);
      this.mTitleLayout = ((LinearLayout)getChildAt(-1 + getChildCount()));
      this.mTitleView = ((TextView)this.mTitleLayout.findViewById(R.id.abs__action_bar_title));
      this.mSubtitleView = ((TextView)this.mTitleLayout.findViewById(R.id.abs__action_bar_subtitle));
      if (this.mTitleStyleRes != 0) {
        this.mTitleView.setTextAppearance(this.mContext, this.mTitleStyleRes);
      }
      if (this.mSubtitleStyleRes != 0) {
        this.mSubtitleView.setTextAppearance(this.mContext, this.mSubtitleStyleRes);
      }
    }
    this.mTitleView.setText(this.mTitle);
    this.mSubtitleView.setText(this.mSubtitle);
    int j;
    int k;
    label166:
    TextView localTextView;
    if (TextUtils.isEmpty(this.mTitle))
    {
      j = 0;
      if (!TextUtils.isEmpty(this.mSubtitle)) {
        break label232;
      }
      k = 0;
      localTextView = this.mSubtitleView;
      if (k == 0) {
        break label237;
      }
    }
    label232:
    label237:
    for (int m = 0;; m = i)
    {
      localTextView.setVisibility(m);
      LinearLayout localLinearLayout = this.mTitleLayout;
      if ((j != 0) || (k != 0)) {
        i = 0;
      }
      localLinearLayout.setVisibility(i);
      if (this.mTitleLayout.getParent() == null) {
        addView(this.mTitleLayout);
      }
      return;
      j = 1;
      break;
      k = 1;
      break label166;
    }
  }
  
  private Animator makeInAnimation()
  {
    this.mClose.setTranslationX(-this.mClose.getWidth() - ((ViewGroup.MarginLayoutParams)this.mClose.getLayoutParams()).leftMargin);
    ObjectAnimator localObjectAnimator1 = ObjectAnimator.ofFloat(this.mClose, "translationX", new float[] { 0.0F });
    localObjectAnimator1.setDuration(200L);
    localObjectAnimator1.addListener(this);
    localObjectAnimator1.setInterpolator(new DecelerateInterpolator());
    AnimatorSet localAnimatorSet = new AnimatorSet();
    AnimatorSet.Builder localBuilder = localAnimatorSet.play(localObjectAnimator1);
    int j;
    if (this.mMenuView != null)
    {
      int i = this.mMenuView.getChildCount();
      if (i > 0) {
        j = i - 1;
      }
    }
    for (int k = 0;; k++)
    {
      if (j < 0) {
        return localAnimatorSet;
      }
      AnimatorProxy localAnimatorProxy = AnimatorProxy.wrap(this.mMenuView.getChildAt(j));
      localAnimatorProxy.setScaleY(0.0F);
      ObjectAnimator localObjectAnimator2 = ObjectAnimator.ofFloat(localAnimatorProxy, "scaleY", new float[] { 0.0F, 1.0F });
      localObjectAnimator2.setDuration(100L);
      localObjectAnimator2.setStartDelay(k * 70);
      localBuilder.with(localObjectAnimator2);
      j--;
    }
  }
  
  private Animator makeOutAnimation()
  {
    NineLinearLayout localNineLinearLayout = this.mClose;
    float[] arrayOfFloat = new float[1];
    arrayOfFloat[0] = (-this.mClose.getWidth() - ((ViewGroup.MarginLayoutParams)this.mClose.getLayoutParams()).leftMargin);
    ObjectAnimator localObjectAnimator1 = ObjectAnimator.ofFloat(localNineLinearLayout, "translationX", arrayOfFloat);
    localObjectAnimator1.setDuration(200L);
    localObjectAnimator1.addListener(this);
    localObjectAnimator1.setInterpolator(new DecelerateInterpolator());
    AnimatorSet localAnimatorSet = new AnimatorSet();
    AnimatorSet.Builder localBuilder = localAnimatorSet.play(localObjectAnimator1);
    if ((this.mMenuView != null) && (this.mMenuView.getChildCount() > 0)) {}
    for (int i = 0;; i++)
    {
      if (i >= 0) {
        return localAnimatorSet;
      }
      AnimatorProxy localAnimatorProxy = AnimatorProxy.wrap(this.mMenuView.getChildAt(i));
      localAnimatorProxy.setScaleY(0.0F);
      ObjectAnimator localObjectAnimator2 = ObjectAnimator.ofFloat(localAnimatorProxy, "scaleY", new float[] { 0.0F });
      localObjectAnimator2.setDuration(100L);
      localObjectAnimator2.setStartDelay(i * 70);
      localBuilder.with(localObjectAnimator2);
    }
  }
  
  public void closeMode()
  {
    if (this.mAnimationMode == 2) {
      return;
    }
    if (this.mClose == null)
    {
      killMode();
      return;
    }
    finishAnimation();
    this.mAnimationMode = 2;
    this.mCurrentAnimation = makeOutAnimation();
    this.mCurrentAnimation.start();
  }
  
  protected ViewGroup.LayoutParams generateDefaultLayoutParams()
  {
    return new ViewGroup.MarginLayoutParams(-1, -2);
  }
  
  public ViewGroup.LayoutParams generateLayoutParams(AttributeSet paramAttributeSet)
  {
    return new ViewGroup.MarginLayoutParams(getContext(), paramAttributeSet);
  }
  
  public CharSequence getSubtitle()
  {
    return this.mSubtitle;
  }
  
  public CharSequence getTitle()
  {
    return this.mTitle;
  }
  
  public boolean hideOverflowMenu()
  {
    if (this.mActionMenuPresenter != null) {
      return this.mActionMenuPresenter.hideOverflowMenu();
    }
    return false;
  }
  
  public void initForMode(final ActionMode paramActionMode)
  {
    MenuBuilder localMenuBuilder;
    ViewGroup.LayoutParams localLayoutParams;
    if (this.mClose == null)
    {
      this.mClose = ((NineLinearLayout)LayoutInflater.from(this.mContext).inflate(R.layout.abs__action_mode_close_item, this, false));
      addView(this.mClose);
      this.mClose.findViewById(R.id.abs__action_mode_close_button).setOnClickListener(new View.OnClickListener()
      {
        public void onClick(View paramAnonymousView)
        {
          paramActionMode.finish();
        }
      });
      localMenuBuilder = (MenuBuilder)paramActionMode.getMenu();
      if (this.mActionMenuPresenter != null) {
        this.mActionMenuPresenter.dismissPopupMenus();
      }
      this.mActionMenuPresenter = new ActionMenuPresenter(this.mContext);
      this.mActionMenuPresenter.setReserveOverflow(true);
      localLayoutParams = new ViewGroup.LayoutParams(-2, -1);
      if (this.mSplitActionBar) {
        break label190;
      }
      localMenuBuilder.addMenuPresenter(this.mActionMenuPresenter);
      this.mMenuView = ((ActionMenuView)this.mActionMenuPresenter.getMenuView(this));
      this.mMenuView.setBackgroundDrawable(null);
      addView(this.mMenuView, localLayoutParams);
    }
    for (;;)
    {
      this.mAnimateInOnLayout = true;
      return;
      if (this.mClose.getParent() != null) {
        break;
      }
      addView(this.mClose);
      break;
      label190:
      this.mActionMenuPresenter.setWidthLimit(getContext().getResources().getDisplayMetrics().widthPixels, true);
      this.mActionMenuPresenter.setItemLimit(Integer.MAX_VALUE);
      localLayoutParams.width = -1;
      localLayoutParams.height = this.mContentHeight;
      localMenuBuilder.addMenuPresenter(this.mActionMenuPresenter);
      this.mMenuView = ((ActionMenuView)this.mActionMenuPresenter.getMenuView(this));
      this.mMenuView.setBackgroundDrawable(this.mSplitBackground);
      this.mSplitView.addView(this.mMenuView, localLayoutParams);
    }
  }
  
  public boolean isOverflowMenuShowing()
  {
    if (this.mActionMenuPresenter != null) {
      return this.mActionMenuPresenter.isOverflowMenuShowing();
    }
    return false;
  }
  
  public void killMode()
  {
    finishAnimation();
    removeAllViews();
    if (this.mSplitView != null) {
      this.mSplitView.removeView(this.mMenuView);
    }
    this.mCustomView = null;
    this.mMenuView = null;
    this.mAnimateInOnLayout = false;
  }
  
  public void onAnimationCancel(Animator paramAnimator) {}
  
  public void onAnimationEnd(Animator paramAnimator)
  {
    if (this.mAnimationMode == 2) {
      killMode();
    }
    this.mAnimationMode = 0;
  }
  
  public void onAnimationRepeat(Animator paramAnimator) {}
  
  public void onAnimationStart(Animator paramAnimator) {}
  
  public void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    if (this.mActionMenuPresenter != null)
    {
      this.mActionMenuPresenter.hideOverflowMenu();
      this.mActionMenuPresenter.hideSubMenus();
    }
  }
  
  public void onInitializeAccessibilityEvent(AccessibilityEvent paramAccessibilityEvent)
  {
    if (paramAccessibilityEvent.getEventType() == 32)
    {
      paramAccessibilityEvent.setClassName(getClass().getName());
      paramAccessibilityEvent.setPackageName(getContext().getPackageName());
      paramAccessibilityEvent.setContentDescription(this.mTitle);
    }
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    int i = getPaddingLeft();
    int j = getPaddingTop();
    int k = paramInt4 - paramInt2 - getPaddingTop() - getPaddingBottom();
    if ((this.mClose != null) && (this.mClose.getVisibility() != 8))
    {
      ViewGroup.MarginLayoutParams localMarginLayoutParams = (ViewGroup.MarginLayoutParams)this.mClose.getLayoutParams();
      int n = i + localMarginLayoutParams.leftMargin;
      i = n + positionChild(this.mClose, n, j, k) + localMarginLayoutParams.rightMargin;
      if (this.mAnimateInOnLayout)
      {
        this.mAnimationMode = 1;
        this.mCurrentAnimation = makeInAnimation();
        this.mCurrentAnimation.start();
        this.mAnimateInOnLayout = false;
      }
    }
    if ((this.mTitleLayout != null) && (this.mCustomView == null)) {
      i += positionChild(this.mTitleLayout, i, j, k);
    }
    if (this.mCustomView != null) {
      (i + positionChild(this.mCustomView, i, j, k));
    }
    int m = paramInt3 - paramInt1 - getPaddingRight();
    if (this.mMenuView != null) {
      (m - positionChildInverse(this.mMenuView, m, j, k));
    }
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    if (View.MeasureSpec.getMode(paramInt1) != 1073741824) {
      throw new IllegalStateException(getClass().getSimpleName() + " can only be used " + "with android:layout_width=\"match_parent\" (or fill_parent)");
    }
    if (View.MeasureSpec.getMode(paramInt2) == 0) {
      throw new IllegalStateException(getClass().getSimpleName() + " can only be used " + "with android:layout_height=\"wrap_content\"");
    }
    int i = View.MeasureSpec.getSize(paramInt1);
    int j;
    int k;
    int m;
    int n;
    int i6;
    label299:
    int i7;
    label319:
    int i8;
    label334:
    int i9;
    label354:
    int i2;
    int i3;
    if (this.mContentHeight > 0)
    {
      j = this.mContentHeight;
      k = getPaddingTop() + getPaddingBottom();
      m = i - getPaddingLeft() - getPaddingRight();
      n = j - k;
      int i1 = View.MeasureSpec.makeMeasureSpec(n, Integer.MIN_VALUE);
      if (this.mClose != null)
      {
        int i10 = measureChildView(this.mClose, m, i1, 0);
        ViewGroup.MarginLayoutParams localMarginLayoutParams = (ViewGroup.MarginLayoutParams)this.mClose.getLayoutParams();
        m = i10 - (localMarginLayoutParams.leftMargin + localMarginLayoutParams.rightMargin);
      }
      if ((this.mMenuView != null) && (this.mMenuView.getParent() == this)) {
        m = measureChildView(this.mMenuView, m, i1, 0);
      }
      if ((this.mTitleLayout != null) && (this.mCustomView == null)) {
        m = measureChildView(this.mTitleLayout, m, i1, 0);
      }
      if (this.mCustomView != null)
      {
        ViewGroup.LayoutParams localLayoutParams = this.mCustomView.getLayoutParams();
        if (localLayoutParams.width == -2) {
          break label418;
        }
        i6 = 1073741824;
        if (localLayoutParams.width < 0) {
          break label426;
        }
        i7 = Math.min(localLayoutParams.width, m);
        if (localLayoutParams.height == -2) {
          break label433;
        }
        i8 = 1073741824;
        if (localLayoutParams.height < 0) {
          break label441;
        }
        i9 = Math.min(localLayoutParams.height, n);
        this.mCustomView.measure(View.MeasureSpec.makeMeasureSpec(i7, i6), View.MeasureSpec.makeMeasureSpec(i9, i8));
      }
      if (this.mContentHeight > 0) {
        break label479;
      }
      i2 = 0;
      i3 = getChildCount();
    }
    for (int i4 = 0;; i4++)
    {
      if (i4 >= i3)
      {
        setMeasuredDimension(i, i2);
        return;
        j = View.MeasureSpec.getSize(paramInt2);
        break;
        label418:
        i6 = Integer.MIN_VALUE;
        break label299;
        label426:
        i7 = m;
        break label319;
        label433:
        i8 = Integer.MIN_VALUE;
        break label334;
        label441:
        i9 = n;
        break label354;
      }
      int i5 = k + getChildAt(i4).getMeasuredHeight();
      if (i5 > i2) {
        i2 = i5;
      }
    }
    label479:
    setMeasuredDimension(i, j);
  }
  
  public void setContentHeight(int paramInt)
  {
    this.mContentHeight = paramInt;
  }
  
  public void setCustomView(View paramView)
  {
    if (this.mCustomView != null) {
      removeView(this.mCustomView);
    }
    this.mCustomView = paramView;
    if (this.mTitleLayout != null)
    {
      removeView(this.mTitleLayout);
      this.mTitleLayout = null;
    }
    if (paramView != null) {
      addView(paramView);
    }
    requestLayout();
  }
  
  public void setSplitActionBar(boolean paramBoolean)
  {
    ViewGroup.LayoutParams localLayoutParams;
    if (this.mSplitActionBar != paramBoolean) {
      if (this.mActionMenuPresenter != null)
      {
        localLayoutParams = new ViewGroup.LayoutParams(-2, -1);
        if (paramBoolean) {
          break label94;
        }
        this.mMenuView = ((ActionMenuView)this.mActionMenuPresenter.getMenuView(this));
        this.mMenuView.setBackgroundDrawable(null);
        ViewGroup localViewGroup2 = (ViewGroup)this.mMenuView.getParent();
        if (localViewGroup2 != null) {
          localViewGroup2.removeView(this.mMenuView);
        }
        addView(this.mMenuView, localLayoutParams);
      }
    }
    for (;;)
    {
      super.setSplitActionBar(paramBoolean);
      return;
      label94:
      this.mActionMenuPresenter.setWidthLimit(getContext().getResources().getDisplayMetrics().widthPixels, true);
      this.mActionMenuPresenter.setItemLimit(Integer.MAX_VALUE);
      localLayoutParams.width = -1;
      localLayoutParams.height = this.mContentHeight;
      this.mMenuView = ((ActionMenuView)this.mActionMenuPresenter.getMenuView(this));
      this.mMenuView.setBackgroundDrawable(this.mSplitBackground);
      ViewGroup localViewGroup1 = (ViewGroup)this.mMenuView.getParent();
      if (localViewGroup1 != null) {
        localViewGroup1.removeView(this.mMenuView);
      }
      this.mSplitView.addView(this.mMenuView, localLayoutParams);
    }
  }
  
  public void setSubtitle(CharSequence paramCharSequence)
  {
    this.mSubtitle = paramCharSequence;
    initTitle();
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    this.mTitle = paramCharSequence;
    initTitle();
  }
  
  public boolean shouldDelayChildPressedState()
  {
    return false;
  }
  
  public boolean showOverflowMenu()
  {
    if (this.mActionMenuPresenter != null) {
      return this.mActionMenuPresenter.showOverflowMenu();
    }
    return false;
  }
}
