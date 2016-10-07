package com.actionbarsherlock.internal.nineoldandroids.animation;

import android.view.animation.Interpolator;

public abstract class Keyframe
  implements Cloneable
{
  float mFraction;
  boolean mHasValue = false;
  private Interpolator mInterpolator = null;
  Class mValueType;
  
  public Keyframe() {}
  
  public static Keyframe ofFloat(float paramFloat)
  {
    return new FloatKeyframe(paramFloat);
  }
  
  public static Keyframe ofFloat(float paramFloat1, float paramFloat2)
  {
    return new FloatKeyframe(paramFloat1, paramFloat2);
  }
  
  public static Keyframe ofInt(float paramFloat)
  {
    return new IntKeyframe(paramFloat);
  }
  
  public static Keyframe ofInt(float paramFloat, int paramInt)
  {
    return new IntKeyframe(paramFloat, paramInt);
  }
  
  public static Keyframe ofObject(float paramFloat)
  {
    return new ObjectKeyframe(paramFloat, null);
  }
  
  public static Keyframe ofObject(float paramFloat, Object paramObject)
  {
    return new ObjectKeyframe(paramFloat, paramObject);
  }
  
  public abstract Keyframe clone();
  
  public float getFraction()
  {
    return this.mFraction;
  }
  
  public Interpolator getInterpolator()
  {
    return this.mInterpolator;
  }
  
  public Class getType()
  {
    return this.mValueType;
  }
  
  public abstract Object getValue();
  
  public boolean hasValue()
  {
    return this.mHasValue;
  }
  
  public void setFraction(float paramFloat)
  {
    this.mFraction = paramFloat;
  }
  
  public void setInterpolator(Interpolator paramInterpolator)
  {
    this.mInterpolator = paramInterpolator;
  }
  
  public abstract void setValue(Object paramObject);
  
  static class FloatKeyframe
    extends Keyframe
  {
    float mValue;
    
    FloatKeyframe(float paramFloat)
    {
      this.mFraction = paramFloat;
      this.mValueType = Float.TYPE;
    }
    
    FloatKeyframe(float paramFloat1, float paramFloat2)
    {
      this.mFraction = paramFloat1;
      this.mValue = paramFloat2;
      this.mValueType = Float.TYPE;
      this.mHasValue = true;
    }
    
    public FloatKeyframe clone()
    {
      FloatKeyframe localFloatKeyframe = new FloatKeyframe(getFraction(), this.mValue);
      localFloatKeyframe.setInterpolator(getInterpolator());
      return localFloatKeyframe;
    }
    
    public float getFloatValue()
    {
      return this.mValue;
    }
    
    public Object getValue()
    {
      return Float.valueOf(this.mValue);
    }
    
    public void setValue(Object paramObject)
    {
      if ((paramObject != null) && (paramObject.getClass() == Float.class))
      {
        this.mValue = ((Float)paramObject).floatValue();
        this.mHasValue = true;
      }
    }
  }
  
  static class IntKeyframe
    extends Keyframe
  {
    int mValue;
    
    IntKeyframe(float paramFloat)
    {
      this.mFraction = paramFloat;
      this.mValueType = Integer.TYPE;
    }
    
    IntKeyframe(float paramFloat, int paramInt)
    {
      this.mFraction = paramFloat;
      this.mValue = paramInt;
      this.mValueType = Integer.TYPE;
      this.mHasValue = true;
    }
    
    public IntKeyframe clone()
    {
      IntKeyframe localIntKeyframe = new IntKeyframe(getFraction(), this.mValue);
      localIntKeyframe.setInterpolator(getInterpolator());
      return localIntKeyframe;
    }
    
    public int getIntValue()
    {
      return this.mValue;
    }
    
    public Object getValue()
    {
      return Integer.valueOf(this.mValue);
    }
    
    public void setValue(Object paramObject)
    {
      if ((paramObject != null) && (paramObject.getClass() == Integer.class))
      {
        this.mValue = ((Integer)paramObject).intValue();
        this.mHasValue = true;
      }
    }
  }
  
  static class ObjectKeyframe
    extends Keyframe
  {
    Object mValue;
    
    ObjectKeyframe(float paramFloat, Object paramObject)
    {
      this.mFraction = paramFloat;
      this.mValue = paramObject;
      boolean bool;
      if (paramObject != null)
      {
        bool = true;
        this.mHasValue = bool;
        if (!this.mHasValue) {
          break label50;
        }
      }
      label50:
      for (Object localObject = paramObject.getClass();; localObject = Object.class)
      {
        this.mValueType = ((Class)localObject);
        return;
        bool = false;
        break;
      }
    }
    
    public ObjectKeyframe clone()
    {
      ObjectKeyframe localObjectKeyframe = new ObjectKeyframe(getFraction(), this.mValue);
      localObjectKeyframe.setInterpolator(getInterpolator());
      return localObjectKeyframe;
    }
    
    public Object getValue()
    {
      return this.mValue;
    }
    
    public void setValue(Object paramObject)
    {
      this.mValue = paramObject;
      if (paramObject != null) {}
      for (boolean bool = true;; bool = false)
      {
        this.mHasValue = bool;
        return;
      }
    }
  }
}
