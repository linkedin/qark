package org.owasp.goatdroid.fourgoats.base;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.SherlockActivity;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuInflater;
import com.actionbarsherlock.view.MenuItem;
import org.owasp.goatdroid.fourgoats.activities.DestinationInfo;
import org.owasp.goatdroid.fourgoats.activities.Login;

public class BaseUnauthenticatedActivity
  extends SherlockActivity
{
  Context context;
  
  public BaseUnauthenticatedActivity() {}
  
  public void launchLogin()
  {
    startActivity(new Intent(this.context, Login.class));
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    getSupportActionBar().setIcon(2130837628);
  }
  
  public boolean onCreateOptionsMenu(Menu paramMenu)
  {
    getSupportMenuInflater().inflate(2131492864, paramMenu);
    this.context = getApplicationContext();
    return true;
  }
  
  public boolean onOptionsItemSelected(MenuItem paramMenuItem)
  {
    startActivity(new Intent(this, DestinationInfo.class));
    return true;
  }
}
