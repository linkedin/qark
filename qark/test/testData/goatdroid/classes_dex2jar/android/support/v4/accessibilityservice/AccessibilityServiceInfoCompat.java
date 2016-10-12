package android.support.v4.accessibilityservice;

import android.accessibilityservice.AccessibilityServiceInfo;
import android.content.pm.ResolveInfo;
import android.os.Build.VERSION;

public class AccessibilityServiceInfoCompat
{
  public static final int FEEDBACK_ALL_MASK = -1;
  private static final AccessibilityServiceInfoVersionImpl IMPL = new AccessibilityServiceInfoStubImpl();
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14)
    {
      IMPL = new AccessibilityServiceInfoIcsImpl();
      return;
    }
  }
  
  private AccessibilityServiceInfoCompat() {}
  
  public static String feedbackTypeToString(int paramInt)
  {
    StringBuilder localStringBuilder = new StringBuilder();
    localStringBuilder.append("[");
    while (paramInt > 0)
    {
      int i = 1 << Integer.numberOfTrailingZeros(paramInt);
      paramInt &= (i ^ 0xFFFFFFFF);
      if (localStringBuilder.length() > 1) {
        localStringBuilder.append(", ");
      }
      switch (i)
      {
      default: 
        break;
      case 1: 
        localStringBuilder.append("FEEDBACK_SPOKEN");
        break;
      case 4: 
        localStringBuilder.append("FEEDBACK_AUDIBLE");
        break;
      case 2: 
        localStringBuilder.append("FEEDBACK_HAPTIC");
        break;
      case 16: 
        localStringBuilder.append("FEEDBACK_GENERIC");
        break;
      case 8: 
        localStringBuilder.append("FEEDBACK_VISUAL");
      }
    }
    localStringBuilder.append("]");
    return localStringBuilder.toString();
  }
  
  public static String flagToString(int paramInt)
  {
    switch (paramInt)
    {
    default: 
      return null;
    }
    return "DEFAULT";
  }
  
  public static boolean getCanRetrieveWindowContent(AccessibilityServiceInfo paramAccessibilityServiceInfo)
  {
    return IMPL.getCanRetrieveWindowContent(paramAccessibilityServiceInfo);
  }
  
  public static String getDescription(AccessibilityServiceInfo paramAccessibilityServiceInfo)
  {
    return IMPL.getDescription(paramAccessibilityServiceInfo);
  }
  
  public static String getId(AccessibilityServiceInfo paramAccessibilityServiceInfo)
  {
    return IMPL.getId(paramAccessibilityServiceInfo);
  }
  
  public static ResolveInfo getResolveInfo(AccessibilityServiceInfo paramAccessibilityServiceInfo)
  {
    return IMPL.getResolveInfo(paramAccessibilityServiceInfo);
  }
  
  public static String getSettingsActivityName(AccessibilityServiceInfo paramAccessibilityServiceInfo)
  {
    return IMPL.getSettingsActivityName(paramAccessibilityServiceInfo);
  }
  
  static class AccessibilityServiceInfoIcsImpl
    extends AccessibilityServiceInfoCompat.AccessibilityServiceInfoStubImpl
  {
    AccessibilityServiceInfoIcsImpl() {}
    
    public boolean getCanRetrieveWindowContent(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return AccessibilityServiceInfoCompatIcs.getCanRetrieveWindowContent(paramAccessibilityServiceInfo);
    }
    
    public String getDescription(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return AccessibilityServiceInfoCompatIcs.getDescription(paramAccessibilityServiceInfo);
    }
    
    public String getId(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return AccessibilityServiceInfoCompatIcs.getId(paramAccessibilityServiceInfo);
    }
    
    public ResolveInfo getResolveInfo(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return AccessibilityServiceInfoCompatIcs.getResolveInfo(paramAccessibilityServiceInfo);
    }
    
    public String getSettingsActivityName(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return AccessibilityServiceInfoCompatIcs.getSettingsActivityName(paramAccessibilityServiceInfo);
    }
  }
  
  static class AccessibilityServiceInfoStubImpl
    implements AccessibilityServiceInfoCompat.AccessibilityServiceInfoVersionImpl
  {
    AccessibilityServiceInfoStubImpl() {}
    
    public boolean getCanRetrieveWindowContent(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return false;
    }
    
    public String getDescription(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return null;
    }
    
    public String getId(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return null;
    }
    
    public ResolveInfo getResolveInfo(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return null;
    }
    
    public String getSettingsActivityName(AccessibilityServiceInfo paramAccessibilityServiceInfo)
    {
      return null;
    }
  }
  
  static abstract interface AccessibilityServiceInfoVersionImpl
  {
    public abstract boolean getCanRetrieveWindowContent(AccessibilityServiceInfo paramAccessibilityServiceInfo);
    
    public abstract String getDescription(AccessibilityServiceInfo paramAccessibilityServiceInfo);
    
    public abstract String getId(AccessibilityServiceInfo paramAccessibilityServiceInfo);
    
    public abstract ResolveInfo getResolveInfo(AccessibilityServiceInfo paramAccessibilityServiceInfo);
    
    public abstract String getSettingsActivityName(AccessibilityServiceInfo paramAccessibilityServiceInfo);
  }
}
