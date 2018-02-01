/*
 * Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package com.secbro.qark.webviewtests;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.content.SharedPreferences;
import android.content.Context;
import android.util.Log;

import com.secbro.qark.R;

public class WebViewTestsActivity extends AppCompatActivity {
    private WebView webView;

    public void onCreate(Bundle savedInstanceState) {
        Log.d("QARK","Hit OnCreate******");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.webview);
        String browser=getIntent().getStringExtra(WebViewTestsActivityFragment.WEBVIEW_TEST_ID);
        String url="http://www.secbro.com";
        int currentapiVersion= Build.VERSION.SDK_INT;

        //Create a preferences file as a means to show filesystem access
        Log.d("QARK", "Started trying to write shared_prefs");
        final String qarkPrefs = "qarkPrefs";
        final String testKey = "secretPassword";
        final String testPassword = "You are seeing the contents of /data/data/com.secbro.qark/shared_prefs/qarkPrefs.xml";
        SharedPreferences sharedpreferences;
        sharedpreferences = getSharedPreferences(qarkPrefs, Context.MODE_PRIVATE);

        Log.d("QARK", "Got half way through shared_prefs");

        SharedPreferences.Editor editor = sharedpreferences.edit();
        editor.putString(testKey,testPassword);
        editor.commit();
        Log.d("QARK", "Completed SharedPreference creation");
        //End of creating shared preferences

        webView = (WebView) findViewById(R.id.nav_web_view_tests);
        Log.d("QARK","Set View");
        //Offering same tests, but for different WebViewClients
        if (browser.matches(".*_AOSP")){
            Log.d("QARK", "Android Browser");
            webView.setWebViewClient(new WebViewClient());
        }else{
            Log.d("QARK","Chrome Browser");
            webView.setWebChromeClient(new WebChromeClient());
        }

        //speed things up a bit?
        //webView.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE);

        //We'll default to JS being off for now
        webView.getSettings().setJavaScriptEnabled(false);
        Log.d("QARK","Javascript disabled");

        //Derive test urls and settings based on which test they are running
        if (browser.matches("JS_.*")){
            Log.d("QARK","JS");
            url="http://secbro.com/qark/poc/JS_WARNING.html";
            webView.getSettings().setJavaScriptEnabled(true);
        } else if(browser.matches("FS_.*")){
            //We can remove the version check
            if ((currentapiVersion)<Build.VERSION_CODES.KITKAT){
                Log.d("QARK","FS");
                webView.getSettings().setAllowFileAccess(true);
                Log.d("QARK", "FS");
                url="file:////data/data/com.secbro.qark/shared_prefs/qarkPrefs.xml";
            }else{
                //url="http://secbro.com/qark/poc/wrongVersion.html";
                url="file:////data/data/com.secbro.qark/shared_prefs/qarkPrefs.xml";
            }
        } else if(browser.matches("BU_.*")){
            Log.d("QARK","BU");
            url="http://secbro.com/qark/poc/BURL_WARNING.html";
        } else if(browser.matches("SOP_.*")){
            if ((currentapiVersion)<Build.VERSION_CODES.KITKAT){
                url = "http://secbro.com/qark/poc/WEBVIEW_SOP_WARNING.html";
            }else{
                url="http://secbro.com/qark/poc/wrongVersion.html";
            }

        } else if(browser.matches("IFRAME_.*")) {
            Log.d("QARK", "IFRAME");
            if ((currentapiVersion) < Build.VERSION_CODES.KITKAT) {
                url = "http://secbro.com/qark/poc/WEBVIEW_SOP_WARNING_IFRAME.html";
            } else {
                url = "http://secbro.com/qark/poc/wrongVersion.html";
            }
        }

        if (browser.matches("BU_.*")){
            Log.d("QARK","BU2");
            webView.getSettings().setJavaScriptEnabled(true);
            String contents="<html>\n" +
                    "<head>\n" +
                    "</head>\n" +
                    "<body>\n" +
                    "<script>\n" +
                    "if(document.domain)\n" +
                    "{\n" +
                    "\tdocument.write(\"The base domain for this WebView is set to \" + document.domain);\n" +
                    "}\n" +
                    "else\n" +
                    "{\n" +
                    "\tdocument.write(\"<p style=\\\"color:black\\\">This file appears to be running in the <b>file</b> context, as document.domain is not set</p> <br>\");\n" +
                    "\tdocument.write(\"<p style=\\\"color:black\\\">If the BaseURL were set, the document.domain would be set to it's value</p>\")\n" +
                    "}\n" +
                    "</script>\n" +
                    "\n" +
                    "</body>\n" +
                    "</html>";
            webView.loadDataWithBaseURL("http://www.nsa.gov", contents, "text/html", "utf-8", "http://secbro.com/poc/fail.html");
        }else {
            webView.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE);
            webView.loadUrl(url);
        }



    }

}
