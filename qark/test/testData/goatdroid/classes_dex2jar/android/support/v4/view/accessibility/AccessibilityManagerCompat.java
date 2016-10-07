package android.support.v4.view.accessibility;

import android.accessibilityservice.AccessibilityServiceInfo;
import android.os.Build.VERSION;
import android.view.accessibility.AccessibilityManager;
import java.util.Collections;
import java.util.List;

public class AccessibilityManagerCompat
{
  private static final AccessibilityManagerVersionImpl IMPL = new AccessibilityManagerStubImpl();
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14)
    {
      IMPL = new AccessibilityManagerIcsImpl();
      return;
    }
  }
  
  public AccessibilityManagerCompat() {}
  
  public static boolean addAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
  {
    return IMPL.addAccessibilityStateChangeListener(paramAccessibilityManager, paramAccessibilityStateChangeListenerCompat);
  }
  
  public static List<AccessibilityServiceInfo> getEnabledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager, int paramInt)
  {
    return IMPL.getEnabledAccessibilityServiceList(paramAccessibilityManager, paramInt);
  }
  
  public static List<AccessibilityServiceInfo> getInstalledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager)
  {
    return IMPL.getInstalledAccessibilityServiceList(paramAccessibilityManager);
  }
  
  public static boolean removeAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
  {
    return IMPL.removeAccessibilityStateChangeListener(paramAccessibilityManager, paramAccessibilityStateChangeListenerCompat);
  }
  
  static class AccessibilityManagerIcsImpl
    extends AccessibilityManagerCompat.AccessibilityManagerStubImpl
  {
    AccessibilityManagerIcsImpl() {}
    
    public boolean addAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      return AccessibilityManagerCompatIcs.addAccessibilityStateChangeListener(paramAccessibilityManager, paramAccessibilityStateChangeListenerCompat.mListener);
    }
    
    public List<AccessibilityServiceInfo> getEnabledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager, int paramInt)
    {
      return AccessibilityManagerCompatIcs.getEnabledAccessibilityServiceList(paramAccessibilityManager, paramInt);
    }
    
    public List<AccessibilityServiceInfo> getInstalledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager)
    {
      return AccessibilityManagerCompatIcs.getInstalledAccessibilityServiceList(paramAccessibilityManager);
    }
    
    public boolean isTouchExplorationEnabled(AccessibilityManager paramAccessibilityManager)
    {
      return AccessibilityManagerCompatIcs.isTouchExplorationEnabled(paramAccessibilityManager);
    }
    
    public Object newAccessiblityStateChangeListener(final AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      AccessibilityManagerCompatIcs.newAccessibilityStateChangeListener(new AccessibilityManagerCompatIcs.AccessibilityStateChangeListenerBridge()
      {
        public void onAccessibilityStateChanged(boolean paramAnonymousBoolean)
        {
          paramAccessibilityStateChangeListenerCompat.onAccessibilityStateChanged(paramAnonymousBoolean);
        }
      });
    }
    
    public boolean removeAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      return AccessibilityManagerCompatIcs.removeAccessibilityStateChangeListener(paramAccessibilityManager, paramAccessibilityStateChangeListenerCompat.mListener);
    }
  }
  
  static class AccessibilityManagerStubImpl
    implements AccessibilityManagerCompat.AccessibilityManagerVersionImpl
  {
    AccessibilityManagerStubImpl() {}
    
    public boolean addAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      return false;
    }
    
    public List<AccessibilityServiceInfo> getEnabledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager, int paramInt)
    {
      return Collections.emptyList();
    }
    
    public List<AccessibilityServiceInfo> getInstalledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager)
    {
      return Collections.emptyList();
    }
    
    public boolean isTouchExplorationEnabled(AccessibilityManager paramAccessibilityManager)
    {
      return false;
    }
    
    public Object newAccessiblityStateChangeListener(AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      return null;
    }
    
    public boolean removeAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat)
    {
      return false;
    }
  }
  
  static abstract interface AccessibilityManagerVersionImpl
  {
    public abstract boolean addAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat);
    
    public abstract List<AccessibilityServiceInfo> getEnabledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager, int paramInt);
    
    public abstract List<AccessibilityServiceInfo> getInstalledAccessibilityServiceList(AccessibilityManager paramAccessibilityManager);
    
    public abstract boolean isTouchExplorationEnabled(AccessibilityManager paramAccessibilityManager);
    
    public abstract Object newAccessiblityStateChangeListener(AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat);
    
    public abstract boolean removeAccessibilityStateChangeListener(AccessibilityManager paramAccessibilityManager, AccessibilityManagerCompat.AccessibilityStateChangeListenerCompat paramAccessibilityStateChangeListenerCompat);
  }
  
  public static abstract class AccessibilityStateChangeListenerCompat
  {
    final Object mListener = AccessibilityManagerCompat.IMPL.newAccessiblityStateChangeListener(this);
    
    public AccessibilityStateChangeListenerCompat() {}
    
    public abstract void onAccessibilityStateChanged(boolean paramBoolean);
  }
}
