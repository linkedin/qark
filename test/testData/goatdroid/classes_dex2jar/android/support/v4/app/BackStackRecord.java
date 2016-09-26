package android.support.v4.app;

import android.util.Log;
import java.io.FileDescriptor;
import java.io.PrintWriter;
import java.util.ArrayList;

final class BackStackRecord
  extends FragmentTransaction
  implements FragmentManager.BackStackEntry, Runnable
{
  static final int OP_ADD = 1;
  static final int OP_ATTACH = 7;
  static final int OP_DETACH = 6;
  static final int OP_HIDE = 4;
  static final int OP_NULL = 0;
  static final int OP_REMOVE = 3;
  static final int OP_REPLACE = 2;
  static final int OP_SHOW = 5;
  static final String TAG = "BackStackEntry";
  boolean mAddToBackStack;
  boolean mAllowAddToBackStack = true;
  int mBreadCrumbShortTitleRes;
  CharSequence mBreadCrumbShortTitleText;
  int mBreadCrumbTitleRes;
  CharSequence mBreadCrumbTitleText;
  boolean mCommitted;
  int mEnterAnim;
  int mExitAnim;
  Op mHead;
  int mIndex;
  final FragmentManagerImpl mManager;
  String mName;
  int mNumOp;
  int mPopEnterAnim;
  int mPopExitAnim;
  Op mTail;
  int mTransition;
  int mTransitionStyle;
  
  public BackStackRecord(FragmentManagerImpl paramFragmentManagerImpl)
  {
    this.mManager = paramFragmentManagerImpl;
  }
  
  private void doAddOp(int paramInt1, Fragment paramFragment, String paramString, int paramInt2)
  {
    paramFragment.mFragmentManager = this.mManager;
    if (paramString != null)
    {
      if ((paramFragment.mTag != null) && (!paramString.equals(paramFragment.mTag))) {
        throw new IllegalStateException("Can't change tag of fragment " + paramFragment + ": was " + paramFragment.mTag + " now " + paramString);
      }
      paramFragment.mTag = paramString;
    }
    if (paramInt1 != 0)
    {
      if ((paramFragment.mFragmentId != 0) && (paramFragment.mFragmentId != paramInt1)) {
        throw new IllegalStateException("Can't change container ID of fragment " + paramFragment + ": was " + paramFragment.mFragmentId + " now " + paramInt1);
      }
      paramFragment.mFragmentId = paramInt1;
      paramFragment.mContainerId = paramInt1;
    }
    Op localOp = new Op();
    localOp.cmd = paramInt2;
    localOp.fragment = paramFragment;
    addOp(localOp);
  }
  
  public FragmentTransaction add(int paramInt, Fragment paramFragment)
  {
    doAddOp(paramInt, paramFragment, null, 1);
    return this;
  }
  
  public FragmentTransaction add(int paramInt, Fragment paramFragment, String paramString)
  {
    doAddOp(paramInt, paramFragment, paramString, 1);
    return this;
  }
  
  public FragmentTransaction add(Fragment paramFragment, String paramString)
  {
    doAddOp(0, paramFragment, paramString, 1);
    return this;
  }
  
  void addOp(Op paramOp)
  {
    if (this.mHead == null)
    {
      this.mTail = paramOp;
      this.mHead = paramOp;
    }
    for (;;)
    {
      paramOp.enterAnim = this.mEnterAnim;
      paramOp.exitAnim = this.mExitAnim;
      paramOp.popEnterAnim = this.mPopEnterAnim;
      paramOp.popExitAnim = this.mPopExitAnim;
      this.mNumOp = (1 + this.mNumOp);
      return;
      paramOp.prev = this.mTail;
      this.mTail.next = paramOp;
      this.mTail = paramOp;
    }
  }
  
  public FragmentTransaction addToBackStack(String paramString)
  {
    if (!this.mAllowAddToBackStack) {
      throw new IllegalStateException("This FragmentTransaction is not allowed to be added to the back stack.");
    }
    this.mAddToBackStack = true;
    this.mName = paramString;
    return this;
  }
  
  public FragmentTransaction attach(Fragment paramFragment)
  {
    Op localOp = new Op();
    localOp.cmd = 7;
    localOp.fragment = paramFragment;
    addOp(localOp);
    return this;
  }
  
  void bumpBackStackNesting(int paramInt)
  {
    if (!this.mAddToBackStack) {}
    for (;;)
    {
      return;
      if (FragmentManagerImpl.DEBUG) {
        Log.v("BackStackEntry", "Bump nesting in " + this + " by " + paramInt);
      }
      for (Op localOp = this.mHead; localOp != null; localOp = localOp.next)
      {
        Fragment localFragment1 = localOp.fragment;
        localFragment1.mBackStackNesting = (paramInt + localFragment1.mBackStackNesting);
        if (FragmentManagerImpl.DEBUG) {
          Log.v("BackStackEntry", "Bump nesting of " + localOp.fragment + " to " + localOp.fragment.mBackStackNesting);
        }
        if (localOp.removed != null) {
          for (int i = -1 + localOp.removed.size(); i >= 0; i--)
          {
            Fragment localFragment2 = (Fragment)localOp.removed.get(i);
            localFragment2.mBackStackNesting = (paramInt + localFragment2.mBackStackNesting);
            if (FragmentManagerImpl.DEBUG) {
              Log.v("BackStackEntry", "Bump nesting of " + localFragment2 + " to " + localFragment2.mBackStackNesting);
            }
          }
        }
      }
    }
  }
  
  public int commit()
  {
    return commitInternal(false);
  }
  
  public int commitAllowingStateLoss()
  {
    return commitInternal(true);
  }
  
  int commitInternal(boolean paramBoolean)
  {
    if (this.mCommitted) {
      throw new IllegalStateException("commit already called");
    }
    if (FragmentManagerImpl.DEBUG) {
      Log.v("BackStackEntry", "Commit: " + this);
    }
    this.mCommitted = true;
    if (this.mAddToBackStack) {}
    for (this.mIndex = this.mManager.allocBackStackIndex(this);; this.mIndex = -1)
    {
      this.mManager.enqueueAction(this, paramBoolean);
      return this.mIndex;
    }
  }
  
  public FragmentTransaction detach(Fragment paramFragment)
  {
    Op localOp = new Op();
    localOp.cmd = 6;
    localOp.fragment = paramFragment;
    addOp(localOp);
    return this;
  }
  
  public FragmentTransaction disallowAddToBackStack()
  {
    if (this.mAddToBackStack) {
      throw new IllegalStateException("This transaction is already being added to the back stack");
    }
    this.mAllowAddToBackStack = false;
    return this;
  }
  
  public void dump(String paramString, FileDescriptor paramFileDescriptor, PrintWriter paramPrintWriter, String[] paramArrayOfString)
  {
    paramPrintWriter.print(paramString);
    paramPrintWriter.print("mName=");
    paramPrintWriter.print(this.mName);
    paramPrintWriter.print(" mIndex=");
    paramPrintWriter.print(this.mIndex);
    paramPrintWriter.print(" mCommitted=");
    paramPrintWriter.println(this.mCommitted);
    if (this.mTransition != 0)
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.print("mTransition=#");
      paramPrintWriter.print(Integer.toHexString(this.mTransition));
      paramPrintWriter.print(" mTransitionStyle=#");
      paramPrintWriter.println(Integer.toHexString(this.mTransitionStyle));
    }
    if ((this.mEnterAnim != 0) || (this.mExitAnim != 0))
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.print("mEnterAnim=#");
      paramPrintWriter.print(Integer.toHexString(this.mEnterAnim));
      paramPrintWriter.print(" mExitAnim=#");
      paramPrintWriter.println(Integer.toHexString(this.mExitAnim));
    }
    if ((this.mPopEnterAnim != 0) || (this.mPopExitAnim != 0))
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.print("mPopEnterAnim=#");
      paramPrintWriter.print(Integer.toHexString(this.mPopEnterAnim));
      paramPrintWriter.print(" mPopExitAnim=#");
      paramPrintWriter.println(Integer.toHexString(this.mPopExitAnim));
    }
    if ((this.mBreadCrumbTitleRes != 0) || (this.mBreadCrumbTitleText != null))
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.print("mBreadCrumbTitleRes=#");
      paramPrintWriter.print(Integer.toHexString(this.mBreadCrumbTitleRes));
      paramPrintWriter.print(" mBreadCrumbTitleText=");
      paramPrintWriter.println(this.mBreadCrumbTitleText);
    }
    if ((this.mBreadCrumbShortTitleRes != 0) || (this.mBreadCrumbShortTitleText != null))
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.print("mBreadCrumbShortTitleRes=#");
      paramPrintWriter.print(Integer.toHexString(this.mBreadCrumbShortTitleRes));
      paramPrintWriter.print(" mBreadCrumbShortTitleText=");
      paramPrintWriter.println(this.mBreadCrumbShortTitleText);
    }
    if (this.mHead != null)
    {
      paramPrintWriter.print(paramString);
      paramPrintWriter.println("Operations:");
      String str = paramString + "    ";
      for (Op localOp = this.mHead; localOp != null; localOp = localOp.next)
      {
        paramPrintWriter.print(paramString);
        paramPrintWriter.print("  Op #");
        paramPrintWriter.print(0);
        paramPrintWriter.println(":");
        paramPrintWriter.print(str);
        paramPrintWriter.print("cmd=");
        paramPrintWriter.print(localOp.cmd);
        paramPrintWriter.print(" fragment=");
        paramPrintWriter.println(localOp.fragment);
        if ((localOp.enterAnim != 0) || (localOp.exitAnim != 0))
        {
          paramPrintWriter.print(paramString);
          paramPrintWriter.print("enterAnim=#");
          paramPrintWriter.print(Integer.toHexString(localOp.enterAnim));
          paramPrintWriter.print(" exitAnim=#");
          paramPrintWriter.println(Integer.toHexString(localOp.exitAnim));
        }
        if ((localOp.popEnterAnim != 0) || (localOp.popExitAnim != 0))
        {
          paramPrintWriter.print(paramString);
          paramPrintWriter.print("popEnterAnim=#");
          paramPrintWriter.print(Integer.toHexString(localOp.popEnterAnim));
          paramPrintWriter.print(" popExitAnim=#");
          paramPrintWriter.println(Integer.toHexString(localOp.popExitAnim));
        }
        if ((localOp.removed != null) && (localOp.removed.size() > 0))
        {
          int i = 0;
          if (i < localOp.removed.size())
          {
            paramPrintWriter.print(str);
            if (localOp.removed.size() == 1) {
              paramPrintWriter.print("Removed: ");
            }
            for (;;)
            {
              paramPrintWriter.println(localOp.removed.get(i));
              i++;
              break;
              paramPrintWriter.println("Removed:");
              paramPrintWriter.print(str);
              paramPrintWriter.print("  #");
              paramPrintWriter.print(0);
              paramPrintWriter.print(": ");
            }
          }
        }
      }
    }
  }
  
  public CharSequence getBreadCrumbShortTitle()
  {
    if (this.mBreadCrumbShortTitleRes != 0) {
      return this.mManager.mActivity.getText(this.mBreadCrumbShortTitleRes);
    }
    return this.mBreadCrumbShortTitleText;
  }
  
  public int getBreadCrumbShortTitleRes()
  {
    return this.mBreadCrumbShortTitleRes;
  }
  
  public CharSequence getBreadCrumbTitle()
  {
    if (this.mBreadCrumbTitleRes != 0) {
      return this.mManager.mActivity.getText(this.mBreadCrumbTitleRes);
    }
    return this.mBreadCrumbTitleText;
  }
  
  public int getBreadCrumbTitleRes()
  {
    return this.mBreadCrumbTitleRes;
  }
  
  public int getId()
  {
    return this.mIndex;
  }
  
  public String getName()
  {
    return this.mName;
  }
  
  public int getTransition()
  {
    return this.mTransition;
  }
  
  public int getTransitionStyle()
  {
    return this.mTransitionStyle;
  }
  
  public FragmentTransaction hide(Fragment paramFragment)
  {
    Op localOp = new Op();
    localOp.cmd = 4;
    localOp.fragment = paramFragment;
    addOp(localOp);
    return this;
  }
  
  public boolean isAddToBackStackAllowed()
  {
    return this.mAllowAddToBackStack;
  }
  
  public boolean isEmpty()
  {
    return this.mNumOp == 0;
  }
  
  public void popFromBackStack(boolean paramBoolean)
  {
    if (FragmentManagerImpl.DEBUG) {
      Log.v("BackStackEntry", "popFromBackStack: " + this);
    }
    bumpBackStackNesting(-1);
    Op localOp = this.mTail;
    if (localOp != null)
    {
      switch (localOp.cmd)
      {
      default: 
        throw new IllegalArgumentException("Unknown cmd: " + localOp.cmd);
      case 1: 
        Fragment localFragment8 = localOp.fragment;
        localFragment8.mNextAnim = localOp.popExitAnim;
        this.mManager.removeFragment(localFragment8, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
      }
      for (;;)
      {
        localOp = localOp.prev;
        break;
        Fragment localFragment6 = localOp.fragment;
        localFragment6.mNextAnim = localOp.popExitAnim;
        this.mManager.removeFragment(localFragment6, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
        if (localOp.removed != null)
        {
          for (int i = 0; i < localOp.removed.size(); i++)
          {
            Fragment localFragment7 = (Fragment)localOp.removed.get(i);
            localFragment7.mNextAnim = localOp.popEnterAnim;
            this.mManager.addFragment(localFragment7, false);
          }
          Fragment localFragment5 = localOp.fragment;
          localFragment5.mNextAnim = localOp.popEnterAnim;
          this.mManager.addFragment(localFragment5, false);
          continue;
          Fragment localFragment4 = localOp.fragment;
          localFragment4.mNextAnim = localOp.popEnterAnim;
          this.mManager.showFragment(localFragment4, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
          continue;
          Fragment localFragment3 = localOp.fragment;
          localFragment3.mNextAnim = localOp.popExitAnim;
          this.mManager.hideFragment(localFragment3, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
          continue;
          Fragment localFragment2 = localOp.fragment;
          localFragment2.mNextAnim = localOp.popEnterAnim;
          this.mManager.attachFragment(localFragment2, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
          continue;
          Fragment localFragment1 = localOp.fragment;
          localFragment1.mNextAnim = localOp.popEnterAnim;
          this.mManager.detachFragment(localFragment1, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle);
        }
      }
    }
    if (paramBoolean) {
      this.mManager.moveToState(this.mManager.mCurState, FragmentManagerImpl.reverseTransit(this.mTransition), this.mTransitionStyle, true);
    }
    if (this.mIndex >= 0)
    {
      this.mManager.freeBackStackIndex(this.mIndex);
      this.mIndex = -1;
    }
  }
  
  public FragmentTransaction remove(Fragment paramFragment)
  {
    Op localOp = new Op();
    localOp.cmd = 3;
    localOp.fragment = paramFragment;
    addOp(localOp);
    return this;
  }
  
  public FragmentTransaction replace(int paramInt, Fragment paramFragment)
  {
    return replace(paramInt, paramFragment, null);
  }
  
  public FragmentTransaction replace(int paramInt, Fragment paramFragment, String paramString)
  {
    if (paramInt == 0) {
      throw new IllegalArgumentException("Must use non-zero containerViewId");
    }
    doAddOp(paramInt, paramFragment, paramString, 2);
    return this;
  }
  
  public void run()
  {
    if (FragmentManagerImpl.DEBUG) {
      Log.v("BackStackEntry", "Run: " + this);
    }
    if ((this.mAddToBackStack) && (this.mIndex < 0)) {
      throw new IllegalStateException("addToBackStack() called after commit()");
    }
    bumpBackStackNesting(1);
    Op localOp = this.mHead;
    if (localOp != null)
    {
      switch (localOp.cmd)
      {
      default: 
        throw new IllegalArgumentException("Unknown cmd: " + localOp.cmd);
      case 1: 
        Fragment localFragment8 = localOp.fragment;
        localFragment8.mNextAnim = localOp.enterAnim;
        this.mManager.addFragment(localFragment8, false);
      }
      for (;;)
      {
        localOp = localOp.next;
        break;
        Fragment localFragment6 = localOp.fragment;
        if (this.mManager.mAdded != null) {
          for (int i = 0; i < this.mManager.mAdded.size(); i++)
          {
            Fragment localFragment7 = (Fragment)this.mManager.mAdded.get(i);
            if (FragmentManagerImpl.DEBUG) {
              Log.v("BackStackEntry", "OP_REPLACE: adding=" + localFragment6 + " old=" + localFragment7);
            }
            if (localFragment7.mContainerId == localFragment6.mContainerId)
            {
              if (localOp.removed == null) {
                localOp.removed = new ArrayList();
              }
              localOp.removed.add(localFragment7);
              localFragment7.mNextAnim = localOp.exitAnim;
              if (this.mAddToBackStack)
              {
                localFragment7.mBackStackNesting = (1 + localFragment7.mBackStackNesting);
                if (FragmentManagerImpl.DEBUG) {
                  Log.v("BackStackEntry", "Bump nesting of " + localFragment7 + " to " + localFragment7.mBackStackNesting);
                }
              }
              this.mManager.removeFragment(localFragment7, this.mTransition, this.mTransitionStyle);
            }
          }
        }
        localFragment6.mNextAnim = localOp.enterAnim;
        this.mManager.addFragment(localFragment6, false);
        continue;
        Fragment localFragment5 = localOp.fragment;
        localFragment5.mNextAnim = localOp.exitAnim;
        this.mManager.removeFragment(localFragment5, this.mTransition, this.mTransitionStyle);
        continue;
        Fragment localFragment4 = localOp.fragment;
        localFragment4.mNextAnim = localOp.exitAnim;
        this.mManager.hideFragment(localFragment4, this.mTransition, this.mTransitionStyle);
        continue;
        Fragment localFragment3 = localOp.fragment;
        localFragment3.mNextAnim = localOp.enterAnim;
        this.mManager.showFragment(localFragment3, this.mTransition, this.mTransitionStyle);
        continue;
        Fragment localFragment2 = localOp.fragment;
        localFragment2.mNextAnim = localOp.exitAnim;
        this.mManager.detachFragment(localFragment2, this.mTransition, this.mTransitionStyle);
        continue;
        Fragment localFragment1 = localOp.fragment;
        localFragment1.mNextAnim = localOp.enterAnim;
        this.mManager.attachFragment(localFragment1, this.mTransition, this.mTransitionStyle);
      }
    }
    this.mManager.moveToState(this.mManager.mCurState, this.mTransition, this.mTransitionStyle, true);
    if (this.mAddToBackStack) {
      this.mManager.addBackStackState(this);
    }
  }
  
  public FragmentTransaction setBreadCrumbShortTitle(int paramInt)
  {
    this.mBreadCrumbShortTitleRes = paramInt;
    this.mBreadCrumbShortTitleText = null;
    return this;
  }
  
  public FragmentTransaction setBreadCrumbShortTitle(CharSequence paramCharSequence)
  {
    this.mBreadCrumbShortTitleRes = 0;
    this.mBreadCrumbShortTitleText = paramCharSequence;
    return this;
  }
  
  public FragmentTransaction setBreadCrumbTitle(int paramInt)
  {
    this.mBreadCrumbTitleRes = paramInt;
    this.mBreadCrumbTitleText = null;
    return this;
  }
  
  public FragmentTransaction setBreadCrumbTitle(CharSequence paramCharSequence)
  {
    this.mBreadCrumbTitleRes = 0;
    this.mBreadCrumbTitleText = paramCharSequence;
    return this;
  }
  
  public FragmentTransaction setCustomAnimations(int paramInt1, int paramInt2)
  {
    return setCustomAnimations(paramInt1, paramInt2, 0, 0);
  }
  
  public FragmentTransaction setCustomAnimations(int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    this.mEnterAnim = paramInt1;
    this.mExitAnim = paramInt2;
    this.mPopEnterAnim = paramInt3;
    this.mPopExitAnim = paramInt4;
    return this;
  }
  
  public FragmentTransaction setTransition(int paramInt)
  {
    this.mTransition = paramInt;
    return this;
  }
  
  public FragmentTransaction setTransitionStyle(int paramInt)
  {
    this.mTransitionStyle = paramInt;
    return this;
  }
  
  public FragmentTransaction show(Fragment paramFragment)
  {
    Op localOp = new Op();
    localOp.cmd = 5;
    localOp.fragment = paramFragment;
    addOp(localOp);
    return this;
  }
  
  static final class Op
  {
    int cmd;
    int enterAnim;
    int exitAnim;
    Fragment fragment;
    Op next;
    int popEnterAnim;
    int popExitAnim;
    Op prev;
    ArrayList<Fragment> removed;
    
    Op() {}
  }
}
