package android.support.v4.view;

import android.os.Build.VERSION;
import android.view.VelocityTracker;

public class VelocityTrackerCompat
{
  static final VelocityTrackerVersionImpl IMPL = new BaseVelocityTrackerVersionImpl();
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      IMPL = new HoneycombVelocityTrackerVersionImpl();
      return;
    }
  }
  
  public VelocityTrackerCompat() {}
  
  public static float getXVelocity(VelocityTracker paramVelocityTracker, int paramInt)
  {
    return IMPL.getXVelocity(paramVelocityTracker, paramInt);
  }
  
  public static float getYVelocity(VelocityTracker paramVelocityTracker, int paramInt)
  {
    return IMPL.getYVelocity(paramVelocityTracker, paramInt);
  }
  
  static class BaseVelocityTrackerVersionImpl
    implements VelocityTrackerCompat.VelocityTrackerVersionImpl
  {
    BaseVelocityTrackerVersionImpl() {}
    
    public float getXVelocity(VelocityTracker paramVelocityTracker, int paramInt)
    {
      return paramVelocityTracker.getXVelocity();
    }
    
    public float getYVelocity(VelocityTracker paramVelocityTracker, int paramInt)
    {
      return paramVelocityTracker.getYVelocity();
    }
  }
  
  static class HoneycombVelocityTrackerVersionImpl
    implements VelocityTrackerCompat.VelocityTrackerVersionImpl
  {
    HoneycombVelocityTrackerVersionImpl() {}
    
    public float getXVelocity(VelocityTracker paramVelocityTracker, int paramInt)
    {
      return VelocityTrackerCompatHoneycomb.getXVelocity(paramVelocityTracker, paramInt);
    }
    
    public float getYVelocity(VelocityTracker paramVelocityTracker, int paramInt)
    {
      return VelocityTrackerCompatHoneycomb.getYVelocity(paramVelocityTracker, paramInt);
    }
  }
  
  static abstract interface VelocityTrackerVersionImpl
  {
    public abstract float getXVelocity(VelocityTracker paramVelocityTracker, int paramInt);
    
    public abstract float getYVelocity(VelocityTracker paramVelocityTracker, int paramInt);
  }
}
