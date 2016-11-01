package android.support.v4.view;

import android.view.MotionEvent;

class MotionEventCompatEclair
{
  MotionEventCompatEclair() {}
  
  public static int findPointerIndex(MotionEvent paramMotionEvent, int paramInt)
  {
    return paramMotionEvent.findPointerIndex(paramInt);
  }
  
  public static int getPointerId(MotionEvent paramMotionEvent, int paramInt)
  {
    return paramMotionEvent.getPointerId(paramInt);
  }
  
  public static float getX(MotionEvent paramMotionEvent, int paramInt)
  {
    return paramMotionEvent.getX(paramInt);
  }
  
  public static float getY(MotionEvent paramMotionEvent, int paramInt)
  {
    return paramMotionEvent.getY(paramInt);
  }
}
