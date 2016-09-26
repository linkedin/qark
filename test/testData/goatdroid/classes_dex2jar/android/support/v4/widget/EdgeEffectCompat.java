package android.support.v4.widget;

import android.content.Context;
import android.graphics.Canvas;
import android.os.Build.VERSION;

public class EdgeEffectCompat
{
  private static final EdgeEffectImpl IMPL = new BaseEdgeEffectImpl();
  private Object mEdgeEffect;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 14)
    {
      IMPL = new EdgeEffectIcsImpl();
      return;
    }
  }
  
  public EdgeEffectCompat(Context paramContext)
  {
    this.mEdgeEffect = IMPL.newEdgeEffect(paramContext);
  }
  
  public boolean draw(Canvas paramCanvas)
  {
    return IMPL.draw(this.mEdgeEffect, paramCanvas);
  }
  
  public void finish()
  {
    IMPL.finish(this.mEdgeEffect);
  }
  
  public boolean isFinished()
  {
    return IMPL.isFinished(this.mEdgeEffect);
  }
  
  public boolean onAbsorb(int paramInt)
  {
    return IMPL.onAbsorb(this.mEdgeEffect, paramInt);
  }
  
  public boolean onPull(float paramFloat)
  {
    return IMPL.onPull(this.mEdgeEffect, paramFloat);
  }
  
  public boolean onRelease()
  {
    return IMPL.onRelease(this.mEdgeEffect);
  }
  
  public void setSize(int paramInt1, int paramInt2)
  {
    IMPL.setSize(this.mEdgeEffect, paramInt1, paramInt2);
  }
  
  static class BaseEdgeEffectImpl
    implements EdgeEffectCompat.EdgeEffectImpl
  {
    BaseEdgeEffectImpl() {}
    
    public boolean draw(Object paramObject, Canvas paramCanvas)
    {
      return false;
    }
    
    public void finish(Object paramObject) {}
    
    public boolean isFinished(Object paramObject)
    {
      return true;
    }
    
    public Object newEdgeEffect(Context paramContext)
    {
      return null;
    }
    
    public boolean onAbsorb(Object paramObject, int paramInt)
    {
      return false;
    }
    
    public boolean onPull(Object paramObject, float paramFloat)
    {
      return false;
    }
    
    public boolean onRelease(Object paramObject)
    {
      return false;
    }
    
    public void setSize(Object paramObject, int paramInt1, int paramInt2) {}
  }
  
  static class EdgeEffectIcsImpl
    implements EdgeEffectCompat.EdgeEffectImpl
  {
    EdgeEffectIcsImpl() {}
    
    public boolean draw(Object paramObject, Canvas paramCanvas)
    {
      return EdgeEffectCompatIcs.draw(paramObject, paramCanvas);
    }
    
    public void finish(Object paramObject)
    {
      EdgeEffectCompatIcs.finish(paramObject);
    }
    
    public boolean isFinished(Object paramObject)
    {
      return EdgeEffectCompatIcs.isFinished(paramObject);
    }
    
    public Object newEdgeEffect(Context paramContext)
    {
      return EdgeEffectCompatIcs.newEdgeEffect(paramContext);
    }
    
    public boolean onAbsorb(Object paramObject, int paramInt)
    {
      return EdgeEffectCompatIcs.onAbsorb(paramObject, paramInt);
    }
    
    public boolean onPull(Object paramObject, float paramFloat)
    {
      return EdgeEffectCompatIcs.onPull(paramObject, paramFloat);
    }
    
    public boolean onRelease(Object paramObject)
    {
      return EdgeEffectCompatIcs.onRelease(paramObject);
    }
    
    public void setSize(Object paramObject, int paramInt1, int paramInt2)
    {
      EdgeEffectCompatIcs.setSize(paramObject, paramInt1, paramInt2);
    }
  }
  
  static abstract interface EdgeEffectImpl
  {
    public abstract boolean draw(Object paramObject, Canvas paramCanvas);
    
    public abstract void finish(Object paramObject);
    
    public abstract boolean isFinished(Object paramObject);
    
    public abstract Object newEdgeEffect(Context paramContext);
    
    public abstract boolean onAbsorb(Object paramObject, int paramInt);
    
    public abstract boolean onPull(Object paramObject, float paramFloat);
    
    public abstract boolean onRelease(Object paramObject);
    
    public abstract void setSize(Object paramObject, int paramInt1, int paramInt2);
  }
}
