/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.customintent;

import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.secbro.qark.R;

import java.util.ArrayList;

public class CreateCustomIntentActivity extends AppCompatActivity {

    public static final String CUSTOM_INTENT_EXTRA = "CustomIntent";

    AutoCompleteTextView extrasKey;
    AutoCompleteTextView intentAction;
    AutoCompleteTextView intentCategory;
    AutoCompleteTextView intentFlags;
    EditText intentData;
    EditText extrasValue;
    EditText componentName;
    EditText componentPackageName;
    ImageButton addMoreExtras;
    Button nextButton;
    Intent customIntent;
    AlertDialog errorDialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_create_custom_intent);

        //intent component name
        componentName = (EditText) findViewById(R.id.intent_component_name);

        //intent component package name
        componentPackageName = (EditText) findViewById(R.id.intent_component_package_name);

        //intent action
        intentAction = (AutoCompleteTextView) findViewById(R.id.intent_action_text_view);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_dropdown_item_1line, getResources().getStringArray(R.array.intent_actions_array));
        intentAction.setAdapter(adapter);
        intentAction.setSelection(intentAction.getText().length());
        intentAction.setOnTouchListener(new View.OnTouchListener() {
            @SuppressLint("ClickableViewAccessibility")
            @Override
            public boolean onTouch(View paramView, MotionEvent paramMotionEvent) {
                intentAction.showDropDown();
                intentAction.requestFocus();
                return false;
            }
        });

        //intent data
        intentData = (EditText) findViewById(R.id.intent_data);

        //intent category
        intentCategory =  (AutoCompleteTextView) findViewById(R.id.intent_category_text_view);
        ArrayAdapter<String> adapter1 = new ArrayAdapter<String>(this,
                android.R.layout.simple_dropdown_item_1line, getResources().getStringArray(R.array.intent_category_array));
        intentCategory.setAdapter(adapter1);
        intentCategory.setSelection(intentCategory.getText().length());
        intentCategory.setOnTouchListener(new View.OnTouchListener() {
            @SuppressLint("ClickableViewAccessibility")
            @Override
            public boolean onTouch(View paramView, MotionEvent paramMotionEvent) {
                intentCategory.showDropDown();
                intentCategory.requestFocus();
                return false;
            }
        });

        //intent flags
        intentFlags =  (AutoCompleteTextView) findViewById(R.id.intent_flags_text_view);
        ArrayAdapter<String> adapter2 = new ArrayAdapter<String>(this,
                android.R.layout.simple_dropdown_item_1line, getResources().getStringArray(R.array.intent_flags_array));
        intentFlags.setAdapter(adapter2);
        intentFlags.setSelection(intentFlags.getText().length());
        intentFlags.setOnTouchListener(new View.OnTouchListener() {
            @SuppressLint("ClickableViewAccessibility")
            @Override
            public boolean onTouch(View paramView, MotionEvent paramMotionEvent) {
                intentFlags.showDropDown();
                intentFlags.requestFocus();
                return false;
            }
        });

        //intent extras key
        extrasKey = (AutoCompleteTextView) findViewById(R.id.key1);
        ArrayAdapter<String> adapter3 = new ArrayAdapter<String>(this,
                android.R.layout.simple_dropdown_item_1line, getResources().getStringArray(R.array.intent_extras_array));
        extrasKey.setAdapter(adapter3);
        extrasKey.setSelection(extrasKey.getText().length());
        extrasKey.setOnTouchListener(new View.OnTouchListener() {
            @SuppressLint("ClickableViewAccessibility")
            @Override
            public boolean onTouch(View paramView, MotionEvent paramMotionEvent) {
                extrasKey.showDropDown();
                extrasKey.requestFocus();
                return false;
            }
        });

        //intent extras value
        extrasValue = (EditText) findViewById(R.id.value1);

        //add more extras button
        addMoreExtras = (ImageButton) findViewById(R.id.add_more_extras_button);
        addMoreExtras.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createExtrasView();
            }
        });

        //next button
        nextButton = (Button) findViewById(R.id.activity_create_custom_intent_next_button);
        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                createIntentFromFormData();
                Intent nextIntent = new Intent(CreateCustomIntentActivity.this, ChooseIntentUseCaseActivity.class);
                nextIntent.putExtra(CUSTOM_INTENT_EXTRA, customIntent);
                startActivity(nextIntent);
            }
        });

    }

    private void createIntentFromFormData() {
        customIntent = new Intent();
        if (!TextUtils.isEmpty(componentName.getText()) && !TextUtils.isEmpty(componentPackageName.getText())) {
            customIntent.setClassName(componentPackageName.getText().toString(),
                    componentName.getText().toString());
        }

        if(!TextUtils.isEmpty(intentAction.getText())) {
            customIntent.setAction(intentAction.getText().toString());
        }

        if(!TextUtils.isEmpty(intentData.getText())) {
            customIntent.setData(Uri.parse(intentData.getText().toString()));
        }

        if(!TextUtils.isEmpty(intentCategory.getText())) {
            customIntent.addCategory(intentCategory.getText().toString());
        }

        if(!TextUtils.isEmpty(intentFlags.getText())) {
            customIntent.setFlags(Integer.parseInt(intentFlags.getText().toString()));
        }

        populateExtrasKeyValuePairs();

        //intent is ready now!


    }

    private void populateExtrasKeyValuePairs() {
        ViewGroup extrasContainer = (ViewGroup) findViewById(R.id.extras_key_value_container);
        ArrayList<String> keys = new ArrayList<>();
        ArrayList<String> values = new ArrayList<>();

        findAllKeys(keys, extrasContainer);
        findAllValues(values, extrasContainer);

        if (keys.size() != values.size()) {
            errorDialog = new AlertDialog.Builder(CreateCustomIntentActivity.this).create();
            errorDialog.setTitle("Error");
            errorDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                    new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                            dialog.dismiss();
                        }
                    });
            errorDialog.setMessage("Intent extras key value do not match in number");
            errorDialog.show();
        } else {
            for (int i=0; i<keys.size() ; i++) {
                Log.d("Extras key/value pair", keys.get(i) + "/" + values.get(i));
                customIntent.putExtra(keys.get(i), values.get(i));
            }
        }

    }

    private ArrayList<String> findAllKeys(ArrayList<String> keys, ViewGroup viewGroup) {
        int count = viewGroup.getChildCount();
        for (int i = 0; i < count; i++) {
            View view = viewGroup.getChildAt(i);
            if (view instanceof ViewGroup)
                findAllKeys(keys, (ViewGroup) view);
            else if (view instanceof TextView) {
                TextView textview = (TextView) view;
//                if (!textview.getText().toString().equals(getResources().getString(R.string.intent_extras_key)) &&
//                        !textview.getText().toString().equals(getResources().getString(R.string.intent_extras_value)) &&
//                        !textview.getTag().toString().equals("value_field")) {
                if (textview.getTag() != null && textview.getTag().toString().equals("key_field")) {
                    keys.add(textview.getText().toString());
                }
            }
        }
        return keys;
    }

        private ArrayList<String> findAllValues(ArrayList<String> values, ViewGroup viewGroup) {
        int count = viewGroup.getChildCount();
        for (int i = 0; i < count; i++) {
            View view = viewGroup.getChildAt(i);
            if (view instanceof ViewGroup)
                findAllValues(values, (ViewGroup) view);
            else if (view instanceof EditText) {
                EditText edittext = (EditText) view;
                if (edittext.getTag() != null && edittext.getTag().toString().equals("value_field")) {
                    values.add(edittext.getText().toString());
                }
            }
        }
            return values;
        }


    private void createExtrasView() {
        LinearLayout topLayout = (LinearLayout) findViewById(R.id.extras_key_value_container);

        LinearLayout.LayoutParams llpTextView = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        llpTextView.setMargins(10, 20, 10, 10); // llp.setMargins(left, top, right, bottom);

        LinearLayout.LayoutParams llpEditText = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        llpEditText.setMargins(10, 20, 10, 10); // llp.setMargins(left, top, right, bottom);

        //key
        LinearLayout keyLinearLayout = new LinearLayout(this);
        keyLinearLayout.setOrientation(LinearLayout.HORIZONTAL);

        TextView keyTextView = new TextView(this);
        keyTextView.setText(getResources().getString(R.string.intent_extras_key));
        keyTextView.setLayoutParams(llpTextView);

        AutoCompleteTextView keyEditText = new AutoCompleteTextView(this);
        keyEditText.setLayoutParams(llpEditText);
        ArrayAdapter<String> adapter3 = new ArrayAdapter<String>(this,
                android.R.layout.simple_dropdown_item_1line, getResources().getStringArray(R.array.intent_extras_array));
        keyEditText.setAdapter(adapter3);
        keyEditText.setSelection(keyEditText.getText().length());
        keyEditText.setTag("key_field");

        keyLinearLayout.addView(keyTextView);
        keyLinearLayout.addView(keyEditText);

        //value
        LinearLayout valueLinearLayout = new LinearLayout(this);
        valueLinearLayout.setOrientation(LinearLayout.HORIZONTAL);

        TextView valueTextView = new TextView(this);
        valueTextView.setText(getResources().getString(R.string.intent_extras_value));
        valueTextView.setLayoutParams(llpTextView);

        EditText valueEditText = new EditText(this);
        valueEditText.setTag("value_field");
        valueEditText.setLayoutParams(llpEditText);

        valueLinearLayout.addView(valueTextView);
        valueLinearLayout.addView(valueEditText);

        topLayout.addView(keyLinearLayout);
        topLayout.addView(valueLinearLayout);
    }
}
