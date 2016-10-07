package org.owasp.goatdroid.fourgoats.activities;

import android.os.Bundle;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.Tab;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity.TabsAdapter;
import org.owasp.goatdroid.fourgoats.fragments.MyFriends;
import org.owasp.goatdroid.fourgoats.fragments.PendingFriendRequests;
import org.owasp.goatdroid.fourgoats.fragments.SearchForFriends;

public class Friends
  extends BaseTabsViewPagerActivity
{
  public Friends() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    ActionBar localActionBar = getSupportActionBar();
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296292), MyFriends.class, null);
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296294), SearchForFriends.class, null);
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296296), PendingFriendRequests.class, null);
  }
}
