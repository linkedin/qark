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
import org.owasp.goatdroid.fourgoats.activities.ViewFriendRequest;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.friends.FriendRequest;

public class PendingFriendRequests
  extends SherlockFragment
{
  Bundle bundle;
  ListView listView;
  TextView noPendingFriendRequestsTextView;
  
  public PendingFriendRequests() {}
  
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
      if ((localHashMap.get("userName") != null) && (localHashMap.get("firstName") != null) && (localHashMap.get("lastName") != null)) {
        localArrayList.add((String)localHashMap.get("userName") + "\n" + (String)localHashMap.get("firstName") + " " + (String)localHashMap.get("lastName"));
      }
    }
  }
  
  public View onCreateView(LayoutInflater paramLayoutInflater, ViewGroup paramViewGroup, Bundle paramBundle)
  {
    View localView = paramLayoutInflater.inflate(2130903084, paramViewGroup, false);
    this.noPendingFriendRequestsTextView = ((TextView)localView.findViewById(2130968658));
    this.listView = ((ListView)localView.findViewById(2130968659));
    this.listView.setOnItemClickListener(new AdapterView.OnItemClickListener()
    {
      public void onItemClick(AdapterView<?> paramAnonymousAdapterView, View paramAnonymousView, int paramAnonymousInt, long paramAnonymousLong)
      {
        String[] arrayOfString = ((String)PendingFriendRequests.this.listView.getItemAtPosition(paramAnonymousInt)).split("\n");
        Intent localIntent = new Intent(PendingFriendRequests.this.getActivity(), ViewFriendRequest.class);
        Bundle localBundle = new Bundle();
        localBundle.putString("userName", arrayOfString[0]);
        localBundle.putString("fullName", arrayOfString[1]);
        localIntent.putExtras(localBundle);
        PendingFriendRequests.this.startActivity(localIntent);
      }
    });
    new GetPendingFriendRequests(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class GetPendingFriendRequests
    extends AsyncTask<Void, Void, String[]>
  {
    private GetPendingFriendRequests() {}
    
    protected String[] doInBackground(Void... paramVarArgs)
    {
      new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(PendingFriendRequests.this.getActivity());
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      FriendRequest localFriendRequest = new FriendRequest(PendingFriendRequests.this.getActivity());
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(PendingFriendRequests.this.getActivity(), Login.class);
          PendingFriendRequests.this.startActivity(localIntent2);
          return new String[0];
        }
        ArrayList localArrayList = localFriendRequest.getPendingFriendRequests(str);
        if (localArrayList.size() > 0)
        {
          if (((String)((HashMap)localArrayList.get(0)).get("success")).equals("true"))
          {
            if (localArrayList.size() > 1) {
              return PendingFriendRequests.this.bindListView(localArrayList);
            }
            return new String[0];
          }
          Utils.makeToast(PendingFriendRequests.this.getActivity(), "Something weird happened", 1);
          return new String[0];
        }
        String[] arrayOfString = new String[0];
        return arrayOfString;
      }
      catch (Exception localException)
      {
        Intent localIntent1 = new Intent(PendingFriendRequests.this.getActivity(), Login.class);
        PendingFriendRequests.this.startActivity(localIntent1);
      }
      return new String[0];
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (PendingFriendRequests.this.getActivity() != null)
      {
        if (paramArrayOfString.length > 0) {
          PendingFriendRequests.this.listView.setAdapter(new ArrayAdapter(PendingFriendRequests.this.getActivity(), 17367043, paramArrayOfString));
        }
      }
      else {
        return;
      }
      PendingFriendRequests.this.noPendingFriendRequestsTextView.setVisibility(1);
    }
  }
}
