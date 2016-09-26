package com.actionbarsherlock.internal.nineoldandroids.view.animation;

import android.graphics.Matrix;
import android.graphics.RectF;
import android.os.Build.VERSION;
import android.util.FloatMath;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.Transformation;
import java.lang.ref.WeakReference;
import java.util.WeakHashMap;

public final class AnimatorProxy
  extends Animation
{
  public static final boolean NEEDS_PROXY;
  private static final WeakHashMap<View, AnimatorProxy> PROXIES;
  private final RectF mAfter = new RectF();
  private float mAlpha = 1.0F;
  private final RectF mBefore = new RectF();
  private float mScaleX = 1.0F;
  private float mScaleY = 1.0F;
  private final Matrix mTempMatrix = new Matrix();
  private float mTranslationX;
  private float mTranslationY;
  private final WeakReference<View> mView;
  
  static
  {
    if (Build.VERSION.SDK_INT < 11) {}
    for (boolean bool = true;; bool = false)
    {
      NEEDS_PROXY = bool;
      PROXIES = new WeakHashMap();
      return;
    }
  }
  
  private AnimatorProxy(View paramView)
  {
    setDuration(0L);
    setFillAfter(true);
    paramView.setAnimation(this);
    this.mView = new WeakReference(paramView);
  }
  
  private void computeRect(RectF paramRectF, View paramView)
  {
    paramRectF.set(0.0F, 0.0F, paramView.getWidth(), paramView.getHeight());
    Matrix localMatrix = this.mTempMatrix;
    localMatrix.reset();
    transformMatrix(localMatrix, paramView);
    this.mTempMatrix.mapRect(paramRectF);
    paramRectF.offset(paramView.getLeft(), paramView.getTop());
    if (paramRectF.right < paramRectF.left)
    {
      float f2 = paramRectF.right;
      paramRectF.right = paramRectF.left;
      paramRectF.left = f2;
    }
    if (paramRectF.bottom < paramRectF.top)
    {
      float f1 = paramRectF.top;
      paramRectF.top = paramRectF.bottom;
      paramRectF.bottom = f1;
    }
  }
  
  private void invalidateAfterUpdate()
  {
    View localView1 = (View)this.mView.get();
    if (localView1 == null) {}
    View localView2;
    do
    {
      return;
      localView2 = (View)localView1.getParent();
    } while (localView2 == null);
    localView1.setAnimation(this);
    RectF localRectF = this.mAfter;
    computeRect(localRectF, localView1);
    localRectF.union(this.mBefore);
    localView2.invalidate((int)FloatMath.floor(localRectF.left), (int)FloatMath.floor(localRectF.top), (int)FloatMath.ceil(localRectF.right), (int)FloatMath.ceil(localRectF.bottom));
  }
  
  private void prepareForUpdate()
  {
    View localView = (View)this.mView.get();
    if (localView != null) {
      computeRect(this.mBefore, localView);
    }
  }
  
  private void transformMatrix(Matrix paramMatrix, View paramView)
  {
    float f1 = paramView.getWidth();
    float f2 = paramView.getHeight();
    float f3 = this.mScaleX;
    float f4 = this.mScaleY;
    if ((f3 != 1.0F) || (f4 != 1.0F))
    {
      float f5 = (f3 * f1 - f1) / 2.0F;
      float f6 = (f4 * f2 - f2) / 2.0F;
      paramMatrix.postScale(f3, f4);
      paramMatrix.postTranslate(-f5, -f6);
    }
    paramMatrix.postTranslate(this.mTranslationX, this.mTranslationY);
  }
  
  public static AnimatorProxy wrap(View paramView)
  {
    AnimatorProxy localAnimatorProxy = (AnimatorProxy)PROXIES.get(paramView);
    if (localAnimatorProxy == null)
    {
      localAnimatorProxy = new AnimatorProxy(paramView);
      PROXIES.put(paramView, localAnimatorProxy);
    }
    return localAnimatorProxy;
  }
  
  protected void applyTransformation(float paramFloat, Transformation paramTransformation)
  {
    View localView = (View)this.mView.get();
    if (localView != null)
    {
      paramTransformation.setAlpha(this.mAlpha);
      transformMatrix(paramTransformation.getMatrix(), localView);
    }
  }
  
  public float getAlpha()
  {
    return this.mAlpha;
  }
  
  public float getScaleX()
  {
    return this.mScaleX;
  }
  
  public float getScaleY()
  {
    return this.mScaleY;
  }
  
  public int getScrollX()
  {
    View localView = (View)this.mView.get();
    if (localView == null) {
      return 0;
    }
    return localView.getScrollX();
  }
  
  public int getScrollY()
  {
    View localView = (View)this.mView.get();
    if (localView == null) {
      return 0;
    }
    return localView.getScrollY();
  }
  
  public float getTranslationX()
  {
    return this.mTranslationX;
  }
  
  public float getTranslationY()
  {
    return this.mTranslationY;
  }
  
  public void reset() {}
  
  public void setAlpha(float paramFloat)
  {
    if (this.mAlpha != paramFloat)
    {
      this.mAlpha = paramFloat;
      View localView = (View)this.mView.get();
      if (localView != null) {
        localView.invalidate();
      }
    }
  }
  
  public void setScaleX(float paramFloat)
  {
    if (this.mScaleX != paramFloat)
    {
      prepareForUpdate();
      this.mScaleX = paramFloat;
      invalidateAfterUpdate();
    }
  }
  
  public void setScaleY(float paramFloat)
  {
    if (this.mScaleY != paramFloat)
    {
      prepareForUpdate();
      this.mScaleY = paramFloat;
      invalidateAfterUpdate();
    }
  }
  
  public void setScrollX(int paramInt)
  {
    View localView = (View)this.mView.get();
    if (localView != null) {
      localView.scrollTo(paramInt, localView.getScrollY());
    }
  }
  
  public void setScrollY(int paramInt)
  {
    View localView = (View)this.mView.get();
    if (localView != null) {
      localView.scrollTo(localView.getScrollY(), paramInt);
    }
  }
  
  public void setTranslationX(float paramFloat)
  {
    if (this.mTranslationX != paramFloat)
    {
      prepareForUpdate();
      this.mTranslationX = paramFloat;
      invalidateAfterUpdate();
    }
  }
  
  public void setTranslationY(float paramFloat)
  {
    if (this.mTranslationY != paramFloat)
    {
      prepareForUpdate();
      this.mTranslationY = paramFloat;
      invalidateAfterUpdate();
    }
  }
}
