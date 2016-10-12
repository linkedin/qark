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
import org.owasp.goatdroid.fourgoats.activities.AdminHome;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.admin.AdminRequest;

public class DoAdminDeleteUser
extends BaseActivity {
    Bundle bundle;
    Context context;
    TextView userNameTextView;

    public void doDeleteUser(View view) {
        new DeleteUserAsyncTask().execute((Object[])new Void[]{null, null});
    }

    public void launchAdminHome() {
        this.startActivity(new Intent((Context)this, (Class)AdminHome.class));
    }

    public void launchAdminHome(View view) {
        this.startActivity(new Intent((Context)this, (Class)AdminHome.class));
    }

    public void launchHome() {
        this.startActivity(new Intent(this.context, (Class)AdminHome.class));
    }

    public void launchLogin() {
        this.startActivity(new Intent(this.context, (Class)Login.class));
    }

    @Override
    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        this.setContentView(2130903073);
        this.context = this.getApplicationContext();
        this.bundle = this.getIntent().getExtras();
        this.userNameTextView = (TextView)this.findViewById(2130968640);
        this.userNameTextView.setText((CharSequence)this.bundle.getString("userName"));
    }

}

