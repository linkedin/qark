package android.support.v4.view.accessibility;

import android.os.Parcelable;
import android.view.View;
import android.view.accessibility.AccessibilityRecord;
import java.util.List;

class AccessibilityRecordCompatIcs
{
  AccessibilityRecordCompatIcs() {}
  
  public static int getAddedCount(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getAddedCount();
  }
  
  public static CharSequence getBeforeText(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getBeforeText();
  }
  
  public static CharSequence getClassName(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getClassName();
  }
  
  public static CharSequence getContentDescription(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getContentDescription();
  }
  
  public static int getCurrentItemIndex(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getCurrentItemIndex();
  }
  
  public static int getFromIndex(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getFromIndex();
  }
  
  public static int getItemCount(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getItemCount();
  }
  
  public static Parcelable getParcelableData(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getParcelableData();
  }
  
  public static int getRemovedCount(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getRemovedCount();
  }
  
  public static int getScrollX(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getScrollX();
  }
  
  public static int getScrollY(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getScrollY();
  }
  
  public static Object getSource(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getSource();
  }
  
  public static List<CharSequence> getText(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getText();
  }
  
  public static int getToIndex(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getToIndex();
  }
  
  public static int getWindowId(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).getWindowId();
  }
  
  public static boolean isChecked(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).isChecked();
  }
  
  public static boolean isEnabled(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).isEnabled();
  }
  
  public static boolean isFullScreen(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).isFullScreen();
  }
  
  public static boolean isPassword(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).isPassword();
  }
  
  public static boolean isScrollable(Object paramObject)
  {
    return ((AccessibilityRecord)paramObject).isScrollable();
  }
  
  public static Object obtain()
  {
    return AccessibilityRecord.obtain();
  }
  
  public static Object obtain(Object paramObject)
  {
    return AccessibilityRecord.obtain((AccessibilityRecord)paramObject);
  }
  
  public static void recycle(Object paramObject)
  {
    ((AccessibilityRecord)paramObject).recycle();
  }
  
  public static void setAddedCount(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setAddedCount(paramInt);
  }
  
  public static void setBeforeText(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityRecord)paramObject).setBeforeText(paramCharSequence);
  }
  
  public static void setChecked(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityRecord)paramObject).setChecked(paramBoolean);
  }
  
  public static void setClassName(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityRecord)paramObject).setClassName(paramCharSequence);
  }
  
  public static void setContentDescription(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityRecord)paramObject).setContentDescription(paramCharSequence);
  }
  
  public static void setCurrentItemIndex(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setCurrentItemIndex(paramInt);
  }
  
  public static void setEnabled(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityRecord)paramObject).setEnabled(paramBoolean);
  }
  
  public static void setFromIndex(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setFromIndex(paramInt);
  }
  
  public static void setFullScreen(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityRecord)paramObject).setFullScreen(paramBoolean);
  }
  
  public static void setItemCount(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setItemCount(paramInt);
  }
  
  public static void setParcelableData(Object paramObject, Parcelable paramParcelable)
  {
    ((AccessibilityRecord)paramObject).setParcelableData(paramParcelable);
  }
  
  public static void setPassword(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityRecord)paramObject).setPassword(paramBoolean);
  }
  
  public static void setRemovedCount(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setRemovedCount(paramInt);
  }
  
  public static void setScrollX(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setScrollX(paramInt);
  }
  
  public static void setScrollY(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setScrollY(paramInt);
  }
  
  public static void setScrollable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityRecord)paramObject).setScrollable(paramBoolean);
  }
  
  public static void setSource(Object paramObject, View paramView)
  {
    ((AccessibilityRecord)paramObject).setSource(paramView);
  }
  
  public static void setToIndex(Object paramObject, int paramInt)
  {
    ((AccessibilityRecord)paramObject).setToIndex(paramInt);
  }
}
