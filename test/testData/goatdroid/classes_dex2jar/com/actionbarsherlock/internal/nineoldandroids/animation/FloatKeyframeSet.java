package com.actionbarsherlock.internal.nineoldandroids.animation;

import android.view.animation.Interpolator;
import java.util.ArrayList;

class FloatKeyframeSet
  extends KeyframeSet
{
  private float deltaValue;
  private boolean firstTime = true;
  private float firstValue;
  private float lastValue;
  
  public FloatKeyframeSet(Keyframe.FloatKeyframe... paramVarArgs)
  {
    super(paramVarArgs);
  }
  
  public FloatKeyframeSet clone()
  {
    ArrayList localArrayList = this.mKeyframes;
    int i = this.mKeyframes.size();
    Keyframe.FloatKeyframe[] arrayOfFloatKeyframe = new Keyframe.FloatKeyframe[i];
    for (int j = 0;; j++)
    {
      if (j >= i) {
        return new FloatKeyframeSet(arrayOfFloatKeyframe);
      }
      arrayOfFloatKeyframe[j] = ((Keyframe.FloatKeyframe)((Keyframe)localArrayList.get(j)).clone());
    }
  }
  
  public float getFloatValue(float paramFloat)
  {
    if (this.mNumKeyframes == 2)
    {
      if (this.firstTime)
      {
        this.firstTime = false;
        this.firstValue = ((Keyframe.FloatKeyframe)this.mKeyframes.get(0)).getFloatValue();
        this.lastValue = ((Keyframe.FloatKeyframe)this.mKeyframes.get(1)).getFloatValue();
        this.deltaValue = (this.lastValue - this.firstValue);
      }
      if (this.mInterpolator != null) {
        paramFloat = this.mInterpolator.getInterpolation(paramFloat);
      }
      if (this.mEvaluator == null) {
        return this.firstValue + paramFloat * this.deltaValue;
      }
      return ((Number)this.mEvaluator.evaluate(paramFloat, Float.valueOf(this.firstValue), Float.valueOf(this.lastValue))).floatValue();
    }
    if (paramFloat <= 0.0F)
    {
      Keyframe.FloatKeyframe localFloatKeyframe4 = (Keyframe.FloatKeyframe)this.mKeyframes.get(0);
      Keyframe.FloatKeyframe localFloatKeyframe5 = (Keyframe.FloatKeyframe)this.mKeyframes.get(1);
      float f9 = localFloatKeyframe4.getFloatValue();
      float f10 = localFloatKeyframe5.getFloatValue();
      float f11 = localFloatKeyframe4.getFraction();
      float f12 = localFloatKeyframe5.getFraction();
      Interpolator localInterpolator3 = localFloatKeyframe5.getInterpolator();
      if (localInterpolator3 != null) {
        paramFloat = localInterpolator3.getInterpolation(paramFloat);
      }
      float f13 = (paramFloat - f11) / (f12 - f11);
      if (this.mEvaluator == null) {
        return f9 + f13 * (f10 - f9);
      }
      return ((Number)this.mEvaluator.evaluate(f13, Float.valueOf(f9), Float.valueOf(f10))).floatValue();
    }
    if (paramFloat >= 1.0F)
    {
      Keyframe.FloatKeyframe localFloatKeyframe2 = (Keyframe.FloatKeyframe)this.mKeyframes.get(-2 + this.mNumKeyframes);
      Keyframe.FloatKeyframe localFloatKeyframe3 = (Keyframe.FloatKeyframe)this.mKeyframes.get(-1 + this.mNumKeyframes);
      float f4 = localFloatKeyframe2.getFloatValue();
      float f5 = localFloatKeyframe3.getFloatValue();
      float f6 = localFloatKeyframe2.getFraction();
      float f7 = localFloatKeyframe3.getFraction();
      Interpolator localInterpolator2 = localFloatKeyframe3.getInterpolator();
      if (localInterpolator2 != null) {
        paramFloat = localInterpolator2.getInterpolation(paramFloat);
      }
      float f8 = (paramFloat - f6) / (f7 - f6);
      if (this.mEvaluator == null) {
        return f4 + f8 * (f5 - f4);
      }
      return ((Number)this.mEvaluator.evaluate(f8, Float.valueOf(f4), Float.valueOf(f5))).floatValue();
    }
    Object localObject = (Keyframe.FloatKeyframe)this.mKeyframes.get(0);
    for (int i = 1;; i++)
    {
      if (i >= this.mNumKeyframes) {
        return ((Number)((Keyframe)this.mKeyframes.get(-1 + this.mNumKeyframes)).getValue()).floatValue();
      }
      Keyframe.FloatKeyframe localFloatKeyframe1 = (Keyframe.FloatKeyframe)this.mKeyframes.get(i);
      if (paramFloat < localFloatKeyframe1.getFraction())
      {
        Interpolator localInterpolator1 = localFloatKeyframe1.getInterpolator();
        if (localInterpolator1 != null) {
          paramFloat = localInterpolator1.getInterpolation(paramFloat);
        }
        float f1 = (paramFloat - ((Keyframe.FloatKeyframe)localObject).getFraction()) / (localFloatKeyframe1.getFraction() - ((Keyframe.FloatKeyframe)localObject).getFraction());
        float f2 = ((Keyframe.FloatKeyframe)localObject).getFloatValue();
        float f3 = localFloatKeyframe1.getFloatValue();
        if (this.mEvaluator == null) {
          return f2 + f1 * (f3 - f2);
        }
        return ((Number)this.mEvaluator.evaluate(f1, Float.valueOf(f2), Float.valueOf(f3))).floatValue();
      }
      localObject = localFloatKeyframe1;
    }
  }
  
  public Object getValue(float paramFloat)
  {
    return Float.valueOf(getFloatValue(paramFloat));
  }
}
