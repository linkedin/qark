/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.customintent;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import com.secbro.qark.R;

public class ChooseIntentUseCaseActivity extends AppCompatActivity {

    private static final int START_ACTIVITY_FOR_RESULT = 1;
    private Spinner usecaseSpinner;
    private Button sendIntentButton;
    private AlertDialog errorDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_choose_intent_use_case);

        final Intent customIntent = getIntent().getParcelableExtra(CreateCustomIntentActivity.CUSTOM_INTENT_EXTRA);

        if (customIntent == null) {
            throw new IllegalArgumentException("customIntent is null");
        }

        //intent usecase spinner
        usecaseSpinner = (Spinner) findViewById(R.id.intent_use_case_spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
                this, R.array.intent_use_case, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        usecaseSpinner.setAdapter(adapter);

        //Send intent button
        sendIntentButton = (Button) findViewById(R.id.activity_choose_intent_use_case_send_button);
        errorDialog = new AlertDialog.Builder(this).create();
        errorDialog.setTitle("Error");
        errorDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                    }
                });

        sendIntentButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (usecaseSpinner.getSelectedItem() == null) {
                    errorDialog.setMessage("Invalid intent use case");
                    errorDialog.show();
                } else {
                    String useCase = usecaseSpinner.getSelectedItem().toString();
                    switch (useCase) {
                        case "startActivity":
                            //TODO: Validate data for startActivity is present
                            startActivity(customIntent);
                            break;
                        case "startActivityForResult":
                            //TODO:Validate customIntent
                            startActivityForResult(customIntent, START_ACTIVITY_FOR_RESULT);
                            break;
                        case "startService":
                            //TODO:Validate customIntent
                            startService(customIntent);
                            break;
                        case "bindService":
                            //TODO:
                            break;
                        case "sendBroadcast":
                            //TODO:Validate customIntent
                            sendBroadcast(customIntent);
                            break;
                        case "sendOrderedBroadcast":
                            //TODO:
                            //sendOrderedBroadcast(customIntent);
                            break;
                        case "sendStickyBroadcast":
                            //TODO:Validate customIntent
                            sendStickyBroadcast(customIntent);
                            break;
                        default:
                            break;
                    }
                }
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        // Check which request we're responding to
        if (requestCode == START_ACTIVITY_FOR_RESULT) {
            // Make sure the request was successful
            if (resultCode == RESULT_OK) {
                AlertDialog result = new AlertDialog.Builder(this).create();
                result.setTitle("Result from startActivityForResult()");
                result.setMessage(data.getDataString());
                result.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                        new DialogInterface.OnClickListener() {
                            public void onClick(DialogInterface dialog, int which) {
                                dialog.dismiss();
                            }
                        });
                result.show();
            }
        }
    }
}
