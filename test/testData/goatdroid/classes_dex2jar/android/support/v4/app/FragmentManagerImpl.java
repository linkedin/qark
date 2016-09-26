// 
// Decompiled by Procyon v0.5.30
// 

package android.support.v4.app;

import android.support.v4.util.DebugUtils;
import java.io.Writer;
import android.support.v4.util.LogWriter;
import android.os.Handler;
import android.view.View;
import android.view.animation.Animation$AnimationListener;
import android.view.ViewGroup;
import android.app.Activity;
import android.view.animation.AnimationUtils;
import android.os.Looper;
import java.util.Arrays;
import java.io.PrintWriter;
import java.io.FileDescriptor;
import android.view.MenuInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.content.res.Configuration;
import android.util.Log;
import android.view.animation.ScaleAnimation;
import android.view.animation.AnimationSet;
import android.view.animation.AlphaAnimation;
import android.view.animation.Animation;
import android.content.Context;
import android.view.animation.AccelerateInterpolator;
import android.view.animation.DecelerateInterpolator;
import android.os.Build$VERSION;
import android.os.Bundle;
import android.os.Parcelable;
import android.util.SparseArray;
import java.util.ArrayList;
import android.view.animation.Interpolator;

final class FragmentManagerImpl extends FragmentManager
{
    static final Interpolator ACCELERATE_CUBIC;
    static final Interpolator ACCELERATE_QUINT;
    static final int ANIM_DUR = 220;
    public static final int ANIM_STYLE_CLOSE_ENTER = 3;
    public static final int ANIM_STYLE_CLOSE_EXIT = 4;
    public static final int ANIM_STYLE_FADE_ENTER = 5;
    public static final int ANIM_STYLE_FADE_EXIT = 6;
    public static final int ANIM_STYLE_OPEN_ENTER = 1;
    public static final int ANIM_STYLE_OPEN_EXIT = 2;
    static boolean DEBUG = false;
    static final Interpolator DECELERATE_CUBIC;
    static final Interpolator DECELERATE_QUINT;
    static final boolean HONEYCOMB = false;
    static final String TAG = "FragmentManager";
    static final String TARGET_REQUEST_CODE_STATE_TAG = "android:target_req_state";
    static final String TARGET_STATE_TAG = "android:target_state";
    static final String USER_VISIBLE_HINT_TAG = "android:user_visible_hint";
    static final String VIEW_STATE_TAG = "android:view_state";
    ArrayList<Fragment> mActive;
    FragmentActivity mActivity;
    ArrayList<Fragment> mAdded;
    ArrayList<Integer> mAvailBackStackIndices;
    ArrayList<Integer> mAvailIndices;
    ArrayList<BackStackRecord> mBackStack;
    ArrayList<OnBackStackChangedListener> mBackStackChangeListeners;
    ArrayList<BackStackRecord> mBackStackIndices;
    ArrayList<Fragment> mCreatedMenus;
    int mCurState;
    boolean mDestroyed;
    Runnable mExecCommit;
    boolean mExecutingActions;
    boolean mHavePendingDeferredStart;
    boolean mNeedMenuInvalidate;
    String mNoTransactionsBecause;
    ArrayList<Runnable> mPendingActions;
    SparseArray<Parcelable> mStateArray;
    Bundle mStateBundle;
    boolean mStateSaved;
    Runnable[] mTmpActions;
    
    static {
        FragmentManagerImpl.DEBUG = false;
        final int sdk_INT = Build$VERSION.SDK_INT;
        boolean honeycomb = false;
        if (sdk_INT >= 11) {
            honeycomb = true;
        }
        DECELERATE_QUINT = (Interpolator)new DecelerateInterpolator(2.5f);
        DECELERATE_CUBIC = (Interpolator)new DecelerateInterpolator(1.5f);
        ACCELERATE_QUINT = (Interpolator)new AccelerateInterpolator(2.5f);
        ACCELERATE_CUBIC = (Interpolator)new AccelerateInterpolator(1.5f);
    }
    
    FragmentManagerImpl() {
        this.mCurState = 0;
        this.mStateBundle = null;
        this.mStateArray = null;
        this.mExecCommit = new Runnable() {
            @Override
            public void run() {
                FragmentManagerImpl.this.execPendingActions();
            }
        };
    }
    
    private void checkStateLoss() {
        if (this.mStateSaved) {
            throw new IllegalStateException("Can not perform this action after onSaveInstanceState");
        }
        if (this.mNoTransactionsBecause != null) {
            throw new IllegalStateException("Can not perform this action inside of " + this.mNoTransactionsBecause);
        }
    }
    
    static Animation makeFadeAnimation(final Context context, final float n, final float n2) {
        final AlphaAnimation alphaAnimation = new AlphaAnimation(n, n2);
        alphaAnimation.setInterpolator(FragmentManagerImpl.DECELERATE_CUBIC);
        alphaAnimation.setDuration(220L);
        return (Animation)alphaAnimation;
    }
    
    static Animation makeOpenCloseAnimation(final Context context, final float n, final float n2, final float n3, final float n4) {
        final AnimationSet set = new AnimationSet(false);
        final ScaleAnimation scaleAnimation = new ScaleAnimation(n, n2, n, n2, 1, 0.5f, 1, 0.5f);
        scaleAnimation.setInterpolator(FragmentManagerImpl.DECELERATE_QUINT);
        scaleAnimation.setDuration(220L);
        set.addAnimation((Animation)scaleAnimation);
        final AlphaAnimation alphaAnimation = new AlphaAnimation(n3, n4);
        alphaAnimation.setInterpolator(FragmentManagerImpl.DECELERATE_CUBIC);
        alphaAnimation.setDuration(220L);
        set.addAnimation((Animation)alphaAnimation);
        return (Animation)set;
    }
    
    public static int reverseTransit(final int n) {
        switch (n) {
            default: {
                return 0;
            }
            case 4097: {
                return 8194;
            }
            case 8194: {
                return 4097;
            }
            case 4099: {
                return 4099;
            }
        }
    }
    
    public static int transitToStyleIndex(final int n, final boolean b) {
        switch (n) {
            default: {
                return -1;
            }
            case 4097: {
                if (b) {
                    return 1;
                }
                return 2;
            }
            case 8194: {
                if (b) {
                    return 3;
                }
                return 4;
            }
            case 4099: {
                if (b) {
                    return 5;
                }
                return 6;
            }
        }
    }
    
    void addBackStackState(final BackStackRecord backStackRecord) {
        if (this.mBackStack == null) {
            this.mBackStack = new ArrayList<BackStackRecord>();
        }
        this.mBackStack.add(backStackRecord);
        this.reportBackStackChanged();
    }
    
