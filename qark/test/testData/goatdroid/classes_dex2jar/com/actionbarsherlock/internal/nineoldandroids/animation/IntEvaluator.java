package com.actionbarsherlock.internal.nineoldandroids.animation;

public class IntEvaluator
  implements TypeEvaluator<Integer>
{
  public IntEvaluator() {}
  
  public Integer evaluate(float paramFloat, Integer paramInteger1, Integer paramInteger2)
  {
    int i = paramInteger1.intValue();
    return Integer.valueOf((int)(i + paramFloat * (paramInteger2.intValue() - i)));
  }
}
