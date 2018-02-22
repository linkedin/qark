/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark;



import android.content.Intent;
import android.content.res.Configuration;
import android.support.design.widget.NavigationView;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.os.Bundle;
import android.support.v4.view.GravityCompat;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.MenuItem;
import android.support.v4.widget.DrawerLayout;

import com.secbro.qark.customintent.CreateCustomIntentActivity;
import com.secbro.qark.intentsniffer.BroadcastIntentSnifferFragment;
import com.secbro.qark.exportedcomponent.ExportedComponentsFragment;
import com.secbro.qark.filebrowser.FileBrowserFragment;
import com.secbro.qark.tapjacking.TapJackingExploitFragment;
import com.secbro.qark.webviewtests.WebViewTestsActivityFragment;


public class TopLevelActivity extends AppCompatActivity {

    private DrawerLayout mDrawer;
    private NavigationView mNavigationView;
    private Toolbar mToolbar;
    private ActionBarDrawerToggle mDrawerToggle;

    public static String PACKAGE_NAME = "com.secbro.qark";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_top_level);
        PACKAGE_NAME = getApplicationContext().getPackageName();

        // Set a Toolbar to replace the ActionBar.
        mToolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(mToolbar);

        mDrawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        mDrawerToggle = setupDrawerToggle();

        // Tie DrawerLayout events to the ActionBarToggle
        mDrawer.setDrawerListener(mDrawerToggle);

        // Find our drawer view
        mNavigationView = (NavigationView) findViewById(R.id.nvView);
        // Setup drawer view
        setupDrawerContent(mNavigationView);

    }

    private ActionBarDrawerToggle setupDrawerToggle() {
        return new ActionBarDrawerToggle(this, mDrawer, mToolbar, R.string.drawer_open,  R.string.drawer_close);
    }

    private void setupDrawerContent(NavigationView navigationView) {
        navigationView.setNavigationItemSelectedListener(
                new NavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(MenuItem menuItem) {
                        selectDrawerItem(menuItem);
                        return true;
                    }
                });
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        // Sync the toggle state after onRestoreInstanceState has occurred.
        mDrawerToggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        // Pass any configuration change to the drawer toggles
        mDrawerToggle.onConfigurationChanged(newConfig);
    }

    public void selectDrawerItem(MenuItem menuItem) {
        // update the main content by replacing fragments
        FragmentManager fragmentManager = getSupportFragmentManager();

        switch(menuItem.getItemId()) {
            case R.id.nav_broadcast_intent_sniffer:
                fragmentManager.beginTransaction()
                        .replace(R.id.container, BroadcastIntentSnifferFragment.newInstance())
                        .commit();
                break;
            case R.id.nav_exported_components:
                fragmentManager.beginTransaction()
                        .replace(R.id.container, new ExportedComponentsFragment())
                        .commit();
                break;
            case R.id.nav_tap_jacking:
                    fragmentManager.beginTransaction()
                    .replace(R.id.container, new TapJackingExploitFragment())
                    .commit();
                break;
            case R.id.nav_web_view_tests:
                fragmentManager.beginTransaction()
                        .replace(R.id.container, new WebViewTestsActivityFragment())
                        .commit();
                break;
            case R.id.nav_file_browser:
                Bundle args = new Bundle();
                args.putString(FileBrowserFragment.INTENT_ACTION_SELECT_FILE, FileBrowserFragment.INTENT_ACTION_SELECT_FILE);

                Fragment instance = FileBrowserFragment.newInstance();
                instance.setArguments(args);
                fragmentManager.beginTransaction()
                        .replace(R.id.container, instance)
                        .commit();
                break;
            case R.id.nav_custom_intent:
                Intent createNewIntent = new Intent(this, CreateCustomIntentActivity.class);
                startActivity(createNewIntent);
            default:
                //TODO:
        }

        // Highlight the selected item, update the title, and close the drawer
        menuItem.setChecked(true);
        setTitle(menuItem.getTitle());
        mDrawer.closeDrawers();
    }


    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        switch (item.getItemId()) {
            case android.R.id.home:
                mDrawer.openDrawer(GravityCompat.START);
                return true;
        }

        if (mDrawerToggle.onOptionsItemSelected(item)) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
