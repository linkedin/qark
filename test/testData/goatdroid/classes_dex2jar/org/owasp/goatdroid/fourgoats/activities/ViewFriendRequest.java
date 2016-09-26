/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  android.content.Intent
 *  android.os.AsyncTask
 *  android.os.Bundle
 *  android.view.View
 *  android.widget.TextView
 */
package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.friends.FriendRequest;

public class ViewFriendRequest
extends BaseActivity {
    Bundle bundle;
    Context context;
    TextView fullName;
    TextView userName;

    public void acceptFriendRequest(View view) {
        new AcceptRequestAsyncTask().execute((Object[])new Void[]{null, null});
    }

    public void denyFriendRequest(View view) {
        new DenyRequestAsyncTask().execute((Object[])new Void[]{null, null});
    }

    @Override
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        this.setContentView(2130903075);
        this.context = this.getApplicationContext();
        this.bundle = this.getIntent().getExtras();
        this.userName = (TextView)this.findViewById(2130968646);
        this.fullName = (TextView)this.findViewById(2130968647);
        this.userName.setText((CharSequence)("Username: " + this.bundle.getString("userName")));
        this.fullName.setText((CharSequence)("Full Name: " + this.bundle.getString("fullName")));
    }

}

