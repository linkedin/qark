/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.exportedcomponent.exportedactivity;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.support.v4.app.FragmentActivity;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;

import com.secbro.qark.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class IntentSenderActivity extends AppCompatActivity implements IntentParamsFragment.ActivityResultListener {

    public static final String INTENT_KEYS = "INTENT_KEYS";
    private final static int REQUEST_CODE = 2;

    private ArrayList<String> intentKeys;
    private String exportedActivityName;
    private String exportedActivityId;
    private TextView mResultText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_exploit_exported_result);

        mResultText = (TextView) findViewById(R.id.activity_exploit_exported_result_text);

        intentKeys = new ArrayList<String>();

        if (getIntent() != null) {
            exportedActivityId = getIntent().getStringExtra(ExportedActivityListFragment.EXPORTED_ACTIVITY_ID);
            exportedActivityName = getIntent().getStringExtra(ExportedActivityListFragment.EXPORTED_ACTIVITY_NAME);

            if (getResources().getIdentifier(exportedActivityId, "array", this.getPackageName()) != 0) {
                intentKeys.addAll(Arrays.asList(getResources().getStringArray(
                                getResources().getIdentifier(exportedActivityId, "array", this.getPackageName()))));
            }
        }

        if (!intentKeys.isEmpty()) {
            //If the exported activity needs intent params to be passed, then pass in the params from UI.
            Bundle keys = new Bundle();
            keys.putString(ExportedActivityListFragment.EXPORTED_ACTIVITY_NAME, exportedActivityName);
            keys.putString(ExportedActivityListFragment.EXPORTED_ACTIVITY_ID, exportedActivityId);
            keys.putStringArrayList(INTENT_KEYS, intentKeys);

            IntentParamsFragment exploitExportedActivityParamsFragment = new IntentParamsFragment();
            exploitExportedActivityParamsFragment.setArguments(keys);

            if (savedInstanceState == null) {
                getSupportFragmentManager().beginTransaction()
                        .add(R.id.container, exploitExportedActivityParamsFragment)
                        .commit();
            }
        } else {
            Log.d("INFO", "Exported activity needs no params");
            //Start activity
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(getResources().getString(R.string.packageName), exportedActivityName));
            startActivityForResult(intent, REQUEST_CODE);
        }
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
            case REQUEST_CODE: {
                if (resultCode == Activity.RESULT_OK) {
                    if (data != null) {
                        Map resultMap = new HashMap<Object, Object>();
                        Bundle bundle = data.getExtras();
                        for (String key : bundle.keySet()) {
                            Object value = bundle.get(key);
                            Log.d("key", key);
                            Log.d("value", value.toString());
                            resultMap.put(key, value);
                        }
                        showResultFromExploit(resultMap);
                    }
                } else {
                    Log.d("INFO", "No data received");
                }
            }
        }
    }

    @Override
    public void onActivityResultListener(Map resultMap) {
        showResultFromExploit(resultMap);
    }

    private void showResultFromExploit(Map resultMap) {
        if (mResultText != null) {
            mResultText.setText(resultMap.toString());
        }
    }
}