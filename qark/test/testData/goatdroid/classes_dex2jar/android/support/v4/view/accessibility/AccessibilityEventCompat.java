package android.support.v4.view.accessibility;

import android.os.Build.VERSION;
import android.view.accessibility.AccessibilityEvent;

public class AccessibilityEventCompat
{
  private static final AccessibilityEventVersionImpl IMPL = new AccessibilityEventStubImpl();
  public static final int TYPE_TOUCH_EXPLORATION_GESTURE_END = 1024;
  public static final int TYPE_TOUCH_EXPLORATION_GESTURE_START = 512;
  public static final int TYPE_VIEW_HOVER_ENTER = 128;
  public static final int TYPE_VIEW_HOVER_EXIT = 256;
  public static final int TYPE_VIEW_SCROLLED = 4096;
  public static final int TYPE_VIEW_TEXT_SELECTION_CHANGED = 8192;
  public static final int TYPE_WINDOW_CONTENT_CHANGED = 2048;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14)
    {
      IMPL = new AccessibilityEventIcsImpl();
      return;
    }
  }
  
  private AccessibilityEventCompat() {}
  
  public static void appendRecord(AccessibilityEvent paramAccessibilityEvent, AccessibilityRecordCompat paramAccessibilityRecordCompat)
  {
    IMPL.appendRecord(paramAccessibilityEvent, paramAccessibilityRecordCompat.getImpl());
  }
  
  public static AccessibilityRecordCompat getRecord(AccessibilityEvent paramAccessibilityEvent, int paramInt)
  {
    return new AccessibilityRecordCompat(IMPL.getRecord(paramAccessibilityEvent, paramInt));
  }
  
  public static int getRecordCount(AccessibilityEvent paramAccessibilityEvent)
  {
    return IMPL.getRecordCount(paramAccessibilityEvent);
  }
  
  static class AccessibilityEventIcsImpl
    extends AccessibilityEventCompat.AccessibilityEventStubImpl
  {
    AccessibilityEventIcsImpl() {}
    
    public void appendRecord(AccessibilityEvent paramAccessibilityEvent, Object paramObject)
    {
      AccessibilityEventCompatIcs.appendRecord(paramAccessibilityEvent, paramObject);
    }
    
    public Object getRecord(AccessibilityEvent paramAccessibilityEvent, int paramInt)
    {
      return AccessibilityEventCompatIcs.getRecord(paramAccessibilityEvent, paramInt);
    }
    
    public int getRecordCount(AccessibilityEvent paramAccessibilityEvent)
    {
      return AccessibilityEventCompatIcs.getRecordCount(paramAccessibilityEvent);
    }
  }
  
  static class AccessibilityEventStubImpl
    implements AccessibilityEventCompat.AccessibilityEventVersionImpl
  {
    AccessibilityEventStubImpl() {}
    
    public void appendRecord(AccessibilityEvent paramAccessibilityEvent, Object paramObject) {}
    
    public Object getRecord(AccessibilityEvent paramAccessibilityEvent, int paramInt)
    {
      return null;
    }
    
    public int getRecordCount(AccessibilityEvent paramAccessibilityEvent)
    {
      return 0;
    }
  }
  
  static abstract interface AccessibilityEventVersionImpl
  {
    public abstract void appendRecord(AccessibilityEvent paramAccessibilityEvent, Object paramObject);
    
    public abstract Object getRecord(AccessibilityEvent paramAccessibilityEvent, int paramInt);
    
    public abstract int getRecordCount(AccessibilityEvent paramAccessibilityEvent);
  }
}
