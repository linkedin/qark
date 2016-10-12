package org.owasp.goatdroid.fourgoats.fragments;

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
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.activities.ViewProfile;
import org.owasp.goatdroid.fourgoats.adapter.SearchForFriendsAdapter;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.searchforfriends.SearchForFriendsRequest;

public class SearchForFriends
  extends SherlockFragment
{
  ListView listView;
  
  public SearchForFriends() {}
  
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
      if ((localHashMap.get("firstName") != null) && (localHashMap.get("lastName") != null) && (localHashMap.get("userID") != null) && (localHashMap.get("userName") != null)) {
        localArrayList.add((String)localHashMap.get("firstName") + " " + (String)localHashMap.get("lastName") + "\n" + (String)localHashMap.get("userName"));
      }
    }
  }
  
  public View onCreateView(LayoutInflater paramLayoutInflater, ViewGroup paramViewGroup, Bundle paramBundle)
  {
    View localView = paramLayoutInflater.inflate(2130903090, paramViewGroup, false);
    this.listView = ((ListView)localView.findViewById(2130968673));
    this.listView.setOnItemClickListener(new AdapterView.OnItemClickListener()
    {
      public void onItemClick(AdapterView<?> paramAnonymousAdapterView, View paramAnonymousView, int paramAnonymousInt, long paramAnonymousLong)
      {
        String str = ((String)SearchForFriends.this.listView.getItemAtPosition(paramAnonymousInt)).split("\n")[1];
        Intent localIntent = new Intent(SearchForFriends.this.getActivity(), ViewProfile.class);
        Bundle localBundle = new Bundle();
        localBundle.putString("userName", str);
        localIntent.putExtras(localBundle);
        SearchForFriends.this.startActivity(localIntent);
      }
    });
    new SearchFriends(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class SearchFriends
    extends AsyncTask<Void, Void, String[]>
  {
    private SearchFriends() {}
    
    protected String[] doInBackground(Void... paramVarArgs)
    {
      new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(SearchForFriends.this.getActivity());
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      SearchForFriendsRequest localSearchForFriendsRequest = new SearchForFriendsRequest(SearchForFriends.this.getActivity());
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(SearchForFriends.this.getActivity(), Login.class);
          SearchForFriends.this.startActivity(localIntent2);
          return new String[0];
        }
        ArrayList localArrayList = localSearchForFriendsRequest.getUsers(str);
        if (localArrayList.size() > 0)
        {
          if (((String)((HashMap)localArrayList.get(0)).get("success")).equals("true")) {
            return SearchForFriends.this.bindListView(localArrayList);
          }
          Utils.makeToast(SearchForFriends.this.getActivity(), "Something weird happened", 1);
          return new String[0];
        }
        String[] arrayOfString = new String[0];
        return arrayOfString;
      }
      catch (Exception localException)
      {
        Intent localIntent1 = new Intent(SearchForFriends.this.getActivity(), Login.class);
        SearchForFriends.this.startActivity(localIntent1);
      }
      return new String[0];
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (SearchForFriends.this.getActivity() != null) {
        SearchForFriends.this.listView.setAdapter(new SearchForFriendsAdapter(SearchForFriends.this.getActivity(), paramArrayOfString));
      }
    }
  }
}
