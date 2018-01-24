/*
 * Decompiled with CFR 0_124.
 *
 * Could not load the following classes:
 *  android.content.BroadcastReceiver
 *  android.content.Context
 *  android.content.Intent
 *  android.content.IntentFilter
 *  android.os.Handler
 *  android.os.Looper
 *  android.os.Message
 */
package android.support.v4.content;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import java.util.ArrayList;
import java.util.HashMap;

public class LocalBroadcastManager {

    /*
     * Exception decompiling
     */
    public boolean sendBroadcast(Intent var1_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendBroadcast(Intent var1_1, String var2_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendBroadcastAsUser(Intent var1_1, String var2_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendBroadcastAsUser(Intent var1_1, String var2_1, String var3_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendOrderedBroadcast(Intent var1_1, String var2_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendOrderedBroadcast(Intent var1_1, String var2_1, String var3_1, String var4_1, String var5_1,
                                            String var6_1, String var7_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendOrderedBroadcastAsUser(Intent var1_1, String var2_1, String var3_1, String var4_1, String var5_1,
        String var6_1, String var7_1) {
        throw new IllegalStateException("Decompilation failed");
    }
    public boolean sendStickyBroadcast(Intent var1_1) {
        throw new IllegalStateException("Decompilation failed");
    }

    public void vulnerableMethod(Intent intent) {
        if (this.sendBroadcast(intent)) {
            this.executePendingBroadcasts();
        }
        if (this.sendBroadcast(intent, "permission")) {
            this.executePendingBroadcasts();
        }
        if (this.sendBroadcastAsUser(intent, "argument2")) {
            this.executePendingBroadcasts();
        }
        if (this.sendBroadcastAsUser(intent, "argument2", "argument3")) {
            this.executePendingBroadcasts();
        }
        if (this.sendOrderedBroadcast(intent, "permission")) {
            this.executePendingBroadcasts();
        }
        if (this.sendOrderedBroadcast(intent, "2", "3", "4", "5", "6", "7")) {
            this.executePendingBroadcasts();
        }
        if (this.sendOrderedBroadcastAsUser(intent, "2", "3", "4", "5", "6", "7")) {
            this.executePendingBroadcasts();
        }
        if (this.sendStickyBroadcast(intent)) {
            this.executePendingBroadcasts();
        }

    }
}

