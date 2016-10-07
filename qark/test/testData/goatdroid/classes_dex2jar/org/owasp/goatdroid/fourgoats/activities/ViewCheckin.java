package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.SmsJSInterface;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.ViewCheckinJSInterface;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.WebViewJSInterface;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.viewcheckin.ViewCheckinRequest;

public class ViewCheckin
  extends BaseActivity
{
  Bundle bundle;
  Context context;
  String sessionToken;
  WebView webview;
  
  public ViewCheckin() {}
  
  public String generateComments(HashMap<String, String> paramHashMap)
  {
    String str1 = "";
    int i;
    if (paramHashMap.size() > 3)
    {
      if (-3 + paramHashMap.size() / 6 != -2) {
        break label59;
      }
      i = 1;
      str1 = str1 + "<b><big>Comments:</big></b><p>";
    }
    for (int j = 0;; j++)
    {
      if (j >= i)
      {
        return str1;
        label59:
        i = paramHashMap.size() / 6;
        break;
      }
      String str2 = (String)paramHashMap.get("firstName" + j);
      String str3 = (String)paramHashMap.get("lastName" + j);
      String[] arrayOfString = ((String)paramHashMap.get("dateTime" + j)).split(" ");
      String str4 = arrayOfString[0];
      String str5 = arrayOfString[1];
      String str6 = (String)paramHashMap.get("comment" + j);
      str1 = new StringBuilder(String.valueOf(new StringBuilder(String.valueOf(str1)).append("<p><b>").append(str2).append(" ").append(str3).append("</b><br>").append(str4).append("<br>").append(str5).append("<br>").toString())).append("<b>\"").append(str6).append("\"</b><br>").toString() + "<button style=\"color: white; background-color:#2E9AFE\" type=\"button\" onclick=\"window.viewCheckinJSInterface.deleteComment('" + (String)paramHashMap.get(new StringBuilder("commentID").append(j).toString()) + "','" + this.bundle.getString("venueName") + "','" + this.bundle.getString("venueWebsite") + "','" + this.bundle.getString("dateTime") + "','" + this.bundle.getString("latitude") + "','" + this.bundle.getString("longitude") + "','" + this.bundle.getString("checkinID") + "')\">" + "Delete Comment</button><br>";
    }
  }
  
  public String generateViewCheckinHTML(HashMap<String, String> paramHashMap)
  {
    String str = "" + "<p><b>" + this.bundle.getString("venueName") + "</b></p>";
    String[] arrayOfString = this.bundle.getString("dateTime").split(" ");
    return new StringBuilder(String.valueOf(new StringBuilder(String.valueOf(new StringBuilder(String.valueOf(new StringBuilder(String.valueOf(str)).append("<p><b>Date:</b> ").append(arrayOfString[0]).append(" <b>Time:</b> ").append(arrayOfString[1]).append("</p>").toString())).append("<button style=\"color: white; background-color:#2E9AFE\" type=\"button\" onclick=\"window.webViewJSInterface.launchWebView('").append(this.bundle.getString("venueWebsite")).append("')\">").append("Visit Website</button><br><br>").toString())).append("<button style=\"color: white; background-color:#2E9AFE\" type=\"button\" onclick=\"window.smsJSInterface.launchSendSMSActivity('").append(this.bundle.getString("venueName")).append("','").append(this.bundle.getString("dateTime")).append("')\">").append("Text This To A Friend</button><p>").toString())).append("<button style=\"color: white; background-color:#2E9AFE\" type=\"button\" onclick=\"window.viewCheckinJSInterface.launchDoCommentActivity('").append(this.bundle.getString("venueName")).append("','").append(this.bundle.getString("venueWebsite")).append("','").append(this.bundle.getString("dateTime")).append("','").append(this.bundle.getString("latitude")).append("','").append(this.bundle.getString("longitude")).append("','").append(this.bundle.getString("checkinID")).append("')\">").append("Leave a Comment</button><br><br>").toString() + generateComments(paramHashMap);
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903097);
    this.context = getApplicationContext();
    this.bundle = getIntent().getExtras();
    this.webview = ((WebView)findViewById(2130968678));
    this.webview.getSettings().setJavaScriptEnabled(true);
    this.webview.addJavascriptInterface(new SmsJSInterface(this), "smsJSInterface");
    this.webview.addJavascriptInterface(new ViewCheckinJSInterface(this), "viewCheckinJSInterface");
    this.webview.addJavascriptInterface(new WebViewJSInterface(this), "webViewJSInterface");
    new GetCommentData(null).execute(new Void[] { null, null });
  }
  
  private class GetCommentData
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private GetCommentData() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      HashMap localHashMap = new HashMap();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(ViewCheckin.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      ViewCheckinRequest localViewCheckinRequest = new ViewCheckinRequest(ViewCheckin.this.context);
      try
      {
        localHashMap = localViewCheckinRequest.getCheckin(str, ViewCheckin.this.bundle.getString("checkinID"));
        if (((String)localHashMap.get("success")).equals("true")) {
          localHashMap.put("htmlResponse", ViewCheckin.this.generateViewCheckinHTML(localHashMap));
        }
        return localHashMap;
      }
      catch (Exception localException)
      {
        localHashMap.put("errors", localException.getMessage());
        localHashMap.put("success", "false");
        return localHashMap;
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        ViewCheckin.this.webview.loadData((String)paramHashMap.get("htmlResponse"), "text/html", "UTF-8");
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        ViewCheckin.this.launchLogin();
        return;
      }
      Utils.makeToast(ViewCheckin.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
