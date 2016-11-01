package android.support.v4.app;

import android.os.Bundle;
import java.io.FileDescriptor;
import java.io.PrintWriter;

public abstract class FragmentManager
{
  public static final int POP_BACK_STACK_INCLUSIVE = 1;
  
  public FragmentManager() {}
  
  public static void enableDebugLogging(boolean paramBoolean)
  {
    FragmentManagerImpl.DEBUG = paramBoolean;
  }
  
  public abstract void addOnBackStackChangedListener(OnBackStackChangedListener paramOnBackStackChangedListener);
  
  public abstract FragmentTransaction beginTransaction();
  
  public abstract void dump(String paramString, FileDescriptor paramFileDescriptor, PrintWriter paramPrintWriter, String[] paramArrayOfString);
  
  public abstract boolean executePendingTransactions();
  
  public abstract Fragment findFragmentById(int paramInt);
  
  public abstract Fragment findFragmentByTag(String paramString);
  
  public abstract BackStackEntry getBackStackEntryAt(int paramInt);
  
  public abstract int getBackStackEntryCount();
  
  public abstract Fragment getFragment(Bundle paramBundle, String paramString);
  
  @Deprecated
  public FragmentTransaction openTransaction()
  {
    return beginTransaction();
  }
  
  public abstract void popBackStack();
  
  public abstract void popBackStack(int paramInt1, int paramInt2);
  
  public abstract void popBackStack(String paramString, int paramInt);
  
  public abstract boolean popBackStackImmediate();
  
  public abstract boolean popBackStackImmediate(int paramInt1, int paramInt2);
  
  public abstract boolean popBackStackImmediate(String paramString, int paramInt);
  
  public abstract void putFragment(Bundle paramBundle, String paramString, Fragment paramFragment);
  
  public abstract void removeOnBackStackChangedListener(OnBackStackChangedListener paramOnBackStackChangedListener);
  
  public abstract Fragment.SavedState saveFragmentInstanceState(Fragment paramFragment);
  
  public static abstract interface BackStackEntry
  {
    public abstract CharSequence getBreadCrumbShortTitle();
    
    public abstract int getBreadCrumbShortTitleRes();
    
    public abstract CharSequence getBreadCrumbTitle();
    
    public abstract int getBreadCrumbTitleRes();
    
    public abstract int getId();
    
    public abstract String getName();
  }
  
  public static abstract interface OnBackStackChangedListener
  {
    public abstract void onBackStackChanged();
  }
}
