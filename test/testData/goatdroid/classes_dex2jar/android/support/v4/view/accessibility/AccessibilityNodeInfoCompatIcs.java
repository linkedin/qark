package android.support.v4.view.accessibility;

import android.graphics.Rect;
import android.view.View;
import android.view.accessibility.AccessibilityNodeInfo;
import java.util.List;

class AccessibilityNodeInfoCompatIcs
{
  AccessibilityNodeInfoCompatIcs() {}
  
  public static void addAction(Object paramObject, int paramInt)
  {
    ((AccessibilityNodeInfo)paramObject).addAction(paramInt);
  }
  
  public static void addChild(Object paramObject, View paramView)
  {
    ((AccessibilityNodeInfo)paramObject).addChild(paramView);
  }
  
  public static List<Object> findAccessibilityNodeInfosByText(Object paramObject, String paramString)
  {
    return (List)((AccessibilityNodeInfo)paramObject).findAccessibilityNodeInfosByText(paramString);
  }
  
  public static int getActions(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getActions();
  }
  
  public static void getBoundsInParent(Object paramObject, Rect paramRect)
  {
    ((AccessibilityNodeInfo)paramObject).getBoundsInParent(paramRect);
  }
  
  public static void getBoundsInScreen(Object paramObject, Rect paramRect)
  {
    ((AccessibilityNodeInfo)paramObject).getBoundsInScreen(paramRect);
  }
  
  public static Object getChild(Object paramObject, int paramInt)
  {
    return ((AccessibilityNodeInfo)paramObject).getChild(paramInt);
  }
  
  public static int getChildCount(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getChildCount();
  }
  
  public static CharSequence getClassName(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getClassName();
  }
  
  public static CharSequence getContentDescription(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getContentDescription();
  }
  
  public static CharSequence getPackageName(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getPackageName();
  }
  
  public static Object getParent(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getParent();
  }
  
  public static CharSequence getText(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getText();
  }
  
  public static int getWindowId(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).getWindowId();
  }
  
  public static boolean isCheckable(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isCheckable();
  }
  
  public static boolean isChecked(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isChecked();
  }
  
  public static boolean isClickable(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isClickable();
  }
  
  public static boolean isEnabled(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isEnabled();
  }
  
  public static boolean isFocusable(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isFocusable();
  }
  
  public static boolean isFocused(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isFocused();
  }
  
  public static boolean isLongClickable(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isLongClickable();
  }
  
  public static boolean isPassword(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isPassword();
  }
  
  public static boolean isScrollable(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isScrollable();
  }
  
  public static boolean isSelected(Object paramObject)
  {
    return ((AccessibilityNodeInfo)paramObject).isSelected();
  }
  
  public static Object obtain()
  {
    return AccessibilityNodeInfo.obtain();
  }
  
  public static Object obtain(View paramView)
  {
    return AccessibilityNodeInfo.obtain(paramView);
  }
  
  public static Object obtain(Object paramObject)
  {
    return AccessibilityNodeInfo.obtain((AccessibilityNodeInfo)paramObject);
  }
  
  public static boolean performAction(Object paramObject, int paramInt)
  {
    return ((AccessibilityNodeInfo)paramObject).performAction(paramInt);
  }
  
  public static void recycle(Object paramObject)
  {
    ((AccessibilityNodeInfo)paramObject).recycle();
  }
  
  public static void setBoundsInParent(Object paramObject, Rect paramRect)
  {
    ((AccessibilityNodeInfo)paramObject).setBoundsInParent(paramRect);
  }
  
  public static void setBoundsInScreen(Object paramObject, Rect paramRect)
  {
    ((AccessibilityNodeInfo)paramObject).setBoundsInScreen(paramRect);
  }
  
  public static void setCheckable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setCheckable(paramBoolean);
  }
  
  public static void setChecked(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setChecked(paramBoolean);
  }
  
  public static void setClassName(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityNodeInfo)paramObject).setClassName(paramCharSequence);
  }
  
  public static void setClickable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setClickable(paramBoolean);
  }
  
  public static void setContentDescription(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityNodeInfo)paramObject).setContentDescription(paramCharSequence);
  }
  
  public static void setEnabled(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setEnabled(paramBoolean);
  }
  
  public static void setFocusable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setFocusable(paramBoolean);
  }
  
  public static void setFocused(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setFocused(paramBoolean);
  }
  
  public static void setLongClickable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setLongClickable(paramBoolean);
  }
  
  public static void setPackageName(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityNodeInfo)paramObject).setPackageName(paramCharSequence);
  }
  
  public static void setParent(Object paramObject, View paramView)
  {
    ((AccessibilityNodeInfo)paramObject).setParent(paramView);
  }
  
  public static void setPassword(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setPassword(paramBoolean);
  }
  
  public static void setScrollable(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setScrollable(paramBoolean);
  }
  
  public static void setSelected(Object paramObject, boolean paramBoolean)
  {
    ((AccessibilityNodeInfo)paramObject).setSelected(paramBoolean);
  }
  
  public static void setSource(Object paramObject, View paramView)
  {
    ((AccessibilityNodeInfo)paramObject).setSource(paramView);
  }
  
  public static void setText(Object paramObject, CharSequence paramCharSequence)
  {
    ((AccessibilityNodeInfo)paramObject).setText(paramCharSequence);
  }
}
