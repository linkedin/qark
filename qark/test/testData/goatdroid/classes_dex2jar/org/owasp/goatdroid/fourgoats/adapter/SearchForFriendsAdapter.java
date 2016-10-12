package org.owasp.goatdroid.fourgoats.adapter;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

public class SearchForFriendsAdapter
  extends ArrayAdapter<String>
{
  private final Activity activity;
  private final String[] values;
  
  public SearchForFriendsAdapter(Activity paramActivity, String[] paramArrayOfString)
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
      localView = this.activity.getLayoutInflater().inflate(2130903091, null);
      ViewHolder localViewHolder2 = new ViewHolder();
      localViewHolder2.name = ((TextView)localView.findViewById(2130968625));
      localViewHolder2.username = ((TextView)localView.findViewById(2130968674));
      localView.setTag(localViewHolder2);
    }
    ViewHolder localViewHolder1 = (ViewHolder)localView.getTag();
    String[] arrayOfString = this.values[paramInt].split("\n");
    localViewHolder1.name.setText(arrayOfString[0]);
    localViewHolder1.username.setText(arrayOfString[1]);
    return localView;
  }
  
  static class ViewHolder
  {
    public TextView name;
    public TextView username;
    
    ViewHolder() {}
  }
}
