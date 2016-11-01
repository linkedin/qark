package android.support.v4.app;

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager.NameNotFoundException;
import android.os.Build.VERSION;
import android.util.Log;
import java.util.ArrayList;
import java.util.Iterator;

public class TaskStackBuilder
  implements Iterable<Intent>
{
  private static final TaskStackBuilderImpl IMPL = new TaskStackBuilderImplBase();
  private static final String TAG = "TaskStackBuilder";
  private final ArrayList<Intent> mIntents = new ArrayList();
  private final Context mSourceContext;
  
  static
  {
    if (Build.VERSION.SDK_INT >= 11)
    {
      IMPL = new TaskStackBuilderImplHoneycomb();
      return;
    }
  }
  
  private TaskStackBuilder(Context paramContext)
  {
    this.mSourceContext = paramContext;
  }
  
  public static TaskStackBuilder from(Context paramContext)
  {
    return new TaskStackBuilder(paramContext);
  }
  
  public TaskStackBuilder addNextIntent(Intent paramIntent)
  {
    this.mIntents.add(paramIntent);
    return this;
  }
  
  public TaskStackBuilder addParentStack(Activity paramActivity)
  {
    int i = this.mIntents.size();
    Object localObject = NavUtils.getParentActivityIntent(paramActivity);
    while (localObject != null)
    {
      this.mIntents.add(i, localObject);
      try
      {
        Intent localIntent = NavUtils.getParentActivityIntent(paramActivity, ((Intent)localObject).getComponent());
        localObject = localIntent;
      }
      catch (PackageManager.NameNotFoundException localNameNotFoundException)
      {
        Log.e("TaskStackBuilder", "Bad ComponentName while traversing activity parent metadata");
        throw new IllegalArgumentException(localNameNotFoundException);
      }
    }
    return this;
  }
  
  public TaskStackBuilder addParentStack(Class<?> paramClass)
  {
    int i = this.mIntents.size();
    try
    {
      Intent localIntent;
      for (Object localObject = NavUtils.getParentActivityIntent(this.mSourceContext, paramClass); localObject != null; localObject = localIntent)
      {
        this.mIntents.add(i, localObject);
        localIntent = NavUtils.getParentActivityIntent(this.mSourceContext, ((Intent)localObject).getComponent());
      }
      return this;
    }
    catch (PackageManager.NameNotFoundException localNameNotFoundException)
    {
      Log.e("TaskStackBuilder", "Bad ComponentName while traversing activity parent metadata");
      throw new IllegalArgumentException(localNameNotFoundException);
    }
  }
  
  public Intent getIntent(int paramInt)
  {
    return (Intent)this.mIntents.get(paramInt);
  }
  
  public int getIntentCount()
  {
    return this.mIntents.size();
  }
  
  public PendingIntent getPendingIntent(int paramInt1, int paramInt2)
  {
    Intent[] arrayOfIntent = (Intent[])this.mIntents.toArray(new Intent[this.mIntents.size()]);
    return IMPL.getPendingIntent(this.mSourceContext, arrayOfIntent, paramInt1, paramInt2);
  }
  
  public Iterator<Intent> iterator()
  {
    return this.mIntents.iterator();
  }
  
  public void startActivities()
  {
    if (this.mIntents.isEmpty()) {
      throw new IllegalStateException("No intents added to TaskStackBuilder; cannot startActivities");
    }
    Intent[] arrayOfIntent = (Intent[])this.mIntents.toArray(new Intent[this.mIntents.size()]);
    arrayOfIntent[0].addFlags(268484608);
    if (!ActivityCompat.startActivities((Activity)this.mSourceContext, arrayOfIntent))
    {
      Intent localIntent = arrayOfIntent[(-1 + arrayOfIntent.length)];
      localIntent.addFlags(268435456);
      this.mSourceContext.startActivity(localIntent);
    }
  }
  
  static abstract interface TaskStackBuilderImpl
  {
    public abstract PendingIntent getPendingIntent(Context paramContext, Intent[] paramArrayOfIntent, int paramInt1, int paramInt2);
  }
  
  static class TaskStackBuilderImplBase
    implements TaskStackBuilder.TaskStackBuilderImpl
  {
    TaskStackBuilderImplBase() {}
    
    public PendingIntent getPendingIntent(Context paramContext, Intent[] paramArrayOfIntent, int paramInt1, int paramInt2)
    {
      Intent localIntent = paramArrayOfIntent[(-1 + paramArrayOfIntent.length)];
      localIntent.addFlags(268435456);
      return PendingIntent.getActivity(paramContext, paramInt1, localIntent, paramInt2);
    }
  }
  
  static class TaskStackBuilderImplHoneycomb
    implements TaskStackBuilder.TaskStackBuilderImpl
  {
    TaskStackBuilderImplHoneycomb() {}
    
    public PendingIntent getPendingIntent(Context paramContext, Intent[] paramArrayOfIntent, int paramInt1, int paramInt2)
    {
      paramArrayOfIntent[0].addFlags(268468224);
      return TaskStackBuilderHoneycomb.getActivitiesPendingIntent(paramContext, paramInt1, paramArrayOfIntent, paramInt2);
    }
  }
}
