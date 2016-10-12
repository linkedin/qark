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
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
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

public class IntentSenderFragment extends Fragment {

    private ArrayList<String> keys;
    private String exportedReceiverName;
    private String exportedReceiverId;

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public IntentSenderFragment() {
    }

    @Override
    public void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        outState.putStringArrayList(IntentSenderActivity.INTENT_KEYS, keys);
        outState.putString(ExportedReceiverListFragment.EXPORTED_RECEIVER_NAME, exportedReceiverName);
        outState.putString(ExportedReceiverListFragment.EXPORTED_RECEIVER_ID, exportedReceiverId);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View retVal = inflater.inflate(R.layout.fragment_intent_sender, container, false);
        return retVal;
    }


    @Override
    public void onActivityCreated(@Nullable Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        if (savedInstanceState != null) {
            keys = savedInstanceState.getStringArrayList(IntentSenderActivity.INTENT_KEYS);
            exportedReceiverName = savedInstanceState.getString(ExportedReceiverListFragment.EXPORTED_RECEIVER_NAME);
            exportedReceiverId = savedInstanceState.getString(ExportedReceiverListFragment.EXPORTED_RECEIVER_ID);
        } else {
            Bundle bundle = getArguments();
            if (bundle != null) {
                keys = bundle.getStringArrayList(IntentSenderActivity.INTENT_KEYS);
                exportedReceiverName = bundle.getString(ExportedReceiverListFragment.EXPORTED_RECEIVER_NAME);
                exportedReceiverId = bundle.getString(ExportedReceiverListFragment.EXPORTED_RECEIVER_ID);
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
                sendBroadcast();
            }
        });
    }

    private void sendBroadcast() {
        Intent intent = new Intent();
        intent.setAction(exportedReceiverName);
        if (keys.size() != 0) {
            // if intent has extras
            for (String key : keys) {
                intent.putExtra(((TextView) getView().findViewWithTag("key" + key)).getText().toString(), ((EditText) getView().findViewWithTag("value" + key)).getText().toString());
            }
        }
        getActivity().sendBroadcast(intent);
        Toast.makeText(getActivity(), "Intent sent", Toast.LENGTH_LONG).show();
    }

    private void createKeyValuePairLayout(String key, LinearLayout paramsLayout) {
        LinearLayout linearLayout = new LinearLayout(getActivity());
        linearLayout.setOrientation(LinearLayout.HORIZONTAL);

        LinearLayout.LayoutParams llp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        llp.setMargins(50, 10, 50, 10); // llp.setMargins(left, top, right, bottom);
        TextView keyTextView = new TextView(getActivity());
        keyTextView.setTag("key" + key);
        keyTextView.setText(key);
        keyTextView.setLayoutParams(llp);

        LinearLayout.LayoutParams llp1 = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        llp.setMargins(50, 10, 50, 10); // llp.setMargins(left, top, right, bottom);
        EditText valueEditText = new EditText(getActivity());
        valueEditText.setTag("value" + key);
        valueEditText.setLayoutParams(llp1);

        linearLayout.addView(keyTextView);
        linearLayout.addView(valueEditText);
        paramsLayout.addView(linearLayout);
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
}