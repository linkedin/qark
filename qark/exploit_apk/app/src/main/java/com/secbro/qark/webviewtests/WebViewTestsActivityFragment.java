/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.webviewtests;

import android.content.Intent;
import android.support.v4.app.ListFragment;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.secbro.qark.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;


/**
 * A placeholder fragment containing a simple view.
 */
public class WebViewTestsActivityFragment extends ListFragment {

    private final static String LOG_TAG = WebViewTestsActivityFragment.class.getSimpleName();
    public static final String WEBVIEW_TEST_ID = "TestId";

    private List<String> webviewTests;
    private Map<String, String> webviewNamesMap;

    /**
     * The Adapter which will be used to populate the ListView/GridView with
     * Views.
     */
    private ListAdapter mAdapter;
    /**
     * The fragment's ListView/GridView.
     */
    private ListView mListView;

    public static WebViewTestsActivityFragment newInstance() {
        WebViewTestsActivityFragment fragment = new WebViewTestsActivityFragment();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public WebViewTestsActivityFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);

        View retVal = inflater.inflate(R.layout.fragment_web_view_tests, container, false);

        mListView = (ListView) retVal.findViewById(android.R.id.list);
        ((AdapterView<ListAdapter>) mListView).setAdapter(mAdapter);

        return retVal;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webviewTests = Arrays.asList(getResources().getStringArray(R.array.webViewTests));

        webviewNamesMap= new LinkedHashMap<>();

        webviewNamesMap.put("TestName0","Javascript Enabled: WebViewClient");
        webviewNamesMap.put("TestName1","Javascript Enabled: WebChromeClient");
        webviewNamesMap.put("TestName2","File URI Access: WebViewClient");
        webviewNamesMap.put("TestName3","File URI Access: WebChromeClient");
        webviewNamesMap.put("TestName4","BaseURL Override: WebViewClient");
        webviewNamesMap.put("TestName5","BaseURL Override: WebChromeClient");
        webviewNamesMap.put("TestName6","SOP Bypass: WebViewClient");
        webviewNamesMap.put("TestName7","SOP Bypass: WebChromeClient");
        webviewNamesMap.put("TestName8","SOP Bypass IFrame: WebViewClient");
        webviewNamesMap.put("TestName9","SOP Bypass IFrame: WebChromeClient");


        mAdapter = (new ArrayAdapter<String>(getActivity(),
                android.R.layout.simple_list_item_1, android.R.id.text1, new ArrayList<String>(webviewNamesMap.values())));

    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);

        Intent startActivityIntent = new Intent(getActivity(), WebViewTestsActivity.class);
        startActivityIntent.putExtra(WEBVIEW_TEST_ID, webviewTests.get(position));
        startActivity(startActivityIntent);
    }


}
