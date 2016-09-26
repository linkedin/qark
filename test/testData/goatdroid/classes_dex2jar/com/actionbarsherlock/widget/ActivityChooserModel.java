/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.ComponentName
 *  android.content.Context
 *  android.content.Intent
 *  android.content.pm.ActivityInfo
 *  android.content.pm.PackageManager
 *  android.content.pm.ResolveInfo
 *  android.database.DataSetObservable
 *  android.os.Handler
 *  android.text.TextUtils
 */
package com.actionbarsherlock.widget;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.database.DataSetObservable;
import android.os.Handler;
import android.text.TextUtils;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executor;

class ActivityChooserModel
extends DataSetObservable {
    private static final String ATTRIBUTE_ACTIVITY = "activity";
    private static final String ATTRIBUTE_TIME = "time";
    private static final String ATTRIBUTE_WEIGHT = "weight";
    private static final boolean DEBUG = false;
    private static final int DEFAULT_ACTIVITY_INFLATION = 5;
    private static final float DEFAULT_HISTORICAL_RECORD_WEIGHT = 1.0f;
    public static final String DEFAULT_HISTORY_FILE_NAME = "activity_choser_model_history.xml";
    public static final int DEFAULT_HISTORY_MAX_LENGTH = 50;
    private static final String HISTORY_FILE_EXTENSION = ".xml";
    private static final int INVALID_INDEX = -1;
    private static final String LOG_TAG = ActivityChooserModel.class.getSimpleName();
    private static final SerialExecutor SERIAL_EXECUTOR;
    private static final String TAG_HISTORICAL_RECORD = "historical-record";
    private static final String TAG_HISTORICAL_RECORDS = "historical-records";
    private static final Map<String, ActivityChooserModel> sDataModelRegistry;
    private static final Object sRegistryLock;
    private final List<ActivityResolveInfo> mActivites = new ArrayList<ActivityResolveInfo>();
    private OnChooseActivityListener mActivityChoserModelPolicy;
    private ActivitySorter mActivitySorter;
    private boolean mCanReadHistoricalData;
    private final Context mContext;
    private final Handler mHandler;
    private final List<HistoricalRecord> mHistoricalRecords = new ArrayList<HistoricalRecord>();
    private boolean mHistoricalRecordsChanged;
    private final String mHistoryFileName;
    private int mHistoryMaxSize;
    private final Object mInstanceLock = new Object();
    private Intent mIntent;
    private boolean mReadShareHistoryCalled;

    static {
        sRegistryLock = new Object();
        sDataModelRegistry = new HashMap<String, ActivityChooserModel>();
        SERIAL_EXECUTOR = new SerialExecutor();
    }

    private ActivityChooserModel(Context context, String string2) {
        this.mActivitySorter = new DefaultSorter();
        this.mHistoryMaxSize = 50;
        this.mCanReadHistoricalData = true;
        this.mReadShareHistoryCalled = false;
        this.mHistoricalRecordsChanged = true;
        this.mHandler = new Handler();
        this.mContext = context.getApplicationContext();
        if (!TextUtils.isEmpty((CharSequence)string2) && !string2.endsWith(".xml")) {
            this.mHistoryFileName = String.valueOf(string2) + ".xml";
            return;
        }
        this.mHistoryFileName = string2;
    }

    static /* synthetic */ Context access$0(ActivityChooserModel activityChooserModel) {
        return activityChooserModel.mContext;
    }

    static /* synthetic */ String access$1(ActivityChooserModel activityChooserModel) {
        return activityChooserModel.mHistoryFileName;
    }

    static /* synthetic */ Object access$2(ActivityChooserModel activityChooserModel) {
        return activityChooserModel.mInstanceLock;
    }

    static /* synthetic */ List access$3(ActivityChooserModel activityChooserModel) {
        return activityChooserModel.mHistoricalRecords;
    }

    static /* synthetic */ void access$4(ActivityChooserModel activityChooserModel, boolean bl) {
        activityChooserModel.mHistoricalRecordsChanged = bl;
    }

    static /* synthetic */ Handler access$5(ActivityChooserModel activityChooserModel) {
        return activityChooserModel.mHandler;
    }

    static /* synthetic */ String access$8() {
        return LOG_TAG;
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private boolean addHisoricalRecord(HistoricalRecord historicalRecord) {
        Object object = this.mInstanceLock;
        synchronized (object) {
            boolean bl = this.mHistoricalRecords.add(historicalRecord);
            if (bl) {
                this.mHistoricalRecordsChanged = true;
                this.pruneExcessiveHistoricalRecordsLocked();
                this.persistHistoricalData();
                this.sortActivities();
            }
            return bl;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public static ActivityChooserModel get(Context context, String string2) {
        Object object = sRegistryLock;
        synchronized (object) {
            ActivityChooserModel activityChooserModel = sDataModelRegistry.get(string2);
            if (activityChooserModel == null) {
                activityChooserModel = new ActivityChooserModel(context, string2);
                sDataModelRegistry.put(string2, activityChooserModel);
            }
            activityChooserModel.readHistoricalData();
            return activityChooserModel;
        }
    }

    private void loadActivitiesLocked() {
        this.mActivites.clear();
        if (this.mIntent != null) {
            List list = this.mContext.getPackageManager().queryIntentActivities(this.mIntent, 0);
            int n = list.size();
            int n2 = 0;
            do {
                if (n2 >= n) {
                    this.sortActivities();
                    return;
                }
                ResolveInfo resolveInfo = (ResolveInfo)list.get(n2);
                this.mActivites.add(new ActivityResolveInfo(resolveInfo));
                ++n2;
            } while (true);
        }
        this.notifyChanged();
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private void persistHistoricalData() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (!this.mReadShareHistoryCalled) {
                throw new IllegalStateException("No preceding call to #readHistoricalData");
            }
            if (!this.mHistoricalRecordsChanged) {
                return;
            }
            this.mHistoricalRecordsChanged = false;
            this.mCanReadHistoricalData = true;
            if (!TextUtils.isEmpty((CharSequence)this.mHistoryFileName)) {
                SERIAL_EXECUTOR.execute(new HistoryPersister());
            }
            return;
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    private void pruneExcessiveHistoricalRecordsLocked() {
        List<HistoricalRecord> list = this.mHistoricalRecords;
        int n = list.size() - this.mHistoryMaxSize;
        if (n <= 0) {
            return;
        }
        this.mHistoricalRecordsChanged = true;
        int n2 = 0;
        while (n2 < n) {
            list.remove(0);
            ++n2;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private void readHistoricalData() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (!this.mCanReadHistoricalData || !this.mHistoricalRecordsChanged) {
                return;
            }
            this.mCanReadHistoricalData = false;
            this.mReadShareHistoryCalled = true;
            if (!TextUtils.isEmpty((CharSequence)this.mHistoryFileName)) {
                SERIAL_EXECUTOR.execute(new HistoryLoader());
            }
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    private void sortActivities() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (this.mActivitySorter != null && !this.mActivites.isEmpty()) {
                this.mActivitySorter.sort(this.mIntent, this.mActivites, Collections.unmodifiableList(this.mHistoricalRecords));
                this.notifyChanged();
            }
            return;
        }
    }

    public Intent chooseActivity(int n) {
        Intent intent;
        ActivityResolveInfo activityResolveInfo = this.mActivites.get(n);
        ComponentName componentName = new ComponentName(activityResolveInfo.resolveInfo.activityInfo.packageName, activityResolveInfo.resolveInfo.activityInfo.name);
        Intent intent2 = new Intent(this.mIntent);
        intent2.setComponent(componentName);
        if (this.mActivityChoserModelPolicy != null && this.mActivityChoserModelPolicy.onChooseActivity(this, intent = new Intent(intent2))) {
            return null;
        }
        this.addHisoricalRecord(new HistoricalRecord(componentName, System.currentTimeMillis(), 1.0f));
        return intent2;
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public ResolveInfo getActivity(int n) {
        Object object = this.mInstanceLock;
        synchronized (object) {
            return this.mActivites.get((int)n).resolveInfo;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public int getActivityCount() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            return this.mActivites.size();
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    public int getActivityIndex(ResolveInfo resolveInfo) {
        List<ActivityResolveInfo> list = this.mActivites;
        int n = list.size();
        int n2 = 0;
        while (n2 < n) {
            if (list.get((int)n2).resolveInfo == resolveInfo) return n2;
            ++n2;
        }
        return -1;
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public ResolveInfo getDefaultActivity() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (this.mActivites.isEmpty()) return null;
            return this.mActivites.get((int)0).resolveInfo;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public int getHistoryMaxSize() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            return this.mHistoryMaxSize;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public int getHistorySize() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            return this.mHistoricalRecords.size();
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public Intent getIntent() {
        Object object = this.mInstanceLock;
        synchronized (object) {
            return this.mIntent;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void setActivitySorter(ActivitySorter activitySorter) {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (this.mActivitySorter == activitySorter) {
                return;
            }
            this.mActivitySorter = activitySorter;
            this.sortActivities();
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     */
    public void setDefaultActivity(int n) {
        ActivityResolveInfo activityResolveInfo = this.mActivites.get(n);
        ActivityResolveInfo activityResolveInfo2 = this.mActivites.get(0);
        float f = activityResolveInfo2 != null ? 5.0f + (activityResolveInfo2.weight - activityResolveInfo.weight) : 1.0f;
        this.addHisoricalRecord(new HistoricalRecord(new ComponentName(activityResolveInfo.resolveInfo.activityInfo.packageName, activityResolveInfo.resolveInfo.activityInfo.name), System.currentTimeMillis(), f));
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void setHistoryMaxSize(int n) {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (this.mHistoryMaxSize == n) {
                return;
            }
            this.mHistoryMaxSize = n;
            this.pruneExcessiveHistoricalRecordsLocked();
            this.sortActivities();
            return;
        }
    }

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    public void setIntent(Intent intent) {
        Object object = this.mInstanceLock;
        synchronized (object) {
            if (this.mIntent == intent) {
                return;
            }
            this.mIntent = intent;
            this.loadActivitiesLocked();
            return;
        }
    }

    public void setOnChooseActivityListener(OnChooseActivityListener onChooseActivityListener) {
        this.mActivityChoserModelPolicy = onChooseActivityListener;
    }

    public static interface ActivityChooserModelClient {
        public void setActivityChooserModel(ActivityChooserModel var1);
    }

    public final class ActivityResolveInfo
    implements Comparable<ActivityResolveInfo> {
        public final ResolveInfo resolveInfo;
        public float weight;

        public ActivityResolveInfo(ResolveInfo resolveInfo) {
            this.resolveInfo = resolveInfo;
        }

        @Override
        public int compareTo(ActivityResolveInfo activityResolveInfo) {
            return Float.floatToIntBits(activityResolveInfo.weight) - Float.floatToIntBits(this.weight);
        }

        /*
         * Enabled aggressive block sorting
         * Lifted jumps to return sites
         */
        public boolean equals(Object object) {
            if (this == object) {
                return true;
            }
            if (object == null) {
                return false;
            }
            if (this.getClass() != object.getClass()) {
                return false;
            }
            ActivityResolveInfo activityResolveInfo = (ActivityResolveInfo)object;
            if (Float.floatToIntBits(this.weight) == Float.floatToIntBits(activityResolveInfo.weight)) return true;
            return false;
        }

        public int hashCode() {
            return 31 + Float.floatToIntBits(this.weight);
        }

        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.append("[");
            stringBuilder.append("resolveInfo:").append(this.resolveInfo.toString());
            stringBuilder.append("; weight:").append(new BigDecimal(this.weight));
            stringBuilder.append("]");
            return stringBuilder.toString();
        }
    }

    public static interface ActivitySorter {
        public void sort(Intent var1, List<ActivityResolveInfo> var2, List<HistoricalRecord> var3);
    }

    public static final class HistoricalRecord {
        public final ComponentName activity;
        public final long time;
        public final float weight;

        public HistoricalRecord(ComponentName componentName, long l, float f) {
            this.activity = componentName;
            this.time = l;
            this.weight = f;
        }

        public HistoricalRecord(String string2, long l, float f) {
            this(ComponentName.unflattenFromString((String)string2), l, f);
        }

        /*
         * Enabled aggressive block sorting
         * Lifted jumps to return sites
         */
        public boolean equals(Object object) {
            if (this == object) {
                return true;
            }
            if (object == null) {
                return false;
            }
            if (this.getClass() != object.getClass()) {
                return false;
            }
            HistoricalRecord historicalRecord = (HistoricalRecord)object;
            if (this.activity == null ? historicalRecord.activity != null : !this.activity.equals((Object)historicalRecord.activity)) {
                return false;
            }
            if (this.time != historicalRecord.time) {
                return false;
            }
            if (Float.floatToIntBits(this.weight) == Float.floatToIntBits(historicalRecord.weight)) return true;
            return false;
        }

        /*
         * Enabled force condition propagation
         * Lifted jumps to return sites
         */
        public int hashCode() {
            int n;
            if (this.activity == null) {
                n = 0;
                do {
                    return 31 * (31 * (n + 31) + (int)(this.time ^ this.time >>> 32)) + Float.floatToIntBits(this.weight);
                    break;
                } while (true);
            }
            n = this.activity.hashCode();
            return 31 * (31 * (n + 31) + (int)(this.time ^ this.time >>> 32)) + Float.floatToIntBits(this.weight);
        }

        public String toString() {
            StringBuilder stringBuilder = new StringBuilder();
            stringBuilder.append("[");
            stringBuilder.append("; activity:").append((Object)this.activity);
            stringBuilder.append("; time:").append(this.time);
            stringBuilder.append("; weight:").append(new BigDecimal(this.weight));
            stringBuilder.append("]");
            return stringBuilder.toString();
        }
    }

    public static interface OnChooseActivityListener {
        public boolean onChooseActivity(ActivityChooserModel var1, Intent var2);
    }

}

