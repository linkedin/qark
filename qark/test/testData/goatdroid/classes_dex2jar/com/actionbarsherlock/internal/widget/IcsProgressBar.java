/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  android.content.res.TypedArray
 *  android.graphics.Bitmap
 *  android.graphics.BitmapShader
 *  android.graphics.Canvas
 *  android.graphics.Paint
 *  android.graphics.Rect
 *  android.graphics.RectF
 *  android.graphics.Shader
 *  android.graphics.Shader$TileMode
 *  android.graphics.drawable.Animatable
 *  android.graphics.drawable.AnimationDrawable
 *  android.graphics.drawable.BitmapDrawable
 *  android.graphics.drawable.ClipDrawable
 *  android.graphics.drawable.Drawable
 *  android.graphics.drawable.Drawable$Callback
 *  android.graphics.drawable.LayerDrawable
 *  android.graphics.drawable.ShapeDrawable
 *  android.graphics.drawable.shapes.RoundRectShape
 *  android.graphics.drawable.shapes.Shape
 *  android.os.Build
 *  android.os.Build$VERSION
 *  android.os.Parcel
 *  android.os.Parcelable
 *  android.os.Parcelable$Creator
 *  android.os.SystemClock
 *  android.util.AttributeSet
 *  android.view.View
 *  android.view.View$BaseSavedState
 *  android.view.ViewDebug
 *  android.view.ViewDebug$ExportedProperty
 *  android.view.accessibility.AccessibilityEvent
 *  android.view.accessibility.AccessibilityManager
 *  android.view.animation.AlphaAnimation
 *  android.view.animation.AnimationUtils
 *  android.view.animation.Interpolator
 *  android.view.animation.LinearInterpolator
 *  android.view.animation.Transformation
 *  android.widget.RemoteViews
 *  android.widget.RemoteViews$RemoteView
 */
package com.actionbarsherlock.internal.widget;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Bitmap;
import android.graphics.BitmapShader;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.graphics.Shader;
import android.graphics.drawable.Animatable;
import android.graphics.drawable.AnimationDrawable;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.ClipDrawable;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.LayerDrawable;
import android.graphics.drawable.ShapeDrawable;
import android.graphics.drawable.shapes.RoundRectShape;
import android.graphics.drawable.shapes.Shape;
import android.os.Build;
import android.os.Parcel;
import android.os.Parcelable;
import android.os.SystemClock;
import android.util.AttributeSet;
import android.view.View;
import android.view.ViewDebug;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityManager;
import android.view.animation.AlphaAnimation;
import android.view.animation.AnimationUtils;
import android.view.animation.Interpolator;
import android.view.animation.LinearInterpolator;
import android.view.animation.Transformation;
import android.widget.RemoteViews;

