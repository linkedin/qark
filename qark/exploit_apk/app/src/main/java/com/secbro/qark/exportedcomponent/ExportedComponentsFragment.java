/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.exportedcomponent;

import android.os.Bundle;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.ListFragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import com.secbro.qark.R;
import com.secbro.qark.exportedcomponent.exportedactivity.ExportedActivityListFragment;
import com.secbro.qark.exportedcomponent.exportedreceiver.ExportedReceiverListFragment;


public class ExportedComponentsFragment extends ListFragment {
    private static final String LOG_TAG = ExportedComponentsFragment.class.getSimpleName();

    public interface IExportedComponents {
        String EXPORTED_ACTIVITIES = "Activities";
        String EXPORTED_RECEIVERS = "Broadcast Receivers";
        String EXPORTED_SERVICES = "Services";
        String EXPORTED_CONTENT_PROVIDERS = "Content Providers";
    }

    private static String[] exportedComponents = {
            IExportedComponents.EXPORTED_ACTIVITIES,
            IExportedComponents.EXPORTED_RECEIVERS,
            IExportedComponents.EXPORTED_SERVICES,
            IExportedComponents.EXPORTED_CONTENT_PROVIDERS
    };

    private ListView mListView;

    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public ExportedComponentsFragment() {
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        super.onCreateView(inflater, container, savedInstanceState);

        View retVal = inflater.inflate(R.layout.fragment_exported_components, container, false);

        mListView = (ListView) retVal.findViewById(android.R.id.list);

        return retVal;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setListAdapter(new ArrayAdapter<String>(getActivity(),
                android.R.layout.simple_list_item_1, android.R.id.text1, exportedComponents));
    }


    @Override
    public void onListItemClick(ListView l, View v, int position, long id) {
        super.onListItemClick(l, v, position, id);
        FragmentManager fragmentManager = getFragmentManager();
        switch (exportedComponents[position]) {
            case IExportedComponents.EXPORTED_ACTIVITIES:
                fragmentManager.beginTransaction()
                        .replace(R.id.container, new ExportedActivityListFragment())
                        .commit();
                break;
            case IExportedComponents.EXPORTED_RECEIVERS:
                fragmentManager.beginTransaction()
                        .replace(R.id.container, new ExportedReceiverListFragment())
                        .commit();
                break;
            case IExportedComponents.EXPORTED_SERVICES:
                //TODO
                break;
            case IExportedComponents.EXPORTED_CONTENT_PROVIDERS:
                //TODO
                break;
            default:
                Log.d(LOG_TAG, "Exported component not supported");
                break;
        }
    }


}
