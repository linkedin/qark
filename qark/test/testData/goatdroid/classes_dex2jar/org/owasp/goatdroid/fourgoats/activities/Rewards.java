package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.os.Bundle;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.Tab;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity.TabsAdapter;
import org.owasp.goatdroid.fourgoats.fragments.AvailableRewards;
import org.owasp.goatdroid.fourgoats.fragments.MyRewards;

public class Rewards
  extends BaseTabsViewPagerActivity
{
  Context context;
  
  public Rewards() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    ActionBar localActionBar = getSupportActionBar();
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296301), MyRewards.class, null);
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296302), AvailableRewards.class, null);
  }
}
