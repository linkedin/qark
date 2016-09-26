package com.actionbarsherlock.internal.nineoldandroids.animation;

import android.view.animation.Interpolator;
import java.util.ArrayList;

public abstract class Animator
  implements Cloneable
{
  ArrayList<AnimatorListener> mListeners = null;
  
  public Animator() {}
  
  public void addListener(AnimatorListener paramAnimatorListener)
  {
    if (this.mListeners == null) {
      this.mListeners = new ArrayList();
    }
    this.mListeners.add(paramAnimatorListener);
  }
  
  public void cancel() {}
  
  public Animator clone()
  {
    Animator localAnimator;
    int i;
    int j;
    do
    {
      try
      {
        localAnimator = (Animator)super.clone();
        if (this.mListeners == null) {
          break;
        }
        localArrayList = this.mListeners;
        localAnimator.mListeners = new ArrayList();
        i = localArrayList.size();
        j = 0;
      }
      catch (CloneNotSupportedException localCloneNotSupportedException)
      {
        ArrayList localArrayList;
        throw new AssertionError();
      }
      localAnimator.mListeners.add((AnimatorListener)localArrayList.get(j));
      j++;
    } while (j < i);
    return localAnimator;
  }
  
  public void end() {}
  
  public abstract long getDuration();
  
  public ArrayList<AnimatorListener> getListeners()
  {
    return this.mListeners;
  }
  
  public abstract long getStartDelay();
  
  public abstract boolean isRunning();
  
  public boolean isStarted()
  {
    return isRunning();
  }
  
  public void removeAllListeners()
  {
    if (this.mListeners != null)
    {
      this.mListeners.clear();
      this.mListeners = null;
    }
  }
  
  public void removeListener(AnimatorListener paramAnimatorListener)
  {
    if (this.mListeners == null) {}
    do
    {
      return;
      this.mListeners.remove(paramAnimatorListener);
    } while (this.mListeners.size() != 0);
    this.mListeners = null;
  }
  
  public abstract Animator setDuration(long paramLong);
  
  public abstract void setInterpolator(Interpolator paramInterpolator);
  
  public abstract void setStartDelay(long paramLong);
  
  public void setTarget(Object paramObject) {}
  
  public void setupEndValues() {}
  
  public void setupStartValues() {}
  
  public void start() {}
  
  public static abstract interface AnimatorListener
  {
    public abstract void onAnimationCancel(Animator paramAnimator);
    
    public abstract void onAnimationEnd(Animator paramAnimator);
    
    public abstract void onAnimationRepeat(Animator paramAnimator);
    
    public abstract void onAnimationStart(Animator paramAnimator);
  }
}
