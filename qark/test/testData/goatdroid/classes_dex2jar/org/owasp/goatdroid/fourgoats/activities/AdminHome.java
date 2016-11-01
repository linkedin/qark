package org.owasp.goatdroid.fourgoats.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;
import com.actionbarsherlock.app.ActionBar;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.services.LocationService;

public class AdminHome
  extends BaseActivity
{
  ListView listview;
  
  public AdminHome() {}
  
  public void launchCheckins(View paramView)
  {
    startActivity(new Intent(this, Checkins.class));
  }
  
  public void launchFriends(View paramView)
  {
    startActivity(new Intent(this, Friends.class));
  }
  
  public void launchManageUsers(View paramView)
  {
    startActivity(new Intent(this, AdminOptions.class));
  }
  
  public void launchRewards(View paramView)
  {
    startActivity(new Intent(this, Rewards.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    getSupportActionBar().setTitle("Home");
    getSupportActionBar().setDisplayHomeAsUpEnabled(false);
    setContentView(2130903062);
    startService(new Intent(this, LocationService.class));
  }
}
