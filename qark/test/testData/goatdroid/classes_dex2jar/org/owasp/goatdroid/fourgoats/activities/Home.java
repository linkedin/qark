package org.owasp.goatdroid.fourgoats.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;
import com.actionbarsherlock.app.ActionBar;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.services.LocationService;

public class Home
  extends BaseActivity
{
  ListView listview;
  
  public Home() {}
  
  public void launchCheckins(View paramView)
  {
    startActivity(new Intent(this, Checkins.class));
  }
  
  public void launchFriends(View paramView)
  {
    startActivity(new Intent(this, Friends.class));
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
    setContentView(2130903079);
    startService(new Intent(this, LocationService.class));
  }
}