@RemoteViews.RemoteView
public class IcsProgressBar
extends View {
    private static final int ANIMATION_RESOLUTION = 200;
    private static final boolean IS_HONEYCOMB = false;
    private static final int MAX_LEVEL = 10000;
    private static final int[] ProgressBar;
    private static final int ProgressBar_animationResolution = 14;
    private static final int ProgressBar_indeterminate = 5;
    private static final int ProgressBar_indeterminateBehavior = 10;
    private static final int ProgressBar_indeterminateDrawable = 7;
    private static final int ProgressBar_indeterminateDuration = 9;
    private static final int ProgressBar_indeterminateOnly = 6;
    private static final int ProgressBar_interpolator = 13;
    private static final int ProgressBar_max = 2;
    private static final int ProgressBar_maxHeight = 1;
    private static final int ProgressBar_maxWidth = 0;
    private static final int ProgressBar_minHeight = 12;
    private static final int ProgressBar_minWidth = 11;
    private static final int ProgressBar_progress = 3;
    private static final int ProgressBar_progressDrawable = 8;
    private static final int ProgressBar_secondaryProgress = 4;
    private static final int TIMEOUT_SEND_ACCESSIBILITY_EVENT = 200;
    private AccessibilityEventSender mAccessibilityEventSender;
    private AccessibilityManager mAccessibilityManager;
    private AlphaAnimation mAnimation;
    private int mAnimationResolution;
    private int mBehavior;
    private Drawable mCurrentDrawable;
    private int mDuration;
    private boolean mInDrawing;
    private boolean mIndeterminate;
    private Drawable mIndeterminateDrawable;
    private int mIndeterminateRealLeft;
    private int mIndeterminateRealTop;
    private Interpolator mInterpolator;
    private long mLastDrawTime;
    private int mMax;
    int mMaxHeight;
    int mMaxWidth;
    int mMinHeight;
    int mMinWidth;
    private boolean mNoInvalidate;
    private boolean mOnlyIndeterminate;
    private int mProgress;
    private Drawable mProgressDrawable;
    private RefreshProgressRunnable mRefreshProgressRunnable;
    Bitmap mSampleTile;
    private int mSecondaryProgress;
    private boolean mShouldStartAnimationDrawable;
    private Transformation mTransformation;
    private long mUiThreadId;

    /*
     * Enabled aggressive block sorting
     */
    static {
        boolean bl = Build.VERSION.SDK_INT >= 11;
        IS_HONEYCOMB = bl;
        ProgressBar = new int[]{16843039, 16843040, 16843062, 16843063, 16843064, 16843065, 16843066, 16843067, 16843068, 16843069, 16843070, 16843071, 16843072, 16843073, 16843546};
    }

    public IcsProgressBar(Context context) {
        this(context, null);
    }

    public IcsProgressBar(Context context, AttributeSet attributeSet) {
        this(context, attributeSet, 16842871);
    }

    public IcsProgressBar(Context context, AttributeSet attributeSet, int n) {
        this(context, attributeSet, n, 0);
    }

    /*
     * Enabled aggressive block sorting
     */
    public IcsProgressBar(Context context, AttributeSet attributeSet, int n, int n2) {
        boolean bl;
        TypedArray typedArray;
        block5 : {
            super(context, attributeSet, n);
            this.mUiThreadId = Thread.currentThread().getId();
            this.initProgressBar();
            typedArray = context.obtainStyledAttributes(attributeSet, ProgressBar, n, n2);
            this.mNoInvalidate = true;
            Drawable drawable2 = typedArray.getDrawable(8);
            if (drawable2 != null) {
                this.setProgressDrawable(this.tileify(drawable2, false));
            }
            this.mDuration = typedArray.getInt(9, this.mDuration);
            this.mMinWidth = typedArray.getDimensionPixelSize(11, this.mMinWidth);
            this.mMaxWidth = typedArray.getDimensionPixelSize(0, this.mMaxWidth);
            this.mMinHeight = typedArray.getDimensionPixelSize(12, this.mMinHeight);
            this.mMaxHeight = typedArray.getDimensionPixelSize(1, this.mMaxHeight);
            this.mBehavior = typedArray.getInt(10, this.mBehavior);
            int n3 = typedArray.getResourceId(13, 17432587);
            if (n3 > 0) {
                this.setInterpolator(context, n3);
            }
            this.setMax(typedArray.getInt(2, this.mMax));
            this.setProgress(typedArray.getInt(3, this.mProgress));
            this.setSecondaryProgress(typedArray.getInt(4, this.mSecondaryProgress));
            Drawable drawable3 = typedArray.getDrawable(7);
            if (drawable3 != null) {
                this.setIndeterminateDrawable(this.tileifyIndeterminate(drawable3));
            }
            this.mOnlyIndeterminate = typedArray.getBoolean(6, this.mOnlyIndeterminate);
            this.mNoInvalidate = false;
            if (!this.mOnlyIndeterminate) {
                boolean bl2 = typedArray.getBoolean(5, this.mIndeterminate);
                bl = false;
                if (!bl2) break block5;
            }
            bl = true;
        }
        this.setIndeterminate(bl);
        this.mAnimationResolution = typedArray.getInteger(14, 200);
        typedArray.recycle();
        this.mAccessibilityManager = (AccessibilityManager)context.getSystemService("accessibility");
    }

    static /* synthetic */ void access$1(IcsProgressBar icsProgressBar, RefreshProgressRunnable refreshProgressRunnable) {
        icsProgressBar.mRefreshProgressRunnable = refreshProgressRunnable;
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private void doRefreshProgress(int n, int n2, boolean bl, boolean bl2) {
        synchronized (this) {
            float f = this.mMax > 0 ? (float)n2 / (float)this.mMax : 0.0f;
            Drawable drawable2 = this.mCurrentDrawable;
            if (drawable2 == null) {
                this.invalidate();
            } else {
                boolean bl3 = drawable2 instanceof LayerDrawable;
                Drawable drawable3 = null;
                if (bl3) {
                    drawable3 = ((LayerDrawable)drawable2).findDrawableByLayerId(n);
                }
                int n3 = (int)(10000.0f * f);
                if (drawable3 == null) {
                    drawable3 = drawable2;
                }
                drawable3.setLevel(n3);
            }
            if (bl2 && n == 16908301) {
                this.onProgressRefresh(f, bl);
            }
            return;
        }
    }

    private void initProgressBar() {
        this.mMax = 100;
        this.mProgress = 0;
        this.mSecondaryProgress = 0;
        this.mIndeterminate = false;
        this.mOnlyIndeterminate = false;
        this.mDuration = 4000;
        this.mBehavior = 1;
        this.mMinWidth = 24;
        this.mMaxWidth = 48;
        this.mMinHeight = 24;
        this.mMaxHeight = 48;
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private void refreshProgress(int n, int n2, boolean bl) {
        synchronized (this) {
            if (this.mUiThreadId == Thread.currentThread().getId()) {
                this.doRefreshProgress(n, n2, bl, true);
            } else {
                RefreshProgressRunnable refreshProgressRunnable;
                if (this.mRefreshProgressRunnable != null) {
                    refreshProgressRunnable = this.mRefreshProgressRunnable;
                    this.mRefreshProgressRunnable = null;
                    refreshProgressRunnable.setup(n, n2, bl);
                } else {
                    refreshProgressRunnable = new RefreshProgressRunnable(n, n2, bl);
                }
                this.post((Runnable)refreshProgressRunnable);
            }
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     */
    private void scheduleAccessibilityEventSender() {
        if (this.mAccessibilityEventSender == null) {
            this.mAccessibilityEventSender = new AccessibilityEventSender();
        } else {
            this.removeCallbacks((Runnable)this.mAccessibilityEventSender);
        }
        this.postDelayed((Runnable)this.mAccessibilityEventSender, 200);
    }

    /*
     * Enabled aggressive block sorting
     */
    private Drawable tileify(Drawable drawable2, boolean bl) {
        if (!(drawable2 instanceof LayerDrawable)) {
            if (!(drawable2 instanceof BitmapDrawable)) {
                return drawable2;
            }
            Bitmap bitmap = ((BitmapDrawable)drawable2).getBitmap();
            if (this.mSampleTile == null) {
                this.mSampleTile = bitmap;
            }
            ShapeDrawable shapeDrawable = new ShapeDrawable(this.getDrawableShape());
            BitmapShader bitmapShader = new BitmapShader(bitmap, Shader.TileMode.REPEAT, Shader.TileMode.CLAMP);
            shapeDrawable.getPaint().setShader((Shader)bitmapShader);
            if (!bl) return shapeDrawable;
            return new ClipDrawable((Drawable)shapeDrawable, 3, 1);
        }
        LayerDrawable layerDrawable = (LayerDrawable)drawable2;
        int n = layerDrawable.getNumberOfLayers();
        Drawable[] arrdrawable = new Drawable[n];
        int n2 = 0;
        do {
            if (n2 >= n) break;
            int n3 = layerDrawable.getId(n2);
            Drawable drawable3 = layerDrawable.getDrawable(n2);
            boolean bl2 = n3 == 16908301 || n3 == 16908303;
            arrdrawable[n2] = this.tileify(drawable3, bl2);
            ++n2;
        } while (true);
        LayerDrawable layerDrawable2 = new LayerDrawable(arrdrawable);
        int n4 = 0;
        while (n4 < n) {
            layerDrawable2.setId(n4, layerDrawable.getId(n4));
            ++n4;
        }
        return layerDrawable2;
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    private Drawable tileifyIndeterminate(Drawable drawable2) {
        if (!(drawable2 instanceof AnimationDrawable)) return drawable2;
        AnimationDrawable animationDrawable = (AnimationDrawable)drawable2;
        int n = animationDrawable.getNumberOfFrames();
        AnimationDrawable animationDrawable2 = new AnimationDrawable();
        animationDrawable2.setOneShot(animationDrawable.isOneShot());
        int n2 = 0;
        do {
            if (n2 >= n) {
                animationDrawable2.setLevel(10000);
                return animationDrawable2;
            }
            Drawable drawable3 = this.tileify(animationDrawable.getFrame(n2), true);
            drawable3.setLevel(10000);
            animationDrawable2.addFrame(drawable3, animationDrawable.getDuration(n2));
            ++n2;
        } while (true);
    }

    /*
     * Enabled aggressive block sorting
     */
    private void updateDrawableBounds(int n, int n2) {
        int n3 = n - this.getPaddingRight() - this.getPaddingLeft();
        int n4 = n2 - this.getPaddingBottom() - this.getPaddingTop();
        if (this.mIndeterminateDrawable != null) {
            boolean bl = this.mOnlyIndeterminate;
            int n5 = 0;
            int n6 = 0;
            if (bl) {
                boolean bl2 = this.mIndeterminateDrawable instanceof AnimationDrawable;
                n5 = 0;
                n6 = 0;
                if (!bl2) {
                    int n7 = this.mIndeterminateDrawable.getIntrinsicWidth();
                    int n8 = this.mIndeterminateDrawable.getIntrinsicHeight();
                    float f = (float)n7 / (float)n8;
                    float f2 = (float)n / (float)n2;
                    float f3 = f FCMPL f2;
                    n5 = 0;
                    n6 = 0;
                    if (f3 != false) {
                        if (f2 > f) {
                            int n9 = (int)(f * (float)n2);
                            n5 = (n - n9) / 2;
                            n3 = n5 + n9;
                        } else {
                            int n10 = (int)((float)n * (1.0f / f));
                            n6 = (n2 - n10) / 2;
                            n4 = n6 + n10;
                            n5 = 0;
                        }
                    }
                }
            }
            this.mIndeterminateDrawable.setBounds(0, 0, n3 - n5, n4 - n6);
            this.mIndeterminateRealLeft = n5;
            this.mIndeterminateRealTop = n6;
        }
        if (this.mProgressDrawable != null) {
            this.mProgressDrawable.setBounds(0, 0, n3, n4);
        }
    }

    private void updateDrawableState() {
        int[] arrn = this.getDrawableState();
        if (this.mProgressDrawable != null && this.mProgressDrawable.isStateful()) {
            this.mProgressDrawable.setState(arrn);
        }
        if (this.mIndeterminateDrawable != null && this.mIndeterminateDrawable.isStateful()) {
            this.mIndeterminateDrawable.setState(arrn);
        }
    }

    protected void drawableStateChanged() {
        super.drawableStateChanged();
        this.updateDrawableState();
    }

    Drawable getCurrentDrawable() {
        return this.mCurrentDrawable;
    }

    Shape getDrawableShape() {
        return new RoundRectShape(new float[]{5.0f, 5.0f, 5.0f, 5.0f, 5.0f, 5.0f, 5.0f, 5.0f}, null, null);
    }

    public Drawable getIndeterminateDrawable() {
        return this.mIndeterminateDrawable;
    }

    public Interpolator getInterpolator() {
        return this.mInterpolator;
    }

    @ViewDebug.ExportedProperty(category="progress")
    public int getMax() {
        synchronized (this) {
            int n = this.mMax;
            return n;
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    @ViewDebug.ExportedProperty(category="progress")
    public int getProgress() {
        synchronized (this) {
            block6 : {
                boolean bl = this.mIndeterminate;
                if (!bl) break block6;
                return 0;
            }
            int n = this.mProgress;
            return n;
        }
    }

    public Drawable getProgressDrawable() {
        return this.mProgressDrawable;
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    @ViewDebug.ExportedProperty(category="progress")
    public int getSecondaryProgress() {
        synchronized (this) {
            block6 : {
                boolean bl = this.mIndeterminate;
                if (!bl) break block6;
                return 0;
            }
            int n = this.mSecondaryProgress;
            return n;
        }
    }

    public final void incrementProgressBy(int n) {
        synchronized (this) {
            this.setProgress(n + this.mProgress);
            return;
        }
    }

    public final void incrementSecondaryProgressBy(int n) {
        synchronized (this) {
            this.setSecondaryProgress(n + this.mSecondaryProgress);
            return;
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    public void invalidateDrawable(Drawable drawable2) {
        if (this.mInDrawing) return;
        if (this.verifyDrawable(drawable2)) {
            Rect rect = drawable2.getBounds();
            int n = this.getScrollX() + this.getPaddingLeft();
            int n2 = this.getScrollY() + this.getPaddingTop();
            this.invalidate(n + rect.left, n2 + rect.top, n + rect.right, n2 + rect.bottom);
            return;
        }
        super.invalidateDrawable(drawable2);
    }

    @ViewDebug.ExportedProperty(category="progress")
    public boolean isIndeterminate() {
        synchronized (this) {
            boolean bl = this.mIndeterminate;
            return bl;
        }
    }

    public void jumpDrawablesToCurrentState() {
        super.jumpDrawablesToCurrentState();
        if (this.mProgressDrawable != null) {
            this.mProgressDrawable.jumpToCurrentState();
        }
        if (this.mIndeterminateDrawable != null) {
            this.mIndeterminateDrawable.jumpToCurrentState();
        }
    }

    protected void onAttachedToWindow() {
        super.onAttachedToWindow();
        if (this.mIndeterminate) {
            this.startAnimation();
        }
    }

    protected void onDetachedFromWindow() {
        if (this.mIndeterminate) {
            this.stopAnimation();
        }
        if (this.mRefreshProgressRunnable != null) {
            this.removeCallbacks((Runnable)this.mRefreshProgressRunnable);
        }
        if (this.mAccessibilityEventSender != null) {
            this.removeCallbacks((Runnable)this.mAccessibilityEventSender);
        }
        super.onDetachedFromWindow();
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    protected void onDraw(Canvas canvas) {
        synchronized (this) {
            super.onDraw(canvas);
            Drawable drawable2 = this.mCurrentDrawable;
            if (drawable2 != null) {
                block9 : {
                    canvas.save();
                    canvas.translate((float)(this.getPaddingLeft() + this.mIndeterminateRealLeft), (float)(this.getPaddingTop() + this.mIndeterminateRealTop));
                    long l = this.getDrawingTime();
                    if (this.mAnimation != null) {
                        this.mAnimation.getTransformation(l, this.mTransformation);
                        float f = this.mTransformation.getAlpha();
                        this.mInDrawing = true;
                        drawable2.setLevel((int)(10000.0f * f));
                        if (SystemClock.uptimeMillis() - this.mLastDrawTime < (long)this.mAnimationResolution) break block9;
                        this.mLastDrawTime = SystemClock.uptimeMillis();
                        this.postInvalidateDelayed((long)this.mAnimationResolution);
                    }
                }
                drawable2.draw(canvas);
                canvas.restore();
                if (this.mShouldStartAnimationDrawable && drawable2 instanceof Animatable) {
                    ((Animatable)drawable2).start();
                    this.mShouldStartAnimationDrawable = false;
                }
            }
            return;
            finally {
                this.mInDrawing = false;
            }
        }
    }

    public void onInitializeAccessibilityEvent(AccessibilityEvent accessibilityEvent) {
        super.onInitializeAccessibilityEvent(accessibilityEvent);
        accessibilityEvent.setItemCount(this.mMax);
        accessibilityEvent.setCurrentItemIndex(this.mProgress);
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    protected void onMeasure(int n, int n2) {
        synchronized (this) {
            Drawable drawable2 = this.mCurrentDrawable;
            int n3 = 0;
            int n4 = 0;
            if (drawable2 != null) {
                n4 = Math.max(this.mMinWidth, Math.min(this.mMaxWidth, drawable2.getIntrinsicWidth()));
                n3 = Math.max(this.mMinHeight, Math.min(this.mMaxHeight, drawable2.getIntrinsicHeight()));
            }
            this.updateDrawableState();
            int n5 = n4 + (this.getPaddingLeft() + this.getPaddingRight());
            int n6 = n3 + (this.getPaddingTop() + this.getPaddingBottom());
            if (IS_HONEYCOMB) {
                this.setMeasuredDimension(View.resolveSizeAndState((int)n5, (int)n, (int)0), View.resolveSizeAndState((int)n6, (int)n2, (int)0));
            } else {
                this.setMeasuredDimension(View.resolveSize((int)n5, (int)n), View.resolveSize((int)n6, (int)n2));
            }
            return;
        }
    }

    void onProgressRefresh(float f, boolean bl) {
        if (this.mAccessibilityManager.isEnabled()) {
            this.scheduleAccessibilityEventSender();
        }
    }

    public void onRestoreInstanceState(Parcelable parcelable) {
        SavedState savedState = (SavedState)parcelable;
        super.onRestoreInstanceState(savedState.getSuperState());
        this.setProgress(savedState.progress);
        this.setSecondaryProgress(savedState.secondaryProgress);
    }

    public Parcelable onSaveInstanceState() {
        SavedState savedState = new SavedState(super.onSaveInstanceState());
        savedState.progress = this.mProgress;
        savedState.secondaryProgress = this.mSecondaryProgress;
        return savedState;
    }

    protected void onSizeChanged(int n, int n2, int n3, int n4) {
        this.updateDrawableBounds(n, n2);
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    protected void onVisibilityChanged(View view, int n) {
        super.onVisibilityChanged(view, n);
        if (!this.mIndeterminate) return;
        if (n == 8 || n == 4) {
            this.stopAnimation();
            return;
        }
        this.startAnimation();
    }

    public void postInvalidate() {
        if (!this.mNoInvalidate) {
            super.postInvalidate();
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void setIndeterminate(boolean bl) {
        synchronized (this) {
            if (!(this.mOnlyIndeterminate && this.mIndeterminate || bl == this.mIndeterminate)) {
                this.mIndeterminate = bl;
                if (bl) {
                    this.mCurrentDrawable = this.mIndeterminateDrawable;
                    this.startAnimation();
                } else {
                    this.mCurrentDrawable = this.mProgressDrawable;
                    this.stopAnimation();
                }
            }
            return;
        }
    }

    public void setIndeterminateDrawable(Drawable drawable2) {
        if (drawable2 != null) {
            drawable2.setCallback((Drawable.Callback)this);
        }
        this.mIndeterminateDrawable = drawable2;
        if (this.mIndeterminate) {
            this.mCurrentDrawable = drawable2;
            this.postInvalidate();
        }
    }

    public void setInterpolator(Context context, int n) {
        this.setInterpolator(AnimationUtils.loadInterpolator((Context)context, (int)n));
    }

    public void setInterpolator(Interpolator interpolator) {
        this.mInterpolator = interpolator;
    }

    public void setMax(int n) {
        synchronized (this) {
            if (n < 0) {
                n = 0;
            }
            if (n != this.mMax) {
                this.mMax = n;
                this.postInvalidate();
                if (this.mProgress > n) {
                    this.mProgress = n;
                }
                this.refreshProgress(16908301, this.mProgress, false);
            }
            return;
        }
    }

    public void setProgress(int n) {
        synchronized (this) {
            this.setProgress(n, false);
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    void setProgress(int n, boolean bl) {
        synchronized (this) {
            boolean bl2 = this.mIndeterminate;
            if (!bl2) {
                if (n < 0) {
                    n = 0;
                }
                if (n > this.mMax) {
                    n = this.mMax;
                }
                if (n != this.mProgress) {
                    this.mProgress = n;
                    this.refreshProgress(16908301, this.mProgress, bl);
                }
            }
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     */
    public void setProgressDrawable(Drawable drawable2) {
        boolean bl;
        if (this.mProgressDrawable != null && drawable2 != this.mProgressDrawable) {
            this.mProgressDrawable.setCallback(null);
            bl = true;
        } else {
            bl = false;
        }
        if (drawable2 != null) {
            drawable2.setCallback((Drawable.Callback)this);
            int n = drawable2.getMinimumHeight();
            if (this.mMaxHeight < n) {
                this.mMaxHeight = n;
                this.requestLayout();
            }
        }
        this.mProgressDrawable = drawable2;
        if (!this.mIndeterminate) {
            this.mCurrentDrawable = drawable2;
            this.postInvalidate();
        }
        if (bl) {
            this.updateDrawableBounds(this.getWidth(), this.getHeight());
            this.updateDrawableState();
            this.doRefreshProgress(16908301, this.mProgress, false, false);
            this.doRefreshProgress(16908303, this.mSecondaryProgress, false, false);
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void setSecondaryProgress(int n) {
        synchronized (this) {
            boolean bl = this.mIndeterminate;
            if (!bl) {
                if (n < 0) {
                    n = 0;
                }
                if (n > this.mMax) {
                    n = this.mMax;
                }
                if (n != this.mSecondaryProgress) {
                    this.mSecondaryProgress = n;
                    this.refreshProgress(16908303, this.mSecondaryProgress, false);
                }
            }
            return;
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    public void setVisibility(int n) {
        if (this.getVisibility() == n) return;
        super.setVisibility(n);
        if (!this.mIndeterminate) return;
        if (n == 8 || n == 4) {
            this.stopAnimation();
            return;
        }
        this.startAnimation();
    }

    /*
     * Enabled aggressive block sorting
     */
    void startAnimation() {
        if (this.getVisibility() != 0) {
            return;
        }
        if (this.mIndeterminateDrawable instanceof Animatable) {
            this.mShouldStartAnimationDrawable = true;
            this.mAnimation = null;
        } else {
            if (this.mInterpolator == null) {
                this.mInterpolator = new LinearInterpolator();
            }
            this.mTransformation = new Transformation();
            this.mAnimation = new AlphaAnimation(0.0f, 1.0f);
            this.mAnimation.setRepeatMode(this.mBehavior);
            this.mAnimation.setRepeatCount(-1);
            this.mAnimation.setDuration((long)this.mDuration);
            this.mAnimation.setInterpolator(this.mInterpolator);
            this.mAnimation.setStartTime(-1);
        }
        this.postInvalidate();
    }

    void stopAnimation() {
        this.mAnimation = null;
        this.mTransformation = null;
        if (this.mIndeterminateDrawable instanceof Animatable) {
            ((Animatable)this.mIndeterminateDrawable).stop();
            this.mShouldStartAnimationDrawable = false;
        }
        this.postInvalidate();
    }

    protected boolean verifyDrawable(Drawable drawable2) {
        if (drawable2 != this.mProgressDrawable && drawable2 != this.mIndeterminateDrawable && !super.verifyDrawable(drawable2)) {
            return false;
        }
        return true;
    }

    private class RefreshProgressRunnable
    implements Runnable {
        private boolean mFromUser;
        private int mId;
        private int mProgress;

        RefreshProgressRunnable(int n, int n2, boolean bl) {
            this.mId = n;
            this.mProgress = n2;
            this.mFromUser = bl;
        }

        @Override
        public void run() {
            IcsProgressBar.this.doRefreshProgress(this.mId, this.mProgress, this.mFromUser, true);
            IcsProgressBar.access$1(IcsProgressBar.this, this);
        }

        public void setup(int n, int n2, boolean bl) {
            this.mId = n;
            this.mProgress = n2;
            this.mFromUser = bl;
        }
    }

}

