/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  android.content.Intent
 *  android.os.AsyncTask
 *  android.os.Bundle
 *  android.text.Editable
 *  android.view.View
 *  android.widget.EditText
 */
package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.activities.AdminHome;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.admin.AdminRequest;

public class DoAdminPasswordReset
extends BaseActivity {
    Bundle bundle;
    Context context;
    EditText passwordConfirmEditText;
    EditText passwordEditText;
    EditText userNameEditText;

    public void doPasswordReset(View view) {
        if (this.passwordEditText.getText().toString().equals(this.passwordConfirmEditText.getText().toString())) {
            new ResetPasswordAsyncTask().execute((Object[])new Void[]{null, null});
            return;
        }
        Utils.makeToast(this.context, "Passwords didn't match", 1);
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
        this.setContentView(2130903074);
        this.context = this.getApplicationContext();
        this.userNameEditText = (EditText)this.findViewById(2130968643);
        this.passwordEditText = (EditText)this.findViewById(2130968644);
        this.passwordConfirmEditText = (EditText)this.findViewById(2130968645);
        this.bundle = this.getIntent().getExtras();
        this.userNameEditText.setText((CharSequence)this.bundle.getString("userName"));
    }

}

