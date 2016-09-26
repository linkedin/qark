package org.owasp.goatdroid.fourgoats.base;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build.VERSION;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.view.ViewPager;
import android.support.v4.view.ViewPager.OnPageChangeListener;
import android.widget.TextView;
import com.actionbarsherlock.app.ActionBar.Tab;
import com.actionbarsherlock.app.ActionBar.TabListener;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuInflater;
import com.actionbarsherlock.view.MenuItem;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.activities.About;
import org.owasp.goatdroid.fourgoats.activities.AdminHome;
import org.owasp.goatdroid.fourgoats.activities.Home;
import org.owasp.goatdroid.fourgoats.activities.Login;
import org.owasp.goatdroid.fourgoats.activities.Preferences;
import org.owasp.goatdroid.fourgoats.activities.ViewProfile;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.login.LoginRequest;

public class BaseTabsViewPagerActivity
  extends SherlockFragmentActivity
{
  protected Context context;
  protected TabsAdapter mTabsAdapter;
  ViewPager mViewPager;
  TextView tabCenter;
  TextView tabText;
  
  public BaseTabsViewPagerActivity() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903096);
    this.mViewPager = ((ViewPager)findViewById(2130968677));
    getSupportActionBar().setNavigationMode(2);
    this.mTabsAdapter = new TabsAdapter(this, this.mViewPager);
    getSupportActionBar().setIcon(2130837628);
    if (Build.VERSION.SDK_INT >= 14)
    {
      getActionBar().setHomeButtonEnabled(true);
      getActionBar().setDisplayHomeAsUpEnabled(true);
      return;
    }
    getSupportActionBar().setHomeButtonEnabled(true);
    getSupportActionBar().setDisplayHomeAsUpEnabled(true);
  }
  
  public boolean onCreateOptionsMenu(Menu paramMenu)
  {
    getSupportMenuInflater().inflate(2131492865, paramMenu);
    this.context = getApplicationContext();
    return super.onCreateOptionsMenu(paramMenu);
  }
  
  public boolean onOptionsItemSelected(MenuItem paramMenuItem)
  {
    int i = paramMenuItem.getItemId();
    UserInfoDBHelper localUserInfoDBHelper1;
    if (i == 16908332) {
      localUserInfoDBHelper1 = new UserInfoDBHelper(this.context);
    }
    label102:
    do
    {
      try
      {
        if (localUserInfoDBHelper1.getIsAdmin()) {}
        for (Intent localIntent1 = new Intent(this, AdminHome.class);; localIntent1 = new Intent(this, Home.class))
        {
          localUserInfoDBHelper1.close();
          startActivity(localIntent1);
          return true;
        }
        if (i != 2130968680) {
          break label102;
        }
      }
      finally
      {
        localUserInfoDBHelper1.close();
      }
      startActivity(new Intent(this, Preferences.class));
      return true;
      if (i == 2130968681)
      {
        Intent localIntent2 = new Intent(this, ViewProfile.class);
        Bundle localBundle = new Bundle();
        UserInfoDBHelper localUserInfoDBHelper2 = new UserInfoDBHelper(this.context);
        String str = localUserInfoDBHelper2.getUserName();
        localUserInfoDBHelper2.close();
        localBundle.putString("userName", str);
        localIntent2.putExtras(localBundle);
        startActivity(localIntent2);
        return true;
      }
      if (i == 2130968683)
      {
        new LogOutAsyncTask().execute(new Void[] { null, null });
        return true;
      }
    } while (i != 2130968682);
    startActivity(new Intent(this, About.class));
    return true;
  }
  
  public class LogOutAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    public LogOutAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      LoginRequest localLoginRequest = new LoginRequest(BaseTabsViewPagerActivity.this.context);
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(BaseTabsViewPagerActivity.this.context);
      HashMap localHashMap = new HashMap();
      try
      {
        localHashMap = localLoginRequest.logOut(localUserInfoDBHelper.getSessionToken());
        localUserInfoDBHelper.deleteInfo();
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
        Intent localIntent1 = new Intent(BaseTabsViewPagerActivity.this.context, Login.class);
        BaseTabsViewPagerActivity.this.startActivity(localIntent1);
        return;
      }
      if (((String)paramHashMap.get("errors")).equals("Invalid session"))
      {
        Utils.makeToast(BaseTabsViewPagerActivity.this.context, "Invalid session", 1);
        Intent localIntent2 = new Intent(BaseTabsViewPagerActivity.this.context, Login.class);
        BaseTabsViewPagerActivity.this.startActivity(localIntent2);
        return;
      }
      Utils.makeToast(BaseTabsViewPagerActivity.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
  
  public static class TabsAdapter
    extends FragmentPagerAdapter
    implements ActionBar.TabListener, ViewPager.OnPageChangeListener
  {
    private final com.actionbarsherlock.app.ActionBar mActionBar;
    private final Context mContext;
    private final ArrayList<TabInfo> mTabs = new ArrayList();
    private final ViewPager mViewPager;
    
    public TabsAdapter(SherlockFragmentActivity paramSherlockFragmentActivity, ViewPager paramViewPager)
    {
      super();
      this.mContext = paramSherlockFragmentActivity;
      this.mActionBar = paramSherlockFragmentActivity.getSupportActionBar();
      this.mViewPager = paramViewPager;
      this.mViewPager.setAdapter(this);
      this.mViewPager.setOnPageChangeListener(this);
    }
    
    public void addTab(ActionBar.Tab paramTab, Class<?> paramClass, Bundle paramBundle)
    {
      TabInfo localTabInfo = new TabInfo(paramClass, paramBundle);
      paramTab.setTag(localTabInfo);
      paramTab.setTabListener(this);
      this.mTabs.add(localTabInfo);
      this.mActionBar.addTab(paramTab);
      notifyDataSetChanged();
    }
    
    public int getCount()
    {
      return this.mTabs.size();
    }
    
    public Fragment getItem(int paramInt)
    {
      TabInfo localTabInfo = (TabInfo)this.mTabs.get(paramInt);
      return Fragment.instantiate(this.mContext, localTabInfo.clss.getName(), localTabInfo.args);
    }
    
    public void onPageScrollStateChanged(int paramInt) {}
    
    public void onPageScrolled(int paramInt1, float paramFloat, int paramInt2) {}
    
    public void onPageSelected(int paramInt)
    {
      this.mActionBar.setSelectedNavigationItem(paramInt);
    }
    
    public void onTabReselected(ActionBar.Tab paramTab, FragmentTransaction paramFragmentTransaction) {}
    
    public void onTabSelected(ActionBar.Tab paramTab, FragmentTransaction paramFragmentTransaction)
    {
      Object localObject = paramTab.getTag();
      for (int i = 0;; i++)
      {
        if (i >= this.mTabs.size()) {
          return;
        }
        if (this.mTabs.get(i) == localObject) {
          this.mViewPager.setCurrentItem(i);
        }
      }
    }
    
    public void onTabUnselected(ActionBar.Tab paramTab, FragmentTransaction paramFragmentTransaction) {}
    
    static final class TabInfo
    {
      private final Bundle args;
      private final Class<?> clss;
      
      TabInfo(Class<?> paramClass, Bundle paramBundle)
      {
        this.clss = paramClass;
        this.args = paramBundle;
      }
    }
  }
}
