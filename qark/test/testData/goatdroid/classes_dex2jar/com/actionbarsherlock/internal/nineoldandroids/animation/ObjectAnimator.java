package com.actionbarsherlock.internal.nineoldandroids.animation;

import java.util.HashMap;

public final class ObjectAnimator
  extends ValueAnimator
{
  private static final boolean DBG;
  private String mPropertyName;
  private Object mTarget;
  
  public ObjectAnimator() {}
  
  private ObjectAnimator(Object paramObject, String paramString)
  {
    this.mTarget = paramObject;
    setPropertyName(paramString);
  }
  
  public static ObjectAnimator ofFloat(Object paramObject, String paramString, float... paramVarArgs)
  {
    ObjectAnimator localObjectAnimator = new ObjectAnimator(paramObject, paramString);
    localObjectAnimator.setFloatValues(paramVarArgs);
    return localObjectAnimator;
  }
  
  public static ObjectAnimator ofInt(Object paramObject, String paramString, int... paramVarArgs)
  {
    ObjectAnimator localObjectAnimator = new ObjectAnimator(paramObject, paramString);
    localObjectAnimator.setIntValues(paramVarArgs);
    return localObjectAnimator;
  }
  
  public static ObjectAnimator ofObject(Object paramObject, String paramString, TypeEvaluator paramTypeEvaluator, Object... paramVarArgs)
  {
    ObjectAnimator localObjectAnimator = new ObjectAnimator(paramObject, paramString);
    localObjectAnimator.setObjectValues(paramVarArgs);
    localObjectAnimator.setEvaluator(paramTypeEvaluator);
    return localObjectAnimator;
  }
  
  public static ObjectAnimator ofPropertyValuesHolder(Object paramObject, PropertyValuesHolder... paramVarArgs)
  {
    ObjectAnimator localObjectAnimator = new ObjectAnimator();
    localObjectAnimator.mTarget = paramObject;
    localObjectAnimator.setValues(paramVarArgs);
    return localObjectAnimator;
  }
  
  void animateValue(float paramFloat)
  {
    super.animateValue(paramFloat);
    int i = this.mValues.length;
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      this.mValues[j].setAnimatedValue(this.mTarget);
    }
  }
  
  public ObjectAnimator clone()
  {
    return (ObjectAnimator)super.clone();
  }
  
  public String getPropertyName()
  {
    return this.mPropertyName;
  }
  
  public Object getTarget()
  {
    return this.mTarget;
  }
  
  void initAnimation()
  {
    int i;
    if (!this.mInitialized) {
      i = this.mValues.length;
    }
    for (int j = 0;; j++)
    {
      if (j >= i)
      {
        super.initAnimation();
        return;
      }
      this.mValues[j].setupSetterAndGetter(this.mTarget);
    }
  }
  
  public ObjectAnimator setDuration(long paramLong)
  {
    super.setDuration(paramLong);
    return this;
  }
  
  public void setFloatValues(float... paramVarArgs)
  {
    if ((this.mValues == null) || (this.mValues.length == 0))
    {
      PropertyValuesHolder[] arrayOfPropertyValuesHolder = new PropertyValuesHolder[1];
      arrayOfPropertyValuesHolder[0] = PropertyValuesHolder.ofFloat(this.mPropertyName, paramVarArgs);
      setValues(arrayOfPropertyValuesHolder);
      return;
    }
    super.setFloatValues(paramVarArgs);
  }
  
  public void setIntValues(int... paramVarArgs)
  {
    if ((this.mValues == null) || (this.mValues.length == 0))
    {
      PropertyValuesHolder[] arrayOfPropertyValuesHolder = new PropertyValuesHolder[1];
      arrayOfPropertyValuesHolder[0] = PropertyValuesHolder.ofInt(this.mPropertyName, paramVarArgs);
      setValues(arrayOfPropertyValuesHolder);
      return;
    }
    super.setIntValues(paramVarArgs);
  }
  
  public void setObjectValues(Object... paramVarArgs)
  {
    if ((this.mValues == null) || (this.mValues.length == 0))
    {
      PropertyValuesHolder[] arrayOfPropertyValuesHolder = new PropertyValuesHolder[1];
      arrayOfPropertyValuesHolder[0] = PropertyValuesHolder.ofObject(this.mPropertyName, null, paramVarArgs);
      setValues(arrayOfPropertyValuesHolder);
      return;
    }
    super.setObjectValues(paramVarArgs);
  }
  
  public void setPropertyName(String paramString)
  {
    if (this.mValues != null)
    {
      PropertyValuesHolder localPropertyValuesHolder = this.mValues[0];
      String str = localPropertyValuesHolder.getPropertyName();
      localPropertyValuesHolder.setPropertyName(paramString);
      this.mValuesMap.remove(str);
      this.mValuesMap.put(paramString, localPropertyValuesHolder);
    }
    this.mPropertyName = paramString;
    this.mInitialized = false;
  }
  
  public void setTarget(Object paramObject)
  {
    if (this.mTarget != paramObject)
    {
      Object localObject = this.mTarget;
      this.mTarget = paramObject;
      if ((localObject == null) || (paramObject == null) || (localObject.getClass() != paramObject.getClass())) {}
    }
    else
    {
      return;
    }
    this.mInitialized = false;
  }
  
  public void setupEndValues()
  {
    initAnimation();
    int i = this.mValues.length;
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      this.mValues[j].setupEndValue(this.mTarget);
    }
  }
  
  public void setupStartValues()
  {
    initAnimation();
    int i = this.mValues.length;
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return;
      }
      this.mValues[j].setupStartValue(this.mTarget);
    }
  }
  
  public void start()
  {
    super.start();
  }
  
  public String toString()
  {
    String str = "ObjectAnimator@" + Integer.toHexString(hashCode()) + ", target " + this.mTarget;
    if (this.mValues != null) {}
    for (int i = 0;; i++)
    {
      if (i >= this.mValues.length) {
        return str;
      }
      str = str + "\n    " + this.mValues[i].toString();
    }
  }
}
