package org.owasp.goatdroid.fourgoats.javascriptinterfaces;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import org.owasp.goatdroid.fourgoats.activities.GenericWebViewActivity;

public class WebViewJSInterface
  implements Cloneable
{
  Context mContext;
  
  public WebViewJSInterface(Context paramContext)
  {
    this.mContext = paramContext;
  }
  
  public void launchWebView(String paramString)
  {
    Intent localIntent = new Intent(this.mContext, GenericWebViewActivity.class);
    Bundle localBundle = new Bundle();
    localBundle.putString("url", paramString);
    localIntent.putExtras(localBundle);
    this.mContext.startActivity(localIntent);
  }
}
