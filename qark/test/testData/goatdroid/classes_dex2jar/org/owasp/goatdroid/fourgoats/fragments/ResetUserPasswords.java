package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ListView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.DoAdminPasswordReset;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.adapter.SearchForFriendsAdapter;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.admin.AdminRequest;

public class ResetUserPasswords
  extends SherlockFragment
{
  Context context;
  ListView listView;
  
  public ResetUserPasswords() {}
  
  public String[] bindListView(ArrayList<HashMap<String, String>> paramArrayList)
  {
    ArrayList localArrayList = new ArrayList();
    Iterator localIterator = paramArrayList.iterator();
    for (;;)
    {
      if (!localIterator.hasNext()) {
        return (String[])localArrayList.toArray(new String[localArrayList.size()]);
      }
      HashMap localHashMap = (HashMap)localIterator.next();
      if ((localHashMap.get("firstName") != null) && (localHashMap.get("lastName") != null) && (localHashMap.get("userName") != null)) {
        localArrayList.add((String)localHashMap.get("firstName") + " " + (String)localHashMap.get("lastName") + "\n" + (String)localHashMap.get("userName"));
      }
    }
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    this.context = getActivity();
  }
  
  public View onCreateView(LayoutInflater paramLayoutInflater, ViewGroup paramViewGroup, Bundle paramBundle)
  {
    View localView = paramLayoutInflater.inflate(2130903088, paramViewGroup, false);
    this.listView = ((ListView)localView.findViewById(2130968633));
    this.listView.setOnItemClickListener(new AdapterView.OnItemClickListener()
    {
      public void onItemClick(AdapterView<?> paramAnonymousAdapterView, View paramAnonymousView, int paramAnonymousInt, long paramAnonymousLong)
      {
        String str = ((String)ResetUserPasswords.this.listView.getItemAtPosition(paramAnonymousInt)).split("\n")[1];
        Intent localIntent = new Intent(ResetUserPasswords.this.getActivity(), DoAdminPasswordReset.class);
        Bundle localBundle = new Bundle();
        localBundle.putString("userName", str);
        localIntent.putExtras(localBundle);
        ResetUserPasswords.this.startActivity(localIntent);
      }
    });
    new SearchForUsers(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class SearchForUsers
    extends AsyncTask<Void, Void, String[]>
  {
    private SearchForUsers() {}
    
    protected String[] doInBackground(Void... paramVarArgs)
    {
      new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(ResetUserPasswords.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      AdminRequest localAdminRequest = new AdminRequest(ResetUserPasswords.this.context);
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(ResetUserPasswords.this.getActivity(), Login.class);
          ResetUserPasswords.this.startActivity(localIntent2);
        }
        for (;;)
        {
          return new String[0];
          ArrayList localArrayList = localAdminRequest.getUsers(str);
          if (localArrayList.size() <= 0) {
            break;
          }
          if (((String)((HashMap)localArrayList.get(0)).get("success")).equals("true")) {
            return ResetUserPasswords.this.bindListView(localArrayList);
          }
          Utils.makeToast(ResetUserPasswords.this.context, (String)((HashMap)localArrayList.get(1)).get("errors"), 1);
        }
      }
      catch (Exception localException)
      {
        for (;;)
        {
          Intent localIntent1 = new Intent(ResetUserPasswords.this.getActivity(), Login.class);
          ResetUserPasswords.this.startActivity(localIntent1);
          continue;
          Utils.makeToast(ResetUserPasswords.this.context, "Something weird happened", 1);
        }
      }
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (ResetUserPasswords.this.getActivity() != null) {
        ResetUserPasswords.this.listView.setAdapter(new SearchForFriendsAdapter(ResetUserPasswords.this.getActivity(), paramArrayOfString));
      }
    }
  }
}
