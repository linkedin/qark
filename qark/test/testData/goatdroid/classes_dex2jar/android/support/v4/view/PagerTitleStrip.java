package android.support.v4.view;

import android.content.Context;
import android.content.res.ColorStateList;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.database.DataSetObserver;
import android.graphics.drawable.Drawable;
import android.text.TextUtils.TruncateAt;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.View.MeasureSpec;
import android.view.ViewGroup;
import android.view.ViewParent;
import android.widget.TextView;

public class PagerTitleStrip
  extends ViewGroup
  implements ViewPager.Decor
{
  private static final int[] ATTRS = { 16842804, 16842904, 16842901 };
  private static final int SIDE_ALPHA = 153;
  private static final String TAG = "PagerTitleStrip";
  private static final int TEXT_SPACING = 16;
  private TextView mCurrText;
  private int mLastKnownCurrentPage = -1;
  private float mLastKnownPositionOffset = -1.0F;
  private TextView mNextText;
  private final PageListener mPageListener = new PageListener(null);
  ViewPager mPager;
  private TextView mPrevText;
  private int mScaledTextSpacing;
  private boolean mUpdatingPositions;
  private boolean mUpdatingText;
  
  public PagerTitleStrip(Context paramContext)
  {
    this(paramContext, null);
  }
  
  public PagerTitleStrip(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    TextView localTextView1 = new TextView(paramContext);
    this.mPrevText = localTextView1;
    addView(localTextView1);
    TextView localTextView2 = new TextView(paramContext);
    this.mCurrText = localTextView2;
    addView(localTextView2);
    TextView localTextView3 = new TextView(paramContext);
    this.mNextText = localTextView3;
    addView(localTextView3);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, ATTRS);
    int i = localTypedArray.getResourceId(0, 0);
    if (i != 0)
    {
      this.mPrevText.setTextAppearance(paramContext, i);
      this.mCurrText.setTextAppearance(paramContext, i);
      this.mNextText.setTextAppearance(paramContext, i);
    }
    if (localTypedArray.hasValue(1))
    {
      int m = localTypedArray.getColor(1, 0);
      this.mPrevText.setTextColor(m);
      this.mCurrText.setTextColor(m);
      this.mNextText.setTextColor(m);
    }
    int j = localTypedArray.getDimensionPixelSize(2, 0);
    if (j != 0)
    {
      this.mPrevText.setTextSize(0, j);
      this.mCurrText.setTextSize(0, j);
      this.mNextText.setTextSize(0, j);
    }
    localTypedArray.recycle();
    int k = 0x99000000 | 0xFFFFFF & this.mPrevText.getTextColors().getDefaultColor();
    this.mPrevText.setTextColor(k);
    this.mNextText.setTextColor(k);
    this.mPrevText.setEllipsize(TextUtils.TruncateAt.END);
    this.mCurrText.setEllipsize(TextUtils.TruncateAt.END);
    this.mNextText.setEllipsize(TextUtils.TruncateAt.END);
    this.mPrevText.setSingleLine();
    this.mCurrText.setSingleLine();
    this.mNextText.setSingleLine();
    this.mScaledTextSpacing = ((int)(16.0F * paramContext.getResources().getDisplayMetrics().density));
  }
  
  protected void onAttachedToWindow()
  {
    super.onAttachedToWindow();
    ViewParent localViewParent = getParent();
    if (!(localViewParent instanceof ViewPager)) {
      throw new IllegalStateException("PagerTitleStrip must be a direct child of a ViewPager.");
    }
    ViewPager localViewPager = (ViewPager)localViewParent;
    PagerAdapter localPagerAdapter = localViewPager.getAdapter();
    localViewPager.setInternalPageChangeListener(this.mPageListener);
    localViewPager.setOnAdapterChangeListener(this.mPageListener);
    this.mPager = localViewPager;
    updateAdapter(null, localPagerAdapter);
  }
  
  protected void onDetachedFromWindow()
  {
    updateAdapter(this.mPager.getAdapter(), null);
    this.mPager.setInternalPageChangeListener(null);
    this.mPager.setOnAdapterChangeListener(null);
    this.mPager = null;
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    if (this.mPager != null) {
      updateTextPositions(this.mPager.getCurrentItem(), 0.0F);
    }
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    int i = View.MeasureSpec.getMode(paramInt1);
    int j = View.MeasureSpec.getMode(paramInt2);
    int k = View.MeasureSpec.getSize(paramInt1);
    int m = View.MeasureSpec.getSize(paramInt2);
    if (i != 1073741824) {
      throw new IllegalStateException("Must measure with an exact width");
    }
    Drawable localDrawable = getBackground();
    int n = 0;
    if (localDrawable != null) {
      n = localDrawable.getIntrinsicHeight();
    }
    int i1 = getPaddingTop() + getPaddingBottom();
    int i2 = m - i1;
    int i3 = View.MeasureSpec.makeMeasureSpec((int)(0.8F * k), Integer.MIN_VALUE);
    int i4 = View.MeasureSpec.makeMeasureSpec(i2, j);
    this.mPrevText.measure(i3, i4);
    this.mCurrText.measure(i3, i4);
    this.mNextText.measure(i3, i4);
    if (j == 1073741824)
    {
      setMeasuredDimension(k, m);
      return;
    }
    setMeasuredDimension(k, Math.max(n, i1 + this.mCurrText.getMeasuredHeight()));
  }
  
  public void requestLayout()
  {
    if (!this.mUpdatingText) {
      super.requestLayout();
    }
  }
  
  void updateAdapter(PagerAdapter paramPagerAdapter1, PagerAdapter paramPagerAdapter2)
  {
    if (paramPagerAdapter1 != null) {
      paramPagerAdapter1.unregisterDataSetObserver(this.mPageListener);
    }
    if (paramPagerAdapter2 != null) {
      paramPagerAdapter2.registerDataSetObserver(this.mPageListener);
    }
    if (this.mPager != null)
    {
      this.mLastKnownCurrentPage = -1;
      this.mLastKnownPositionOffset = -1.0F;
      updateText(this.mPager.getCurrentItem(), paramPagerAdapter2);
      requestLayout();
    }
  }
  
  void updateText(int paramInt, PagerAdapter paramPagerAdapter)
  {
    int i;
    TextView localTextView;
    if (paramPagerAdapter != null)
    {
      i = paramPagerAdapter.getCount();
      this.mUpdatingText = true;
      CharSequence localCharSequence1 = null;
      if (paramInt >= 1)
      {
        localCharSequence1 = null;
        if (paramPagerAdapter != null) {
          localCharSequence1 = paramPagerAdapter.getPageTitle(paramInt - 1);
        }
      }
      this.mPrevText.setText(localCharSequence1);
      localTextView = this.mCurrText;
      if (paramPagerAdapter == null) {
        break label230;
      }
    }
    label230:
    for (CharSequence localCharSequence2 = paramPagerAdapter.getPageTitle(paramInt);; localCharSequence2 = null)
    {
      localTextView.setText(localCharSequence2);
      int j = paramInt + 1;
      CharSequence localCharSequence3 = null;
      if (j < i)
      {
        localCharSequence3 = null;
        if (paramPagerAdapter != null) {
          localCharSequence3 = paramPagerAdapter.getPageTitle(paramInt + 1);
        }
      }
      this.mNextText.setText(localCharSequence3);
      int k = getWidth() - getPaddingLeft() - getPaddingRight();
      int m = getHeight() - getPaddingTop() - getPaddingBottom();
      int n = View.MeasureSpec.makeMeasureSpec((int)(0.8F * k), Integer.MIN_VALUE);
      int i1 = View.MeasureSpec.makeMeasureSpec(m, 1073741824);
      this.mPrevText.measure(n, i1);
      this.mCurrText.measure(n, i1);
      this.mNextText.measure(n, i1);
      this.mLastKnownCurrentPage = paramInt;
      if (!this.mUpdatingPositions) {
        updateTextPositions(paramInt, this.mLastKnownPositionOffset);
      }
      this.mUpdatingText = false;
      return;
      i = 0;
      break;
    }
  }
  
  void updateTextPositions(int paramInt, float paramFloat)
  {
    if (paramInt != this.mLastKnownCurrentPage) {
      updateText(paramInt, this.mPager.getAdapter());
    }
    while (paramFloat != this.mLastKnownPositionOffset)
    {
      this.mUpdatingPositions = true;
      int i = this.mPrevText.getMeasuredWidth();
      int j = this.mCurrText.getMeasuredWidth();
      int k = this.mNextText.getMeasuredWidth();
      int m = j / 2;
      int n = getWidth();
      int i1 = getPaddingLeft();
      int i2 = getPaddingRight();
      int i3 = getPaddingTop();
      int i4 = i1 + m;
      int i5 = i2 + m;
      int i6 = n - i4 - i5;
      float f = paramFloat + 0.5F;
      if (f > 1.0F) {
        f -= 1.0F;
      }
      int i7 = n - i5 - (int)(f * i6) - j / 2;
      int i8 = i7 + j;
      this.mCurrText.layout(i7, i3, i8, i3 + this.mCurrText.getMeasuredHeight());
      int i9 = Math.min(i1, i7 - this.mScaledTextSpacing - i);
      this.mPrevText.layout(i9, i3, i9 + i, i3 + this.mPrevText.getMeasuredHeight());
      int i10 = Math.max(n - i2 - k, i8 + this.mScaledTextSpacing);
      this.mNextText.layout(i10, i3, i10 + k, i3 + this.mNextText.getMeasuredHeight());
      this.mLastKnownPositionOffset = paramFloat;
      this.mUpdatingPositions = false;
      return;
    }
  }
  
  private class PageListener
    extends DataSetObserver
    implements ViewPager.OnPageChangeListener, ViewPager.OnAdapterChangeListener
  {
    private int mScrollState;
    
    private PageListener() {}
    
    public void onAdapterChanged(PagerAdapter paramPagerAdapter1, PagerAdapter paramPagerAdapter2)
    {
      PagerTitleStrip.this.updateAdapter(paramPagerAdapter1, paramPagerAdapter2);
    }
    
    public void onChanged()
    {
      PagerTitleStrip.this.updateText(PagerTitleStrip.this.mPager.getCurrentItem(), PagerTitleStrip.this.mPager.getAdapter());
    }
    
    public void onPageScrollStateChanged(int paramInt)
    {
      this.mScrollState = paramInt;
    }
    
    public void onPageScrolled(int paramInt1, float paramFloat, int paramInt2)
    {
      if (paramFloat > 0.5F) {
        paramInt1++;
      }
      PagerTitleStrip.this.updateTextPositions(paramInt1, paramFloat);
    }
    
    public void onPageSelected(int paramInt)
    {
      if (this.mScrollState == 0) {
        PagerTitleStrip.this.updateText(PagerTitleStrip.this.mPager.getCurrentItem(), PagerTitleStrip.this.mPager.getAdapter());
      }
    }
  }
}
