package android.support.v4.view;

import android.os.Build.VERSION;
import android.view.KeyEvent;

public class KeyEventCompat
{
  static final KeyEventVersionImpl IMPL = new BaseKeyEventVersionImpl();
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      IMPL = new HoneycombKeyEventVersionImpl();
      return;
    }
  }
  
  public KeyEventCompat() {}
  
  public static boolean hasModifiers(KeyEvent paramKeyEvent, int paramInt)
  {
    return IMPL.metaStateHasModifiers(paramKeyEvent.getMetaState(), paramInt);
  }
  
  public static boolean hasNoModifiers(KeyEvent paramKeyEvent)
  {
    return IMPL.metaStateHasNoModifiers(paramKeyEvent.getMetaState());
  }
  
  public static boolean metaStateHasModifiers(int paramInt1, int paramInt2)
  {
    return IMPL.metaStateHasModifiers(paramInt1, paramInt2);
  }
  
  public static boolean metaStateHasNoModifiers(int paramInt)
  {
    return IMPL.metaStateHasNoModifiers(paramInt);
  }
  
  public static int normalizeMetaState(int paramInt)
  {
    return IMPL.normalizeMetaState(paramInt);
  }
  
  static class BaseKeyEventVersionImpl
    implements KeyEventCompat.KeyEventVersionImpl
  {
    private static final int META_ALL_MASK = 247;
    private static final int META_MODIFIER_MASK = 247;
    
    BaseKeyEventVersionImpl() {}
    
    private static int metaStateFilterDirectionalModifiers(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5)
    {
      int i = 1;
      int j;
      int k;
      if ((paramInt2 & paramInt3) != 0)
      {
        j = i;
        k = paramInt4 | paramInt5;
        if ((paramInt2 & k) == 0) {
          break label52;
        }
      }
      for (;;)
      {
        if (j != 0)
        {
          if (i != 0)
          {
            throw new IllegalArgumentException("bad arguments");
            j = 0;
            break;
            label52:
            i = 0;
            continue;
          }
          paramInt1 &= (k ^ 0xFFFFFFFF);
        }
      }
      while (i == 0) {
        return paramInt1;
      }
      return paramInt1 & (paramInt3 ^ 0xFFFFFFFF);
    }
    
    public boolean metaStateHasModifiers(int paramInt1, int paramInt2)
    {
      return metaStateFilterDirectionalModifiers(metaStateFilterDirectionalModifiers(0xF7 & normalizeMetaState(paramInt1), paramInt2, 1, 64, 128), paramInt2, 2, 16, 32) == paramInt2;
    }
    
    public boolean metaStateHasNoModifiers(int paramInt)
    {
      return (0xF7 & normalizeMetaState(paramInt)) == 0;
    }
    
    public int normalizeMetaState(int paramInt)
    {
      if ((paramInt & 0xC0) != 0) {
        paramInt |= 0x1;
      }
      if ((paramInt & 0x30) != 0) {
        paramInt |= 0x2;
      }
      return paramInt & 0xF7;
    }
  }
  
  static class HoneycombKeyEventVersionImpl
    implements KeyEventCompat.KeyEventVersionImpl
  {
    HoneycombKeyEventVersionImpl() {}
    
    public boolean metaStateHasModifiers(int paramInt1, int paramInt2)
    {
      return KeyEventCompatHoneycomb.metaStateHasModifiers(paramInt1, paramInt2);
    }
    
    public boolean metaStateHasNoModifiers(int paramInt)
    {
      return KeyEventCompatHoneycomb.metaStateHasNoModifiers(paramInt);
    }
    
    public int normalizeMetaState(int paramInt)
    {
      return KeyEventCompatHoneycomb.normalizeMetaState(paramInt);
    }
  }
  
  static abstract interface KeyEventVersionImpl
  {
    public abstract boolean metaStateHasModifiers(int paramInt1, int paramInt2);
    
    public abstract boolean metaStateHasNoModifiers(int paramInt);
    
    public abstract int normalizeMetaState(int paramInt);
  }
}
