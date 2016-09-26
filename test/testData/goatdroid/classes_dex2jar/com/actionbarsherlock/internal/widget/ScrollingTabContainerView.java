package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.Configuration;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.text.TextUtils.TruncateAt;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.ViewParent;
import android.view.animation.DecelerateInterpolator;
import android.view.animation.Interpolator;
import android.widget.AbsListView.LayoutParams;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import com.actionbarsherlock.R.attr;
import com.actionbarsherlock.R.layout;
import com.actionbarsherlock.R.styleable;
import com.actionbarsherlock.app.ActionBar.Tab;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator;
import com.actionbarsherlock.internal.nineoldandroids.animation.Animator.AnimatorListener;
import com.actionbarsherlock.internal.nineoldandroids.animation.ObjectAnimator;
import com.actionbarsherlock.internal.nineoldandroids.widget.NineHorizontalScrollView;

public class ScrollingTabContainerView
  extends NineHorizontalScrollView
  implements IcsAdapterView.OnItemSelectedListener
{
  private static final int FADE_DURATION = 200;
  private static final Interpolator sAlphaInterpolator = new DecelerateInterpolator();
  private boolean mAllowCollapse;
  private int mContentHeight;
  private LayoutInflater mInflater;
  int mMaxTabWidth;
  private int mSelectedTabIndex;
  private TabClickListener mTabClickListener;
  private IcsLinearLayout mTabLayout;
  Runnable mTabSelector;
  private IcsSpinner mTabSpinner;
  protected final VisibilityAnimListener mVisAnimListener = new VisibilityAnimListener();
  protected Animator mVisibilityAnim;
  
  public ScrollingTabContainerView(Context paramContext)
  {
    super(paramContext);
    setHorizontalScrollBarEnabled(false);
    TypedArray localTypedArray = getContext().obtainStyledAttributes(null, R.styleable.SherlockActionBar, R.attr.actionBarStyle, 0);
    setContentHeight(localTypedArray.getLayoutDimension(4, 0));
    localTypedArray.recycle();
    this.mInflater = LayoutInflater.from(paramContext);
    this.mTabLayout = createTabLayout();
    addView(this.mTabLayout, new ViewGroup.LayoutParams(-2, -1));
  }
  
  private IcsSpinner createSpinner()
  {
    IcsSpinner localIcsSpinner = new IcsSpinner(getContext(), null, R.attr.actionDropDownStyle);
    localIcsSpinner.setLayoutParams(new LinearLayout.LayoutParams(-2, -1));
    localIcsSpinner.setOnItemSelectedListener(this);
    return localIcsSpinner;
  }
  
  private IcsLinearLayout createTabLayout()
  {
    IcsLinearLayout localIcsLinearLayout = (IcsLinearLayout)LayoutInflater.from(getContext()).inflate(R.layout.abs__action_bar_tab_bar_view, null);
    localIcsLinearLayout.setLayoutParams(new LinearLayout.LayoutParams(-2, -1));
    return localIcsLinearLayout;
  }
  
  private TabView createTabView(ActionBar.Tab paramTab, boolean paramBoolean)
  {
    TabView localTabView = (TabView)this.mInflater.inflate(R.layout.abs__action_bar_tab, null);
    localTabView.init(this, paramTab, paramBoolean);
    if (paramBoolean)
    {
      localTabView.setBackgroundDrawable(null);
      localTabView.setLayoutParams(new AbsListView.LayoutParams(-1, this.mContentHeight));
      return localTabView;
    }
    localTabView.setFocusable(true);
    if (this.mTabClickListener == null) {
      this.mTabClickListener = new TabClickListener(null);
    }
    localTabView.setOnClickListener(this.mTabClickListener);
    return localTabView;
  }
  
  private boolean isCollapsed()
  {
    return (this.mTabSpinner != null) && (this.mTabSpinner.getParent() == this);
  }
  
  private void performCollapse()
  {
    if (isCollapsed()) {
      return;
    }
    if (this.mTabSpinner == null) {
      this.mTabSpinner = createSpinner();
    }
    removeView(this.mTabLayout);
    addView(this.mTabSpinner, new ViewGroup.LayoutParams(-2, -1));
    if (this.mTabSpinner.getAdapter() == null) {
      this.mTabSpinner.setAdapter(new TabAdapter(null));
    }
    if (this.mTabSelector != null)
    {
      removeCallbacks(this.mTabSelector);
      this.mTabSelector = null;
    }
    this.mTabSpinner.setSelection(this.mSelectedTabIndex);
  }
  
  private boolean performExpand()
  {
    if (!isCollapsed()) {
      return false;
    }
    removeView(this.mTabSpinner);
    addView(this.mTabLayout, new ViewGroup.LayoutParams(-2, -1));
    setTabSelected(this.mTabSpinner.getSelectedItemPosition());
    return false;
  }
  
  public void addTab(ActionBar.Tab paramTab, int paramInt, boolean paramBoolean)
  {
    TabView localTabView = createTabView(paramTab, false);
    this.mTabLayout.addView(localTabView, paramInt, new LinearLayout.LayoutParams(0, -1, 1.0F));
    if (this.mTabSpinner != null) {
      ((TabAdapter)this.mTabSpinner.getAdapter()).notifyDataSetChanged();
    }
    if (paramBoolean) {
      localTabView.setSelected(true);
    }
    if (this.mAllowCollapse) {
      requestLayout();
    }
  }
  
  public void addTab(ActionBar.Tab paramTab, boolean paramBoolean)
  {
    TabView localTabView = createTabView(paramTab, false);
    this.mTabLayout.addView(localTabView, new LinearLayout.LayoutParams(0, -1, 1.0F));
    if (this.mTabSpinner != null) {
      ((TabAdapter)this.mTabSpinner.getAdapter()).notifyDataSetChanged();
    }
    if (paramBoolean) {
      localTabView.setSelected(true);
    }
    if (this.mAllowCollapse) {
      requestLayout();
    }
  }
  
  public void animateToTab(int paramInt)
  {
    final View localView = this.mTabLayout.getChildAt(paramInt);
    if (this.mTabSelector != null) {
      removeCallbacks(this.mTabSelector);
    }
    this.mTabSelector = new Runnable()
    {
      public void run()
      {
        int i = localView.getLeft() - (ScrollingTabContainerView.this.getWidth() - localView.getWidth()) / 2;
        ScrollingTabContainerView.this.smoothScrollTo(i, 0);
        ScrollingTabContainerView.this.mTabSelector = null;
      }
    };
    post(this.mTabSelector);
  }
  
  public void animateToVisibility(int paramInt)
  {
    if (this.mVisibilityAnim != null) {
      this.mVisibilityAnim.cancel();
    }
    if (paramInt == 0)
    {
      if (getVisibility() != 0) {
        setAlpha(0.0F);
      }
      ObjectAnimator localObjectAnimator2 = ObjectAnimator.ofFloat(this, "alpha", new float[] { 1.0F });
      localObjectAnimator2.setDuration(200L);
      localObjectAnimator2.setInterpolator(sAlphaInterpolator);
      localObjectAnimator2.addListener(this.mVisAnimListener.withFinalVisibility(paramInt));
      localObjectAnimator2.start();
      return;
    }
    ObjectAnimator localObjectAnimator1 = ObjectAnimator.ofFloat(this, "alpha", new float[] { 0.0F });
    localObjectAnimator1.setDuration(200L);
    localObjectAnimator1.setInterpolator(sAlphaInterpolator);
    localObjectAnimator1.addListener(this.mVisAnimListener.withFinalVisibility(paramInt));
    localObjectAnimator1.start();
  }
  
  public void onAttachedToWindow()
  {
    super.onAttachedToWindow();
    if (this.mTabSelector != null) {
      post(this.mTabSelector);
    }
  }
  
  protected void onConfigurationChanged(Configuration paramConfiguration)
  {
    super.onConfigurationChanged(paramConfiguration);
    TypedArray localTypedArray = getContext().obtainStyledAttributes(null, R.styleable.SherlockActionBar, R.attr.actionBarStyle, 0);
    setContentHeight(localTypedArray.getLayoutDimension(4, 0));
    localTypedArray.recycle();
  }
  
  public void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    if (this.mTabSelector != null) {
      removeCallbacks(this.mTabSelector);
    }
  }
  
  public void onItemSelected(IcsAdapterView<?> paramIcsAdapterView, View paramView, int paramInt, long paramLong)
  {
    ((TabView)paramView).getTab().select();
  }
  
  public void onMeasure(int paramInt1, int paramInt2)
  {
    int i = View.MeasureSpec.getMode(paramInt1);
    boolean bool;
    label70:
    int k;
    int m;
    if (i == 1073741824)
    {
      bool = true;
      setFillViewport(bool);
      int j = this.mTabLayout.getChildCount();
      if ((j <= 1) || ((i != 1073741824) && (i != Integer.MIN_VALUE))) {
        break label189;
      }
      if (j <= 2) {
        break label176;
      }
      this.mMaxTabWidth = ((int)(0.4F * View.MeasureSpec.getSize(paramInt1)));
      k = View.MeasureSpec.makeMeasureSpec(this.mContentHeight, 1073741824);
      if ((bool) || (!this.mAllowCollapse)) {
        break label197;
      }
      m = 1;
      label97:
      if (m == 0) {
        break label211;
      }
      this.mTabLayout.measure(0, k);
      if (this.mTabLayout.getMeasuredWidth() <= View.MeasureSpec.getSize(paramInt1)) {
        break label203;
      }
      performCollapse();
    }
    for (;;)
    {
      int n = getMeasuredWidth();
      super.onMeasure(paramInt1, k);
      int i1 = getMeasuredWidth();
      if ((bool) && (n != i1)) {
        setTabSelected(this.mSelectedTabIndex);
      }
      return;
      bool = false;
      break;
      label176:
      this.mMaxTabWidth = (View.MeasureSpec.getSize(paramInt1) / 2);
      break label70;
      label189:
      this.mMaxTabWidth = -1;
      break label70;
      label197:
      m = 0;
      break label97;
      label203:
      performExpand();
      continue;
      label211:
      performExpand();
    }
  }
  
  public void onNothingSelected(IcsAdapterView<?> paramIcsAdapterView) {}
  
  public void removeAllTabs()
  {
    this.mTabLayout.removeAllViews();
    if (this.mTabSpinner != null) {
      ((TabAdapter)this.mTabSpinner.getAdapter()).notifyDataSetChanged();
    }
    if (this.mAllowCollapse) {
      requestLayout();
    }
  }
  
  public void removeTabAt(int paramInt)
  {
    this.mTabLayout.removeViewAt(paramInt);
    if (this.mTabSpinner != null) {
      ((TabAdapter)this.mTabSpinner.getAdapter()).notifyDataSetChanged();
    }
    if (this.mAllowCollapse) {
      requestLayout();
    }
  }
  
  public void setAllowCollapse(boolean paramBoolean)
  {
    this.mAllowCollapse = paramBoolean;
  }
  
  public void setContentHeight(int paramInt)
  {
    this.mContentHeight = paramInt;
    requestLayout();
  }
  
  public void setTabSelected(int paramInt)
  {
    this.mSelectedTabIndex = paramInt;
    int i = this.mTabLayout.getChildCount();
    int j = 0;
    if (j >= i) {
      return;
    }
    View localView = this.mTabLayout.getChildAt(j);
    if (j == paramInt) {}
    for (boolean bool = true;; bool = false)
    {
      localView.setSelected(bool);
      if (bool) {
        animateToTab(paramInt);
      }
      j++;
      break;
    }
  }
  
  public void updateTab(int paramInt)
  {
    ((TabView)this.mTabLayout.getChildAt(paramInt)).update();
    if (this.mTabSpinner != null) {
      ((TabAdapter)this.mTabSpinner.getAdapter()).notifyDataSetChanged();
    }
    if (this.mAllowCollapse) {
      requestLayout();
    }
  }
  
  private class TabAdapter
    extends BaseAdapter
  {
    private TabAdapter() {}
    
    public int getCount()
    {
      return ScrollingTabContainerView.this.mTabLayout.getChildCount();
    }
    
    public Object getItem(int paramInt)
    {
      return ((ScrollingTabContainerView.TabView)ScrollingTabContainerView.this.mTabLayout.getChildAt(paramInt)).getTab();
    }
    
    public long getItemId(int paramInt)
    {
      return paramInt;
    }
    
    public View getView(int paramInt, View paramView, ViewGroup paramViewGroup)
    {
      if (paramView == null) {
        return ScrollingTabContainerView.this.createTabView((ActionBar.Tab)getItem(paramInt), true);
      }
      ((ScrollingTabContainerView.TabView)paramView).bindTab((ActionBar.Tab)getItem(paramInt));
      return paramView;
    }
  }
  
  private class TabClickListener
    implements View.OnClickListener
  {
    private TabClickListener() {}
    
    public void onClick(View paramView)
    {
      ((ScrollingTabContainerView.TabView)paramView).getTab().select();
      int i = ScrollingTabContainerView.this.mTabLayout.getChildCount();
      int j = 0;
      if (j >= i) {
        return;
      }
      View localView = ScrollingTabContainerView.this.mTabLayout.getChildAt(j);
      if (localView == paramView) {}
      for (boolean bool = true;; bool = false)
      {
        localView.setSelected(bool);
        j++;
        break;
      }
    }
  }
  
  public static class TabView
    extends LinearLayout
  {
    private View mCustomView;
    private ImageView mIconView;
    private ScrollingTabContainerView mParent;
    private ActionBar.Tab mTab;
    private CapitalizingTextView mTextView;
    
    public TabView(Context paramContext, AttributeSet paramAttributeSet)
    {
      super(paramAttributeSet);
    }
    
    public void bindTab(ActionBar.Tab paramTab)
    {
      this.mTab = paramTab;
      update();
    }
    
    public ActionBar.Tab getTab()
    {
      return this.mTab;
    }
    
    public void init(ScrollingTabContainerView paramScrollingTabContainerView, ActionBar.Tab paramTab, boolean paramBoolean)
    {
      this.mParent = paramScrollingTabContainerView;
      this.mTab = paramTab;
      if (paramBoolean) {
        setGravity(19);
      }
      update();
    }
    
    public void onMeasure(int paramInt1, int paramInt2)
    {
      super.onMeasure(paramInt1, paramInt2);
      if ((this.mParent.mMaxTabWidth > 0) && (getMeasuredWidth() > this.mParent.mMaxTabWidth)) {
        super.onMeasure(View.MeasureSpec.makeMeasureSpec(this.mParent.mMaxTabWidth, 1073741824), paramInt2);
      }
    }
    
    public void update()
    {
      ActionBar.Tab localTab = this.mTab;
      View localView = localTab.getCustomView();
      if (localView != null)
      {
        ViewParent localViewParent = localView.getParent();
        if (localViewParent != this)
        {
          if (localViewParent != null) {
            ((ViewGroup)localViewParent).removeView(localView);
          }
          addView(localView);
        }
        this.mCustomView = localView;
        if (this.mTextView != null) {
          this.mTextView.setVisibility(8);
        }
        if (this.mIconView != null)
        {
          this.mIconView.setVisibility(8);
          this.mIconView.setImageDrawable(null);
        }
      }
      label341:
      label366:
      for (;;)
      {
        return;
        if (this.mCustomView != null)
        {
          removeView(this.mCustomView);
          this.mCustomView = null;
        }
        Drawable localDrawable = localTab.getIcon();
        CharSequence localCharSequence = localTab.getText();
        if (localDrawable != null)
        {
          if (this.mIconView == null)
          {
            ImageView localImageView = new ImageView(getContext());
            LinearLayout.LayoutParams localLayoutParams2 = new LinearLayout.LayoutParams(-2, -2);
            localLayoutParams2.gravity = 16;
            localImageView.setLayoutParams(localLayoutParams2);
            addView(localImageView, 0);
            this.mIconView = localImageView;
          }
          this.mIconView.setImageDrawable(localDrawable);
          this.mIconView.setVisibility(0);
          if (localCharSequence == null) {
            break label341;
          }
          if (this.mTextView == null)
          {
            CapitalizingTextView localCapitalizingTextView = new CapitalizingTextView(getContext(), null, R.attr.actionBarTabTextStyle);
            localCapitalizingTextView.setEllipsize(TextUtils.TruncateAt.END);
            LinearLayout.LayoutParams localLayoutParams1 = new LinearLayout.LayoutParams(-2, -2);
            localLayoutParams1.gravity = 16;
            localCapitalizingTextView.setLayoutParams(localLayoutParams1);
            addView(localCapitalizingTextView);
            this.mTextView = localCapitalizingTextView;
          }
          this.mTextView.setTextCompat(localCharSequence);
          this.mTextView.setVisibility(0);
        }
        for (;;)
        {
          if (this.mIconView == null) {
            break label366;
          }
          this.mIconView.setContentDescription(localTab.getContentDescription());
          return;
          if (this.mIconView == null) {
            break;
          }
          this.mIconView.setVisibility(8);
          this.mIconView.setImageDrawable(null);
          break;
          if (this.mTextView != null)
          {
            this.mTextView.setVisibility(8);
            this.mTextView.setText(null);
          }
        }
      }
    }
  }
  
  protected class VisibilityAnimListener
    implements Animator.AnimatorListener
  {
    private boolean mCanceled = false;
    private int mFinalVisibility;
    
    protected VisibilityAnimListener() {}
    
    public void onAnimationCancel(Animator paramAnimator)
    {
      this.mCanceled = true;
    }
    
    public void onAnimationEnd(Animator paramAnimator)
    {
      if (this.mCanceled) {
        return;
      }
      ScrollingTabContainerView.this.mVisibilityAnim = null;
      ScrollingTabContainerView.this.setVisibility(this.mFinalVisibility);
    }
    
    public void onAnimationRepeat(Animator paramAnimator) {}
    
    public void onAnimationStart(Animator paramAnimator)
    {
      ScrollingTabContainerView.this.setVisibility(0);
      ScrollingTabContainerView.this.mVisibilityAnim = paramAnimator;
      this.mCanceled = false;
    }
    
    public VisibilityAnimListener withFinalVisibility(int paramInt)
    {
      this.mFinalVisibility = paramInt;
      return this;
    }
  }
}
