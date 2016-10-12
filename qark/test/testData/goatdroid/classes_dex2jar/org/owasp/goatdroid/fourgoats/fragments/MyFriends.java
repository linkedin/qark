package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.activities.ViewProfile;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.friends.FriendRequest;

public class MyFriends
  extends SherlockFragment
{
  ListView listView;
  TextView noFriendsTextView;
  
  public MyFriends() {}
  
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
    View localView = paramLayoutInflater.inflate(2130903082, paramViewGroup, false);
    this.noFriendsTextView = ((TextView)localView.findViewById(2130968654));
    this.listView = ((ListView)localView.findViewById(2130968655));
    this.listView.setOnItemClickListener(new AdapterView.OnItemClickListener()
    {
      public void onItemClick(AdapterView<?> paramAnonymousAdapterView, View paramAnonymousView, int paramAnonymousInt, long paramAnonymousLong)
      {
        String str = ((String)MyFriends.this.listView.getItemAtPosition(paramAnonymousInt)).split("\n")[1];
        Intent localIntent = new Intent(MyFriends.this.getActivity(), ViewProfile.class);
        Bundle localBundle = new Bundle();
        localBundle.putString("userName", str);
        localIntent.putExtras(localBundle);
        MyFriends.this.startActivity(localIntent);
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
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(MyFriends.this.getActivity());
      String str = localUserInfoDBHelper.getSessionToken();
      FriendRequest localFriendRequest = new FriendRequest(MyFriends.this.getActivity());
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(MyFriends.this.getActivity(), Login.class);
          MyFriends.this.startActivity(localIntent2);
          String[] arrayOfString2 = new String[0];
          return arrayOfString2;
        }
        ArrayList localArrayList = localFriendRequest.getFriends(str);
        if (localArrayList.size() > 0)
        {
          if (((String)((HashMap)localArrayList.get(0)).get("success")).equals("true"))
          {
            String[] arrayOfString5 = MyFriends.this.bindListView(localArrayList);
            return arrayOfString5;
          }
          String[] arrayOfString4 = new String[0];
          return arrayOfString4;
        }
        Utils.makeToast(MyFriends.this.getActivity(), "Something weird happened", 1);
        String[] arrayOfString3 = new String[0];
        return arrayOfString3;
      }
      catch (Exception localException)
      {
        Intent localIntent1 = new Intent(MyFriends.this.getActivity(), Login.class);
        MyFriends.this.startActivity(localIntent1);
        String[] arrayOfString1 = new String[0];
        return arrayOfString1;
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (MyFriends.this.getActivity() != null)
      {
        if (paramArrayOfString.length > 0) {
          MyFriends.this.listView.setAdapter(new ArrayAdapter(MyFriends.this.getActivity(), 17367043, paramArrayOfString));
        }
      }
      else {
        return;
      }
      MyFriends.this.noFriendsTextView.setVisibility(1);
    }
  }
}
