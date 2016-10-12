package android.support.v4.view.accessibility;

import android.os.Build.VERSION;
import android.os.Parcelable;
import android.view.View;
import java.util.Collections;
import java.util.List;

public class AccessibilityRecordCompat
{
  private static final AccessibilityRecordImpl IMPL = new AccessibilityRecordStubImpl();
  private final Object mRecord;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14)
    {
      IMPL = new AccessibilityRecordIcsImpl();
      return;
    }
  }
  
  public AccessibilityRecordCompat(Object paramObject)
  {
    this.mRecord = paramObject;
  }
  
  public static AccessibilityRecordCompat obtain()
  {
    return new AccessibilityRecordCompat(IMPL.obtain());
  }
  
  public static AccessibilityRecordCompat obtain(AccessibilityRecordCompat paramAccessibilityRecordCompat)
  {
    return new AccessibilityRecordCompat(IMPL.obtain(paramAccessibilityRecordCompat.mRecord));
  }
  
  public boolean equals(Object paramObject)
  {
    if (this == paramObject) {}
    AccessibilityRecordCompat localAccessibilityRecordCompat;
    do
    {
      do
      {
        return true;
        if (paramObject == null) {
          return false;
        }
        if (getClass() != paramObject.getClass()) {
          return false;
        }
        localAccessibilityRecordCompat = (AccessibilityRecordCompat)paramObject;
        if (this.mRecord != null) {
          break;
        }
      } while (localAccessibilityRecordCompat.mRecord == null);
      return false;
    } while (this.mRecord.equals(localAccessibilityRecordCompat.mRecord));
    return false;
  }
  
  public int getAddedCount()
  {
    return IMPL.getAddedCount(this.mRecord);
  }
  
  public CharSequence getBeforeText()
  {
    return IMPL.getBeforeText(this.mRecord);
  }
  
  public CharSequence getClassName()
  {
    return IMPL.getClassName(this.mRecord);
  }
  
  public CharSequence getContentDescription()
  {
    return IMPL.getContentDescription(this.mRecord);
  }
  
  public int getCurrentItemIndex()
  {
    return IMPL.getCurrentItemIndex(this.mRecord);
  }
  
  public int getFromIndex()
  {
    return IMPL.getFromIndex(this.mRecord);
  }
  
  public Object getImpl()
  {
    return this.mRecord;
  }
  
  public int getItemCount()
  {
    return IMPL.getItemCount(this.mRecord);
  }
  
  public Parcelable getParcelableData()
  {
    return IMPL.getParcelableData(this.mRecord);
  }
  
  public int getRemovedCount()
  {
    return IMPL.getRemovedCount(this.mRecord);
  }
  
  public int getScrollX()
  {
    return IMPL.getScrollX(this.mRecord);
  }
  
  public int getScrollY()
  {
    return IMPL.getScrollY(this.mRecord);
  }
  
  public AccessibilityNodeInfoCompat getSource()
  {
    return new AccessibilityNodeInfoCompat(IMPL.getSource(this.mRecord));
  }
  
  public List<CharSequence> getText()
  {
    return IMPL.getText(this.mRecord);
  }
  
  public int getToIndex()
  {
    return IMPL.getToIndex(this.mRecord);
  }
  
  public int getWindowId()
  {
    return IMPL.getWindowId(this.mRecord);
  }
  
  public int hashCode()
  {
    if (this.mRecord == null) {
      return 0;
    }
    return this.mRecord.hashCode();
  }
  
  public boolean isChecked()
  {
    return IMPL.isChecked(this.mRecord);
  }
  
  public boolean isEnabled()
  {
    return IMPL.isEnabled(this.mRecord);
  }
  
  public boolean isFullScreen()
  {
    return IMPL.isFullScreen(this.mRecord);
  }
  
  public boolean isPassword()
  {
    return IMPL.isPassword(this.mRecord);
  }
  
  public boolean isScrollable()
  {
    return IMPL.isScrollable(this.mRecord);
  }
  
  public void recycle()
  {
    IMPL.recycle(this.mRecord);
  }
  
  public void setAddedCount(int paramInt)
  {
    IMPL.setAddedCount(this.mRecord, paramInt);
  }
  
  public void setBeforeText(CharSequence paramCharSequence)
  {
    IMPL.setBeforeText(this.mRecord, paramCharSequence);
  }
  
  public void setChecked(boolean paramBoolean)
  {
    IMPL.setChecked(this.mRecord, paramBoolean);
  }
  
  public void setClassName(CharSequence paramCharSequence)
  {
    IMPL.setClassName(this.mRecord, paramCharSequence);
  }
  
  public void setContentDescription(CharSequence paramCharSequence)
  {
    IMPL.setContentDescription(this.mRecord, paramCharSequence);
  }
  
  public void setCurrentItemIndex(int paramInt)
  {
    IMPL.setCurrentItemIndex(this.mRecord, paramInt);
  }
  
  public void setEnabled(boolean paramBoolean)
  {
    IMPL.setEnabled(this.mRecord, paramBoolean);
  }
  
  public void setFromIndex(int paramInt)
  {
    IMPL.setFromIndex(this.mRecord, paramInt);
  }
  
  public void setFullScreen(boolean paramBoolean)
  {
    IMPL.setFullScreen(this.mRecord, paramBoolean);
  }
  
  public void setItemCount(int paramInt)
  {
    IMPL.setItemCount(this.mRecord, paramInt);
  }
  
  public void setParcelableData(Parcelable paramParcelable)
  {
    IMPL.setParcelableData(this.mRecord, paramParcelable);
  }
  
  public void setPassword(boolean paramBoolean)
  {
    IMPL.setPassword(this.mRecord, paramBoolean);
  }
  
  public void setRemovedCount(int paramInt)
  {
    IMPL.setRemovedCount(this.mRecord, paramInt);
  }
  
  public void setScrollX(int paramInt)
  {
    IMPL.setScrollX(this.mRecord, paramInt);
  }
  
  public void setScrollY(int paramInt)
  {
    IMPL.setScrollY(this.mRecord, paramInt);
  }
  
  public void setScrollable(boolean paramBoolean)
  {
    IMPL.setScrollable(this.mRecord, paramBoolean);
  }
  
  public void setSource(View paramView)
  {
    IMPL.setSource(this.mRecord, paramView);
  }
  
  public void setToIndex(int paramInt)
  {
    IMPL.setToIndex(this.mRecord, paramInt);
  }
  
  static class AccessibilityRecordIcsImpl
    implements AccessibilityRecordCompat.AccessibilityRecordImpl
  {
    AccessibilityRecordIcsImpl() {}
    
    public int getAddedCount(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getAddedCount(paramObject);
    }
    
    public CharSequence getBeforeText(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getBeforeText(paramObject);
    }
    
    public CharSequence getClassName(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getClassName(paramObject);
    }
    
    public CharSequence getContentDescription(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getContentDescription(paramObject);
    }
    
    public int getCurrentItemIndex(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getCurrentItemIndex(paramObject);
    }
    
    public int getFromIndex(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getFromIndex(paramObject);
    }
    
    public int getItemCount(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getItemCount(paramObject);
    }
    
    public int getMaxScrollX(Object paramObject)
    {
      return 0;
    }
    
    public int getMaxScrollY(Object paramObject)
    {
      return 0;
    }
    
    public Parcelable getParcelableData(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getParcelableData(paramObject);
    }
    
    public int getRemovedCount(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getRemovedCount(paramObject);
    }
    
    public int getScrollX(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getScrollX(paramObject);
    }
    
    public int getScrollY(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getScrollY(paramObject);
    }
    
    public Object getSource(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getSource(paramObject);
    }
    
    public List<CharSequence> getText(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getText(paramObject);
    }
    
    public int getToIndex(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getToIndex(paramObject);
    }
    
    public int getWindowId(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.getWindowId(paramObject);
    }
    
    public boolean isChecked(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.isChecked(paramObject);
    }
    
    public boolean isEnabled(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.isEnabled(paramObject);
    }
    
    public boolean isFullScreen(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.isFullScreen(paramObject);
    }
    
    public boolean isPassword(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.isPassword(paramObject);
    }
    
    public boolean isScrollable(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.isScrollable(paramObject);
    }
    
    public Object obtain()
    {
      return AccessibilityRecordCompatIcs.obtain();
    }
    
    public Object obtain(Object paramObject)
    {
      return AccessibilityRecordCompatIcs.obtain(paramObject);
    }
    
    public void recycle(Object paramObject)
    {
      AccessibilityRecordCompatIcs.recycle(paramObject);
    }
    
    public void setAddedCount(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setAddedCount(paramObject, paramInt);
    }
    
    public void setBeforeText(Object paramObject, CharSequence paramCharSequence)
    {
      AccessibilityRecordCompatIcs.setBeforeText(paramObject, paramCharSequence);
    }
    
    public void setChecked(Object paramObject, boolean paramBoolean)
    {
      AccessibilityRecordCompatIcs.setChecked(paramObject, paramBoolean);
    }
    
    public void setClassName(Object paramObject, CharSequence paramCharSequence)
    {
      AccessibilityRecordCompatIcs.setClassName(paramObject, paramCharSequence);
    }
    
    public void setContentDescription(Object paramObject, CharSequence paramCharSequence)
    {
      AccessibilityRecordCompatIcs.setContentDescription(paramObject, paramCharSequence);
    }
    
    public void setCurrentItemIndex(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setCurrentItemIndex(paramObject, paramInt);
    }
    
    public void setEnabled(Object paramObject, boolean paramBoolean)
    {
      AccessibilityRecordCompatIcs.setEnabled(paramObject, paramBoolean);
    }
    
    public void setFromIndex(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setFromIndex(paramObject, paramInt);
    }
    
    public void setFullScreen(Object paramObject, boolean paramBoolean)
    {
      AccessibilityRecordCompatIcs.setFullScreen(paramObject, paramBoolean);
    }
    
    public void setItemCount(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setItemCount(paramObject, paramInt);
    }
    
    public void setMaxScrollX(Object paramObject, int paramInt) {}
    
    public void setMaxScrollY(Object paramObject, int paramInt) {}
    
    public void setParcelableData(Object paramObject, Parcelable paramParcelable)
    {
      AccessibilityRecordCompatIcs.setParcelableData(paramObject, paramParcelable);
    }
    
    public void setPassword(Object paramObject, boolean paramBoolean)
    {
      AccessibilityRecordCompatIcs.setPassword(paramObject, paramBoolean);
    }
    
    public void setRemovedCount(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setRemovedCount(paramObject, paramInt);
    }
    
    public void setScrollX(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setScrollX(paramObject, paramInt);
    }
    
    public void setScrollY(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setScrollY(paramObject, paramInt);
    }
    
    public void setScrollable(Object paramObject, boolean paramBoolean)
    {
      AccessibilityRecordCompatIcs.setScrollable(paramObject, paramBoolean);
    }
    
    public void setSource(Object paramObject, View paramView)
    {
      AccessibilityRecordCompatIcs.setSource(paramObject, paramView);
    }
    
    public void setToIndex(Object paramObject, int paramInt)
    {
      AccessibilityRecordCompatIcs.setToIndex(paramObject, paramInt);
    }
  }
  
  static abstract interface AccessibilityRecordImpl
  {
    public abstract int getAddedCount(Object paramObject);
    
    public abstract CharSequence getBeforeText(Object paramObject);
    
    public abstract CharSequence getClassName(Object paramObject);
    
    public abstract CharSequence getContentDescription(Object paramObject);
    
    public abstract int getCurrentItemIndex(Object paramObject);
    
    public abstract int getFromIndex(Object paramObject);
    
    public abstract int getItemCount(Object paramObject);
    
    public abstract int getMaxScrollX(Object paramObject);
    
    public abstract int getMaxScrollY(Object paramObject);
    
    public abstract Parcelable getParcelableData(Object paramObject);
    
    public abstract int getRemovedCount(Object paramObject);
    
    public abstract int getScrollX(Object paramObject);
    
    public abstract int getScrollY(Object paramObject);
    
    public abstract Object getSource(Object paramObject);
    
    public abstract List<CharSequence> getText(Object paramObject);
    
    public abstract int getToIndex(Object paramObject);
    
    public abstract int getWindowId(Object paramObject);
    
    public abstract boolean isChecked(Object paramObject);
    
    public abstract boolean isEnabled(Object paramObject);
    
    public abstract boolean isFullScreen(Object paramObject);
    
    public abstract boolean isPassword(Object paramObject);
    
    public abstract boolean isScrollable(Object paramObject);
    
    public abstract Object obtain();
    
    public abstract Object obtain(Object paramObject);
    
    public abstract void recycle(Object paramObject);
    
    public abstract void setAddedCount(Object paramObject, int paramInt);
    
    public abstract void setBeforeText(Object paramObject, CharSequence paramCharSequence);
    
    public abstract void setChecked(Object paramObject, boolean paramBoolean);
    
    public abstract void setClassName(Object paramObject, CharSequence paramCharSequence);
    
    public abstract void setContentDescription(Object paramObject, CharSequence paramCharSequence);
    
    public abstract void setCurrentItemIndex(Object paramObject, int paramInt);
    
    public abstract void setEnabled(Object paramObject, boolean paramBoolean);
    
    public abstract void setFromIndex(Object paramObject, int paramInt);
    
    public abstract void setFullScreen(Object paramObject, boolean paramBoolean);
    
    public abstract void setItemCount(Object paramObject, int paramInt);
    
    public abstract void setMaxScrollX(Object paramObject, int paramInt);
    
    public abstract void setMaxScrollY(Object paramObject, int paramInt);
    
    public abstract void setParcelableData(Object paramObject, Parcelable paramParcelable);
    
    public abstract void setPassword(Object paramObject, boolean paramBoolean);
    
    public abstract void setRemovedCount(Object paramObject, int paramInt);
    
    public abstract void setScrollX(Object paramObject, int paramInt);
    
    public abstract void setScrollY(Object paramObject, int paramInt);
    
    public abstract void setScrollable(Object paramObject, boolean paramBoolean);
    
    public abstract void setSource(Object paramObject, View paramView);
    
    public abstract void setToIndex(Object paramObject, int paramInt);
  }
  
  static class AccessibilityRecordStubImpl
    implements AccessibilityRecordCompat.AccessibilityRecordImpl
  {
    AccessibilityRecordStubImpl() {}
    
    public int getAddedCount(Object paramObject)
    {
      return 0;
    }
    
    public CharSequence getBeforeText(Object paramObject)
    {
      return null;
    }
    
    public CharSequence getClassName(Object paramObject)
    {
      return null;
    }
    
    public CharSequence getContentDescription(Object paramObject)
    {
      return null;
    }
    
    public int getCurrentItemIndex(Object paramObject)
    {
      return 0;
    }
    
    public int getFromIndex(Object paramObject)
    {
      return 0;
    }
    
    public int getItemCount(Object paramObject)
    {
      return 0;
    }
    
    public int getMaxScrollX(Object paramObject)
    {
      return 0;
    }
    
    public int getMaxScrollY(Object paramObject)
    {
      return 0;
    }
    
    public Parcelable getParcelableData(Object paramObject)
    {
      return null;
    }
    
    public int getRemovedCount(Object paramObject)
    {
      return 0;
    }
    
    public int getScrollX(Object paramObject)
    {
      return 0;
    }
    
    public int getScrollY(Object paramObject)
    {
      return 0;
    }
    
    public Object getSource(Object paramObject)
    {
      return null;
    }
    
    public List<CharSequence> getText(Object paramObject)
    {
      return Collections.emptyList();
    }
    
    public int getToIndex(Object paramObject)
    {
      return 0;
    }
    
    public int getWindowId(Object paramObject)
    {
      return 0;
    }
    
    public boolean isChecked(Object paramObject)
    {
      return false;
    }
    
    public boolean isEnabled(Object paramObject)
    {
      return false;
    }
    
    public boolean isFullScreen(Object paramObject)
    {
      return false;
    }
    
    public boolean isPassword(Object paramObject)
    {
      return false;
    }
    
    public boolean isScrollable(Object paramObject)
    {
      return false;
    }
    
    public Object obtain()
    {
      return null;
    }
    
    public Object obtain(Object paramObject)
    {
      return null;
    }
    
    public void recycle(Object paramObject) {}
    
    public void setAddedCount(Object paramObject, int paramInt) {}
    
    public void setBeforeText(Object paramObject, CharSequence paramCharSequence) {}
    
    public void setChecked(Object paramObject, boolean paramBoolean) {}
    
    public void setClassName(Object paramObject, CharSequence paramCharSequence) {}
    
    public void setContentDescription(Object paramObject, CharSequence paramCharSequence) {}
    
    public void setCurrentItemIndex(Object paramObject, int paramInt) {}
    
    public void setEnabled(Object paramObject, boolean paramBoolean) {}
    
    public void setFromIndex(Object paramObject, int paramInt) {}
    
    public void setFullScreen(Object paramObject, boolean paramBoolean) {}
    
    public void setItemCount(Object paramObject, int paramInt) {}
    
    public void setMaxScrollX(Object paramObject, int paramInt) {}
    
    public void setMaxScrollY(Object paramObject, int paramInt) {}
    
    public void setParcelableData(Object paramObject, Parcelable paramParcelable) {}
    
    public void setPassword(Object paramObject, boolean paramBoolean) {}
    
    public void setRemovedCount(Object paramObject, int paramInt) {}
    
    public void setScrollX(Object paramObject, int paramInt) {}
    
    public void setScrollY(Object paramObject, int paramInt) {}
    
    public void setScrollable(Object paramObject, boolean paramBoolean) {}
    
    public void setSource(Object paramObject, View paramView) {}
    
    public void setToIndex(Object paramObject, int paramInt) {}
  }
}
