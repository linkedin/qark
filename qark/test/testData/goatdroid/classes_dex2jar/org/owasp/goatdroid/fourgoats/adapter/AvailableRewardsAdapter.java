package org.owasp.goatdroid.fourgoats.adapter;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class AvailableRewardsAdapter
  extends ArrayAdapter<String>
{
  private final Activity activity;
  private final String[] values;
  
  public AvailableRewardsAdapter(Activity paramActivity, String[] paramArrayOfString)
  {
    super(paramActivity, 2130903091, paramArrayOfString);
    this.activity = paramActivity;
    this.values = paramArrayOfString;
  }
  
  public View getView(int paramInt, View paramView, ViewGroup paramViewGroup)
  {
    View localView = paramView;
    if (localView == null)
    {
      localView = this.activity.getLayoutInflater().inflate(2130903066, null);
      ViewHolder localViewHolder2 = new ViewHolder();
      localViewHolder2.name = ((TextView)localView.findViewById(2130968625));
      localViewHolder2.description = ((TextView)localView.findViewById(2130968627));
      localViewHolder2.venue = ((TextView)localView.findViewById(2130968628));
      localViewHolder2.latitude = ((TextView)localView.findViewById(2130968629));
      localViewHolder2.longitude = ((TextView)localView.findViewById(2130968630));
      localViewHolder2.checkins = ((TextView)localView.findViewById(2130968631));
      localView.setTag(localViewHolder2);
    }
    ViewHolder localViewHolder1 = (ViewHolder)localView.getTag();
    String[] arrayOfString = this.values[paramInt].split("\n");
    localViewHolder1.name.setText(arrayOfString[0]);
    localViewHolder1.description.setText(arrayOfString[1]);
    localViewHolder1.venue.setText(arrayOfString[2]);
    localViewHolder1.latitude.setText(arrayOfString[3]);
    localViewHolder1.longitude.setText(arrayOfString[4]);
    localViewHolder1.checkins.setText(arrayOfString[5]);
    return localView;
  }
  
  static class ViewHolder
  {
    public TextView checkins;
    public TextView description;
    public TextView latitude;
    public TextView longitude;
    public TextView name;
    public TextView venue;
    
    ViewHolder() {}
  }
}
