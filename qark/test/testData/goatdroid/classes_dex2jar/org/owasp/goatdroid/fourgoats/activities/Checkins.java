package org.owasp.goatdroid.fourgoats.activities;

import android.os.Bundle;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.Tab;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity.TabsAdapter;
import org.owasp.goatdroid.fourgoats.fragments.DoCheckin;
import org.owasp.goatdroid.fourgoats.fragments.HistoryFragment;

public class Checkins
  extends BaseTabsViewPagerActivity
{
  public Checkins() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    ActionBar localActionBar = getSupportActionBar();
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296286), DoCheckin.class, null);
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296272), HistoryFragment.class, null);
  }
}
