package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.os.Build.VERSION;
import android.util.AttributeSet;
import android.widget.TextView;
import java.util.Locale;

public class CapitalizingTextView
  extends TextView
{
  private static final boolean IS_GINGERBREAD;
  private static final int[] R_styleable_TextView;
  private static final int R_styleable_TextView_textAllCaps;
  private static final boolean SANS_ICE_CREAM;
  private boolean mAllCaps;
  
  static
  {
    boolean bool1;
    if (Build.VERSION.SDK_INT < 14)
    {
      bool1 = true;
      SANS_ICE_CREAM = bool1;
      if (Build.VERSION.SDK_INT < 9) {
        break label45;
      }
    }
    label45:
    for (boolean bool2 = true;; bool2 = false)
    {
      IS_GINGERBREAD = bool2;
      R_styleable_TextView = new int[] { 16843660 };
      return;
      bool1 = false;
      break;
    }
  }
  
  public CapitalizingTextView(Context paramContext, AttributeSet paramAttributeSet)
  {
    this(paramContext, paramAttributeSet, 0);
  }
  
  public CapitalizingTextView(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R_styleable_TextView, paramInt, 0);
    this.mAllCaps = localTypedArray.getBoolean(0, true);
    localTypedArray.recycle();
  }
  
  public void setTextCompat(CharSequence paramCharSequence)
  {
    if ((SANS_ICE_CREAM) && (this.mAllCaps) && (paramCharSequence != null))
    {
      if (IS_GINGERBREAD)
      {
        setText(paramCharSequence.toString().toUpperCase(Locale.ROOT));
        return;
      }
      setText(paramCharSequence.toString().toUpperCase());
      return;
    }
    setText(paramCharSequence);
  }
}
