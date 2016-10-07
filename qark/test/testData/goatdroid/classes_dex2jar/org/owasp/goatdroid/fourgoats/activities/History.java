package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.TextView;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.ViewCheckinJSInterface;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.history.HistoryRequest;

public class History
  extends BaseActivity
{
  Bundle bundle;
  Context context;
  TextView noCheckinsTextView;
  WebView webview;
  
  public History() {}
  
  public String generateHistoryHTML(ArrayList<HashMap<String, String>> paramArrayList)
  {
    String str = "<html><head><style type=\"text/css\">body{color: white; background-color: #000;}</style></head><body>";
    Iterator localIterator;
    if (paramArrayList.size() > 1)
    {
      localIterator = paramArrayList.iterator();
      if (localIterator.hasNext()) {}
    }
    for (;;)
    {
      return str + "</body></html>";
      HashMap localHashMap = (HashMap)localIterator.next();
      if ((localHashMap.get("venueName") == null) || (localHashMap.get("checkinID") == null) || (localHashMap.get("dateTime") == null) || (localHashMap.get("latitude") == null) || (localHashMap.get("longitude") == null) || (localHashMap.get("venueWebsite") == null)) {
        break;
      }
      String[] arrayOfString = ((String)localHashMap.get("dateTime")).split(" ");
      str = str + "<p><b>" + (String)localHashMap.get("venueName") + "</b><br><b>Date:</b> " + arrayOfString[0] + "<br><b>Time:</b> " + arrayOfString[1] + "<br><b>Latitude:</b> " + (String)localHashMap.get("latitude") + "<br><b>Longitude:</b> " + (String)localHashMap.get("longitude") + "<br>" + "<button style=\"color: white; background-color:#2E9AFE\" " + "type=\"button\" onclick=\"window.jsInterface.launchViewCheckinActivity('" + (String)localHashMap.get("venueName") + "','" + (String)localHashMap.get("venueWebsite") + "','" + (String)localHashMap.get("dateTime") + "','" + (String)localHashMap.get("latitude") + "','" + (String)localHashMap.get("longitude") + "','" + (String)localHashMap.get("checkinID") + "')\">View Checkin</button><br>";
      break;
      str = str + "<p><p>You have not checked in yet, grasshopper";
    }
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903078);
    this.context = getApplicationContext();
    this.webview = ((WebView)findViewById(2130968651));
    this.bundle = getIntent().getExtras();
    WebSettings localWebSettings = this.webview.getSettings();
    this.webview.addJavascriptInterface(new ViewCheckinJSInterface(this), "jsInterface");
    localWebSettings.setJavaScriptEnabled(true);
    this.noCheckinsTextView = ((TextView)findViewById(2130968650));
    new GetHistory(null).execute(new Void[] { null, null });
  }
  
  private class GetHistory
    extends AsyncTask<Void, Void, ArrayList<HashMap<String, String>>>
  {
    String errors = "";
    String htmlResponse = "";
    boolean isSelf = false;
    boolean success = false;
    
    private GetHistory() {}
    
    protected ArrayList<HashMap<String, String>> doInBackground(Void... paramVarArgs)
    {
      ArrayList localArrayList = new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(History.this.context);
      HistoryRequest localHistoryRequest = new HistoryRequest(History.this.context);
      try
      {
        String str = localUserInfoDBHelper.getSessionToken();
        if (str.equals("")) {
          this.errors = "Invalid session";
        }
        for (;;)
        {
          if (localUserInfoDBHelper.getUserName().equals(History.this.bundle.getString("userName"))) {
            this.isSelf = true;
          }
          return localArrayList;
          localArrayList = localHistoryRequest.getUserHistory(str, History.this.bundle.getString("userName"));
          if (!((String)((HashMap)localArrayList.get(0)).get("success")).equals("true")) {
            break;
          }
          this.success = true;
          this.htmlResponse = History.this.generateHistoryHTML(localArrayList);
        }
      }
      catch (Exception localException)
      {
        for (;;)
        {
          this.errors = "Could not contact the remote service";
          return localArrayList;
          this.errors = ((String)((HashMap)localArrayList.get(0)).get("errors"));
        }
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void onPostExecute(ArrayList<HashMap<String, String>> paramArrayList)
    {
      if (this.success)
      {
        History.this.webview.loadData(this.htmlResponse, "text/html", "UTF-8");
        return;
      }
      if (this.errors.equals("Invalid session"))
      {
        History.this.launchLogin();
        return;
      }
      if (this.errors.equals("You have never checked in"))
      {
        if (this.isSelf) {
          History.this.noCheckinsTextView.setText("You have never checked in anywhere. You should try it sometime, it's fun!");
        }
        for (;;)
        {
          History.this.noCheckinsTextView.setVisibility(1);
          return;
          History.this.noCheckinsTextView.setText("This person has never checked in. Pretty boring, if you ask me!");
        }
      }
      Utils.makeToast(History.this.context, this.errors, 1);
    }
  }
}
