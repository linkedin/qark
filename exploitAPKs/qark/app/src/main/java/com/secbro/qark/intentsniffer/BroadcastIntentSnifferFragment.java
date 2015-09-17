/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.intentsniffer;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.secbro.qark.R;
import com.secbro.qark.intentsniffer.services.BroadcastStealerService;

public class BroadcastIntentSnifferFragment extends Fragment {


    public static BroadcastIntentSnifferFragment newInstance() {
        BroadcastIntentSnifferFragment fragment = new BroadcastIntentSnifferFragment();
        return fragment;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View retVal = inflater.inflate(R.layout.fragment_broadcast_stealer, container, false);

        SharedPreferences prefs = this.getActivity().getSharedPreferences(
                getActivity().getPackageName(), Context.MODE_PRIVATE);
        TextView textview = (TextView) retVal.findViewById(R.id.activity_broadcast_stealer_text_view);

        textview.setText(prefs.getString("foo", "Listening..." ));
        Intent msgIntent = new Intent(this.getActivity(), BroadcastStealerService.class);
        msgIntent.setAction("Start");
        this.getActivity().startService(msgIntent);

       return retVal;
    }

    @Override
    public void onResume() {
        SharedPreferences prefs = this.getActivity().getSharedPreferences(
                getActivity().getPackageName(), Context.MODE_PRIVATE);
        TextView textview = (TextView) this.getActivity().findViewById(R.id.activity_broadcast_stealer_text_view);

        textview.setText(prefs.getString("foo", "Listening..." ));
        super.onResume();
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public BroadcastIntentSnifferFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }
}
