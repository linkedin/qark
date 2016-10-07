package com.actionbarsherlock.internal.nineoldandroids.view;

import android.content.Context;
import android.util.AttributeSet;
import android.view.ViewGroup;
import com.actionbarsherlock.internal.nineoldandroids.view.animation.AnimatorProxy;

public abstract class NineViewGroup
  extends ViewGroup
{
  private final AnimatorProxy mProxy;
  
  public NineViewGroup(Context paramContext)
  {
    super(paramContext);
    if (AnimatorProxy.NEEDS_PROXY) {}
    for (AnimatorProxy localAnimatorProxy = AnimatorProxy.wrap(this);; localAnimatorProxy = null)
    {
      this.mProxy = localAnimatorProxy;
      return;
    }
  }
  
  public NineViewGroup(Context paramContext, AttributeSet paramAttributeSet)
  {
    super(paramContext, paramAttributeSet);
    if (AnimatorProxy.NEEDS_PROXY) {}
    for (AnimatorProxy localAnimatorProxy = AnimatorProxy.wrap(this);; localAnimatorProxy = null)
    {
      this.mProxy = localAnimatorProxy;
      return;
    }
  }
  
  public NineViewGroup(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
    if (AnimatorProxy.NEEDS_PROXY) {}
    for (AnimatorProxy localAnimatorProxy = AnimatorProxy.wrap(this);; localAnimatorProxy = null)
    {
      this.mProxy = localAnimatorProxy;
      return;
    }
  }
  
  public float getAlpha()
  {
    if (AnimatorProxy.NEEDS_PROXY) {
      return this.mProxy.getAlpha();
    }
    return super.getAlpha();
  }
  
  public float getTranslationX()
  {
    if (AnimatorProxy.NEEDS_PROXY) {
      return this.mProxy.getTranslationX();
    }
    return super.getTranslationX();
  }
  
  public float getTranslationY()
  {
    if (AnimatorProxy.NEEDS_PROXY) {
      return this.mProxy.getTranslationY();
    }
    return super.getTranslationY();
  }
  
  public void setAlpha(float paramFloat)
  {
    if (AnimatorProxy.NEEDS_PROXY)
    {
      this.mProxy.setAlpha(paramFloat);
      return;
    }
    super.setAlpha(paramFloat);
  }
  
  public void setTranslationX(float paramFloat)
  {
    if (AnimatorProxy.NEEDS_PROXY)
    {
      this.mProxy.setTranslationX(paramFloat);
      return;
    }
    super.setTranslationX(paramFloat);
  }
  
  public void setTranslationY(float paramFloat)
  {
    if (AnimatorProxy.NEEDS_PROXY)
    {
      this.mProxy.setTranslationY(paramFloat);
      return;
    }
    super.setTranslationY(paramFloat);
  }
  
  public void setVisibility(int paramInt)
  {
    if (this.mProxy != null)
    {
      if (paramInt != 8) {
        break label23;
      }
      clearAnimation();
    }
    for (;;)
    {
      super.setVisibility(paramInt);
      return;
      label23:
      if (paramInt == 0) {
        setAnimation(this.mProxy);
      }
    }
  }
}
