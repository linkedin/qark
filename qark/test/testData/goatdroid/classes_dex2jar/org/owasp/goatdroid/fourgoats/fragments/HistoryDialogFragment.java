package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.TextView;
import com.actionbarsherlock.app.SherlockDialogFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.javascriptinterfaces.ViewCheckinJSInterface;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.history.HistoryRequest;

public class HistoryDialogFragment
  extends SherlockDialogFragment
{
  Context context;
  TextView noCheckinsTextView;
  WebView webview;
  
  public HistoryDialogFragment() {}
  
  public String generateHistoryHTML(ArrayList<HashMap<String, String>> paramArrayList)
  {
    String str1 = "";
    String str2 = "";
    String str3 = "";
    String str4 = "";
    String str5 = "";
    String str6 = "";
    String str7 = "";
    if (paramArrayList.size() > 1)
    {
      Iterator localIterator = paramArrayList.iterator();
      for (;;)
      {
        if (!localIterator.hasNext()) {
          return str1;
        }
        HashMap localHashMap = (HashMap)localIterator.next();
        if (localHashMap.get("venueName") != null) {
          str2 = (String)localHashMap.get("venueName");
        }
        if (localHashMap.get("checkinID") != null) {
          str3 = (String)localHashMap.get("checkinID");
        }
        if (localHashMap.get("dateTime") != null) {
          str4 = (String)localHashMap.get("dateTime");
        }
        if (localHashMap.get("latitude") != null) {
          str5 = (String)localHashMap.get("latitude");
        }
        if (localHashMap.get("longitude") != null) {
          str6 = (String)localHashMap.get("longitude");
        }
        if (localHashMap.get("venueWebsite") != null) {
          str7 = (String)localHashMap.get("venueWebsite");
        }
        String[] arrayOfString = str4.split(" ");
        str1 = str1 + "<p><b>" + str2 + "</b><br><b>Date:</b> " + arrayOfString[0] + "<br><b>Time:</b> " + arrayOfString[1] + "<br><b>Latitude:</b> " + str5 + "<br><b>Longitude:</b> " + str6 + "<br>" + "<button style=\"color: white; background-color:#2E9AFE\" " + "type=\"button\" onclick=\"window.jsInterface.launchViewCheckinActivity('" + str2 + "','" + str7 + "','" + str4 + "','" + str5 + "','" + str6 + "','" + str3 + "')\">View Checkin</button><br>";
      }
    }
    return str1 + "<p><p>You have not checked in yet, grasshopper";
  }
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    this.context = getActivity();
  }
  
  public View onCreateView(LayoutInflater paramLayoutInflater, ViewGroup paramViewGroup, Bundle paramBundle)
  {
    View localView = paramLayoutInflater.inflate(2130903078, paramViewGroup, false);
    this.webview = ((WebView)localView.findViewById(2130968651));
    WebSettings localWebSettings = this.webview.getSettings();
    this.webview.addJavascriptInterface(new ViewCheckinJSInterface(this.context), "jsInterface");
    localWebSettings.setJavaScriptEnabled(true);
    this.noCheckinsTextView = ((TextView)localView.findViewById(2130968650));
    new GetHistory(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class GetHistory
    extends AsyncTask<Void, Void, ArrayList<HashMap<String, String>>>
  {
    String errors = "";
    String htmlResponse = "";
    boolean success = false;
    
    private GetHistory() {}
    
    protected ArrayList<HashMap<String, String>> doInBackground(Void... paramVarArgs)
    {
      ArrayList localArrayList = new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(HistoryDialogFragment.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      HistoryRequest localHistoryRequest = new HistoryRequest(HistoryDialogFragment.this.context);
      try
      {
        if (str.equals("")) {
          this.errors = "Invalid session";
        }
        for (;;)
        {
          return localArrayList;
          localArrayList = localHistoryRequest.getHistory(str);
          if (!((String)((HashMap)localArrayList.get(0)).get("success")).equals("true")) {
            break;
          }
          this.htmlResponse = HistoryDialogFragment.this.generateHistoryHTML(localArrayList);
          this.success = true;
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
        HistoryDialogFragment.this.webview.loadData(this.htmlResponse, "text/html", "UTF-8");
        return;
      }
      if (this.errors.equals("Invalid session"))
      {
        HistoryDialogFragment.this.launchLogin();
        return;
      }
      if (this.errors.equals("You have never checked in"))
      {
        HistoryDialogFragment.this.noCheckinsTextView.setVisibility(1);
        return;
      }
      Utils.makeToast(HistoryDialogFragment.this.context, this.errors, 1);
    }
  }
}
