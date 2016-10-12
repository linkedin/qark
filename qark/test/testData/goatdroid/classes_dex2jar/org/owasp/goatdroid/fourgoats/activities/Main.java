/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.app.Activity
 *  android.content.Context
 *  android.content.Intent
 *  android.os.AsyncTask
 *  android.os.Bundle
 */
package org.owasp.goatdroid.fourgoats.activities;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import org.owasp.goatdroid.fourgoats.activities.AdminHome;
import org.owasp.goatdroid.fourgoats.activities.Home;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.rest.login.LoginRequest;

public class Main
extends Activity {
    Context context;

    public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        this.setContentView(2130903080);
        this.context = this.getApplicationContext();
        new CheckSessionToken().execute((Object[])new Void[]{null, null});
    }

}

