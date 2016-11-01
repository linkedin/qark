package android.support.v4.view;

import android.os.Build.VERSION;
import android.support.v4.view.accessibility.AccessibilityNodeInfoCompat;
import android.view.View;
import android.view.ViewGroup;
import android.view.accessibility.AccessibilityEvent;

public class AccessibilityDelegateCompat
{
  private static final Object DEFAULT_DELEGATE;
  private static final AccessibilityDelegateImpl IMPL;
  final Object mBridge = IMPL.newAccessiblityDelegateBridge(this);
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14) {}
    for (IMPL = new AccessibilityDelegateIcsImpl();; IMPL = new AccessibilityDelegateStubImpl())
    {
      DEFAULT_DELEGATE = IMPL.newAccessiblityDelegateDefaultImpl();
      return;
    }
  }
  
  public AccessibilityDelegateCompat() {}
  
  public boolean dispatchPopulateAccessibilityEvent(View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    return IMPL.dispatchPopulateAccessibilityEvent(DEFAULT_DELEGATE, paramView, paramAccessibilityEvent);
  }
  
  Object getBridge()
  {
    return this.mBridge;
  }
  
  public void onInitializeAccessibilityEvent(View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    IMPL.onInitializeAccessibilityEvent(DEFAULT_DELEGATE, paramView, paramAccessibilityEvent);
  }
  
  public void onInitializeAccessibilityNodeInfo(View paramView, AccessibilityNodeInfoCompat paramAccessibilityNodeInfoCompat)
  {
    IMPL.onInitializeAccessibilityNodeInfo(DEFAULT_DELEGATE, paramView, paramAccessibilityNodeInfoCompat);
  }
  
  public void onPopulateAccessibilityEvent(View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    IMPL.onPopulateAccessibilityEvent(DEFAULT_DELEGATE, paramView, paramAccessibilityEvent);
  }
  
  public boolean onRequestSendAccessibilityEvent(ViewGroup paramViewGroup, View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    return IMPL.onRequestSendAccessibilityEvent(DEFAULT_DELEGATE, paramViewGroup, paramView, paramAccessibilityEvent);
  }
  
  public void sendAccessibilityEvent(View paramView, int paramInt)
  {
    IMPL.sendAccessibilityEvent(DEFAULT_DELEGATE, paramView, paramInt);
  }
  
  public void sendAccessibilityEventUnchecked(View paramView, AccessibilityEvent paramAccessibilityEvent)
  {
    IMPL.sendAccessibilityEventUnchecked(DEFAULT_DELEGATE, paramView, paramAccessibilityEvent);
  }
  
  static class AccessibilityDelegateIcsImpl
    extends AccessibilityDelegateCompat.AccessibilityDelegateStubImpl
  {
    AccessibilityDelegateIcsImpl() {}
    
    public boolean dispatchPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      return AccessibilityDelegateCompatIcs.dispatchPopulateAccessibilityEvent(paramObject, paramView, paramAccessibilityEvent);
    }
    
    public Object newAccessiblityDelegateBridge(final AccessibilityDelegateCompat paramAccessibilityDelegateCompat)
    {
      AccessibilityDelegateCompatIcs.newAccessibilityDelegateBridge(new AccessibilityDelegateCompatIcs.AccessibilityDelegateBridge()
      {
        public boolean dispatchPopulateAccessibilityEvent(View paramAnonymousView, AccessibilityEvent paramAnonymousAccessibilityEvent)
        {
          return paramAccessibilityDelegateCompat.dispatchPopulateAccessibilityEvent(paramAnonymousView, paramAnonymousAccessibilityEvent);
        }
        
        public void onInitializeAccessibilityEvent(View paramAnonymousView, AccessibilityEvent paramAnonymousAccessibilityEvent)
        {
          paramAccessibilityDelegateCompat.onInitializeAccessibilityEvent(paramAnonymousView, paramAnonymousAccessibilityEvent);
        }
        
        public void onInitializeAccessibilityNodeInfo(View paramAnonymousView, Object paramAnonymousObject)
        {
          paramAccessibilityDelegateCompat.onInitializeAccessibilityNodeInfo(paramAnonymousView, new AccessibilityNodeInfoCompat(paramAnonymousObject));
        }
        
        public void onPopulateAccessibilityEvent(View paramAnonymousView, AccessibilityEvent paramAnonymousAccessibilityEvent)
        {
          paramAccessibilityDelegateCompat.onPopulateAccessibilityEvent(paramAnonymousView, paramAnonymousAccessibilityEvent);
        }
        
        public boolean onRequestSendAccessibilityEvent(ViewGroup paramAnonymousViewGroup, View paramAnonymousView, AccessibilityEvent paramAnonymousAccessibilityEvent)
        {
          return paramAccessibilityDelegateCompat.onRequestSendAccessibilityEvent(paramAnonymousViewGroup, paramAnonymousView, paramAnonymousAccessibilityEvent);
        }
        
        public void sendAccessibilityEvent(View paramAnonymousView, int paramAnonymousInt)
        {
          paramAccessibilityDelegateCompat.sendAccessibilityEvent(paramAnonymousView, paramAnonymousInt);
        }
        
        public void sendAccessibilityEventUnchecked(View paramAnonymousView, AccessibilityEvent paramAnonymousAccessibilityEvent)
        {
          paramAccessibilityDelegateCompat.sendAccessibilityEventUnchecked(paramAnonymousView, paramAnonymousAccessibilityEvent);
        }
      });
    }
    
    public Object newAccessiblityDelegateDefaultImpl()
    {
      return AccessibilityDelegateCompatIcs.newAccessibilityDelegateDefaultImpl();
    }
    
    public void onInitializeAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      AccessibilityDelegateCompatIcs.onInitializeAccessibilityEvent(paramObject, paramView, paramAccessibilityEvent);
    }
    
    public void onInitializeAccessibilityNodeInfo(Object paramObject, View paramView, AccessibilityNodeInfoCompat paramAccessibilityNodeInfoCompat)
    {
      AccessibilityDelegateCompatIcs.onInitializeAccessibilityNodeInfo(paramObject, paramView, paramAccessibilityNodeInfoCompat.getImpl());
    }
    
    public void onPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      AccessibilityDelegateCompatIcs.onPopulateAccessibilityEvent(paramObject, paramView, paramAccessibilityEvent);
    }
    
    public boolean onRequestSendAccessibilityEvent(Object paramObject, ViewGroup paramViewGroup, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      return AccessibilityDelegateCompatIcs.onRequestSendAccessibilityEvent(paramObject, paramViewGroup, paramView, paramAccessibilityEvent);
    }
    
    public void sendAccessibilityEvent(Object paramObject, View paramView, int paramInt)
    {
      AccessibilityDelegateCompatIcs.sendAccessibilityEvent(paramObject, paramView, paramInt);
    }
    
    public void sendAccessibilityEventUnchecked(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      AccessibilityDelegateCompatIcs.sendAccessibilityEventUnchecked(paramObject, paramView, paramAccessibilityEvent);
    }
  }
  
  static abstract interface AccessibilityDelegateImpl
  {
    public abstract boolean dispatchPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent);
    
    public abstract Object newAccessiblityDelegateBridge(AccessibilityDelegateCompat paramAccessibilityDelegateCompat);
    
    public abstract Object newAccessiblityDelegateDefaultImpl();
    
    public abstract void onInitializeAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent);
    
    public abstract void onInitializeAccessibilityNodeInfo(Object paramObject, View paramView, AccessibilityNodeInfoCompat paramAccessibilityNodeInfoCompat);
    
    public abstract void onPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent);
    
    public abstract boolean onRequestSendAccessibilityEvent(Object paramObject, ViewGroup paramViewGroup, View paramView, AccessibilityEvent paramAccessibilityEvent);
    
    public abstract void sendAccessibilityEvent(Object paramObject, View paramView, int paramInt);
    
    public abstract void sendAccessibilityEventUnchecked(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent);
  }
  
  static class AccessibilityDelegateStubImpl
    implements AccessibilityDelegateCompat.AccessibilityDelegateImpl
  {
    AccessibilityDelegateStubImpl() {}
    
    public boolean dispatchPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      return false;
    }
    
    public Object newAccessiblityDelegateBridge(AccessibilityDelegateCompat paramAccessibilityDelegateCompat)
    {
      return null;
    }
    
    public Object newAccessiblityDelegateDefaultImpl()
    {
      return null;
    }
    
    public void onInitializeAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent) {}
    
    public void onInitializeAccessibilityNodeInfo(Object paramObject, View paramView, AccessibilityNodeInfoCompat paramAccessibilityNodeInfoCompat) {}
    
    public void onPopulateAccessibilityEvent(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent) {}
    
    public boolean onRequestSendAccessibilityEvent(Object paramObject, ViewGroup paramViewGroup, View paramView, AccessibilityEvent paramAccessibilityEvent)
    {
      return true;
    }
    
    public void sendAccessibilityEvent(Object paramObject, View paramView, int paramInt) {}
    
    public void sendAccessibilityEventUnchecked(Object paramObject, View paramView, AccessibilityEvent paramAccessibilityEvent) {}
  }
}
