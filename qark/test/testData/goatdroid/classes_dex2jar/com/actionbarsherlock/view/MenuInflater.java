/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  android.content.res.Resources
 *  android.content.res.TypedArray
 *  android.content.res.XmlResourceParser
 *  android.util.AttributeSet
 *  android.util.Log
 *  android.util.TypedValue
 *  android.util.Xml
 *  android.view.InflateException
 *  android.view.View
 *  org.xmlpull.v1.XmlPullParser
 *  org.xmlpull.v1.XmlPullParserException
 */
package com.actionbarsherlock.view;

import android.content.Context;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.content.res.XmlResourceParser;
import android.util.AttributeSet;
import android.util.Log;
import android.util.TypedValue;
import android.util.Xml;
import android.view.InflateException;
import android.view.View;
import com.actionbarsherlock.R;
import com.actionbarsherlock.internal.view.menu.MenuItemImpl;
import com.actionbarsherlock.view.ActionProvider;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuItem;
import com.actionbarsherlock.view.SubMenu;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import org.xmlpull.v1.XmlPullParser;
import org.xmlpull.v1.XmlPullParserException;

public class MenuInflater {
    private static final Class<?>[] ACTION_PROVIDER_CONSTRUCTOR_SIGNATURE = MenuInflater.ACTION_VIEW_CONSTRUCTOR_SIGNATURE = new Class[]{Context.class};
    private static final Class<?>[] ACTION_VIEW_CONSTRUCTOR_SIGNATURE;
    private static final String LOG_TAG = "MenuInflater";
    private static final int NO_ID = 0;
    private static final String XML_GROUP = "group";
    private static final String XML_ITEM = "item";
    private static final String XML_MENU = "menu";
    private final Object[] mActionProviderConstructorArguments;
    private final Object[] mActionViewConstructorArguments;
    private Context mContext;

    public MenuInflater(Context context) {
        this.mContext = context;
        this.mActionProviderConstructorArguments = this.mActionViewConstructorArguments = new Object[]{context};
    }

    static /* synthetic */ Class[] access$1() {
        return ACTION_PROVIDER_CONSTRUCTOR_SIGNATURE;
    }

    static /* synthetic */ Object[] access$2(MenuInflater menuInflater) {
        return menuInflater.mActionProviderConstructorArguments;
    }

