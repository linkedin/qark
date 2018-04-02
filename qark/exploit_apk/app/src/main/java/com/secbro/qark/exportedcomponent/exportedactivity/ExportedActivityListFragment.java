/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.exportedcomponent.exportedactivity;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;

import com.secbro.qark.R;
import com.secbro.qark.exportedcomponent.exportedreceiver.ExportedReceiverListFragment;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ExportedActivityListFragment extends ListFragment {
    private final static String LOG_TAG = ExportedActivityListFragment.class.getSimpleName();
    public static final String EXPORTED_ACTIVITY_NAME = "ExportedActivityName";
    public static final String EXPORTED_ACTIVITY_ID = "ExportedActivityId";

    private List<String> exportedActivities;
    private Map<String, String> exportedActivitiesIdNameMap;

    /**
     * The fragment's ListView/GridView.
     */
    private ListView mListView;

    public static ExportedReceiverListFragment newInstance() {
        ExportedReceiverListFragment fragment = new ExportedReceiverListFragment();
        return fragment;
    }

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public ExportedActivityListFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);

        View retVal = inflater.inflate(R.layout.fragment_exported_activity_list, container, false);

        mListView = (ListView) retVal.findViewById(android.R.id.list);

        return retVal;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        exportedActivities = Arrays.asList(getResources().getStringArray(R.array.exportedActivities));

        if (exportedActivities != null && exportedActivities.size() != 0) {
            exportedActivitiesIdNameMap = new LinkedHashMap<>();
            for (String activity : exportedActivities) {
                if (getResources().getIdentifier(activity, "string", getActivity().getPackageName()) != 0) {
                    exportedActivitiesIdNameMap.put(activity, getResources().getString(getResources().getIdentifier(activity, "string", getActivity().getPackageName())));
                } else {
                    throw new IllegalArgumentException("No matching exportedActivities names found in string.xml ");
                }
            }
           setListAdapter(new ArrayAdapter<String>(getActivity(),
                   android.R.layout.simple_list_item_1, android.R.id.text1, new ArrayList<String>(exportedActivitiesIdNameMap.values())));
        } else {
            Log.d(LOG_TAG, "No exported activities to exploit");
        }
    }

    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);

        Intent startActivityIntent = new Intent(getActivity(), IntentSenderActivity.class);
        startActivityIntent.putExtra(EXPORTED_ACTIVITY_NAME, exportedActivitiesIdNameMap.get(exportedActivities.get(position)));
        startActivityIntent.putExtra(EXPORTED_ACTIVITY_ID, exportedActivities.get(position));
        startActivity(startActivityIntent);
    }

}
