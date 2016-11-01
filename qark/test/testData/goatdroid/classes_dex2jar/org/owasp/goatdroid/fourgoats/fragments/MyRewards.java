package org.owasp.goatdroid.fourgoats.fragments;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import com.actionbarsherlock.app.SherlockFragment;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.rest.rewards.RewardsRequest;

public class MyRewards
  extends SherlockFragment
{
  Context context;
  ListView listView;
  TextView noRewardsTextView;
  
  public MyRewards() {}
  
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
      if ((localHashMap.get("rewardName") != null) && (localHashMap.get("rewardDescription") != null) && (localHashMap.get("timeEarned") != null)) {
        localArrayList.add((String)localHashMap.get("rewardName") + "\n" + (String)localHashMap.get("rewardDescription") + "\nEarned On: " + (String)localHashMap.get("timeEarned"));
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
    View localView = paramLayoutInflater.inflate(2130903083, paramViewGroup, false);
    this.listView = ((ListView)localView.findViewById(2130968657));
    this.noRewardsTextView = ((TextView)localView.findViewById(2130968656));
    new GetMyRewards(null).execute(new Void[] { null, null });
    return localView;
  }
  
  private class GetMyRewards
    extends AsyncTask<Void, Void, String[]>
  {
    private GetMyRewards() {}
    
    protected String[] doInBackground(Void... paramVarArgs)
    {
      new ArrayList();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(MyRewards.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      localUserInfoDBHelper.close();
      RewardsRequest localRewardsRequest = new RewardsRequest(MyRewards.this.context);
      try
      {
        if (str.equals(""))
        {
          Intent localIntent2 = new Intent(MyRewards.this.getActivity(), Login.class);
          MyRewards.this.startActivity(localIntent2);
          return new String[0];
        }
        ArrayList localArrayList = localRewardsRequest.getMyRewards(str);
        if (localArrayList.size() > 1) {
          return MyRewards.this.bindListView(localArrayList);
        }
        String[] arrayOfString = new String[0];
        return arrayOfString;
      }
      catch (Exception localException)
      {
        Intent localIntent1 = new Intent(MyRewards.this.getActivity(), Login.class);
        MyRewards.this.startActivity(localIntent1);
      }
      return new String[0];
    }
    
    public void onPostExecute(String[] paramArrayOfString)
    {
      if (MyRewards.this.getActivity() != null)
      {
        if (paramArrayOfString.length > 0) {
          MyRewards.this.listView.setAdapter(new ArrayAdapter(MyRewards.this.getActivity(), 17367043, paramArrayOfString));
        }
      }
      else {
        return;
      }
      MyRewards.this.noRewardsTextView.setVisibility(1);
    }
  }
}
