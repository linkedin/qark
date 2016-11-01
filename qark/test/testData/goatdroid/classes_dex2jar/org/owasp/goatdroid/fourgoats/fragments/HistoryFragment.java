/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  android.content.Intent
 *  android.graphics.Color
 *  android.os.AsyncTask
 *  android.os.Bundle
 *  android.view.LayoutInflater
 *  android.view.View
 *  android.view.ViewGroup
 *  android.webkit.WebSettings
 *  android.webkit.WebView
 *  android.widget.TextView
 */
package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.TextView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.ViewCheckinJSInterface;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.history.HistoryRequest;

public class HistoryFragment
extends SherlockFragment {
    Context context;
    TextView noCheckinsTextView;
    WebView webview;

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    public String generateHistoryHTML(ArrayList<HashMap<String, String>> arrayList) {
        String string2 = "<html><head><style type=\"text/css\">body{color: white; background-color: #000;}</style></head><body>";
        if (arrayList.size() > 1) {
            Iterator<HashMap<String, String>> iterator = arrayList.iterator();
            do {
                if (!iterator.hasNext()) {
                    do {
                        return String.valueOf(string2) + "</body></html>";
                        break;
                    } while (true);
                }
                HashMap<String, String> hashMap = iterator.next();
                if (hashMap.get("venueName") == null || hashMap.get("checkinID") == null || hashMap.get("dateTime") == null || hashMap.get("latitude") == null || hashMap.get("longitude") == null || hashMap.get("venueWebsite") == null) continue;
                String[] arrstring = hashMap.get("dateTime").split(" ");
                string2 = String.valueOf(string2) + "<p><b>" + hashMap.get("venueName") + "</b><br><b>Date:</b> " + arrstring[0] + "<br><b>Time:</b> " + arrstring[1] + "<br><b>Latitude:</b> " + hashMap.get("latitude") + "<br><b>Longitude:</b> " + hashMap.get("longitude") + "<br>" + "<button style=\"color: white; background-color:#2E9AFE\" " + "type=\"button\" onclick=\"window.jsInterface.launchViewCheckinActivity('" + hashMap.get("venueName") + "','" + hashMap.get("venueWebsite") + "','" + hashMap.get("dateTime") + "','" + hashMap.get("latitude") + "','" + hashMap.get("longitude") + "','" + hashMap.get("checkinID") + "')\">View Checkin</button><br>";
            } while (true);
        }
        string2 = String.valueOf(string2) + "<p><p>You have not checked in yet, grasshopper";
        return String.valueOf(string2) + "</body></html>";
    }

    public void launchLogin() {
        this.startActivity(new Intent(this.context, (Class)Login.class));
    }

    @Override
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        this.context = this.getActivity();
    }

    @Override
    public View onCreateView(LayoutInflater layoutInflater, ViewGroup viewGroup, Bundle bundle) {
        View view = layoutInflater.inflate(2130903078, viewGroup, false);
        this.webview = (WebView)view.findViewById(2130968651);
        WebSettings webSettings = this.webview.getSettings();
        this.webview.addJavascriptInterface((Object)new ViewCheckinJSInterface(this.context), "jsInterface");
        this.webview.setBackgroundColor(Color.parseColor((String)"#000000"));
        webSettings.setJavaScriptEnabled(true);
        this.noCheckinsTextView = (TextView)view.findViewById(2130968650);
        new GetHistory().execute((Object[])new Void[]{null, null});
        return view;
    }

}

