package com.actionbarsherlock.internal.view.menu;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.ViewGroup.LayoutParams;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.RadioButton;
import android.widget.TextView;
import com.actionbarsherlock.R.id;
import com.actionbarsherlock.R.layout;
import com.actionbarsherlock.R.styleable;

public class ListMenuItemView
  extends LinearLayout
  implements MenuView.ItemView
{
  private Drawable mBackground;
  private CheckBox mCheckBox;
  final Context mContext;
  private boolean mForceShowIcon;
  private ImageView mIconView;
  private LayoutInflater mInflater;
  private MenuItemImpl mItemData;
  private boolean mPreserveIconSpacing;
  private RadioButton mRadioButton;
  private TextView mShortcutView;
  private int mTextAppearance;
  private Context mTextAppearanceContext;
  private TextView mTitleView;
  
  public ListMenuItemView(Context paramContext, AttributeSet paramAttributeSet)
  {
    this(paramContext, paramAttributeSet, 0);
  }
  
  public ListMenuItemView(Context paramContext, AttributeSet paramAttributeSet, int paramInt)
  {
    super(paramContext, paramAttributeSet);
    this.mContext = paramContext;
    TypedArray localTypedArray = paramContext.obtainStyledAttributes(paramAttributeSet, R.styleable.SherlockMenuView, paramInt, 0);
    this.mBackground = localTypedArray.getDrawable(4);
    this.mTextAppearance = localTypedArray.getResourceId(0, -1);
    this.mPreserveIconSpacing = localTypedArray.getBoolean(7, false);
    this.mTextAppearanceContext = paramContext;
    localTypedArray.recycle();
  }
  
  private LayoutInflater getInflater()
  {
    if (this.mInflater == null) {
      this.mInflater = LayoutInflater.from(this.mContext);
    }
    return this.mInflater;
  }
  
  private void insertCheckBox()
  {
    this.mCheckBox = ((CheckBox)getInflater().inflate(R.layout.abs__list_menu_item_checkbox, this, false));
    addView(this.mCheckBox);
  }
  
  private void insertIconView()
  {
    this.mIconView = ((ImageView)getInflater().inflate(R.layout.abs__list_menu_item_icon, this, false));
    addView(this.mIconView, 0);
  }
  
  private void insertRadioButton()
  {
    this.mRadioButton = ((RadioButton)getInflater().inflate(R.layout.abs__list_menu_item_radio, this, false));
    addView(this.mRadioButton);
  }
  
  public MenuItemImpl getItemData()
  {
    return this.mItemData;
  }
  
  public void initialize(MenuItemImpl paramMenuItemImpl, int paramInt)
  {
    this.mItemData = paramMenuItemImpl;
    if (paramMenuItemImpl.isVisible()) {}
    for (int i = 0;; i = 8)
    {
      setVisibility(i);
      setTitle(paramMenuItemImpl.getTitleForItemView(this));
      setCheckable(paramMenuItemImpl.isCheckable());
      setShortcut(paramMenuItemImpl.shouldShowShortcut(), paramMenuItemImpl.getShortcut());
      setIcon(paramMenuItemImpl.getIcon());
      setEnabled(paramMenuItemImpl.isEnabled());
      return;
    }
  }
  
  protected void onFinishInflate()
  {
    super.onFinishInflate();
    setBackgroundDrawable(this.mBackground);
    this.mTitleView = ((TextView)findViewById(R.id.abs__title));
    if (this.mTextAppearance != -1) {
      this.mTitleView.setTextAppearance(this.mTextAppearanceContext, this.mTextAppearance);
    }
    this.mShortcutView = ((TextView)findViewById(R.id.abs__shortcut));
  }
  
  protected void onMeasure(int paramInt1, int paramInt2)
  {
    if ((this.mIconView != null) && (this.mPreserveIconSpacing))
    {
      ViewGroup.LayoutParams localLayoutParams = getLayoutParams();
      LinearLayout.LayoutParams localLayoutParams1 = (LinearLayout.LayoutParams)this.mIconView.getLayoutParams();
      if ((localLayoutParams.height > 0) && (localLayoutParams1.width <= 0)) {
        localLayoutParams1.width = localLayoutParams.height;
      }
    }
    super.onMeasure(paramInt1, paramInt2);
  }
  
  public boolean prefersCondensedTitle()
  {
    return false;
  }
  
  public void setCheckable(boolean paramBoolean)
  {
    if ((!paramBoolean) && (this.mRadioButton == null) && (this.mCheckBox == null)) {
      return;
    }
    if (this.mRadioButton == null) {
      insertRadioButton();
    }
    if (this.mCheckBox == null) {
      insertCheckBox();
    }
    Object localObject1;
    Object localObject2;
    if (this.mItemData.isExclusiveCheckable())
    {
      localObject1 = this.mRadioButton;
      localObject2 = this.mCheckBox;
      label61:
      if (!paramBoolean) {
        break label134;
      }
      ((CompoundButton)localObject1).setChecked(this.mItemData.isChecked());
      if (!paramBoolean) {
        break label127;
      }
    }
    label127:
    for (int i = 0;; i = 8)
    {
      if (((CompoundButton)localObject1).getVisibility() != i) {
        ((CompoundButton)localObject1).setVisibility(i);
      }
      if (((CompoundButton)localObject2).getVisibility() == 8) {
        break;
      }
      ((CompoundButton)localObject2).setVisibility(8);
      return;
      localObject1 = this.mCheckBox;
      localObject2 = this.mRadioButton;
      break label61;
    }
    label134:
    this.mCheckBox.setVisibility(8);
    this.mRadioButton.setVisibility(8);
  }
  
  public void setChecked(boolean paramBoolean)
  {
    if (this.mItemData.isExclusiveCheckable()) {
      if (this.mRadioButton == null) {
        insertRadioButton();
      }
    }
    for (Object localObject = this.mRadioButton;; localObject = this.mCheckBox)
    {
      ((CompoundButton)localObject).setChecked(paramBoolean);
      return;
      if (this.mCheckBox == null) {
        insertCheckBox();
      }
    }
  }
  
  public void setForceShowIcon(boolean paramBoolean)
  {
    this.mForceShowIcon = paramBoolean;
    this.mPreserveIconSpacing = paramBoolean;
  }
  
  public void setIcon(Drawable paramDrawable)
  {
    int i;
    if ((!this.mItemData.shouldShowIcon()) && (!this.mForceShowIcon))
    {
      i = 0;
      if ((i != 0) || (this.mPreserveIconSpacing)) {
        break label36;
      }
    }
    label36:
    while ((this.mIconView == null) && (paramDrawable == null) && (!this.mPreserveIconSpacing))
    {
      return;
      i = 1;
      break;
    }
    if (this.mIconView == null) {
      insertIconView();
    }
    if ((paramDrawable != null) || (this.mPreserveIconSpacing))
    {
      ImageView localImageView = this.mIconView;
      if (i != 0) {}
      for (;;)
      {
        localImageView.setImageDrawable(paramDrawable);
        if (this.mIconView.getVisibility() == 0) {
          break;
        }
        this.mIconView.setVisibility(0);
        return;
        paramDrawable = null;
      }
    }
    this.mIconView.setVisibility(8);
  }
  
  public void setShortcut(boolean paramBoolean, char paramChar)
  {
    if ((paramBoolean) && (this.mItemData.shouldShowShortcut())) {}
    for (int i = 0;; i = 8)
    {
      if (i == 0) {
        this.mShortcutView.setText(this.mItemData.getShortcutLabel());
      }
      if (this.mShortcutView.getVisibility() != i) {
        this.mShortcutView.setVisibility(i);
      }
      return;
    }
  }
  
  public void setTitle(CharSequence paramCharSequence)
  {
    if (paramCharSequence != null)
    {
      this.mTitleView.setText(paramCharSequence);
      if (this.mTitleView.getVisibility() != 0) {
        this.mTitleView.setVisibility(0);
      }
    }
    while (this.mTitleView.getVisibility() == 8) {
      return;
    }
    this.mTitleView.setVisibility(8);
  }
  
  public boolean showsIcon()
  {
    return this.mForceShowIcon;
  }
}
