package android.support.v4.view;

import android.content.Context;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.database.DataSetObserver;
import android.graphics.Canvas;
import android.graphics.Rect;
import android.graphics.drawable.Drawable;
import android.os.Build.VERSION;
import android.os.Parcel;
import android.os.Parcelable;
import android.os.Parcelable.Creator;
import android.os.SystemClock;
import android.support.v4.os.ParcelableCompat;
import android.support.v4.os.ParcelableCompatCreatorCallbacks;
import android.support.v4.widget.EdgeEffectCompat;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.FocusFinder;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.SoundEffectConstants;
import android.view.VelocityTracker;
import android.view.View;
import android.view.View.BaseSavedState;
import android.view.View.MeasureSpec;
import android.view.ViewConfiguration;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.view.ViewParent;
import android.view.accessibility.AccessibilityEvent;
import android.view.animation.Interpolator;
import android.widget.Scroller;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class ViewPager
  extends ViewGroup
{
  private static final Comparator<ItemInfo> COMPARATOR = new Comparator()
  {
    public int compare(ViewPager.ItemInfo paramAnonymousItemInfo1, ViewPager.ItemInfo paramAnonymousItemInfo2)
    {
      return paramAnonymousItemInfo1.position - paramAnonymousItemInfo2.position;
    }
  };
  private static final boolean DEBUG = false;
  private static final int DEFAULT_OFFSCREEN_PAGES = 1;
  private static final int INVALID_POINTER = -1;
  private static final int[] LAYOUT_ATTRS = { 16842931 };
  private static final int MAX_SETTLE_DURATION = 600;
  private static final int MIN_DISTANCE_FOR_FLING = 25;
  public static final int SCROLL_STATE_DRAGGING = 1;
  public static final int SCROLL_STATE_IDLE = 0;
  public static final int SCROLL_STATE_SETTLING = 2;
  private static final String TAG = "ViewPager";
  private static final boolean USE_CACHE;
  private static final Interpolator sInterpolator = new Interpolator()
  {
    public float getInterpolation(float paramAnonymousFloat)
    {
      float f = paramAnonymousFloat - 1.0F;
      return 1.0F + f * (f * (f * (f * f)));
    }
  };
  private int mActivePointerId = -1;
  private PagerAdapter mAdapter;
  private OnAdapterChangeListener mAdapterChangeListener;
  private int mBottomPageBounds;
  private boolean mCalledSuper;
  private int mChildHeightMeasureSpec;
  private int mChildWidthMeasureSpec;
  private int mCurItem;
  private int mDecorChildCount;
  private long mFakeDragBeginTime;
  private boolean mFakeDragging;
  private boolean mFirstLayout = true;
  private int mFlingDistance;
  private boolean mInLayout;
  private float mInitialMotionX;
  private OnPageChangeListener mInternalPageChangeListener;
  private boolean mIsBeingDragged;
  private boolean mIsUnableToDrag;
  private final ArrayList<ItemInfo> mItems = new ArrayList();
  private float mLastMotionX;
  private float mLastMotionY;
  private EdgeEffectCompat mLeftEdge;
  private Drawable mMarginDrawable;
  private int mMaximumVelocity;
  private int mMinimumVelocity;
  private PagerObserver mObserver;
  private int mOffscreenPageLimit = 1;
  private OnPageChangeListener mOnPageChangeListener;
  private int mPageMargin;
  private boolean mPopulatePending;
  private Parcelable mRestoredAdapterState = null;
  private ClassLoader mRestoredClassLoader = null;
  private int mRestoredCurItem = -1;
  private EdgeEffectCompat mRightEdge;
  private int mScrollState = 0;
  private Scroller mScroller;
  private boolean mScrolling;
  private boolean mScrollingCacheEnabled;
  private int mTopPageBounds;
  private int mTouchSlop;
  private VelocityTracker mVelocityTracker;
  
  public ViewPager(Context paramContext)
  {
    super(paramContext);
    initViewPager();
  }
  
  public ViewPager(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    initViewPager();
  }
  
  private void completeScroll()
  {
    boolean bool = this.mScrolling;
    if (bool)
    {
      setScrollingCacheEnabled(false);
      this.mScroller.abortAnimation();
      int j = getScrollX();
      int k = getScrollY();
      int m = this.mScroller.getCurrX();
      int n = this.mScroller.getCurrY();
      if ((j != m) || (k != n)) {
        scrollTo(m, n);
      }
      setScrollState(0);
    }
    this.mPopulatePending = false;
    this.mScrolling = false;
    for (int i = 0; i < this.mItems.size(); i++)
    {
      ItemInfo localItemInfo = (ItemInfo)this.mItems.get(i);
      if (localItemInfo.scrolling)
      {
        bool = true;
        localItemInfo.scrolling = false;
      }
    }
    if (bool) {
      populate();
    }
  }
  
  private int determineTargetPage(int paramInt1, float paramFloat, int paramInt2, int paramInt3)
  {
    if ((Math.abs(paramInt3) > this.mFlingDistance) && (Math.abs(paramInt2) > this.mMinimumVelocity))
    {
      if (paramInt2 > 0) {
        return paramInt1;
      }
      return paramInt1 + 1;
    }
    return (int)(0.5F + (paramFloat + paramInt1));
  }
  
  private void endDrag()
  {
    this.mIsBeingDragged = false;
    this.mIsUnableToDrag = false;
    if (this.mVelocityTracker != null)
    {
      this.mVelocityTracker.recycle();
      this.mVelocityTracker = null;
    }
  }
  
  private void onSecondaryPointerUp(MotionEvent paramMotionEvent)
  {
    int i = MotionEventCompat.getActionIndex(paramMotionEvent);
    if (MotionEventCompat.getPointerId(paramMotionEvent, i) == this.mActivePointerId) {
      if (i != 0) {
        break label56;
      }
    }
    label56:
    for (int j = 1;; j = 0)
    {
      this.mLastMotionX = MotionEventCompat.getX(paramMotionEvent, j);
      this.mActivePointerId = MotionEventCompat.getPointerId(paramMotionEvent, j);
      if (this.mVelocityTracker != null) {
        this.mVelocityTracker.clear();
      }
      return;
    }
  }
  
  private void pageScrolled(int paramInt)
  {
    int i = getWidth() + this.mPageMargin;
    int j = paramInt / i;
    int k = paramInt % i;
    float f = k / i;
    this.mCalledSuper = false;
    onPageScrolled(j, f, k);
    if (!this.mCalledSuper) {
      throw new IllegalStateException("onPageScrolled did not call superclass implementation");
    }
  }
  
  private void recomputeScrollPosition(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    int i = paramInt1 + paramInt3;
    if (paramInt2 > 0)
    {
      int k = getScrollX();
      int m = paramInt2 + paramInt4;
      int n = k / m;
      int i1 = (int)((k % m / m + n) * i);
      scrollTo(i1, getScrollY());
      if (!this.mScroller.isFinished())
      {
        int i2 = this.mScroller.getDuration() - this.mScroller.timePassed();
        this.mScroller.startScroll(i1, 0, i * this.mCurItem, 0, i2);
      }
    }
    int j;
    do
    {
      return;
      j = i * this.mCurItem;
    } while (j == getScrollX());
    completeScroll();
    scrollTo(j, getScrollY());
  }
  
  private void removeNonDecorViews()
  {
    for (int i = 0; i < getChildCount(); i++) {
      if (!((LayoutParams)getChildAt(i).getLayoutParams()).isDecor)
      {
        removeViewAt(i);
        i--;
      }
    }
  }
  
  private void setScrollState(int paramInt)
  {
    if (this.mScrollState == paramInt) {}
    do
    {
      return;
      this.mScrollState = paramInt;
    } while (this.mOnPageChangeListener == null);
    this.mOnPageChangeListener.onPageScrollStateChanged(paramInt);
  }
  
  private void setScrollingCacheEnabled(boolean paramBoolean)
  {
    if (this.mScrollingCacheEnabled != paramBoolean) {
      this.mScrollingCacheEnabled = paramBoolean;
    }
  }
  
  public void addFocusables(ArrayList<View> paramArrayList, int paramInt1, int paramInt2)
  {
    int i = paramArrayList.size();
    int j = getDescendantFocusability();
    if (j != 393216) {
      for (int k = 0; k < getChildCount(); k++)
      {
        View localView = getChildAt(k);
        if (localView.getVisibility() == 0)
        {
          ItemInfo localItemInfo = infoForChild(localView);
          if ((localItemInfo != null) && (localItemInfo.position == this.mCurItem)) {
            localView.addFocusables(paramArrayList, paramInt1, paramInt2);
          }
        }
      }
    }
    if (((j == 262144) && (i != paramArrayList.size())) || (!isFocusable())) {}
    while ((((paramInt2 & 0x1) == 1) && (isInTouchMode()) && (!isFocusableInTouchMode())) || (paramArrayList == null)) {
      return;
    }
    paramArrayList.add(this);
  }
  
  void addNewItem(int paramInt1, int paramInt2)
  {
    ItemInfo localItemInfo = new ItemInfo();
    localItemInfo.position = paramInt1;
    localItemInfo.object = this.mAdapter.instantiateItem(this, paramInt1);
    if (paramInt2 < 0)
    {
      this.mItems.add(localItemInfo);
      return;
    }
    this.mItems.add(paramInt2, localItemInfo);
  }
  
  public void addTouchables(ArrayList<View> paramArrayList)
  {
    for (int i = 0; i < getChildCount(); i++)
    {
      View localView = getChildAt(i);
      if (localView.getVisibility() == 0)
      {
        ItemInfo localItemInfo = infoForChild(localView);
        if ((localItemInfo != null) && (localItemInfo.position == this.mCurItem)) {
          localView.addTouchables(paramArrayList);
        }
      }
    }
  }
  
  public void addView(View paramView, int paramInt, ViewGroup.LayoutParams paramLayoutParams)
  {
    if (!checkLayoutParams(paramLayoutParams)) {
      paramLayoutParams = generateLayoutParams(paramLayoutParams);
    }
    LayoutParams localLayoutParams = (LayoutParams)paramLayoutParams;
    localLayoutParams.isDecor |= paramView instanceof Decor;
    if (this.mInLayout)
    {
      if ((localLayoutParams != null) && (localLayoutParams.isDecor)) {
        throw new IllegalStateException("Cannot add pager decor view during layout");
      }
      addViewInLayout(paramView, paramInt, paramLayoutParams);
      paramView.measure(this.mChildWidthMeasureSpec, this.mChildHeightMeasureSpec);
      return;
    }
    super.addView(paramView, paramInt, paramLayoutParams);
  }
  
  public boolean arrowScroll(int paramInt)
  {
    View localView1 = findFocus();
    if (localView1 == this) {
      localView1 = null;
    }
    View localView2 = FocusFinder.getInstance().findNextFocus(this, localView1, paramInt);
    boolean bool;
    if ((localView2 != null) && (localView2 != localView1)) {
      if (paramInt == 17) {
        if ((localView1 != null) && (localView2.getLeft() >= localView1.getLeft())) {
          bool = pageLeft();
        }
      }
    }
    for (;;)
    {
      if (bool) {
        playSoundEffect(SoundEffectConstants.getContantForFocusDirection(paramInt));
      }
      return bool;
      bool = localView2.requestFocus();
      continue;
      bool = false;
      if (paramInt == 66) {
        if ((localView1 != null) && (localView2.getLeft() <= localView1.getLeft()))
        {
          bool = pageRight();
        }
        else
        {
          bool = localView2.requestFocus();
          continue;
          if ((paramInt == 17) || (paramInt == 1))
          {
            bool = pageLeft();
          }
          else if (paramInt != 66)
          {
            bool = false;
            if (paramInt != 2) {}
          }
          else
          {
            bool = pageRight();
          }
        }
      }
    }
  }
  
  public boolean beginFakeDrag()
  {
    if (this.mIsBeingDragged) {
      return false;
    }
    this.mFakeDragging = true;
    setScrollState(1);
    this.mLastMotionX = 0.0F;
    this.mInitialMotionX = 0.0F;
    if (this.mVelocityTracker == null) {
      this.mVelocityTracker = VelocityTracker.obtain();
    }
    for (;;)
    {
      long l = SystemClock.uptimeMillis();
      MotionEvent localMotionEvent = MotionEvent.obtain(l, l, 0, 0.0F, 0.0F, 0);
      this.mVelocityTracker.addMovement(localMotionEvent);
      localMotionEvent.recycle();
      this.mFakeDragBeginTime = l;
      return true;
      this.mVelocityTracker.clear();
    }
  }
  
  protected boolean canScroll(View paramView, boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3)
  {
    if ((paramView instanceof ViewGroup))
    {
      ViewGroup localViewGroup = (ViewGroup)paramView;
      int i = paramView.getScrollX();
      int j = paramView.getScrollY();
      for (int k = -1 + localViewGroup.getChildCount(); k >= 0; k--)
      {
        View localView = localViewGroup.getChildAt(k);
        if ((paramInt2 + i >= localView.getLeft()) && (paramInt2 + i < localView.getRight()) && (paramInt3 + j >= localView.getTop()) && (paramInt3 + j < localView.getBottom()) && (canScroll(localView, true, paramInt1, paramInt2 + i - localView.getLeft(), paramInt3 + j - localView.getTop()))) {
          return true;
        }
      }
    }
    return (paramBoolean) && (ViewCompat.canScrollHorizontally(paramView, -paramInt1));
  }
  
  protected boolean checkLayoutParams(ViewGroup.LayoutParams paramLayoutParams)
  {
    return ((paramLayoutParams instanceof LayoutParams)) && (super.checkLayoutParams(paramLayoutParams));
  }
  
  public void computeScroll()
  {
    if ((!this.mScroller.isFinished()) && (this.mScroller.computeScrollOffset()))
    {
      int i = getScrollX();
      int j = getScrollY();
      int k = this.mScroller.getCurrX();
      int m = this.mScroller.getCurrY();
      if ((i != k) || (j != m))
      {
        scrollTo(k, m);
        pageScrolled(k);
      }
      invalidate();
      return;
    }
    completeScroll();
  }
  
  void dataSetChanged()
  {
    int i;
    int j;
    int k;
    int m;
    label37:
    ItemInfo localItemInfo;
    int n;
    if ((this.mItems.size() < 3) && (this.mItems.size() < this.mAdapter.getCount()))
    {
      i = 1;
      j = -1;
      k = 0;
      m = 0;
      if (m >= this.mItems.size()) {
        break label221;
      }
      localItemInfo = (ItemInfo)this.mItems.get(m);
      n = this.mAdapter.getItemPosition(localItemInfo.object);
      if (n != -1) {
        break label94;
      }
    }
    for (;;)
    {
      m++;
      break label37;
      i = 0;
      break;
      label94:
      if (n == -2)
      {
        this.mItems.remove(m);
        m--;
        if (k == 0)
        {
          this.mAdapter.startUpdate(this);
          k = 1;
        }
        this.mAdapter.destroyItem(this, localItemInfo.position, localItemInfo.object);
        i = 1;
        if (this.mCurItem == localItemInfo.position) {
          j = Math.max(0, Math.min(this.mCurItem, -1 + this.mAdapter.getCount()));
        }
      }
      else if (localItemInfo.position != n)
      {
        if (localItemInfo.position == this.mCurItem) {
          j = n;
        }
        localItemInfo.position = n;
        i = 1;
      }
    }
    label221:
    if (k != 0) {
      this.mAdapter.finishUpdate(this);
    }
    Collections.sort(this.mItems, COMPARATOR);
    if (j >= 0)
    {
      setCurrentItemInternal(j, false, true);
      i = 1;
    }
    if (i != 0)
    {
      populate();
      requestLayout();
    }
  }
  
  public boolean dispatchKeyEvent(KeyEvent paramKeyEvent)
  {
    return (super.dispatchKeyEvent(paramKeyEvent)) || (executeKeyEvent(paramKeyEvent));
  }
  
  public boolean dispatchPopulateAccessibilityEvent(AccessibilityEvent paramAccessibilityEvent)
  {
    int i = getChildCount();
    for (int j = 0; j < i; j++)
    {
      View localView = getChildAt(j);
      if (localView.getVisibility() == 0)
      {
        ItemInfo localItemInfo = infoForChild(localView);
        if ((localItemInfo != null) && (localItemInfo.position == this.mCurItem) && (localView.dispatchPopulateAccessibilityEvent(paramAccessibilityEvent))) {
          return true;
        }
      }
    }
    return false;
  }
  
  float distanceInfluenceForSnapDuration(float paramFloat)
  {
    return (float)Math.sin((float)(0.4712389167638204D * (paramFloat - 0.5F)));
  }
  
  public void draw(Canvas paramCanvas)
  {
    int i = 1;
    super.draw(paramCanvas);
    int j = ViewCompat.getOverScrollMode(this);
    boolean bool2;
    if ((j == 0) || ((j == i) && (this.mAdapter != null) && (this.mAdapter.getCount() > i)))
    {
      boolean bool1 = this.mLeftEdge.isFinished();
      bool2 = false;
      if (!bool1)
      {
        int i1 = paramCanvas.save();
        int i2 = getHeight() - getPaddingTop() - getPaddingBottom();
        paramCanvas.rotate(270.0F);
        paramCanvas.translate(-i2 + getPaddingTop(), 0.0F);
        this.mLeftEdge.setSize(i2, getWidth());
        bool2 = false | this.mLeftEdge.draw(paramCanvas);
        paramCanvas.restoreToCount(i1);
      }
      if (!this.mRightEdge.isFinished())
      {
        int k = paramCanvas.save();
        int m = getWidth();
        int n = getHeight() - getPaddingTop() - getPaddingBottom();
        if (this.mAdapter != null) {
          i = this.mAdapter.getCount();
        }
        paramCanvas.rotate(90.0F);
        paramCanvas.translate(-getPaddingTop(), -i * (m + this.mPageMargin) + this.mPageMargin);
        this.mRightEdge.setSize(n, m);
        bool2 |= this.mRightEdge.draw(paramCanvas);
        paramCanvas.restoreToCount(k);
      }
    }
    for (;;)
    {
      if (bool2) {
        invalidate();
      }
      return;
      this.mLeftEdge.finish();
      this.mRightEdge.finish();
      bool2 = false;
    }
  }
  
  protected void drawableStateChanged()
  {
    super.drawableStateChanged();
    Drawable localDrawable = this.mMarginDrawable;
    if ((localDrawable != null) && (localDrawable.isStateful())) {
      localDrawable.setState(getDrawableState());
    }
  }
  
  public void endFakeDrag()
  {
    if (!this.mFakeDragging) {
      throw new IllegalStateException("No fake drag in progress. Call beginFakeDrag first.");
    }
    VelocityTracker localVelocityTracker = this.mVelocityTracker;
    localVelocityTracker.computeCurrentVelocity(1000, this.mMaximumVelocity);
    int i = (int)VelocityTrackerCompat.getYVelocity(localVelocityTracker, this.mActivePointerId);
    this.mPopulatePending = true;
    int j = (int)(this.mLastMotionX - this.mInitialMotionX);
    int k = getScrollX();
    int m = getWidth() + this.mPageMargin;
    setCurrentItemInternal(determineTargetPage(k / m, k % m / m, i, j), true, true, i);
    endDrag();
    this.mFakeDragging = false;
  }
  
  public boolean executeKeyEvent(KeyEvent paramKeyEvent)
  {
    if (paramKeyEvent.getAction() == 0) {
      switch (paramKeyEvent.getKeyCode())
      {
      }
    }
    do
    {
      do
      {
        return false;
        return arrowScroll(17);
        return arrowScroll(66);
      } while (Build.VERSION.SDK_INT < 11);
      if (KeyEventCompat.hasNoModifiers(paramKeyEvent)) {
        return arrowScroll(2);
      }
    } while (!KeyEventCompat.hasModifiers(paramKeyEvent, 1));
    return arrowScroll(1);
  }
  
  public void fakeDragBy(float paramFloat)
  {
    if (!this.mFakeDragging) {
      throw new IllegalStateException("No fake drag in progress. Call beginFakeDrag first.");
    }
    this.mLastMotionX = (paramFloat + this.mLastMotionX);
    float f1 = getScrollX() - paramFloat;
    int i = getWidth() + this.mPageMargin;
    float f2 = Math.max(0, i * (-1 + this.mCurItem));
    float f3 = i * Math.min(1 + this.mCurItem, -1 + this.mAdapter.getCount());
    if (f1 < f2) {
      f1 = f2;
    }
    for (;;)
    {
      this.mLastMotionX += f1 - (int)f1;
      scrollTo((int)f1, getScrollY());
      pageScrolled((int)f1);
      long l = SystemClock.uptimeMillis();
      MotionEvent localMotionEvent = MotionEvent.obtain(this.mFakeDragBeginTime, l, 2, this.mLastMotionX, 0.0F, 0);
      this.mVelocityTracker.addMovement(localMotionEvent);
      localMotionEvent.recycle();
      return;
      if (f1 > f3) {
        f1 = f3;
      }
    }
  }
  
  protected ViewGroup.LayoutParams generateDefaultLayoutParams()
  {
    return new LayoutParams();
  }
  
  public ViewGroup.LayoutParams generateLayoutParams(AttributeSet paramAttributeSet)
  {
    return new LayoutParams(getContext(), paramAttributeSet);
  }
  
  protected ViewGroup.LayoutParams generateLayoutParams(ViewGroup.LayoutParams paramLayoutParams)
  {
    return generateDefaultLayoutParams();
  }
  
  public PagerAdapter getAdapter()
  {
    return this.mAdapter;
  }
  
  public int getCurrentItem()
  {
    return this.mCurItem;
  }
  
  public int getOffscreenPageLimit()
  {
    return this.mOffscreenPageLimit;
  }
  
  public int getPageMargin()
  {
    return this.mPageMargin;
  }
  
  ItemInfo infoForAnyChild(View paramView)
  {
    for (;;)
    {
      ViewParent localViewParent = paramView.getParent();
      if (localViewParent == this) {
        break;
      }
      if ((localViewParent == null) || (!(localViewParent instanceof View))) {
        return null;
      }
      paramView = (View)localViewParent;
    }
    return infoForChild(paramView);
  }
  
  ItemInfo infoForChild(View paramView)
  {
    for (int i = 0; i < this.mItems.size(); i++)
    {
      ItemInfo localItemInfo = (ItemInfo)this.mItems.get(i);
      if (this.mAdapter.isViewFromObject(paramView, localItemInfo.object)) {
        return localItemInfo;
      }
    }
    return null;
  }
  
  void initViewPager()
  {
    setWillNotDraw(false);
    setDescendantFocusability(262144);
    setFocusable(true);
    Context localContext = getContext();
    this.mScroller = new Scroller(localContext, sInterpolator);
    ViewConfiguration localViewConfiguration = ViewConfiguration.get(localContext);
    this.mTouchSlop = ViewConfigurationCompat.getScaledPagingTouchSlop(localViewConfiguration);
    this.mMinimumVelocity = localViewConfiguration.getScaledMinimumFlingVelocity();
    this.mMaximumVelocity = localViewConfiguration.getScaledMaximumFlingVelocity();
    this.mLeftEdge = new EdgeEffectCompat(localContext);
    this.mRightEdge = new EdgeEffectCompat(localContext);
    this.mFlingDistance = ((int)(25.0F * localContext.getResources().getDisplayMetrics().density));
  }
  
  public boolean isFakeDragging()
  {
    return this.mFakeDragging;
  }
  
  protected void onAttachedToWindow()
  {
    super.onAttachedToWindow();
    this.mFirstLayout = true;
  }
  
  protected void onDraw(Canvas paramCanvas)
  {
    super.onDraw(paramCanvas);
    if ((this.mPageMargin > 0) && (this.mMarginDrawable != null))
    {
      int i = getScrollX();
      int j = getWidth();
      int k = i % (j + this.mPageMargin);
      if (k != 0)
      {
        int m = j + (i - k);
        this.mMarginDrawable.setBounds(m, this.mTopPageBounds, m + this.mPageMargin, this.mBottomPageBounds);
        this.mMarginDrawable.draw(paramCanvas);
      }
    }
  }
  
  public boolean onInterceptTouchEvent(MotionEvent paramMotionEvent)
  {
    int i = 0xFF & paramMotionEvent.getAction();
    if ((i == 3) || (i == 1))
    {
      this.mIsBeingDragged = false;
      this.mIsUnableToDrag = false;
      this.mActivePointerId = -1;
      if (this.mVelocityTracker != null)
      {
        this.mVelocityTracker.recycle();
        this.mVelocityTracker = null;
      }
      return false;
    }
    if (i != 0)
    {
      if (this.mIsBeingDragged) {
        return true;
      }
      if (this.mIsUnableToDrag) {
        return false;
      }
    }
    switch (i)
    {
    }
    for (;;)
    {
      if (!this.mIsBeingDragged)
      {
        if (this.mVelocityTracker == null) {
          this.mVelocityTracker = VelocityTracker.obtain();
        }
        this.mVelocityTracker.addMovement(paramMotionEvent);
      }
      return this.mIsBeingDragged;
      int j = this.mActivePointerId;
      if (j != -1)
      {
        int k = MotionEventCompat.findPointerIndex(paramMotionEvent, j);
        float f2 = MotionEventCompat.getX(paramMotionEvent, k);
        float f3 = f2 - this.mLastMotionX;
        float f4 = Math.abs(f3);
        float f5 = MotionEventCompat.getY(paramMotionEvent, k);
        float f6 = Math.abs(f5 - this.mLastMotionY);
        if (canScroll(this, false, (int)f3, (int)f2, (int)f5))
        {
          this.mLastMotionX = f2;
          this.mInitialMotionX = f2;
          this.mLastMotionY = f5;
          return false;
        }
        if ((f4 > this.mTouchSlop) && (f4 > f6))
        {
          this.mIsBeingDragged = true;
          setScrollState(1);
          this.mLastMotionX = f2;
          setScrollingCacheEnabled(true);
        }
        else if (f6 > this.mTouchSlop)
        {
          this.mIsUnableToDrag = true;
          continue;
          float f1 = paramMotionEvent.getX();
          this.mInitialMotionX = f1;
          this.mLastMotionX = f1;
          this.mLastMotionY = paramMotionEvent.getY();
          this.mActivePointerId = MotionEventCompat.getPointerId(paramMotionEvent, 0);
          if (this.mScrollState == 2)
          {
            this.mIsBeingDragged = true;
            this.mIsUnableToDrag = false;
            setScrollState(1);
          }
          else
          {
            completeScroll();
            this.mIsBeingDragged = false;
            this.mIsUnableToDrag = false;
            continue;
            onSecondaryPointerUp(paramMotionEvent);
          }
        }
      }
    }
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    this.mInLayout = true;
    populate();
    this.mInLayout = false;
    int i = getChildCount();
    int j = paramInt3 - paramInt1;
    int k = paramInt4 - paramInt2;
    int m = getPaddingLeft();
    int n = getPaddingTop();
    int i1 = getPaddingRight();
    int i2 = getPaddingBottom();
    int i3 = getScrollX();
    int i4 = 0;
    int i5 = 0;
    if (i5 < i)
    {
      View localView = getChildAt(i5);
      int i10;
      label172:
      int i11;
      if (localView.getVisibility() != 8)
      {
        LayoutParams localLayoutParams = (LayoutParams)localView.getLayoutParams();
        if (!localLayoutParams.isDecor) {
          break label379;
        }
        int i8 = 0x7 & localLayoutParams.gravity;
        int i9 = 0x70 & localLayoutParams.gravity;
        switch (i8)
        {
        case 2: 
        case 4: 
        default: 
          i10 = m;
          switch (i9)
          {
          default: 
            i11 = n;
            label212:
            int i12 = i10 + i3;
            i4++;
            localView.layout(i12, i11, i12 + localView.getMeasuredWidth(), i11 + localView.getMeasuredHeight());
          }
          break;
        }
      }
      for (;;)
      {
        i5++;
        break;
        i10 = m;
        m += localView.getMeasuredWidth();
        break label172;
        i10 = Math.max((j - localView.getMeasuredWidth()) / 2, m);
        break label172;
        i10 = j - i1 - localView.getMeasuredWidth();
        i1 += localView.getMeasuredWidth();
        break label172;
        i11 = n;
        n += localView.getMeasuredHeight();
        break label212;
        i11 = Math.max((k - localView.getMeasuredHeight()) / 2, n);
        break label212;
        i11 = k - i2 - localView.getMeasuredHeight();
        i2 += localView.getMeasuredHeight();
        break label212;
        label379:
        ItemInfo localItemInfo = infoForChild(localView);
        if (localItemInfo != null)
        {
          int i6 = m + (j + this.mPageMargin) * localItemInfo.position;
          int i7 = n;
          localView.layout(i6, i7, i6 + localView.getMeasuredWidth(), i7 + localView.getMeasuredHeight());
        }
      }
    }
    this.mTopPageBounds = n;
    this.mBottomPageBounds = (k - i2);
    this.mDecorChildCount = i4;
    this.mFirstLayout = false;
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    setMeasuredDimension(getDefaultSize(0, paramInt1), getDefaultSize(0, paramInt2));
    int i = getMeasuredWidth() - getPaddingLeft() - getPaddingRight();
    int j = getMeasuredHeight() - getPaddingTop() - getPaddingBottom();
    int k = getChildCount();
    int m = 0;
    if (m < k)
    {
      View localView2 = getChildAt(m);
      int i5;
      int i6;
      label201:
      int i7;
      if (localView2.getVisibility() != 8)
      {
        LayoutParams localLayoutParams2 = (LayoutParams)localView2.getLayoutParams();
        if ((localLayoutParams2 != null) && (localLayoutParams2.isDecor))
        {
          int i2 = 0x7 & localLayoutParams2.gravity;
          int i3 = 0x70 & localLayoutParams2.gravity;
          Log.d("ViewPager", "gravity: " + localLayoutParams2.gravity + " hgrav: " + i2 + " vgrav: " + i3);
          int i4 = Integer.MIN_VALUE;
          i5 = Integer.MIN_VALUE;
          if ((i3 != 48) && (i3 != 80)) {
            break label265;
          }
          i6 = 1;
          if ((i2 != 3) && (i2 != 5)) {
            break label271;
          }
          i7 = 1;
          label216:
          if (i6 == 0) {
            break label277;
          }
          i4 = 1073741824;
          label226:
          localView2.measure(View.MeasureSpec.makeMeasureSpec(i, i4), View.MeasureSpec.makeMeasureSpec(j, i5));
          if (i6 == 0) {
            break label290;
          }
          j -= localView2.getMeasuredHeight();
        }
      }
      for (;;)
      {
        m++;
        break;
        label265:
        i6 = 0;
        break label201;
        label271:
        i7 = 0;
        break label216;
        label277:
        if (i7 == 0) {
          break label226;
        }
        i5 = 1073741824;
        break label226;
        label290:
        if (i7 != 0) {
          i -= localView2.getMeasuredWidth();
        }
      }
    }
    this.mChildWidthMeasureSpec = View.MeasureSpec.makeMeasureSpec(i, 1073741824);
    this.mChildHeightMeasureSpec = View.MeasureSpec.makeMeasureSpec(j, 1073741824);
    this.mInLayout = true;
    populate();
    this.mInLayout = false;
    int n = getChildCount();
    for (int i1 = 0; i1 < n; i1++)
    {
      View localView1 = getChildAt(i1);
      if (localView1.getVisibility() != 8)
      {
        LayoutParams localLayoutParams1 = (LayoutParams)localView1.getLayoutParams();
        if ((localLayoutParams1 == null) || (!localLayoutParams1.isDecor)) {
          localView1.measure(this.mChildWidthMeasureSpec, this.mChildHeightMeasureSpec);
        }
      }
    }
  }
  
  protected void onPageScrolled(int paramInt1, float paramFloat, int paramInt2)
  {
    if (this.mDecorChildCount > 0)
    {
      int i = getScrollX();
      int j = getPaddingLeft();
      int k = getPaddingRight();
      int m = getWidth();
      int n = getChildCount();
      int i1 = 0;
      while (i1 < n)
      {
        View localView = getChildAt(i1);
        LayoutParams localLayoutParams = (LayoutParams)localView.getLayoutParams();
        if (!localLayoutParams.isDecor)
        {
          i1++;
        }
        else
        {
          int i2;
          switch (0x7 & localLayoutParams.gravity)
          {
          case 2: 
          case 4: 
          default: 
            i2 = j;
          }
          for (;;)
          {
            int i3 = i2 + i - localView.getLeft();
            if (i3 == 0) {
              break;
            }
            localView.offsetLeftAndRight(i3);
            break;
            i2 = j;
            j += localView.getWidth();
            continue;
            i2 = Math.max((m - localView.getMeasuredWidth()) / 2, j);
            continue;
            i2 = m - k - localView.getMeasuredWidth();
            k += localView.getMeasuredWidth();
          }
        }
      }
    }
    if (this.mOnPageChangeListener != null) {
      this.mOnPageChangeListener.onPageScrolled(paramInt1, paramFloat, paramInt2);
    }
    if (this.mInternalPageChangeListener != null) {
      this.mInternalPageChangeListener.onPageScrolled(paramInt1, paramFloat, paramInt2);
    }
    this.mCalledSuper = true;
  }
  
  protected boolean onRequestFocusInDescendants(int paramInt, Rect paramRect)
  {
    int i = getChildCount();
    int j;
    int k;
    int m;
    int n;
    if ((paramInt & 0x2) != 0)
    {
      j = 0;
      k = 1;
      m = i;
      n = j;
    }
    for (;;)
    {
      if (n == m) {
        break label108;
      }
      View localView = getChildAt(n);
      if (localView.getVisibility() == 0)
      {
        ItemInfo localItemInfo = infoForChild(localView);
        if ((localItemInfo != null) && (localItemInfo.position == this.mCurItem) && (localView.requestFocus(paramInt, paramRect)))
        {
          return true;
          j = i - 1;
          k = -1;
          m = -1;
          break;
        }
      }
      n += k;
    }
    label108:
    return false;
  }
  
  public void onRestoreInstanceState(Parcelable paramParcelable)
  {
    if (!(paramParcelable instanceof SavedState))
    {
      super.onRestoreInstanceState(paramParcelable);
      return;
    }
    SavedState localSavedState = (SavedState)paramParcelable;
    super.onRestoreInstanceState(localSavedState.getSuperState());
    if (this.mAdapter != null)
    {
      this.mAdapter.restoreState(localSavedState.adapterState, localSavedState.loader);
      setCurrentItemInternal(localSavedState.position, false, true);
      return;
    }
    this.mRestoredCurItem = localSavedState.position;
    this.mRestoredAdapterState = localSavedState.adapterState;
    this.mRestoredClassLoader = localSavedState.loader;
  }
  
  public Parcelable onSaveInstanceState()
  {
    SavedState localSavedState = new SavedState(super.onSaveInstanceState());
    localSavedState.position = this.mCurItem;
    if (this.mAdapter != null) {
      localSavedState.adapterState = this.mAdapter.saveState();
    }
    return localSavedState;
  }
  
  protected void onSizeChanged(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    super.onSizeChanged(paramInt1, paramInt2, paramInt3, paramInt4);
    if (paramInt1 != paramInt3) {
      recomputeScrollPosition(paramInt1, paramInt3, this.mPageMargin, this.mPageMargin);
    }
  }
  
  public boolean onTouchEvent(MotionEvent paramMotionEvent)
  {
    if (this.mFakeDragging) {
      return true;
    }
    if ((paramMotionEvent.getAction() == 0) && (paramMotionEvent.getEdgeFlags() != 0)) {
      return false;
    }
    if ((this.mAdapter == null) || (this.mAdapter.getCount() == 0)) {
      return false;
    }
    if (this.mVelocityTracker == null) {
      this.mVelocityTracker = VelocityTracker.obtain();
    }
    this.mVelocityTracker.addMovement(paramMotionEvent);
    int i = 0xFF & paramMotionEvent.getAction();
    boolean bool1 = false;
    switch (i)
    {
    }
    for (;;)
    {
      if (bool1) {
        invalidate();
      }
      return true;
      completeScroll();
      float f11 = paramMotionEvent.getX();
      this.mInitialMotionX = f11;
      this.mLastMotionX = f11;
      this.mActivePointerId = MotionEventCompat.getPointerId(paramMotionEvent, 0);
      bool1 = false;
      continue;
      if (!this.mIsBeingDragged)
      {
        int i4 = MotionEventCompat.findPointerIndex(paramMotionEvent, this.mActivePointerId);
        float f8 = MotionEventCompat.getX(paramMotionEvent, i4);
        float f9 = Math.abs(f8 - this.mLastMotionX);
        float f10 = Math.abs(MotionEventCompat.getY(paramMotionEvent, i4) - this.mLastMotionY);
        if ((f9 > this.mTouchSlop) && (f9 > f10))
        {
          this.mIsBeingDragged = true;
          this.mLastMotionX = f8;
          setScrollState(1);
          setScrollingCacheEnabled(true);
        }
      }
      boolean bool4 = this.mIsBeingDragged;
      bool1 = false;
      if (bool4)
      {
        float f1 = MotionEventCompat.getX(paramMotionEvent, MotionEventCompat.findPointerIndex(paramMotionEvent, this.mActivePointerId));
        float f2 = this.mLastMotionX - f1;
        this.mLastMotionX = f1;
        float f3 = f2 + getScrollX();
        int i1 = getWidth();
        int i2 = i1 + this.mPageMargin;
        int i3 = -1 + this.mAdapter.getCount();
        float f4 = Math.max(0, i2 * (-1 + this.mCurItem));
        float f5 = i2 * Math.min(1 + this.mCurItem, i3);
        if (f3 < f4)
        {
          boolean bool7 = f4 < 0.0F;
          bool1 = false;
          if (!bool7)
          {
            float f7 = -f3;
            bool1 = this.mLeftEdge.onPull(f7 / i1);
          }
          f3 = f4;
        }
        for (;;)
        {
          this.mLastMotionX += f3 - (int)f3;
          scrollTo((int)f3, getScrollY());
          pageScrolled((int)f3);
          break;
          boolean bool5 = f3 < f5;
          bool1 = false;
          if (bool5)
          {
            boolean bool6 = f5 < i3 * i2;
            bool1 = false;
            if (!bool6)
            {
              float f6 = f3 - f5;
              bool1 = this.mRightEdge.onPull(f6 / i1);
            }
            f3 = f5;
          }
        }
        boolean bool3 = this.mIsBeingDragged;
        bool1 = false;
        if (bool3)
        {
          VelocityTracker localVelocityTracker = this.mVelocityTracker;
          localVelocityTracker.computeCurrentVelocity(1000, this.mMaximumVelocity);
          int k = (int)VelocityTrackerCompat.getXVelocity(localVelocityTracker, this.mActivePointerId);
          this.mPopulatePending = true;
          int m = getWidth() + this.mPageMargin;
          int n = getScrollX();
          setCurrentItemInternal(determineTargetPage(n / m, n % m / m, k, (int)(MotionEventCompat.getX(paramMotionEvent, MotionEventCompat.findPointerIndex(paramMotionEvent, this.mActivePointerId)) - this.mInitialMotionX)), true, true, k);
          this.mActivePointerId = -1;
          endDrag();
          bool1 = this.mLeftEdge.onRelease() | this.mRightEdge.onRelease();
          continue;
          boolean bool2 = this.mIsBeingDragged;
          bool1 = false;
          if (bool2)
          {
            setCurrentItemInternal(this.mCurItem, true, true);
            this.mActivePointerId = -1;
            endDrag();
            bool1 = this.mLeftEdge.onRelease() | this.mRightEdge.onRelease();
            continue;
            int j = MotionEventCompat.getActionIndex(paramMotionEvent);
            this.mLastMotionX = MotionEventCompat.getX(paramMotionEvent, j);
            this.mActivePointerId = MotionEventCompat.getPointerId(paramMotionEvent, j);
            bool1 = false;
            continue;
            onSecondaryPointerUp(paramMotionEvent);
            this.mLastMotionX = MotionEventCompat.getX(paramMotionEvent, MotionEventCompat.findPointerIndex(paramMotionEvent, this.mActivePointerId));
            bool1 = false;
          }
        }
      }
    }
  }
  
  boolean pageLeft()
  {
    if (this.mCurItem > 0)
    {
      setCurrentItem(-1 + this.mCurItem, true);
      return true;
    }
    return false;
  }
  
  boolean pageRight()
  {
    if ((this.mAdapter != null) && (this.mCurItem < -1 + this.mAdapter.getCount()))
    {
      setCurrentItem(1 + this.mCurItem, true);
      return true;
    }
    return false;
  }
  
  void populate()
  {
    if (this.mAdapter == null) {
      break label7;
    }
    label7:
    label307:
    label313:
    label316:
    label395:
    label514:
    label522:
    label528:
    label532:
    for (;;)
    {
      return;
      if ((!this.mPopulatePending) && (getWindowToken() != null))
      {
        this.mAdapter.startUpdate(this);
        int i = this.mOffscreenPageLimit;
        int j = Math.max(0, this.mCurItem - i);
        int k = Math.min(-1 + this.mAdapter.getCount(), i + this.mCurItem);
        int m = -1;
        int n = 0;
        if (n < this.mItems.size())
        {
          ItemInfo localItemInfo4 = (ItemInfo)this.mItems.get(n);
          if (((localItemInfo4.position < j) || (localItemInfo4.position > k)) && (!localItemInfo4.scrolling))
          {
            this.mItems.remove(n);
            n--;
            this.mAdapter.destroyItem(this, localItemInfo4.position, localItemInfo4.object);
          }
          for (;;)
          {
            m = localItemInfo4.position;
            n++;
            break;
            if ((m < k) && (localItemInfo4.position > j))
            {
              int i7 = m + 1;
              if (i7 < j) {
                i7 = j;
              }
              while ((i7 <= k) && (i7 < localItemInfo4.position))
              {
                addNewItem(i7, n);
                i7++;
                n++;
              }
            }
          }
        }
        int i1;
        int i6;
        if (this.mItems.size() > 0)
        {
          i1 = ((ItemInfo)this.mItems.get(-1 + this.mItems.size())).position;
          if (i1 >= k) {
            break label313;
          }
          i6 = i1 + 1;
          if (i6 <= j) {
            break label307;
          }
        }
        for (;;)
        {
          if (i6 > k) {
            break label313;
          }
          addNewItem(i6, -1);
          i6++;
          continue;
          i1 = -1;
          break;
          i6 = j;
        }
        int i2 = 0;
        int i3 = this.mItems.size();
        ItemInfo localItemInfo1 = null;
        Object localObject;
        View localView1;
        if (i2 < i3)
        {
          if (((ItemInfo)this.mItems.get(i2)).position == this.mCurItem) {
            localItemInfo1 = (ItemInfo)this.mItems.get(i2);
          }
        }
        else
        {
          PagerAdapter localPagerAdapter = this.mAdapter;
          int i4 = this.mCurItem;
          if (localItemInfo1 == null) {
            break label522;
          }
          localObject = localItemInfo1.object;
          localPagerAdapter.setPrimaryItem(this, i4, localObject);
          this.mAdapter.finishUpdate(this);
          if (!hasFocus()) {
            break;
          }
          localView1 = findFocus();
          if (localView1 == null) {
            break label528;
          }
        }
        for (ItemInfo localItemInfo2 = infoForAnyChild(localView1);; localItemInfo2 = null)
        {
          if ((localItemInfo2 != null) && (localItemInfo2.position == this.mCurItem)) {
            break label532;
          }
          for (int i5 = 0;; i5++)
          {
            if (i5 >= getChildCount()) {
              break label514;
            }
            View localView2 = getChildAt(i5);
            ItemInfo localItemInfo3 = infoForChild(localView2);
            if ((localItemInfo3 != null) && (localItemInfo3.position == this.mCurItem) && (localView2.requestFocus(2))) {
              break;
            }
          }
          break label7;
          i2++;
          break label316;
          localObject = null;
          break label395;
        }
      }
    }
  }
  
  public void setAdapter(PagerAdapter paramPagerAdapter)
  {
    if (this.mAdapter != null)
    {
      this.mAdapter.unregisterDataSetObserver(this.mObserver);
      this.mAdapter.startUpdate(this);
      for (int i = 0; i < this.mItems.size(); i++)
      {
        ItemInfo localItemInfo = (ItemInfo)this.mItems.get(i);
        this.mAdapter.destroyItem(this, localItemInfo.position, localItemInfo.object);
      }
      this.mAdapter.finishUpdate(this);
      this.mItems.clear();
      removeNonDecorViews();
      this.mCurItem = 0;
      scrollTo(0, 0);
    }
    PagerAdapter localPagerAdapter = this.mAdapter;
    this.mAdapter = paramPagerAdapter;
    if (this.mAdapter != null)
    {
      if (this.mObserver == null) {
        this.mObserver = new PagerObserver(null);
      }
      this.mAdapter.registerDataSetObserver(this.mObserver);
      this.mPopulatePending = false;
      if (this.mRestoredCurItem < 0) {
        break label230;
      }
      this.mAdapter.restoreState(this.mRestoredAdapterState, this.mRestoredClassLoader);
      setCurrentItemInternal(this.mRestoredCurItem, false, true);
      this.mRestoredCurItem = -1;
      this.mRestoredAdapterState = null;
      this.mRestoredClassLoader = null;
    }
    for (;;)
    {
      if ((this.mAdapterChangeListener != null) && (localPagerAdapter != paramPagerAdapter)) {
        this.mAdapterChangeListener.onAdapterChanged(localPagerAdapter, paramPagerAdapter);
      }
      return;
      label230:
      populate();
    }
  }
  
  public void setCurrentItem(int paramInt)
  {
    this.mPopulatePending = false;
    if (!this.mFirstLayout) {}
    for (boolean bool = true;; bool = false)
    {
      setCurrentItemInternal(paramInt, bool, false);
      return;
    }
  }
  
  public void setCurrentItem(int paramInt, boolean paramBoolean)
  {
    this.mPopulatePending = false;
    setCurrentItemInternal(paramInt, paramBoolean, false);
  }
  
  void setCurrentItemInternal(int paramInt, boolean paramBoolean1, boolean paramBoolean2)
  {
    setCurrentItemInternal(paramInt, paramBoolean1, paramBoolean2, 0);
  }
  
  void setCurrentItemInternal(int paramInt1, boolean paramBoolean1, boolean paramBoolean2, int paramInt2)
  {
    boolean bool = true;
    if ((this.mAdapter == null) || (this.mAdapter.getCount() <= 0))
    {
      setScrollingCacheEnabled(false);
      return;
    }
    if ((!paramBoolean2) && (this.mCurItem == paramInt1) && (this.mItems.size() != 0))
    {
      setScrollingCacheEnabled(false);
      return;
    }
    if (paramInt1 < 0) {
      paramInt1 = 0;
    }
    for (;;)
    {
      int i = this.mOffscreenPageLimit;
      if ((paramInt1 <= i + this.mCurItem) && (paramInt1 >= this.mCurItem - i)) {
        break;
      }
      for (int j = 0; j < this.mItems.size(); j++) {
        ((ItemInfo)this.mItems.get(j)).scrolling = bool;
      }
      if (paramInt1 >= this.mAdapter.getCount()) {
        paramInt1 = -1 + this.mAdapter.getCount();
      }
    }
    if (this.mCurItem != paramInt1) {}
    int k;
    for (;;)
    {
      this.mCurItem = paramInt1;
      populate();
      k = paramInt1 * (getWidth() + this.mPageMargin);
      if (!paramBoolean1) {
        break label244;
      }
      smoothScrollTo(k, 0, paramInt2);
      if ((bool) && (this.mOnPageChangeListener != null)) {
        this.mOnPageChangeListener.onPageSelected(paramInt1);
      }
      if ((!bool) || (this.mInternalPageChangeListener == null)) {
        break;
      }
      this.mInternalPageChangeListener.onPageSelected(paramInt1);
      return;
      bool = false;
    }
    label244:
    if ((bool) && (this.mOnPageChangeListener != null)) {
      this.mOnPageChangeListener.onPageSelected(paramInt1);
    }
    if ((bool) && (this.mInternalPageChangeListener != null)) {
      this.mInternalPageChangeListener.onPageSelected(paramInt1);
    }
    completeScroll();
    scrollTo(k, 0);
  }
  
  OnPageChangeListener setInternalPageChangeListener(OnPageChangeListener paramOnPageChangeListener)
  {
    OnPageChangeListener localOnPageChangeListener = this.mInternalPageChangeListener;
    this.mInternalPageChangeListener = paramOnPageChangeListener;
    return localOnPageChangeListener;
  }
  
  public void setOffscreenPageLimit(int paramInt)
  {
    if (paramInt < 1)
    {
      Log.w("ViewPager", "Requested offscreen page limit " + paramInt + " too small; defaulting to " + 1);
      paramInt = 1;
    }
    if (paramInt != this.mOffscreenPageLimit)
    {
      this.mOffscreenPageLimit = paramInt;
      populate();
    }
  }
  
  void setOnAdapterChangeListener(OnAdapterChangeListener paramOnAdapterChangeListener)
  {
    this.mAdapterChangeListener = paramOnAdapterChangeListener;
  }
  
  public void setOnPageChangeListener(OnPageChangeListener paramOnPageChangeListener)
  {
    this.mOnPageChangeListener = paramOnPageChangeListener;
  }
  
  public void setPageMargin(int paramInt)
  {
    int i = this.mPageMargin;
    this.mPageMargin = paramInt;
    int j = getWidth();
    recomputeScrollPosition(j, j, paramInt, i);
    requestLayout();
  }
  
  public void setPageMarginDrawable(int paramInt)
  {
    setPageMarginDrawable(getContext().getResources().getDrawable(paramInt));
  }
  
  public void setPageMarginDrawable(Drawable paramDrawable)
  {
    this.mMarginDrawable = paramDrawable;
    if (paramDrawable != null) {
      refreshDrawableState();
    }
    if (paramDrawable == null) {}
    for (boolean bool = true;; bool = false)
    {
      setWillNotDraw(bool);
      invalidate();
      return;
    }
  }
  
  void smoothScrollTo(int paramInt1, int paramInt2)
  {
    smoothScrollTo(paramInt1, paramInt2, 0);
  }
  
  void smoothScrollTo(int paramInt1, int paramInt2, int paramInt3)
  {
    if (getChildCount() == 0)
    {
      setScrollingCacheEnabled(false);
      return;
    }
    int i = getScrollX();
    int j = getScrollY();
    int k = paramInt1 - i;
    int m = paramInt2 - j;
    if ((k == 0) && (m == 0))
    {
      completeScroll();
      setScrollState(0);
      return;
    }
    setScrollingCacheEnabled(true);
    this.mScrolling = true;
    setScrollState(2);
    int n = getWidth();
    int i1 = n / 2;
    float f1 = Math.min(1.0F, 1.0F * Math.abs(k) / n);
    float f2 = i1 + i1 * distanceInfluenceForSnapDuration(f1);
    int i2 = Math.abs(paramInt3);
    if (i2 > 0) {}
    for (int i3 = 4 * Math.round(1000.0F * Math.abs(f2 / i2));; i3 = (int)(100.0F * (1.0F + Math.abs(k) / (n + this.mPageMargin))))
    {
      int i4 = Math.min(i3, 600);
      this.mScroller.startScroll(i, j, k, m, i4);
      invalidate();
      return;
    }
  }
  
  protected boolean verifyDrawable(Drawable paramDrawable)
  {
    return (super.verifyDrawable(paramDrawable)) || (paramDrawable == this.mMarginDrawable);
  }
  
  static abstract interface Decor {}
  
  static class ItemInfo
  {
    Object object;
    int position;
    boolean scrolling;
    
    ItemInfo() {}
  }
  
  public static class LayoutParams
    extends ViewGroup.LayoutParams
  {
    public int gravity;
    public boolean isDecor;
    
    public LayoutParams()
    {
      super(-1);
    }
    
    public LayoutParams(Context paramContext, AttributeSet paramAttributeSet)
    {
      super(paramAttributeSet);
      TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, ViewPager.LAYOUT_ATTRS);
      this.gravity = localTypedArray.getInteger(0, 0);
      localTypedArray.recycle();
    }
  }
  
  static abstract interface OnAdapterChangeListener
  {
    public abstract void onAdapterChanged(PagerAdapter paramPagerAdapter1, PagerAdapter paramPagerAdapter2);
  }
  
  public static abstract interface OnPageChangeListener
  {
    public abstract void onPageScrollStateChanged(int paramInt);
    
    public abstract void onPageScrolled(int paramInt1, float paramFloat, int paramInt2);
    
    public abstract void onPageSelected(int paramInt);
  }
  
  private class PagerObserver
    extends DataSetObserver
  {
    private PagerObserver() {}
    
    public void onChanged()
    {
      ViewPager.this.dataSetChanged();
    }
    
    public void onInvalidated()
    {
      ViewPager.this.dataSetChanged();
    }
  }
  
  public static class SavedState
    extends View.BaseSavedState
  {
    public static final Parcelable.Creator<SavedState> CREATOR = ParcelableCompat.newCreator(new ParcelableCompatCreatorCallbacks()
    {
      public ViewPager.SavedState createFromParcel(Parcel paramAnonymousParcel, ClassLoader paramAnonymousClassLoader)
      {
        return new ViewPager.SavedState(paramAnonymousParcel, paramAnonymousClassLoader);
      }
      
      public ViewPager.SavedState[] newArray(int paramAnonymousInt)
      {
        return new ViewPager.SavedState[paramAnonymousInt];
      }
    });
    Parcelable adapterState;
    ClassLoader loader;
    int position;
    
    SavedState(Parcel paramParcel, ClassLoader paramClassLoader)
    {
      super();
      if (paramClassLoader == null) {
        paramClassLoader = getClass().getClassLoader();
      }
      this.position = paramParcel.readInt();
      this.adapterState = paramParcel.readParcelable(paramClassLoader);
      this.loader = paramClassLoader;
    }
    
    public SavedState(Parcelable paramParcelable)
    {
      super();
    }
    
    public String toString()
    {
      return "FragmentPager.SavedState{" + Integer.toHexString(System.identityHashCode(this)) + " position=" + this.position + "}";
    }
    
    public void writeToParcel(Parcel paramParcel, int paramInt)
    {
      super.writeToParcel(paramParcel, paramInt);
      paramParcel.writeInt(this.position);
      paramParcel.writeParcelable(this.adapterState, paramInt);
    }
  }
  
  public static class SimpleOnPageChangeListener
    implements ViewPager.OnPageChangeListener
  {
    public SimpleOnPageChangeListener() {}
    
    public void onPageScrollStateChanged(int paramInt) {}
    
    public void onPageScrolled(int paramInt1, float paramFloat, int paramInt2) {}
    
    public void onPageSelected(int paramInt) {}
  }
}
