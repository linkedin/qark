package com.actionbarsherlock.widget;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.database.DataSetObserver;
import android.graphics.drawable.Drawable;
import android.os.Build.VERSION;
import android.util.AttributeSet;
import android.util.DisplayMetrics;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.MeasureSpec;
import android.view.View.OnClickListener;
import android.view.View.OnLongClickListener;
import android.view.ViewGroup;
import android.view.ViewTreeObserver;
import android.view.ViewTreeObserver.OnGlobalLayoutListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.BaseAdapter;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.PopupWindow.OnDismissListener;
import android.widget.TextView;
import com.actionbarsherlock.R.dimen;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.R.layout;
import com.actionbarsherlock.R.string;
import com.actionbarsherlock.R.styleable;
import com.actionbarsherlock.internal.widget.IcsLinearLayout;
import com.actionbarsherlock.internal.widget.IcsListPopupWindow;
import com.actionbarsherlock.view.ActionProvider;

class ActivityChooserView
  extends ViewGroup
  implements ActivityChooserModel.ActivityChooserModelClient
{
  private static final boolean IS_HONEYCOMB;
  private final IcsLinearLayout mActivityChooserContent;
  private final Drawable mActivityChooserContentBackground;
  private final ActivityChooserViewAdapter mAdapter;
  private final Callbacks mCallbacks;
  private final Context mContext;
  private int mDefaultActionButtonContentDescription;
  private final FrameLayout mDefaultActivityButton;
  private final ImageView mDefaultActivityButtonImage;
  private final FrameLayout mExpandActivityOverflowButton;
  private final ImageView mExpandActivityOverflowButtonImage;
  private int mInitialActivityCount = 4;
  private boolean mIsAttachedToWindow;
  private boolean mIsSelectingDefaultActivity;
  private final int mListPopupMaxWidth;
  private IcsListPopupWindow mListPopupWindow;
  private final DataSetObserver mModelDataSetOberver = new DataSetObserver()
  {
    public void onChanged()
    {
      super.onChanged();
      ActivityChooserView.this.mAdapter.notifyDataSetChanged();
    }
    
    public void onInvalidated()
    {
      super.onInvalidated();
      ActivityChooserView.this.mAdapter.notifyDataSetInvalidated();
    }
  };
  private PopupWindow.OnDismissListener mOnDismissListener;
  private final ViewTreeObserver.OnGlobalLayoutListener mOnGlobalLayoutListener = new ViewTreeObserver.OnGlobalLayoutListener()
  {
    public void onGlobalLayout()
    {
      if (ActivityChooserView.this.isShowingPopup())
      {
        if (ActivityChooserView.this.isShown()) {
          break label31;
        }
        ActivityChooserView.this.getListPopupWindow().dismiss();
      }
      label31:
      do
      {
        return;
        ActivityChooserView.this.getListPopupWindow().show();
      } while (ActivityChooserView.this.mProvider == null);
      ActivityChooserView.this.mProvider.subUiVisibilityChanged(true);
    }
  };
  ActionProvider mProvider;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11) {}
    for (boolean bool = true;; bool = false)
    {
      IS_HONEYCOMB = bool;
      return;
    }
  }
  
  public ActivityChooserView(Context paramContext)
  {
    this(paramContext, null);
  }
  
  public ActivityChooserView(Context paramContext, AttributeSet paramAttributeSet)
  {
    this(paramContext, paramAttributeSet, 0);
  }
  
  public ActivityChooserView(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet, paramInt);
    this.mContext = paramContext;
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockActivityChooserView, paramInt, 0);
    this.mInitialActivityCount = localTypedArray.getInt(1, 4);
    Drawable localDrawable = localTypedArray.getDrawable(2);
    localTypedArray.recycle();
    LayoutInflater.from(this.mContext).inflate(R.layout.abs__activity_chooser_view, this, true);
    this.mCallbacks = new Callbacks(null);
    this.mActivityChooserContent = ((IcsLinearLayout)findViewById(R.id.abs__activity_chooser_view_content));
    this.mActivityChooserContentBackground = this.mActivityChooserContent.getBackground();
    this.mDefaultActivityButton = ((FrameLayout)findViewById(R.id.abs__default_activity_button));
    this.mDefaultActivityButton.setOnClickListener(this.mCallbacks);
    this.mDefaultActivityButton.setOnLongClickListener(this.mCallbacks);
    this.mDefaultActivityButtonImage = ((ImageView)this.mDefaultActivityButton.findViewById(R.id.abs__image));
    this.mExpandActivityOverflowButton = ((FrameLayout)findViewById(R.id.abs__expand_activities_button));
    this.mExpandActivityOverflowButton.setOnClickListener(this.mCallbacks);
    this.mExpandActivityOverflowButtonImage = ((ImageView)this.mExpandActivityOverflowButton.findViewById(R.id.abs__image));
    this.mExpandActivityOverflowButtonImage.setImageDrawable(localDrawable);
    this.mAdapter = new ActivityChooserViewAdapter(null);
    this.mAdapter.registerDataSetObserver(new DataSetObserver()
    {
      public void onChanged()
      {
        super.onChanged();
        ActivityChooserView.this.updateAppearance();
      }
    });
    Resources localResources = paramContext.getResources();
    this.mListPopupMaxWidth = Math.max(localResources.getDisplayMetrics().widthPixels / 2, localResources.getDimensionPixelSize(R.dimen.abs__config_prefDialogWidth));
  }
  
  private IcsListPopupWindow getListPopupWindow()
  {
    if (this.mListPopupWindow == null)
    {
      this.mListPopupWindow = new IcsListPopupWindow(getContext());
      this.mListPopupWindow.setAdapter(this.mAdapter);
      this.mListPopupWindow.setAnchorView(this);
      this.mListPopupWindow.setModal(true);
      this.mListPopupWindow.setOnItemClickListener(this.mCallbacks);
      this.mListPopupWindow.setOnDismissListener(this.mCallbacks);
    }
    return this.mListPopupWindow;
  }
  
  private void showPopupUnchecked(int paramInt)
  {
    if (this.mAdapter.getDataModel() == null) {
      throw new IllegalStateException("No data model. Did you call #setDataModel?");
    }
    getViewTreeObserver().addOnGlobalLayoutListener(this.mOnGlobalLayoutListener);
    boolean bool;
    int j;
    label59:
    label92:
    IcsListPopupWindow localIcsListPopupWindow;
    if (this.mDefaultActivityButton.getVisibility() == 0)
    {
      bool = true;
      int i = this.mAdapter.getActivityCount();
      if (!bool) {
        break label189;
      }
      j = 1;
      if ((paramInt == Integer.MAX_VALUE) || (i <= paramInt + j)) {
        break label195;
      }
      this.mAdapter.setShowFooterView(true);
      this.mAdapter.setMaxActivityCount(paramInt - 1);
      localIcsListPopupWindow = getListPopupWindow();
      if (!localIcsListPopupWindow.isShowing())
      {
        if ((!this.mIsSelectingDefaultActivity) && (bool)) {
          break label214;
        }
        this.mAdapter.setShowDefaultActivity(true, bool);
      }
    }
    for (;;)
    {
      localIcsListPopupWindow.setContentWidth(Math.min(this.mAdapter.measureContentWidth(), this.mListPopupMaxWidth));
      localIcsListPopupWindow.show();
      if (this.mProvider != null) {
        this.mProvider.subUiVisibilityChanged(true);
      }
      localIcsListPopupWindow.getListView().setContentDescription(this.mContext.getString(R.string.abs__activitychooserview_choose_application));
      return;
      bool = false;
      break;
      label189:
      j = 0;
      break label59;
      label195:
      this.mAdapter.setShowFooterView(false);
      this.mAdapter.setMaxActivityCount(paramInt);
      break label92;
      label214:
      this.mAdapter.setShowDefaultActivity(false, false);
    }
  }
  
  private void updateAppearance()
  {
    if (this.mAdapter.getCount() > 0)
    {
      this.mExpandActivityOverflowButton.setEnabled(true);
      int i = this.mAdapter.getActivityCount();
      int j = this.mAdapter.getHistorySize();
      if ((i <= 0) || (j <= 0)) {
        break label159;
      }
      this.mDefaultActivityButton.setVisibility(0);
      ResolveInfo localResolveInfo = this.mAdapter.getDefaultActivity();
      PackageManager localPackageManager = this.mContext.getPackageManager();
      this.mDefaultActivityButtonImage.setImageDrawable(localResolveInfo.loadIcon(localPackageManager));
      if (this.mDefaultActionButtonContentDescription != 0)
      {
        CharSequence localCharSequence = localResolveInfo.loadLabel(localPackageManager);
        String str = this.mContext.getString(this.mDefaultActionButtonContentDescription, new Object[] { localCharSequence });
        this.mDefaultActivityButton.setContentDescription(str);
      }
    }
    for (;;)
    {
      if (this.mDefaultActivityButton.getVisibility() != 0) {
        break label171;
      }
      this.mActivityChooserContent.setBackgroundDrawable(this.mActivityChooserContentBackground);
      return;
      this.mExpandActivityOverflowButton.setEnabled(false);
      break;
      label159:
      this.mDefaultActivityButton.setVisibility(8);
    }
    label171:
    this.mActivityChooserContent.setBackgroundDrawable(null);
  }
  
  public boolean dismissPopup()
  {
    if (isShowingPopup())
    {
      getListPopupWindow().dismiss();
      ViewTreeObserver localViewTreeObserver = getViewTreeObserver();
      if (localViewTreeObserver.isAlive()) {
        localViewTreeObserver.removeGlobalOnLayoutListener(this.mOnGlobalLayoutListener);
      }
    }
    return true;
  }
  
  public ActivityChooserModel getDataModel()
  {
    return this.mAdapter.getDataModel();
  }
  
  public boolean isShowingPopup()
  {
    return getListPopupWindow().isShowing();
  }
  
  protected void onAttachedToWindow()
  {
    super.onAttachedToWindow();
    ActivityChooserModel localActivityChooserModel = this.mAdapter.getDataModel();
    if (localActivityChooserModel != null) {
      localActivityChooserModel.registerObserver(this.mModelDataSetOberver);
    }
    this.mIsAttachedToWindow = true;
  }
  
  protected void onDetachedFromWindow()
  {
    super.onDetachedFromWindow();
    ActivityChooserModel localActivityChooserModel = this.mAdapter.getDataModel();
    if (localActivityChooserModel != null) {
      localActivityChooserModel.unregisterObserver(this.mModelDataSetOberver);
    }
    ViewTreeObserver localViewTreeObserver = getViewTreeObserver();
    if (localViewTreeObserver.isAlive()) {
      localViewTreeObserver.removeGlobalOnLayoutListener(this.mOnGlobalLayoutListener);
    }
    this.mIsAttachedToWindow = false;
  }
  
  protected void onLayout(boolean paramBoolean, int paramInt1, int paramInt2, int paramInt3, int paramInt4)
  {
    this.mActivityChooserContent.layout(0, 0, paramInt3 - paramInt1, paramInt4 - paramInt2);
    if (getListPopupWindow().isShowing())
    {
      showPopupUnchecked(this.mAdapter.getMaxActivityCount());
      return;
    }
    dismissPopup();
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    IcsLinearLayout localIcsLinearLayout = this.mActivityChooserContent;
    if (this.mDefaultActivityButton.getVisibility() != 0) {
      paramInt2 = View.MeasureSpec.makeMeasureSpec(View.MeasureSpec.getSize(paramInt2), 1073741824);
    }
    measureChild(localIcsLinearLayout, paramInt1, paramInt2);
    setMeasuredDimension(localIcsLinearLayout.getMeasuredWidth(), localIcsLinearLayout.getMeasuredHeight());
  }
  
  public void setActivityChooserModel(ActivityChooserModel paramActivityChooserModel)
  {
    this.mAdapter.setDataModel(paramActivityChooserModel);
    if (isShowingPopup())
    {
      dismissPopup();
      showPopup();
    }
  }
  
  public void setDefaultActionButtonContentDescription(int paramInt)
  {
    this.mDefaultActionButtonContentDescription = paramInt;
  }
  
  public void setExpandActivityOverflowButtonContentDescription(int paramInt)
  {
    String str = this.mContext.getString(paramInt);
    this.mExpandActivityOverflowButtonImage.setContentDescription(str);
  }
  
  public void setExpandActivityOverflowButtonDrawable(Drawable paramDrawable)
  {
    this.mExpandActivityOverflowButtonImage.setImageDrawable(paramDrawable);
  }
  
  public void setInitialActivityCount(int paramInt)
  {
    this.mInitialActivityCount = paramInt;
  }
  
  public void setOnDismissListener(PopupWindow.OnDismissListener paramOnDismissListener)
  {
    this.mOnDismissListener = paramOnDismissListener;
  }
  
  public void setProvider(ActionProvider paramActionProvider)
  {
    this.mProvider = paramActionProvider;
  }
  
  public boolean showPopup()
  {
    if ((isShowingPopup()) || (!this.mIsAttachedToWindow)) {
      return false;
    }
    this.mIsSelectingDefaultActivity = false;
    showPopupUnchecked(this.mInitialActivityCount);
    return true;
  }
  
  private class ActivityChooserViewAdapter
    extends BaseAdapter
  {
    private static final int ITEM_VIEW_TYPE_ACTIVITY = 0;
    private static final int ITEM_VIEW_TYPE_COUNT = 3;
    private static final int ITEM_VIEW_TYPE_FOOTER = 1;
    public static final int MAX_ACTIVITY_COUNT_DEFAULT = 4;
    public static final int MAX_ACTIVITY_COUNT_UNLIMITED = Integer.MAX_VALUE;
    private ActivityChooserModel mDataModel;
    private boolean mHighlightDefaultActivity;
    private int mMaxActivityCount = 4;
    private boolean mShowDefaultActivity;
    private boolean mShowFooterView;
    
    private ActivityChooserViewAdapter() {}
    
    public int getActivityCount()
    {
      return this.mDataModel.getActivityCount();
    }
    
    public int getCount()
    {
      int i = this.mDataModel.getActivityCount();
      if ((!this.mShowDefaultActivity) && (this.mDataModel.getDefaultActivity() != null)) {
        i--;
      }
      int j = Math.min(i, this.mMaxActivityCount);
      if (this.mShowFooterView) {
        j++;
      }
      return j;
    }
    
    public ActivityChooserModel getDataModel()
    {
      return this.mDataModel;
    }
    
    public ResolveInfo getDefaultActivity()
    {
      return this.mDataModel.getDefaultActivity();
    }
    
    public int getHistorySize()
    {
      return this.mDataModel.getHistorySize();
    }
    
    public Object getItem(int paramInt)
    {
      switch (getItemViewType(paramInt))
      {
      default: 
        throw new IllegalArgumentException();
      case 1: 
        return null;
      }
      if ((!this.mShowDefaultActivity) && (this.mDataModel.getDefaultActivity() != null)) {
        paramInt++;
      }
      return this.mDataModel.getActivity(paramInt);
    }
    
    public long getItemId(int paramInt)
    {
      return paramInt;
    }
    
    public int getItemViewType(int paramInt)
    {
      if ((this.mShowFooterView) && (paramInt == -1 + getCount())) {
        return 1;
      }
      return 0;
    }
    
    public int getMaxActivityCount()
    {
      return this.mMaxActivityCount;
    }
    
    public boolean getShowDefaultActivity()
    {
      return this.mShowDefaultActivity;
    }
    
    public View getView(int paramInt, View paramView, ViewGroup paramViewGroup)
    {
      switch (getItemViewType(paramInt))
      {
      default: 
        throw new IllegalArgumentException();
      case 1: 
        if ((paramView == null) || (paramView.getId() != 1))
        {
          paramView = LayoutInflater.from(ActivityChooserView.this.getContext()).inflate(R.layout.abs__activity_chooser_view_list_item, paramViewGroup, false);
          paramView.setId(1);
          ((TextView)paramView.findViewById(R.id.abs__title)).setText(ActivityChooserView.this.mContext.getString(R.string.abs__activity_chooser_view_see_all));
        }
        return paramView;
      }
      if ((paramView == null) || (paramView.getId() != R.id.abs__list_item)) {
        paramView = LayoutInflater.from(ActivityChooserView.this.getContext()).inflate(R.layout.abs__activity_chooser_view_list_item, paramViewGroup, false);
      }
      PackageManager localPackageManager = ActivityChooserView.this.mContext.getPackageManager();
      ImageView localImageView = (ImageView)paramView.findViewById(R.id.abs__icon);
      ResolveInfo localResolveInfo = (ResolveInfo)getItem(paramInt);
      localImageView.setImageDrawable(localResolveInfo.loadIcon(localPackageManager));
      ((TextView)paramView.findViewById(R.id.abs__title)).setText(localResolveInfo.loadLabel(localPackageManager));
      if (ActivityChooserView.IS_HONEYCOMB)
      {
        if ((!this.mShowDefaultActivity) || (paramInt != 0) || (!this.mHighlightDefaultActivity)) {
          break label230;
        }
        ActivityChooserView.SetActivated.invoke(paramView, true);
      }
      for (;;)
      {
        return paramView;
        label230:
        ActivityChooserView.SetActivated.invoke(paramView, false);
      }
    }
    
    public int getViewTypeCount()
    {
      return 3;
    }
    
    public int measureContentWidth()
    {
      int i = this.mMaxActivityCount;
      this.mMaxActivityCount = Integer.MAX_VALUE;
      int j = 0;
      View localView = null;
      int k = View.MeasureSpec.makeMeasureSpec(0, 0);
      int m = View.MeasureSpec.makeMeasureSpec(0, 0);
      int n = getCount();
      for (int i1 = 0;; i1++)
      {
        if (i1 >= n)
        {
          this.mMaxActivityCount = i;
          return j;
        }
        localView = getView(i1, localView, null);
        localView.measure(k, m);
        j = Math.max(j, localView.getMeasuredWidth());
      }
    }
    
    public void setDataModel(ActivityChooserModel paramActivityChooserModel)
    {
      ActivityChooserModel localActivityChooserModel = ActivityChooserView.this.mAdapter.getDataModel();
      if ((localActivityChooserModel != null) && (ActivityChooserView.this.isShown())) {
        localActivityChooserModel.unregisterObserver(ActivityChooserView.this.mModelDataSetOberver);
      }
      this.mDataModel = paramActivityChooserModel;
      if ((paramActivityChooserModel != null) && (ActivityChooserView.this.isShown())) {
        paramActivityChooserModel.registerObserver(ActivityChooserView.this.mModelDataSetOberver);
      }
      notifyDataSetChanged();
    }
    
    public void setMaxActivityCount(int paramInt)
    {
      if (this.mMaxActivityCount != paramInt)
      {
        this.mMaxActivityCount = paramInt;
        notifyDataSetChanged();
      }
    }
    
    public void setShowDefaultActivity(boolean paramBoolean1, boolean paramBoolean2)
    {
      if ((this.mShowDefaultActivity != paramBoolean1) || (this.mHighlightDefaultActivity != paramBoolean2))
      {
        this.mShowDefaultActivity = paramBoolean1;
        this.mHighlightDefaultActivity = paramBoolean2;
        notifyDataSetChanged();
      }
    }
    
    public void setShowFooterView(boolean paramBoolean)
    {
      if (this.mShowFooterView != paramBoolean)
      {
        this.mShowFooterView = paramBoolean;
        notifyDataSetChanged();
      }
    }
  }
  
  private class Callbacks
    implements AdapterView.OnItemClickListener, View.OnClickListener, View.OnLongClickListener, PopupWindow.OnDismissListener
  {
    private Callbacks() {}
    
    private void notifyOnDismissListener()
    {
      if (ActivityChooserView.this.mOnDismissListener != null) {
        ActivityChooserView.this.mOnDismissListener.onDismiss();
      }
    }
    
    public void onClick(View paramView)
    {
      if (paramView == ActivityChooserView.this.mDefaultActivityButton)
      {
        ActivityChooserView.this.dismissPopup();
        ResolveInfo localResolveInfo = ActivityChooserView.this.mAdapter.getDefaultActivity();
        int i = ActivityChooserView.this.mAdapter.getDataModel().getActivityIndex(localResolveInfo);
        Intent localIntent = ActivityChooserView.this.mAdapter.getDataModel().chooseActivity(i);
        if (localIntent != null) {
          ActivityChooserView.this.mContext.startActivity(localIntent);
        }
        return;
      }
      if (paramView == ActivityChooserView.this.mExpandActivityOverflowButton)
      {
        ActivityChooserView.this.mIsSelectingDefaultActivity = false;
        ActivityChooserView.this.showPopupUnchecked(ActivityChooserView.this.mInitialActivityCount);
        return;
      }
      throw new IllegalArgumentException();
    }
    
    public void onDismiss()
    {
      notifyOnDismissListener();
      if (ActivityChooserView.this.mProvider != null) {
        ActivityChooserView.this.mProvider.subUiVisibilityChanged(false);
      }
    }
    
    public void onItemClick(AdapterView<?> paramAdapterView, View paramView, int paramInt, long paramLong)
    {
      switch (((ActivityChooserView.ActivityChooserViewAdapter)paramAdapterView.getAdapter()).getItemViewType(paramInt))
      {
      default: 
        throw new IllegalArgumentException();
      case 1: 
        ActivityChooserView.this.showPopupUnchecked(Integer.MAX_VALUE);
      }
      do
      {
        return;
        ActivityChooserView.this.dismissPopup();
        if (!ActivityChooserView.this.mIsSelectingDefaultActivity) {
          break;
        }
      } while (paramInt <= 0);
      ActivityChooserView.this.mAdapter.getDataModel().setDefaultActivity(paramInt);
      return;
      if (ActivityChooserView.this.mAdapter.getShowDefaultActivity()) {}
      for (;;)
      {
        Intent localIntent = ActivityChooserView.this.mAdapter.getDataModel().chooseActivity(paramInt);
        if (localIntent == null) {
          break;
        }
        ActivityChooserView.this.mContext.startActivity(localIntent);
        return;
        paramInt++;
      }
    }
    
    public boolean onLongClick(View paramView)
    {
      if (paramView == ActivityChooserView.this.mDefaultActivityButton)
      {
        if (ActivityChooserView.this.mAdapter.getCount() > 0)
        {
          ActivityChooserView.this.mIsSelectingDefaultActivity = true;
          ActivityChooserView.this.showPopupUnchecked(ActivityChooserView.this.mInitialActivityCount);
        }
        return true;
      }
      throw new IllegalArgumentException();
    }
  }
  
  private static class SetActivated
  {
    private SetActivated() {}
    
    public static void invoke(View paramView, boolean paramBoolean)
    {
      paramView.setActivated(paramBoolean);
    }
  }
}
