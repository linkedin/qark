package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.adapter.AvailableRewardsAdapter;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.rewards.RewardsRequest;

public class AvailableRewards
  extends SherlockFragment
{
  Context context;
  ListView listView;
  
  public AvailableRewards() {}
  
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
      if ((localHashMap.get("rewardName") != null) && (localHashMap.get("rewardDescription") != null) && (localHashMap.get("venueName") != null) && (localHashMap.get("latitude") != null) && (localHashMap.get("longitude") != null) && (localHashMap.get("checkinsRequired") != null)) {
        localArrayList.add((String)localHashMap.get("rewardName") + "\n" + (String)localHashMap.get("rewardDescription") + "\nVenue: " + (String)localHashMap.get("venueName") + "\nLatitude: " + (String)localHashMap.get("latitude") + "\nLongitude: " + (String)localHashMap.get("longitude") + "\nCheckins Required: " + (String)localHashMap.get("checkinsRequired"));
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
    View localView = paramLayoutInflater.inflate(2130903065, paramViewGroup, false);
    this.listView = ((ListView)localView.findViewById(2130968624));
    new GetAvailableRewards(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class GetAvailableRewards
    extends AsyncTask<Void, Void, String[]>
  {
    private GetAvailableRewards() {}
    
    protected String[] doInBackground(Void... paramVarArgs)
    {
      new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(AvailableRewards.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      RewardsRequest localRewardsRequest = new RewardsRequest(AvailableRewards.this.context);
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(AvailableRewards.this.getActivity(), Login.class);
          AvailableRewards.this.startActivity(localIntent2);
          return new String[0];
        }
        ArrayList localArrayList = localRewardsRequest.getAllRewards(str);
        if (localArrayList.size() > 1) {
          return AvailableRewards.this.bindListView(localArrayList);
        }
        Utils.makeToast(AvailableRewards.this.context, "Something weird happened", 1);
        String[] arrayOfString = new String[0];
        return arrayOfString;
      }
      catch (Exception localException)
      {
        Intent localIntent1 = new Intent(AvailableRewards.this.getActivity(), Login.class);
        AvailableRewards.this.startActivity(localIntent1);
      }
      return new String[0];
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (AvailableRewards.this.getActivity() != null) {
        AvailableRewards.this.listView.setAdapter(new AvailableRewardsAdapter(AvailableRewards.this.getActivity(), paramArrayOfString));
      }
    }
  }
}
