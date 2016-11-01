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
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.secbro.qark.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class IntentParamsFragment extends Fragment {

    private final static int REQUEST_CODE = 1;
    private final static String LOG_TAG = IntentParamsFragment.LOG_TAG;


    public interface ActivityResultListener {
        void onActivityResultListener(Map resultMap);
    }

    private ActivityResultListener mListener;

    public IntentParamsFragment() {
        // Required empty public constructor
    }

    private ArrayList<String> keys;
    private String exportedActivityName;
    private String exportedActivityId;

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putStringArrayList(IntentSenderActivity.INTENT_KEYS, keys);
        outState.putString(ExportedActivityListFragment.EXPORTED_ACTIVITY_NAME, exportedActivityName);
        outState.putString(ExportedActivityListFragment.EXPORTED_ACTIVITY_ID, exportedActivityId);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View retVal = inflater.inflate(R.layout.fragment_exploit_exported_activity_params, container, false);
        return retVal;
    }

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mListener = (ActivityResultListener) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException("Activity must implement ExploitExportedActivityListener.");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }

    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        if (savedInstanceState != null) {
            keys = savedInstanceState.getStringArrayList(IntentSenderActivity.INTENT_KEYS);
            exportedActivityName = savedInstanceState.getString(ExportedActivityListFragment.EXPORTED_ACTIVITY_NAME);
            exportedActivityId = savedInstanceState.getString(ExportedActivityListFragment.EXPORTED_ACTIVITY_ID);
        } else {
            Bundle bundle = getArguments();
            if (bundle != null) {
                keys = bundle.getStringArrayList(IntentSenderActivity.INTENT_KEYS);
                exportedActivityName = bundle.getString(ExportedActivityListFragment.EXPORTED_ACTIVITY_NAME);
                exportedActivityId = bundle.getString(ExportedActivityListFragment.EXPORTED_ACTIVITY_ID);
            }
        }

        if (keys == null || keys.isEmpty()) {
            throw new IllegalArgumentException("Keys null");
        }

        LinearLayout paramsLayout = (LinearLayout) getView().findViewById(R.id.paramsLayout);

        for (String key : keys) {
            createKeyValuePairLayout(key, paramsLayout);
        }

        Button button = (Button) getView().findViewById(R.id.submitButton);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                Intent intent = new Intent();
                intent.setComponent(new ComponentName(getResources().getString(R.string.packageName), exportedActivityName));
                for (String key : keys) {
                    intent.putExtra(((TextView) getView().findViewWithTag("key" + key)).getText().toString(), ((EditText) getView().findViewWithTag("value" + key)).getText().toString());

                }
                startActivityForResult(intent, REQUEST_CODE);
                Toast.makeText(getActivity(), "Intent sent", Toast.LENGTH_LONG).show();
            }
        });
    }

    private void createKeyValuePairLayout(String key, LinearLayout topLayout) {
        LinearLayout linearLayout = new LinearLayout(getActivity());
        linearLayout.setOrientation(LinearLayout.HORIZONTAL);

        TextView keyTextView = new TextView(getActivity());
        keyTextView.setTag("key" + key);
        keyTextView.setText(key);
        LinearLayout.LayoutParams llp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        llp.setMargins(50, 40, 50, 10); // llp.setMargins(left, top, right, bottom);
        keyTextView.setLayoutParams(llp);

        LinearLayout.LayoutParams llp1 = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        EditText valueEditText = new EditText(getActivity());
        valueEditText.setTag("value" + key);
        valueEditText.setLayoutParams(llp1);

        linearLayout.addView(keyTextView);
        linearLayout.addView(valueEditText);
        topLayout.addView(linearLayout);
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
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
                        //Call container activity back to display result
                        if (mListener != null) {
                            mListener.onActivityResultListener(resultMap);
                        } else {
                            Log.e(LOG_TAG, "mListener is null");
                        }
                    }
                } else {
                    Log.d("INFO", "No data received");
                }
            }
        }
    }
}