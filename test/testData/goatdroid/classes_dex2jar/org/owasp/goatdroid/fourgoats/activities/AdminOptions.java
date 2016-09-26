package org.owasp.goatdroid.fourgoats.activities;

import android.os.Bundle;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.ActionBar.Tab;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity;
import org.owasp.goatdroid.fourgoats.base.BaseTabsViewPagerActivity.TabsAdapter;
import org.owasp.goatdroid.fourgoats.fragments.DeleteUsers;
import org.owasp.goatdroid.fourgoats.fragments.ResetUserPasswords;

public class AdminOptions
  extends BaseTabsViewPagerActivity
{
  public AdminOptions() {}
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    ActionBar localActionBar = getSupportActionBar();
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296326), ResetUserPasswords.class, null);
    this.mTabsAdapter.addTab(localActionBar.newTab().setText(2131296327), DeleteUsers.class, null);
  }
}
