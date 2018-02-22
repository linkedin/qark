/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.exportedcomponent.exportedreceiver;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Toast;

import com.secbro.qark.R;
import com.secbro.qark.exportedcomponent.exportedactivity.ExportedActivityListFragment;

import java.util.ArrayList;
import java.util.Arrays;

public class IntentSenderActivity extends AppCompatActivity {
    public static final String INTENT_KEYS = "INTENT_KEYS";

    private ArrayList<String> intentKeys;
    private String exportedReceiverName;
    private String exportedReceiverId;
    //private String intentId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_intent_sender);

        intentKeys = new ArrayList<String>();

        if (getIntent() != null) {
            exportedReceiverId = getIntent().getStringExtra(ExportedReceiverListFragment.EXPORTED_RECEIVER_ID);
            exportedReceiverName = getIntent().getStringExtra(ExportedReceiverListFragment.EXPORTED_RECEIVER_NAME);

                if (getResources().getIdentifier(exportedReceiverId, "array", this.getPackageName()) != 0) {
                    intentKeys.addAll(Arrays.asList(
                            getResources().getStringArray(
                                    getResources().getIdentifier(exportedReceiverId, "array", this.getPackageName()))));
                }
        }

        if (!intentKeys.isEmpty()) {
            Bundle keys = new Bundle();
            keys.putString(ExportedReceiverListFragment.EXPORTED_RECEIVER_NAME, exportedReceiverName);
            keys.putString(ExportedReceiverListFragment.EXPORTED_RECEIVER_ID, exportedReceiverId);
            keys.putStringArrayList(INTENT_KEYS, intentKeys);

            IntentSenderFragment intentSenderFragment = new IntentSenderFragment();
            intentSenderFragment.setArguments(keys);

            if (savedInstanceState == null) {
                getSupportFragmentManager().beginTransaction()
                        .add(R.id.container, intentSenderFragment)
                        .commit();
            }
        } else {
            Log.d("INFO", "Exported receiver needs no params");
            Intent intent = new Intent();
            intent.setAction(exportedReceiverName);
            sendBroadcast(intent);
            Toast.makeText(this, "Intent sent", Toast.LENGTH_LONG).show();
        }
    }
}