    /*
     * Unable to fully structure code
     * Enabled aggressive block sorting
     * Lifted jumps to return sites
     */
    private void parseMenu(XmlPullParser var1_1, AttributeSet var2_2, Menu var3_3) throws XmlPullParserException, IOException {
        var4_4 = new MenuState(var3_3);
        var5_5 = var1_1.getEventType();
        var6_6 = false;
        var7_7 = null;
        do {
            if (var5_5 != 2) continue;
            var12_8 = var1_1.getName();
            if (var12_8.equals("menu") == false) throw new RuntimeException("Expecting menu, got " + var12_8);
            var5_5 = var1_1.next();
            break;
        } while ((var5_5 = var1_1.next()) != 1);
        var8_9 = false;
        block6 : do {
            if (var8_9) {
                return;
            }
            switch (var5_5) {
                case 2: {
                    if (!var6_6) {
                        var11_11 = var1_1.getName();
                        if (var11_11.equals("group")) {
                            var4_4.readGroup(var2_2);
                            ** break;
                        }
                        if (var11_11.equals("item")) {
                            var4_4.readItem(var2_2);
                            ** break;
                        }
                        if (var11_11.equals("menu")) {
                            this.parseMenu(var1_1, var2_2, var4_4.addSubMenuItem());
                            ** break;
                        }
                        var6_6 = true;
                        var7_7 = var11_11;
                        ** break;
                    }
                    ** GOTO lbl52
                }
                case 3: {
                    var9_10 = var1_1.getName();
                    if (var6_6 && var9_10.equals(var7_7)) {
                        var6_6 = false;
                        var7_7 = null;
                        ** break;
                    }
                    if (var9_10.equals("group")) {
                        var4_4.resetGroup();
                        ** break;
                    }
                    if (!var9_10.equals("item")) ** GOTO lbl50
                    if (!var4_4.hasAddedItem()) {
                        if (MenuState.access$0(var4_4) != null && MenuState.access$0(var4_4).hasSubMenu()) {
                            var4_4.addSubMenuItem();
                            ** break;
                        }
                        var4_4.addItem();
                        ** break;
                    }
                    ** GOTO lbl52
lbl50: // 1 sources:
                    if (var9_10.equals("menu")) {
                        var8_9 = true;
                    }
                }
lbl52: // 14 sources:
                default: {
                    var5_5 = var1_1.next();
                    continue block6;
                }
                case 1: 
            }
            break;
        } while (true);
        throw new RuntimeException("Unexpected end of document");
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void inflate(int n, Menu menu2) {
        XmlResourceParser xmlResourceParser = null;
        try {
            xmlResourceParser = this.mContext.getResources().getLayout(n);
            this.parseMenu((XmlPullParser)xmlResourceParser, Xml.asAttributeSet((XmlPullParser)xmlResourceParser), menu2);
            return;
        }
        catch (XmlPullParserException var6_4) {
            throw new InflateException("Error inflating menu XML", (Throwable)var6_4);
        }
        catch (IOException var4_6) {
            throw new InflateException("Error inflating menu XML", (Throwable)var4_6);
        }
        finally {
            if (xmlResourceParser != null) {
                xmlResourceParser.close();
            }
        }
    }

    private static class InflatedOnMenuItemClickListener
    implements MenuItem.OnMenuItemClickListener {
        private static final Class<?>[] PARAM_TYPES = new Class[]{MenuItem.class};
        private Context mContext;
        private Method mMethod;

        public InflatedOnMenuItemClickListener(Context context, String string2) {
            this.mContext = context;
            Class class_ = context.getClass();
            try {
                this.mMethod = class_.getMethod(string2, PARAM_TYPES);
                return;
            }
            catch (Exception var4_4) {
                InflateException inflateException = new InflateException("Couldn't resolve menu item onClick handler " + string2 + " in class " + class_.getName());
                inflateException.initCause((Throwable)var4_4);
                throw inflateException;
            }
        }

        @Override
        public boolean onMenuItemClick(MenuItem menuItem) {
            try {
                if (this.mMethod.getReturnType() == Boolean.TYPE) {
                    return (Boolean)this.mMethod.invoke((Object)this.mContext, menuItem);
                }
                this.mMethod.invoke((Object)this.mContext, menuItem);
                return true;
            }
            catch (Exception var2_2) {
                throw new RuntimeException(var2_2);
            }
        }
    }

    private class MenuState {
        private static final int defaultGroupId = 0;
        private static final int defaultItemCategory = 0;
        private static final int defaultItemCheckable = 0;
        private static final boolean defaultItemChecked = false;
        private static final boolean defaultItemEnabled = true;
        private static final int defaultItemId = 0;
        private static final int defaultItemOrder = 0;
        private static final boolean defaultItemVisible = true;
        private int groupCategory;
        private int groupCheckable;
        private boolean groupEnabled;
        private int groupId;
        private int groupOrder;
        private boolean groupVisible;
        private ActionProvider itemActionProvider;
        private String itemActionProviderClassName;
        private String itemActionViewClassName;
        private int itemActionViewLayout;
        private boolean itemAdded;
        private char itemAlphabeticShortcut;
        private int itemCategoryOrder;
        private int itemCheckable;
        private boolean itemChecked;
        private boolean itemEnabled;
        private int itemIconResId;
        private int itemId;
        private String itemListenerMethodName;
        private char itemNumericShortcut;
        private int itemShowAsAction;
        private CharSequence itemTitle;
        private CharSequence itemTitleCondensed;
        private boolean itemVisible;
        private Menu menu;

        public MenuState(Menu menu2) {
            this.menu = menu2;
            this.resetGroup();
        }

        static /* synthetic */ ActionProvider access$0(MenuState menuState) {
            return menuState.itemActionProvider;
        }

        private char getShortcut(String string2) {
            if (string2 == null) {
                return '\u0000';
            }
            return string2.charAt(0);
        }

        private <T> T newInstance(String string2, Class<?>[] arrclass, Object[] arrobject) {
            Object obj;
            try {
                obj = MenuInflater.this.mContext.getClassLoader().loadClass(string2).getConstructor(arrclass).newInstance(arrobject);
            }
            catch (Exception var4_5) {
                Log.w((String)"MenuInflater", (String)("Cannot instantiate class: " + string2), (Throwable)var4_5);
                return null;
            }
            return (T)obj;
        }

        /*
         * Enabled aggressive block sorting
         */
        private void setItem(MenuItem menuItem) {
            MenuItem menuItem2 = menuItem.setChecked(this.itemChecked).setVisible(this.itemVisible).setEnabled(this.itemEnabled);
            boolean bl = this.itemCheckable >= 1;
            menuItem2.setCheckable(bl).setTitleCondensed(this.itemTitleCondensed).setIcon(this.itemIconResId).setAlphabeticShortcut(this.itemAlphabeticShortcut).setNumericShortcut(this.itemNumericShortcut);
            if (this.itemShowAsAction >= 0) {
                menuItem.setShowAsAction(this.itemShowAsAction);
            }
            if (this.itemListenerMethodName != null) {
                if (MenuInflater.this.mContext.isRestricted()) {
                    throw new IllegalStateException("The android:onClick attribute cannot be used within a restricted context");
                }
                menuItem.setOnMenuItemClickListener(new InflatedOnMenuItemClickListener(MenuInflater.this.mContext, this.itemListenerMethodName));
            }
            if (this.itemCheckable >= 2) {
                if (menuItem instanceof MenuItemImpl) {
                    ((MenuItemImpl)menuItem).setExclusiveCheckable(true);
                } else {
                    this.menu.setGroupCheckable(this.groupId, true, true);
                }
            }
            String string2 = this.itemActionViewClassName;
            boolean bl2 = false;
            if (string2 != null) {
                menuItem.setActionView((View)this.newInstance(this.itemActionViewClassName, ACTION_VIEW_CONSTRUCTOR_SIGNATURE, MenuInflater.this.mActionViewConstructorArguments));
                bl2 = true;
            }
            if (this.itemActionViewLayout > 0) {
                if (!bl2) {
                    menuItem.setActionView(this.itemActionViewLayout);
                } else {
                    Log.w((String)"MenuInflater", (String)"Ignoring attribute 'itemActionViewLayout'. Action view already specified.");
                }
            }
            if (this.itemActionProvider != null) {
                menuItem.setActionProvider(this.itemActionProvider);
            }
        }

        public void addItem() {
            this.itemAdded = true;
            this.setItem(this.menu.add(this.groupId, this.itemId, this.itemCategoryOrder, this.itemTitle));
        }

        public SubMenu addSubMenuItem() {
            this.itemAdded = true;
            SubMenu subMenu = this.menu.addSubMenu(this.groupId, this.itemId, this.itemCategoryOrder, this.itemTitle);
            this.setItem(subMenu.getItem());
            return subMenu;
        }

        public boolean hasAddedItem() {
            return this.itemAdded;
        }

        public void readGroup(AttributeSet attributeSet) {
            TypedArray typedArray = MenuInflater.this.mContext.obtainStyledAttributes(attributeSet, R.styleable.SherlockMenuGroup);
            this.groupId = typedArray.getResourceId(1, 0);
            this.groupCategory = typedArray.getInt(3, 0);
            this.groupOrder = typedArray.getInt(4, 0);
            this.groupCheckable = typedArray.getInt(5, 0);
            this.groupVisible = typedArray.getBoolean(2, true);
            this.groupEnabled = typedArray.getBoolean(0, true);
            typedArray.recycle();
        }

        /*
         * Unable to fully structure code
         * Enabled aggressive block sorting
         * Lifted jumps to return sites
         */
        public void readItem(AttributeSet var1_1) {
            var2_2 = MenuInflater.access$0(MenuInflater.this).obtainStyledAttributes(var1_1, R.styleable.SherlockMenuItem);
            this.itemId = var2_2.getResourceId(2, 0);
            var3_3 = var2_2.getInt(5, this.groupCategory);
            var4_4 = var2_2.getInt(6, this.groupOrder);
            this.itemCategoryOrder = -65536 & var3_3 | 65535 & var4_4;
            this.itemTitle = var2_2.getText(7);
            this.itemTitleCondensed = var2_2.getText(8);
            this.itemIconResId = var2_2.getResourceId(0, 0);
            this.itemAlphabeticShortcut = this.getShortcut(var2_2.getString(9));
            this.itemNumericShortcut = this.getShortcut(var2_2.getString(10));
            if (var2_2.hasValue(11)) {
                var10_5 = var2_2.getBoolean(11, false) != false ? 1 : 0;
                this.itemCheckable = var10_5;
            } else {
                this.itemCheckable = this.groupCheckable;
            }
            this.itemChecked = var2_2.getBoolean(3, false);
            this.itemVisible = var2_2.getBoolean(4, this.groupVisible);
            this.itemEnabled = var2_2.getBoolean(1, this.groupEnabled);
            var5_6 = new TypedValue();
            var2_2.getValue(13, var5_6);
            var7_7 = var5_6.type == 17 ? var5_6.data : -1;
            this.itemShowAsAction = var7_7;
            this.itemListenerMethodName = var2_2.getString(12);
            this.itemActionViewLayout = var2_2.getResourceId(14, 0);
            this.itemActionViewClassName = var2_2.getString(15);
            this.itemActionProviderClassName = var2_2.getString(16);
            var8_8 = this.itemActionProviderClassName != null;
            if (!var8_8) ** GOTO lbl-1000
            if (this.itemActionViewLayout == 0) {
                ** if (this.itemActionViewClassName != null) goto lbl-1000
lbl-1000: // 1 sources:
                {
                    this.itemActionProvider = (ActionProvider)this.newInstance((String)this.itemActionProviderClassName, MenuInflater.access$1(), (Object[])MenuInflater.access$2((MenuInflater)MenuInflater.this));
                    ** GOTO lbl37
                }
            }
            ** GOTO lbl-1000
lbl-1000: // 2 sources:
            {
                if (var8_8) lbl-1000: // 2 sources:
                {
                    Log.w((String)"MenuInflater", (String)"Ignoring attribute 'actionProviderClass'. Action view already specified.");
                }
                this.itemActionProvider = null;
            }
lbl37: // 2 sources:
            var2_2.recycle();
            this.itemAdded = false;
        }

        public void resetGroup() {
            this.groupId = 0;
            this.groupCategory = 0;
            this.groupOrder = 0;
            this.groupCheckable = 0;
            this.groupVisible = true;
            this.groupEnabled = true;
        }
    }

}

