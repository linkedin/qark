/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.intentsniffer;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import com.secbro.qark.R;
import com.secbro.qark.intentsniffer.services.BroadcastStealerService;

public class BroadcastIntentSnifferActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fragment_broadcast_stealer);
        SharedPreferences prefs = this.getSharedPreferences(
                getPackageName(), Context.MODE_PRIVATE);
        TextView textview = (TextView) findViewById(R.id.activity_broadcast_stealer_text_view);
        textview.setText(prefs.getString("foo", "Listening..." ));
        Intent msgIntent = new Intent(this, BroadcastStealerService.class);
        msgIntent.setAction("Start");
        startService(msgIntent);
    }
}