    public void addFragment(final Fragment fragment, final boolean b) {
        if (this.mAdded == null) {
            this.mAdded = new ArrayList<Fragment>();
        }
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "add: " + fragment);
        }
        this.makeActive(fragment);
        if (!fragment.mDetached) {
            this.mAdded.add(fragment);
            fragment.mAdded = true;
            fragment.mRemoving = false;
            if (fragment.mHasMenu && fragment.mMenuVisible) {
                this.mNeedMenuInvalidate = true;
            }
            if (b) {
                this.moveToState(fragment);
            }
        }
    }
    
    @Override
    public void addOnBackStackChangedListener(final OnBackStackChangedListener onBackStackChangedListener) {
        if (this.mBackStackChangeListeners == null) {
            this.mBackStackChangeListeners = new ArrayList<OnBackStackChangedListener>();
        }
        this.mBackStackChangeListeners.add(onBackStackChangedListener);
    }
    
    public int allocBackStackIndex(final BackStackRecord backStackRecord) {
        synchronized (this) {
            if (this.mAvailBackStackIndices == null || this.mAvailBackStackIndices.size() <= 0) {
                if (this.mBackStackIndices == null) {
                    this.mBackStackIndices = new ArrayList<BackStackRecord>();
                }
                final int size = this.mBackStackIndices.size();
                if (FragmentManagerImpl.DEBUG) {
                    Log.v("FragmentManager", "Setting back stack index " + size + " to " + backStackRecord);
                }
                this.mBackStackIndices.add(backStackRecord);
                return size;
            }
            final int intValue = this.mAvailBackStackIndices.remove(-1 + this.mAvailBackStackIndices.size());
            if (FragmentManagerImpl.DEBUG) {
                Log.v("FragmentManager", "Adding back stack index " + intValue + " with " + backStackRecord);
            }
            this.mBackStackIndices.set(intValue, backStackRecord);
            return intValue;
        }
    }
    
    public void attachActivity(final FragmentActivity mActivity) {
        if (this.mActivity != null) {
            throw new IllegalStateException();
        }
        this.mActivity = mActivity;
    }
    
    public void attachFragment(final Fragment fragment, final int n, final int n2) {
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "attach: " + fragment);
        }
        if (fragment.mDetached) {
            fragment.mDetached = false;
            if (!fragment.mAdded) {
                this.mAdded.add(fragment);
                fragment.mAdded = true;
                if (fragment.mHasMenu && fragment.mMenuVisible) {
                    this.mNeedMenuInvalidate = true;
                }
                this.moveToState(fragment, this.mCurState, n, n2);
            }
        }
    }
    
    @Override
    public FragmentTransaction beginTransaction() {
        return new BackStackRecord(this);
    }
    
    public void detachFragment(final Fragment fragment, final int n, final int n2) {
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "detach: " + fragment);
        }
        if (!fragment.mDetached) {
            fragment.mDetached = true;
            if (fragment.mAdded) {
                this.mAdded.remove(fragment);
                if (fragment.mHasMenu && fragment.mMenuVisible) {
                    this.mNeedMenuInvalidate = true;
                }
                fragment.mAdded = false;
                this.moveToState(fragment, 1, n, n2);
            }
        }
    }
    
    public void dispatchActivityCreated() {
        this.moveToState(2, this.mStateSaved = false);
    }
    
    public void dispatchConfigurationChanged(final Configuration configuration) {
        if (this.mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null) {
                    fragment.onConfigurationChanged(configuration);
                }
            }
        }
    }
    
    public boolean dispatchContextItemSelected(final MenuItem menuItem) {
        if (this.mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && !fragment.mHidden && fragment.onContextItemSelected(menuItem)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    public void dispatchCreate() {
        this.moveToState(1, this.mStateSaved = false);
    }
    
    public boolean dispatchCreateOptionsMenu(final Menu menu, final MenuInflater menuInflater) {
        final ArrayList<Fragment> mActive = this.mActive;
        ArrayList<Fragment> mCreatedMenus = null;
        boolean b = false;
        if (mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && !fragment.mHidden && fragment.mHasMenu && fragment.mMenuVisible) {
                    b = true;
                    fragment.onCreateOptionsMenu(menu, menuInflater);
                    if (mCreatedMenus == null) {
                        mCreatedMenus = new ArrayList<Fragment>();
                    }
                    mCreatedMenus.add(fragment);
                }
            }
        }
        if (this.mCreatedMenus != null) {
            for (int j = 0; j < this.mCreatedMenus.size(); ++j) {
                final Fragment fragment2 = this.mCreatedMenus.get(j);
                if (mCreatedMenus == null || !mCreatedMenus.contains(fragment2)) {
                    fragment2.onDestroyOptionsMenu();
                }
            }
        }
        this.mCreatedMenus = mCreatedMenus;
        return b;
    }
    
    public void dispatchDestroy() {
        this.mDestroyed = true;
        this.execPendingActions();
        this.moveToState(0, false);
        this.mActivity = null;
    }
    
    public void dispatchLowMemory() {
        if (this.mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null) {
                    fragment.onLowMemory();
                }
            }
        }
    }
    
    public boolean dispatchOptionsItemSelected(final MenuItem menuItem) {
        if (this.mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && !fragment.mHidden && fragment.mHasMenu && fragment.mMenuVisible && fragment.onOptionsItemSelected(menuItem)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    public void dispatchOptionsMenuClosed(final Menu menu) {
        if (this.mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && !fragment.mHidden && fragment.mHasMenu && fragment.mMenuVisible) {
                    fragment.onOptionsMenuClosed(menu);
                }
            }
        }
    }
    
    public void dispatchPause() {
        this.moveToState(4, false);
    }
    
    public boolean dispatchPrepareOptionsMenu(final Menu menu) {
        final ArrayList<Fragment> mActive = this.mActive;
        boolean b = false;
        if (mActive != null) {
            for (int i = 0; i < this.mAdded.size(); ++i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && !fragment.mHidden && fragment.mHasMenu && fragment.mMenuVisible) {
                    b = true;
                    fragment.onPrepareOptionsMenu(menu);
                }
            }
        }
        return b;
    }
    
    public void dispatchReallyStop() {
        this.moveToState(2, false);
    }
    
    public void dispatchResume() {
        this.moveToState(5, this.mStateSaved = false);
    }
    
    public void dispatchStart() {
        this.moveToState(4, this.mStateSaved = false);
    }
    
    public void dispatchStop() {
        this.mStateSaved = true;
        this.moveToState(3, false);
    }
    
    @Override
    public void dump(final String s, final FileDescriptor fileDescriptor, final PrintWriter printWriter, final String[] array) {
        final String string = s + "    ";
        if (this.mActive != null) {
            final int size = this.mActive.size();
            if (size > 0) {
                printWriter.print(s);
                printWriter.print("Active Fragments in ");
                printWriter.print(Integer.toHexString(System.identityHashCode(this)));
                printWriter.println(":");
                for (int i = 0; i < size; ++i) {
                    final Fragment fragment = this.mActive.get(i);
                    printWriter.print(s);
                    printWriter.print("  #");
                    printWriter.print(i);
                    printWriter.print(": ");
                    printWriter.println(fragment);
                    if (fragment != null) {
                        fragment.dump(string, fileDescriptor, printWriter, array);
                    }
                }
            }
        }
        if (this.mAdded != null) {
            final int size2 = this.mAdded.size();
            if (size2 > 0) {
                printWriter.print(s);
                printWriter.println("Added Fragments:");
                for (int j = 0; j < size2; ++j) {
                    final Fragment fragment2 = this.mAdded.get(j);
                    printWriter.print(s);
                    printWriter.print("  #");
                    printWriter.print(j);
                    printWriter.print(": ");
                    printWriter.println(fragment2.toString());
                }
            }
        }
        if (this.mCreatedMenus != null) {
            final int size3 = this.mCreatedMenus.size();
            if (size3 > 0) {
                printWriter.print(s);
                printWriter.println("Fragments Created Menus:");
                for (int k = 0; k < size3; ++k) {
                    final Fragment fragment3 = this.mCreatedMenus.get(k);
                    printWriter.print(s);
                    printWriter.print("  #");
                    printWriter.print(k);
                    printWriter.print(": ");
                    printWriter.println(fragment3.toString());
                }
            }
        }
        if (this.mBackStack != null) {
            final int size4 = this.mBackStack.size();
            if (size4 > 0) {
                printWriter.print(s);
                printWriter.println("Back Stack:");
                for (int l = 0; l < size4; ++l) {
                    final BackStackRecord backStackRecord = this.mBackStack.get(l);
                    printWriter.print(s);
                    printWriter.print("  #");
                    printWriter.print(l);
                    printWriter.print(": ");
                    printWriter.println(backStackRecord.toString());
                    backStackRecord.dump(string, fileDescriptor, printWriter, array);
                }
            }
        }
        synchronized (this) {
            if (this.mBackStackIndices != null) {
                final int size5 = this.mBackStackIndices.size();
                if (size5 > 0) {
                    printWriter.print(s);
                    printWriter.println("Back Stack Indices:");
                    for (int n = 0; n < size5; ++n) {
                        final BackStackRecord backStackRecord2 = this.mBackStackIndices.get(n);
                        printWriter.print(s);
                        printWriter.print("  #");
                        printWriter.print(n);
                        printWriter.print(": ");
                        printWriter.println(backStackRecord2);
                    }
                }
            }
            if (this.mAvailBackStackIndices != null && this.mAvailBackStackIndices.size() > 0) {
                printWriter.print(s);
                printWriter.print("mAvailBackStackIndices: ");
                printWriter.println(Arrays.toString(this.mAvailBackStackIndices.toArray()));
            }
            // monitorexit(this)
            if (this.mPendingActions != null) {
                final int size6 = this.mPendingActions.size();
                if (size6 > 0) {
                    printWriter.print(s);
                    printWriter.println("Pending Actions:");
                    for (int n2 = 0; n2 < size6; ++n2) {
                        final Runnable runnable = this.mPendingActions.get(n2);
                        printWriter.print(s);
                        printWriter.print("  #");
                        printWriter.print(n2);
                        printWriter.print(": ");
                        printWriter.println(runnable);
                    }
                }
            }
        }
        printWriter.print(s);
        printWriter.println("FragmentManager misc state:");
        printWriter.print(s);
        printWriter.print("  mCurState=");
        printWriter.print(this.mCurState);
        printWriter.print(" mStateSaved=");
        printWriter.print(this.mStateSaved);
        printWriter.print(" mDestroyed=");
        printWriter.println(this.mDestroyed);
        if (this.mNeedMenuInvalidate) {
            printWriter.print(s);
            printWriter.print("  mNeedMenuInvalidate=");
            printWriter.println(this.mNeedMenuInvalidate);
        }
        if (this.mNoTransactionsBecause != null) {
            printWriter.print(s);
            printWriter.print("  mNoTransactionsBecause=");
            printWriter.println(this.mNoTransactionsBecause);
        }
        if (this.mAvailIndices != null && this.mAvailIndices.size() > 0) {
            printWriter.print(s);
            printWriter.print("  mAvailIndices: ");
            printWriter.println(Arrays.toString(this.mAvailIndices.toArray()));
        }
    }
    
    public void enqueueAction(final Runnable runnable, final boolean b) {
        if (!b) {
            this.checkStateLoss();
        }
        synchronized (this) {
            if (this.mActivity == null) {
                throw new IllegalStateException("Activity has been destroyed");
            }
        }
        if (this.mPendingActions == null) {
            this.mPendingActions = new ArrayList<Runnable>();
        }
        this.mPendingActions.add(runnable);
        if (this.mPendingActions.size() == 1) {
            this.mActivity.mHandler.removeCallbacks(this.mExecCommit);
            this.mActivity.mHandler.post(this.mExecCommit);
        }
    }
    // monitorexit(this)
    
    public boolean execPendingActions() {
        if (this.mExecutingActions) {
            throw new IllegalStateException("Recursive entry to executePendingTransactions");
        }
        if (Looper.myLooper() != this.mActivity.mHandler.getLooper()) {
            throw new IllegalStateException("Must be called from main thread of process");
        }
        boolean b = false;
        while (true) {
            boolean b2 = false;
            Label_0262: {
                synchronized (this) {
                    if (this.mPendingActions == null || this.mPendingActions.size() == 0) {
                        // monitorexit(this)
                        if (this.mHavePendingDeferredStart) {
                            b2 = false;
                            for (int i = 0; i < this.mActive.size(); ++i) {
                                final Fragment fragment = this.mActive.get(i);
                                if (fragment != null && fragment.mLoaderManager != null) {
                                    b2 |= fragment.mLoaderManager.hasRunningLoaders();
                                }
                            }
                            break Label_0262;
                        }
                        break;
                    }
                    else {
                        final int size = this.mPendingActions.size();
                        if (this.mTmpActions == null || this.mTmpActions.length < size) {
                            this.mTmpActions = new Runnable[size];
                        }
                        this.mPendingActions.toArray(this.mTmpActions);
                        this.mPendingActions.clear();
                        this.mActivity.mHandler.removeCallbacks(this.mExecCommit);
                        // monitorexit(this)
                        this.mExecutingActions = true;
                        for (int j = 0; j < size; ++j) {
                            this.mTmpActions[j].run();
                            this.mTmpActions[j] = null;
                        }
                    }
                }
                this.mExecutingActions = false;
                b = true;
                continue;
            }
            if (!b2) {
                this.mHavePendingDeferredStart = false;
                this.startPendingDeferredFragments();
                break;
            }
            break;
        }
        return b;
    }
    
    @Override
    public boolean executePendingTransactions() {
        return this.execPendingActions();
    }
    
    @Override
    public Fragment findFragmentById(final int n) {
        if (this.mActive != null) {
            for (int i = -1 + this.mAdded.size(); i >= 0; --i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && fragment.mFragmentId == n) {
                    return fragment;
                }
            }
            for (int j = -1 + this.mActive.size(); j >= 0; --j) {
                final Fragment fragment = this.mActive.get(j);
                if (fragment != null && fragment.mFragmentId == n) {
                    return fragment;
                }
            }
        }
        return null;
    }
    
    @Override
    public Fragment findFragmentByTag(final String s) {
        if (this.mActive != null && s != null) {
            for (int i = -1 + this.mAdded.size(); i >= 0; --i) {
                final Fragment fragment = this.mAdded.get(i);
                if (fragment != null && s.equals(fragment.mTag)) {
                    return fragment;
                }
            }
            for (int j = -1 + this.mActive.size(); j >= 0; --j) {
                final Fragment fragment = this.mActive.get(j);
                if (fragment != null && s.equals(fragment.mTag)) {
                    return fragment;
                }
            }
        }
        return null;
    }
    
    public Fragment findFragmentByWho(final String s) {
        if (this.mActive != null && s != null) {
            for (int i = -1 + this.mActive.size(); i >= 0; --i) {
                final Fragment fragment = this.mActive.get(i);
                if (fragment != null && s.equals(fragment.mWho)) {
                    return fragment;
                }
            }
        }
        return null;
    }
    
    public void freeBackStackIndex(final int n) {
        synchronized (this) {
            this.mBackStackIndices.set(n, null);
            if (this.mAvailBackStackIndices == null) {
                this.mAvailBackStackIndices = new ArrayList<Integer>();
            }
            if (FragmentManagerImpl.DEBUG) {
                Log.v("FragmentManager", "Freeing back stack index " + n);
            }
            this.mAvailBackStackIndices.add(n);
        }
    }
    
    @Override
    public BackStackEntry getBackStackEntryAt(final int n) {
        return this.mBackStack.get(n);
    }
    
    @Override
    public int getBackStackEntryCount() {
        if (this.mBackStack != null) {
            return this.mBackStack.size();
        }
        return 0;
    }
    
    @Override
    public Fragment getFragment(final Bundle bundle, final String s) {
        final int int1 = bundle.getInt(s, -1);
        Fragment fragment;
        if (int1 == -1) {
            fragment = null;
        }
        else {
            if (int1 >= this.mActive.size()) {
                throw new IllegalStateException("Fragement no longer exists for key " + s + ": index " + int1);
            }
            fragment = this.mActive.get(int1);
            if (fragment == null) {
                throw new IllegalStateException("Fragement no longer exists for key " + s + ": index " + int1);
            }
        }
        return fragment;
    }
    
    public void hideFragment(final Fragment fragment, final int n, final int n2) {
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "hide: " + fragment);
        }
        if (!fragment.mHidden) {
            fragment.mHidden = true;
            if (fragment.mView != null) {
                final Animation loadAnimation = this.loadAnimation(fragment, n, true, n2);
                if (loadAnimation != null) {
                    fragment.mView.startAnimation(loadAnimation);
                }
                fragment.mView.setVisibility(8);
            }
            if (fragment.mAdded && fragment.mHasMenu && fragment.mMenuVisible) {
                this.mNeedMenuInvalidate = true;
            }
            fragment.onHiddenChanged(true);
        }
    }
    
    Animation loadAnimation(final Fragment fragment, final int n, final boolean b, int windowAnimations) {
        final Animation onCreateAnimation = fragment.onCreateAnimation(n, b, fragment.mNextAnim);
        if (onCreateAnimation != null) {
            return onCreateAnimation;
        }
        if (fragment.mNextAnim != 0) {
            final Animation loadAnimation = AnimationUtils.loadAnimation((Context)this.mActivity, fragment.mNextAnim);
            if (loadAnimation != null) {
                return loadAnimation;
            }
        }
        if (n == 0) {
            return null;
        }
        final int transitToStyleIndex = transitToStyleIndex(n, b);
        if (transitToStyleIndex < 0) {
            return null;
        }
        switch (transitToStyleIndex) {
            default: {
                if (windowAnimations == 0 && this.mActivity.getWindow() != null) {
                    windowAnimations = this.mActivity.getWindow().getAttributes().windowAnimations;
                }
                if (windowAnimations == 0) {
                    return null;
                }
                return null;
            }
            case 1: {
                return makeOpenCloseAnimation((Context)this.mActivity, 1.125f, 1.0f, 0.0f, 1.0f);
            }
            case 2: {
                return makeOpenCloseAnimation((Context)this.mActivity, 1.0f, 0.975f, 1.0f, 0.0f);
            }
            case 3: {
                return makeOpenCloseAnimation((Context)this.mActivity, 0.975f, 1.0f, 0.0f, 1.0f);
            }
            case 4: {
                return makeOpenCloseAnimation((Context)this.mActivity, 1.0f, 1.075f, 1.0f, 0.0f);
            }
            case 5: {
                return makeFadeAnimation((Context)this.mActivity, 0.0f, 1.0f);
            }
            case 6: {
                return makeFadeAnimation((Context)this.mActivity, 1.0f, 0.0f);
            }
        }
    }
    
    void makeActive(final Fragment fragment) {
        if (fragment.mIndex >= 0) {
            return;
        }
        if (this.mAvailIndices == null || this.mAvailIndices.size() <= 0) {
            if (this.mActive == null) {
                this.mActive = new ArrayList<Fragment>();
            }
            fragment.setIndex(this.mActive.size());
            this.mActive.add(fragment);
            return;
        }
        fragment.setIndex(this.mAvailIndices.remove(-1 + this.mAvailIndices.size()));
        this.mActive.set(fragment.mIndex, fragment);
    }
    
    void makeInactive(final Fragment fragment) {
        if (fragment.mIndex < 0) {
            return;
        }
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "Freeing fragment index " + fragment.mIndex);
        }
        this.mActive.set(fragment.mIndex, null);
        if (this.mAvailIndices == null) {
            this.mAvailIndices = new ArrayList<Integer>();
        }
        this.mAvailIndices.add(fragment.mIndex);
        this.mActivity.invalidateSupportFragmentIndex(fragment.mIndex);
        fragment.initState();
    }
    
    void moveToState(final int mCurState, final int n, final int n2, final boolean b) {
        if (this.mActivity == null && mCurState != 0) {
            throw new IllegalStateException("No activity");
        }
        if (b || this.mCurState != mCurState) {
            this.mCurState = mCurState;
            if (this.mActive != null) {
                boolean b2 = false;
                for (int i = 0; i < this.mActive.size(); ++i) {
                    final Fragment fragment = this.mActive.get(i);
                    if (fragment != null) {
                        this.moveToState(fragment, mCurState, n, n2);
                        if (fragment.mLoaderManager != null) {
                            b2 |= fragment.mLoaderManager.hasRunningLoaders();
                        }
                    }
                }
                if (!b2) {
                    this.startPendingDeferredFragments();
                }
                if (this.mNeedMenuInvalidate && this.mActivity != null && this.mCurState == 5) {
                    this.mActivity.supportInvalidateOptionsMenu();
                    this.mNeedMenuInvalidate = false;
                }
            }
        }
    }
    
    void moveToState(final int n, final boolean b) {
        this.moveToState(n, 0, 0, b);
    }
    
    void moveToState(final Fragment fragment) {
        this.moveToState(fragment, this.mCurState, 0, 0);
    }
    
    void moveToState(final Fragment fragment, int mState, final int n, final int n2) {
        if (!fragment.mAdded && mState > 1) {
            mState = 1;
        }
        if (fragment.mRemoving && mState > fragment.mState) {
            mState = fragment.mState;
        }
        if (fragment.mDeferStart && fragment.mState < 4 && mState > 3) {
            mState = 3;
        }
        if (fragment.mState < mState) {
            if (fragment.mFromLayout && !fragment.mInLayout) {
                return;
            }
            if (fragment.mAnimatingAway != null) {
                fragment.mAnimatingAway = null;
                this.moveToState(fragment, fragment.mStateAfterAnimating, 0, 0);
            }
            Label_0919: {
                switch (fragment.mState) {
                    case 0: {
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "moveto CREATED: " + fragment);
                        }
                        if (fragment.mSavedFragmentState != null) {
                            fragment.mSavedViewState = (SparseArray<Parcelable>)fragment.mSavedFragmentState.getSparseParcelableArray("android:view_state");
                            fragment.mTarget = this.getFragment(fragment.mSavedFragmentState, "android:target_state");
                            if (fragment.mTarget != null) {
                                fragment.mTargetRequestCode = fragment.mSavedFragmentState.getInt("android:target_req_state", 0);
                            }
                            if (!(fragment.mUserVisibleHint = fragment.mSavedFragmentState.getBoolean("android:user_visible_hint", true))) {
                                fragment.mDeferStart = true;
                                if (mState > 3) {
                                    mState = 3;
                                }
                            }
                        }
                        fragment.mActivity = this.mActivity;
                        fragment.mFragmentManager = this.mActivity.mFragments;
                        fragment.mCalled = false;
                        fragment.onAttach(this.mActivity);
                        if (!fragment.mCalled) {
                            throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onAttach()");
                        }
                        this.mActivity.onAttachFragment(fragment);
                        if (!fragment.mRetaining) {
                            fragment.mCalled = false;
                            fragment.onCreate(fragment.mSavedFragmentState);
                            if (!fragment.mCalled) {
                                throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onCreate()");
                            }
                        }
                        fragment.mRetaining = false;
                        if (!fragment.mFromLayout) {
                            break Label_0919;
                        }
                        fragment.mView = fragment.onCreateView(fragment.getLayoutInflater(fragment.mSavedFragmentState), null, fragment.mSavedFragmentState);
                        if (fragment.mView != null) {
                            fragment.mInnerView = fragment.mView;
                            fragment.mView = (View)NoSaveStateFrameLayout.wrap(fragment.mView);
                            if (fragment.mHidden) {
                                fragment.mView.setVisibility(8);
                            }
                            fragment.onViewCreated(fragment.mView, fragment.mSavedFragmentState);
                            break Label_0919;
                        }
                        fragment.mInnerView = null;
                        break Label_0919;
                    }
                    case 1: {
                        if (mState <= 1) {
                            break Label_0919;
                        }
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "moveto ACTIVITY_CREATED: " + fragment);
                        }
                        if (!fragment.mFromLayout) {
                            final int mContainerId = fragment.mContainerId;
                            ViewGroup mContainer = null;
                            if (mContainerId != 0) {
                                mContainer = (ViewGroup)this.mActivity.findViewById(fragment.mContainerId);
                                if (mContainer == null && !fragment.mRestored) {
                                    throw new IllegalArgumentException("No view found for id 0x" + Integer.toHexString(fragment.mContainerId) + " for fragment " + fragment);
                                }
                            }
                            fragment.mContainer = mContainer;
                            fragment.mView = fragment.onCreateView(fragment.getLayoutInflater(fragment.mSavedFragmentState), mContainer, fragment.mSavedFragmentState);
                            if (fragment.mView != null) {
                                fragment.mInnerView = fragment.mView;
                                fragment.mView = (View)NoSaveStateFrameLayout.wrap(fragment.mView);
                                if (mContainer != null) {
                                    final Animation loadAnimation = this.loadAnimation(fragment, n, true, n2);
                                    if (loadAnimation != null) {
                                        fragment.mView.startAnimation(loadAnimation);
                                    }
                                    mContainer.addView(fragment.mView);
                                }
                                if (fragment.mHidden) {
                                    fragment.mView.setVisibility(8);
                                }
                                fragment.onViewCreated(fragment.mView, fragment.mSavedFragmentState);
                            }
                            else {
                                fragment.mInnerView = null;
                            }
                        }
                        fragment.mCalled = false;
                        fragment.onActivityCreated(fragment.mSavedFragmentState);
                        if (!fragment.mCalled) {
                            throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onActivityCreated()");
                        }
                        if (fragment.mView != null) {
                            fragment.restoreViewState();
                        }
                        fragment.mSavedFragmentState = null;
                        break Label_0919;
                    }
                    case 2:
                    case 3: {
                        if (mState <= 3) {
                            break Label_0919;
                        }
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "moveto STARTED: " + fragment);
                        }
                        fragment.mCalled = false;
                        fragment.performStart();
                        if (!fragment.mCalled) {
                            throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onStart()");
                        }
                        break Label_0919;
                    }
                    case 4: {
                        if (mState <= 4) {
                            break;
                        }
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "moveto RESUMED: " + fragment);
                        }
                        fragment.mCalled = false;
                        fragment.mResumed = true;
                        fragment.onResume();
                        if (!fragment.mCalled) {
                            throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onResume()");
                        }
                        fragment.mSavedFragmentState = null;
                        fragment.mSavedViewState = null;
                        break;
                    }
                }
            }
        }
        else if (fragment.mState > mState) {
            while (true) {
                Label_1306: {
                    switch (fragment.mState) {
                        case 1: {
                            if (mState >= 1) {
                                break;
                            }
                            if (this.mDestroyed && fragment.mAnimatingAway != null) {
                                final View mAnimatingAway = fragment.mAnimatingAway;
                                fragment.mAnimatingAway = null;
                                mAnimatingAway.clearAnimation();
                            }
                            if (fragment.mAnimatingAway != null) {
                                fragment.mStateAfterAnimating = mState;
                                mState = 1;
                                break;
                            }
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "movefrom CREATED: " + fragment);
                            }
                            if (!fragment.mRetaining) {
                                fragment.mCalled = false;
                                fragment.onDestroy();
                                if (!fragment.mCalled) {
                                    throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onDestroy()");
                                }
                            }
                            fragment.mCalled = false;
                            fragment.onDetach();
                            if (!fragment.mCalled) {
                                throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onDetach()");
                            }
                            if (!fragment.mRetaining) {
                                this.makeInactive(fragment);
                                break;
                            }
                            fragment.mActivity = null;
                            fragment.mFragmentManager = null;
                            break;
                        }
                        case 5: {
                            if (mState >= 5) {
                                break Label_1306;
                            }
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "movefrom RESUMED: " + fragment);
                            }
                            fragment.mCalled = false;
                            fragment.onPause();
                            if (!fragment.mCalled) {
                                throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onPause()");
                            }
                            fragment.mResumed = false;
                            break Label_1306;
                        }
                        case 4: {
                            if (mState >= 4) {
                                break Label_1306;
                            }
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "movefrom STARTED: " + fragment);
                            }
                            fragment.mCalled = false;
                            fragment.performStop();
                            if (!fragment.mCalled) {
                                throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onStop()");
                            }
                            break Label_1306;
                        }
                        case 3: {
                            if (mState < 3) {
                                if (FragmentManagerImpl.DEBUG) {
                                    Log.v("FragmentManager", "movefrom STOPPED: " + fragment);
                                }
                                fragment.performReallyStop();
                            }
                        }
                        case 2: {
                            if (mState >= 2) {
                                continue;
                            }
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "movefrom ACTIVITY_CREATED: " + fragment);
                            }
                            if (fragment.mView != null && !this.mActivity.isFinishing() && fragment.mSavedViewState == null) {
                                this.saveFragmentViewState(fragment);
                            }
                            fragment.mCalled = false;
                            fragment.performDestroyView();
                            if (!fragment.mCalled) {
                                throw new SuperNotCalledException("Fragment " + fragment + " did not call through to super.onDestroyView()");
                            }
                            if (fragment.mView != null && fragment.mContainer != null) {
                                final int mCurState = this.mCurState;
                                Animation loadAnimation2 = null;
                                if (mCurState > 0) {
                                    final boolean mDestroyed = this.mDestroyed;
                                    loadAnimation2 = null;
                                    if (!mDestroyed) {
                                        loadAnimation2 = this.loadAnimation(fragment, n, false, n2);
                                    }
                                }
                                if (loadAnimation2 != null) {
                                    fragment.mAnimatingAway = fragment.mView;
                                    fragment.mStateAfterAnimating = mState;
                                    loadAnimation2.setAnimationListener((Animation$AnimationListener)new Animation$AnimationListener() {
                                        public void onAnimationEnd(final Animation animation) {
                                            if (fragment.mAnimatingAway != null) {
                                                fragment.mAnimatingAway = null;
                                                FragmentManagerImpl.this.moveToState(fragment, fragment.mStateAfterAnimating, 0, 0);
                                            }
                                        }
                                        
                                        public void onAnimationRepeat(final Animation animation) {
                                        }
                                        
                                        public void onAnimationStart(final Animation animation) {
                                        }
                                    });
                                    fragment.mView.startAnimation(loadAnimation2);
                                }
                                fragment.mContainer.removeView(fragment.mView);
                            }
                            fragment.mContainer = null;
                            fragment.mView = null;
                            fragment.mInnerView = null;
                            continue;
                        }
                    }
                }
                break;
            }
        }
        fragment.mState = mState;
    }
    
    public void noteStateNotSaved() {
        this.mStateSaved = false;
    }
    
    public void performPendingDeferredStart(final Fragment fragment) {
        if (fragment.mDeferStart) {
            if (!this.mExecutingActions) {
                fragment.mDeferStart = false;
                this.moveToState(fragment, this.mCurState, 0, 0);
                return;
            }
            this.mHavePendingDeferredStart = true;
        }
    }
    
    @Override
    public void popBackStack() {
        this.enqueueAction(new Runnable() {
            @Override
            public void run() {
                FragmentManagerImpl.this.popBackStackState(FragmentManagerImpl.this.mActivity.mHandler, null, -1, 0);
            }
        }, false);
    }
    
    @Override
    public void popBackStack(final int n, final int n2) {
        if (n < 0) {
            throw new IllegalArgumentException("Bad id: " + n);
        }
        this.enqueueAction(new Runnable() {
            @Override
            public void run() {
                FragmentManagerImpl.this.popBackStackState(FragmentManagerImpl.this.mActivity.mHandler, null, n, n2);
            }
        }, false);
    }
    
    @Override
    public void popBackStack(final String s, final int n) {
        this.enqueueAction(new Runnable() {
            @Override
            public void run() {
                FragmentManagerImpl.this.popBackStackState(FragmentManagerImpl.this.mActivity.mHandler, s, -1, n);
            }
        }, false);
    }
    
    @Override
    public boolean popBackStackImmediate() {
        this.checkStateLoss();
        this.executePendingTransactions();
        return this.popBackStackState(this.mActivity.mHandler, null, -1, 0);
    }
    
    @Override
    public boolean popBackStackImmediate(final int n, final int n2) {
        this.checkStateLoss();
        this.executePendingTransactions();
        if (n < 0) {
            throw new IllegalArgumentException("Bad id: " + n);
        }
        return this.popBackStackState(this.mActivity.mHandler, null, n, n2);
    }
    
    @Override
    public boolean popBackStackImmediate(final String s, final int n) {
        this.checkStateLoss();
        this.executePendingTransactions();
        return this.popBackStackState(this.mActivity.mHandler, s, -1, n);
    }
    
    boolean popBackStackState(final Handler handler, final String s, final int n, final int n2) {
        if (this.mBackStack != null) {
            if (s == null && n < 0 && (n2 & 0x1) == 0x0) {
                final int n3 = -1 + this.mBackStack.size();
                if (n3 < 0) {
                    return false;
                }
                this.mBackStack.remove(n3).popFromBackStack(true);
                this.reportBackStackChanged();
            }
            else {
                int i = -1;
                if (s != null || n >= 0) {
                    for (i = -1 + this.mBackStack.size(); i >= 0; --i) {
                        final BackStackRecord backStackRecord = this.mBackStack.get(i);
                        if ((s != null && s.equals(backStackRecord.getName())) || (n >= 0 && n == backStackRecord.mIndex)) {
                            break;
                        }
                    }
                    if (i < 0) {
                        return false;
                    }
                    if ((n2 & 0x1) != 0x0) {
                        --i;
                        while (i >= 0) {
                            final BackStackRecord backStackRecord2 = this.mBackStack.get(i);
                            if ((s == null || !s.equals(backStackRecord2.getName())) && (n < 0 || n != backStackRecord2.mIndex)) {
                                break;
                            }
                            --i;
                        }
                    }
                }
                if (i == -1 + this.mBackStack.size()) {
                    return false;
                }
                final ArrayList<BackStackRecord> list = new ArrayList<BackStackRecord>();
                for (int j = -1 + this.mBackStack.size(); j > i; --j) {
                    list.add(this.mBackStack.remove(j));
                }
                for (int n4 = -1 + list.size(), k = 0; k <= n4; ++k) {
                    if (FragmentManagerImpl.DEBUG) {
                        Log.v("FragmentManager", "Popping back stack state: " + list.get(k));
                    }
                    list.get(k).popFromBackStack(k == n4);
                }
                this.reportBackStackChanged();
            }
            return true;
        }
        return false;
    }
    
    @Override
    public void putFragment(final Bundle bundle, final String s, final Fragment fragment) {
        if (fragment.mIndex < 0) {
            throw new IllegalStateException("Fragment " + fragment + " is not currently in the FragmentManager");
        }
        bundle.putInt(s, fragment.mIndex);
    }
    
    public void removeFragment(final Fragment fragment, final int n, final int n2) {
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "remove: " + fragment + " nesting=" + fragment.mBackStackNesting);
        }
        boolean b;
        if (!fragment.isInBackStack()) {
            b = true;
        }
        else {
            b = false;
        }
        if (!fragment.mDetached || b) {
            this.mAdded.remove(fragment);
            if (fragment.mHasMenu && fragment.mMenuVisible) {
                this.mNeedMenuInvalidate = true;
            }
            fragment.mAdded = false;
            fragment.mRemoving = true;
            int n3 = 0;
            if (!b) {
                n3 = 1;
            }
            this.moveToState(fragment, n3, n, n2);
        }
    }
    
    @Override
    public void removeOnBackStackChangedListener(final OnBackStackChangedListener onBackStackChangedListener) {
        if (this.mBackStackChangeListeners != null) {
            this.mBackStackChangeListeners.remove(onBackStackChangedListener);
        }
    }
    
    void reportBackStackChanged() {
        if (this.mBackStackChangeListeners != null) {
            for (int i = 0; i < this.mBackStackChangeListeners.size(); ++i) {
                this.mBackStackChangeListeners.get(i).onBackStackChanged();
            }
        }
    }
    
    void restoreAllState(final Parcelable parcelable, final ArrayList<Fragment> list) {
        if (parcelable != null) {
            final FragmentManagerState fragmentManagerState = (FragmentManagerState)parcelable;
            if (fragmentManagerState.mActive != null) {
                if (list != null) {
                    for (int i = 0; i < list.size(); ++i) {
                        final Fragment mInstance = list.get(i);
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "restoreAllState: re-attaching retained " + mInstance);
                        }
                        final FragmentState fragmentState = fragmentManagerState.mActive[mInstance.mIndex];
                        fragmentState.mInstance = mInstance;
                        mInstance.mSavedViewState = null;
                        mInstance.mBackStackNesting = 0;
                        mInstance.mInLayout = false;
                        mInstance.mAdded = false;
                        mInstance.mTarget = null;
                        if (fragmentState.mSavedFragmentState != null) {
                            fragmentState.mSavedFragmentState.setClassLoader(this.mActivity.getClassLoader());
                            mInstance.mSavedViewState = (SparseArray<Parcelable>)fragmentState.mSavedFragmentState.getSparseParcelableArray("android:view_state");
                        }
                    }
                }
                this.mActive = new ArrayList<Fragment>(fragmentManagerState.mActive.length);
                if (this.mAvailIndices != null) {
                    this.mAvailIndices.clear();
                }
                for (int j = 0; j < fragmentManagerState.mActive.length; ++j) {
                    final FragmentState fragmentState2 = fragmentManagerState.mActive[j];
                    if (fragmentState2 != null) {
                        final Fragment instantiate = fragmentState2.instantiate(this.mActivity);
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "restoreAllState: adding #" + j + ": " + instantiate);
                        }
                        this.mActive.add(instantiate);
                        fragmentState2.mInstance = null;
                    }
                    else {
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "restoreAllState: adding #" + j + ": (null)");
                        }
                        this.mActive.add(null);
                        if (this.mAvailIndices == null) {
                            this.mAvailIndices = new ArrayList<Integer>();
                        }
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "restoreAllState: adding avail #" + j);
                        }
                        this.mAvailIndices.add(j);
                    }
                }
                if (list != null) {
                    for (int k = 0; k < list.size(); ++k) {
                        final Fragment fragment = list.get(k);
                        if (fragment.mTargetIndex >= 0) {
                            if (fragment.mTargetIndex < this.mActive.size()) {
                                fragment.mTarget = this.mActive.get(fragment.mTargetIndex);
                            }
                            else {
                                Log.w("FragmentManager", "Re-attaching retained fragment " + fragment + " target no longer exists: " + fragment.mTargetIndex);
                                fragment.mTarget = null;
                            }
                        }
                    }
                }
                if (fragmentManagerState.mAdded != null) {
                    this.mAdded = new ArrayList<Fragment>(fragmentManagerState.mAdded.length);
                    for (int l = 0; l < fragmentManagerState.mAdded.length; ++l) {
                        final Fragment fragment2 = this.mActive.get(fragmentManagerState.mAdded[l]);
                        if (fragment2 == null) {
                            throw new IllegalStateException("No instantiated fragment for index #" + fragmentManagerState.mAdded[l]);
                        }
                        fragment2.mAdded = true;
                        if (FragmentManagerImpl.DEBUG) {
                            Log.v("FragmentManager", "restoreAllState: making added #" + l + ": " + fragment2);
                        }
                        this.mAdded.add(fragment2);
                    }
                }
                else {
                    this.mAdded = null;
                }
                if (fragmentManagerState.mBackStack == null) {
                    this.mBackStack = null;
                    return;
                }
                this.mBackStack = new ArrayList<BackStackRecord>(fragmentManagerState.mBackStack.length);
                for (int n = 0; n < fragmentManagerState.mBackStack.length; ++n) {
                    final BackStackRecord instantiate2 = fragmentManagerState.mBackStack[n].instantiate(this);
                    if (FragmentManagerImpl.DEBUG) {
                        Log.v("FragmentManager", "restoreAllState: adding bse #" + n + " (index " + instantiate2.mIndex + "): " + instantiate2);
                    }
                    this.mBackStack.add(instantiate2);
                    if (instantiate2.mIndex >= 0) {
                        this.setBackStackIndex(instantiate2.mIndex, instantiate2);
                    }
                }
            }
        }
    }
    
    ArrayList<Fragment> retainNonConfig() {
        final ArrayList<Fragment> mActive = this.mActive;
        ArrayList<Fragment> list = null;
        if (mActive != null) {
            for (int i = 0; i < this.mActive.size(); ++i) {
                final Fragment fragment = this.mActive.get(i);
                if (fragment != null && fragment.mRetainInstance) {
                    if (list == null) {
                        list = new ArrayList<Fragment>();
                    }
                    list.add(fragment);
                    fragment.mRetaining = true;
                    int mIndex;
                    if (fragment.mTarget != null) {
                        mIndex = fragment.mTarget.mIndex;
                    }
                    else {
                        mIndex = -1;
                    }
                    fragment.mTargetIndex = mIndex;
                }
            }
        }
        return list;
    }
    
    Parcelable saveAllState() {
        this.execPendingActions();
        if (FragmentManagerImpl.HONEYCOMB) {
            this.mStateSaved = true;
        }
        if (this.mActive != null && this.mActive.size() > 0) {
            final int size = this.mActive.size();
            final FragmentState[] mActive = new FragmentState[size];
            boolean b = false;
            for (int i = 0; i < size; ++i) {
                final Fragment fragment = this.mActive.get(i);
                if (fragment != null) {
                    b = true;
                    final FragmentState fragmentState = new FragmentState(fragment);
                    mActive[i] = fragmentState;
                    if (fragment.mState > 0 && fragmentState.mSavedFragmentState == null) {
                        fragmentState.mSavedFragmentState = this.saveFragmentBasicState(fragment);
                        if (fragment.mTarget != null) {
                            if (fragment.mTarget.mIndex < 0) {
                                final String string = "Failure saving state: " + fragment + " has target not in fragment manager: " + fragment.mTarget;
                                Log.e("FragmentManager", string);
                                this.dump("  ", null, new PrintWriter(new LogWriter("FragmentManager")), new String[0]);
                                throw new IllegalStateException(string);
                            }
                            if (fragmentState.mSavedFragmentState == null) {
                                fragmentState.mSavedFragmentState = new Bundle();
                            }
                            this.putFragment(fragmentState.mSavedFragmentState, "android:target_state", fragment.mTarget);
                            if (fragment.mTargetRequestCode != 0) {
                                fragmentState.mSavedFragmentState.putInt("android:target_req_state", fragment.mTargetRequestCode);
                            }
                        }
                    }
                    else {
                        fragmentState.mSavedFragmentState = fragment.mSavedFragmentState;
                    }
                    if (FragmentManagerImpl.DEBUG) {
                        Log.v("FragmentManager", "Saved state of " + fragment + ": " + fragmentState.mSavedFragmentState);
                    }
                }
            }
            if (b) {
                final ArrayList<Fragment> mAdded = this.mAdded;
                int[] mAdded2 = null;
                if (mAdded != null) {
                    final int size2 = this.mAdded.size();
                    mAdded2 = null;
                    if (size2 > 0) {
                        mAdded2 = new int[size2];
                        for (int j = 0; j < size2; ++j) {
                            mAdded2[j] = this.mAdded.get(j).mIndex;
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "saveAllState: adding fragment #" + j + ": " + this.mAdded.get(j));
                            }
                        }
                    }
                }
                final ArrayList<BackStackRecord> mBackStack = this.mBackStack;
                BackStackState[] mBackStack2 = null;
                if (mBackStack != null) {
                    final int size3 = this.mBackStack.size();
                    mBackStack2 = null;
                    if (size3 > 0) {
                        mBackStack2 = new BackStackState[size3];
                        for (int k = 0; k < size3; ++k) {
                            mBackStack2[k] = new BackStackState(this, this.mBackStack.get(k));
                            if (FragmentManagerImpl.DEBUG) {
                                Log.v("FragmentManager", "saveAllState: adding back stack #" + k + ": " + this.mBackStack.get(k));
                            }
                        }
                    }
                }
                final FragmentManagerState fragmentManagerState = new FragmentManagerState();
                fragmentManagerState.mActive = mActive;
                fragmentManagerState.mAdded = mAdded2;
                fragmentManagerState.mBackStack = mBackStack2;
                return (Parcelable)fragmentManagerState;
            }
            if (FragmentManagerImpl.DEBUG) {
                Log.v("FragmentManager", "saveAllState: no fragments!");
                return null;
            }
        }
        return null;
    }
    
    Bundle saveFragmentBasicState(final Fragment fragment) {
        if (this.mStateBundle == null) {
            this.mStateBundle = new Bundle();
        }
        fragment.onSaveInstanceState(this.mStateBundle);
        final boolean empty = this.mStateBundle.isEmpty();
        Bundle mStateBundle = null;
        if (!empty) {
            mStateBundle = this.mStateBundle;
            this.mStateBundle = null;
        }
        if (fragment.mView != null) {
            this.saveFragmentViewState(fragment);
        }
        if (fragment.mSavedViewState != null) {
            if (mStateBundle == null) {
                mStateBundle = new Bundle();
            }
            mStateBundle.putSparseParcelableArray("android:view_state", (SparseArray)fragment.mSavedViewState);
        }
        if (!fragment.mUserVisibleHint) {
            mStateBundle.putBoolean("android:user_visible_hint", fragment.mUserVisibleHint);
        }
        return mStateBundle;
    }
    
    @Override
    public Fragment.SavedState saveFragmentInstanceState(final Fragment fragment) {
        if (fragment.mIndex < 0) {
            throw new IllegalStateException("Fragment " + fragment + " is not currently in the FragmentManager");
        }
        final int mState = fragment.mState;
        Fragment.SavedState savedState = null;
        if (mState > 0) {
            final Bundle saveFragmentBasicState = this.saveFragmentBasicState(fragment);
            savedState = null;
            if (saveFragmentBasicState != null) {
                savedState = new Fragment.SavedState(saveFragmentBasicState);
            }
        }
        return savedState;
    }
    
    void saveFragmentViewState(final Fragment fragment) {
        if (fragment.mInnerView != null) {
            if (this.mStateArray == null) {
                this.mStateArray = (SparseArray<Parcelable>)new SparseArray();
            }
            else {
                this.mStateArray.clear();
            }
            fragment.mInnerView.saveHierarchyState((SparseArray)this.mStateArray);
            if (this.mStateArray.size() > 0) {
                fragment.mSavedViewState = this.mStateArray;
                this.mStateArray = null;
            }
        }
    }
    
    public void setBackStackIndex(final int n, final BackStackRecord backStackRecord) {
        synchronized (this) {
            if (this.mBackStackIndices == null) {
                this.mBackStackIndices = new ArrayList<BackStackRecord>();
            }
            int i = this.mBackStackIndices.size();
            if (n < i) {
                if (FragmentManagerImpl.DEBUG) {
                    Log.v("FragmentManager", "Setting back stack index " + n + " to " + backStackRecord);
                }
                this.mBackStackIndices.set(n, backStackRecord);
            }
            else {
                while (i < n) {
                    this.mBackStackIndices.add(null);
                    if (this.mAvailBackStackIndices == null) {
                        this.mAvailBackStackIndices = new ArrayList<Integer>();
                    }
                    if (FragmentManagerImpl.DEBUG) {
                        Log.v("FragmentManager", "Adding available back stack index " + i);
                    }
                    this.mAvailBackStackIndices.add(i);
                    ++i;
                }
                if (FragmentManagerImpl.DEBUG) {
                    Log.v("FragmentManager", "Adding back stack index " + n + " with " + backStackRecord);
                }
                this.mBackStackIndices.add(backStackRecord);
            }
        }
    }
    
    public void showFragment(final Fragment fragment, final int n, final int n2) {
        if (FragmentManagerImpl.DEBUG) {
            Log.v("FragmentManager", "show: " + fragment);
        }
        if (fragment.mHidden) {
            fragment.mHidden = false;
            if (fragment.mView != null) {
                final Animation loadAnimation = this.loadAnimation(fragment, n, true, n2);
                if (loadAnimation != null) {
                    fragment.mView.startAnimation(loadAnimation);
                }
                fragment.mView.setVisibility(0);
            }
            if (fragment.mAdded && fragment.mHasMenu && fragment.mMenuVisible) {
                this.mNeedMenuInvalidate = true;
            }
            fragment.onHiddenChanged(false);
        }
    }
    
    void startPendingDeferredFragments() {
        if (this.mActive != null) {
            for (int i = 0; i < this.mActive.size(); ++i) {
                final Fragment fragment = this.mActive.get(i);
                if (fragment != null) {
                    this.performPendingDeferredStart(fragment);
                }
            }
        }
    }
    
    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder(128);
        sb.append("FragmentManager{");
        sb.append(Integer.toHexString(System.identityHashCode(this)));
        sb.append(" in ");
        DebugUtils.buildShortClassTag(this.mActivity, sb);
        sb.append("}}");
        return sb.toString();
    }
}
