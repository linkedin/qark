package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.os.Build.VERSION;
import android.util.AttributeSet;
import android.widget.Button;
import java.util.Locale;

public class CapitalizingButton
  extends Button
{
  private static final boolean IS_GINGERBREAD;
  private static final int[] R_styleable_Button;
  private static final int R_styleable_Button_textAllCaps;
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
      R_styleable_Button = new int[] { 16843660 };
      return;
      bool1 = false;
      break;
    }
  }
  
  public CapitalizingButton(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R_styleable_Button);
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
