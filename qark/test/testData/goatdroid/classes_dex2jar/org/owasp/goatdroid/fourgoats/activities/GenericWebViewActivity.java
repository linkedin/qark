package org.owasp.goatdroid.fourgoats.activities;

import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;

public class GenericWebViewActivity
  extends BaseActivity
{
  public GenericWebViewActivity() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903077);
    WebView localWebView = (WebView)findViewById(2130968649);
    localWebView.getSettings().setJavaScriptEnabled(true);
    localWebView.loadUrl(getIntent().getExtras().getString("url"));
  }
}
