package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.util.TypedValue;
import android.view.View.MeasureSpec;
import android.widget.LinearLayout;
import com.actionbarsherlock.R.styleable;

public class FakeDialogPhoneWindow
  extends LinearLayout
{
  final TypedValue mMinWidthMajor = new TypedValue();
  final TypedValue mMinWidthMinor = new TypedValue();
  
  public FakeDialogPhoneWindow(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockTheme);
    localTypedArray.getValue(34, this.mMinWidthMajor);
    localTypedArray.getValue(35, this.mMinWidthMinor);
    localTypedArray.recycle();
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    DisplayMetrics localDisplayMetrics = getContext().getResources().getDisplayMetrics();
    int i;
    int j;
    int k;
    TypedValue localTypedValue;
    label57:
    int n;
    int i1;
    if (localDisplayMetrics.widthPixels < localDisplayMetrics.heightPixels)
    {
      i = 1;
      super.onMeasure(paramInt1, paramInt2);
      j = getMeasuredWidth();
      k = View.MeasureSpec.makeMeasureSpec(j, 1073741824);
      if (i == 0) {
        break label131;
      }
      localTypedValue = this.mMinWidthMinor;
      int m = localTypedValue.type;
      n = 0;
      if (m != 0)
      {
        if (localTypedValue.type != 5) {
          break label140;
        }
        i1 = (int)localTypedValue.getDimension(localDisplayMetrics);
      }
    }
    for (;;)
    {
      n = 0;
      if (j < i1)
      {
        k = View.MeasureSpec.makeMeasureSpec(i1, 1073741824);
        n = 1;
      }
      if (n != 0) {
        super.onMeasure(k, paramInt2);
      }
      return;
      i = 0;
      break;
      label131:
      localTypedValue = this.mMinWidthMajor;
      break label57;
      label140:
      if (localTypedValue.type == 6) {
        i1 = (int)localTypedValue.getFraction(localDisplayMetrics.widthPixels, localDisplayMetrics.widthPixels);
      } else {
        i1 = 0;
      }
    }
  }
}
