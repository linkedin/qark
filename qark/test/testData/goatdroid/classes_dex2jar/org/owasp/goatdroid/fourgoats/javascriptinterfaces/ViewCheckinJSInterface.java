package org.owasp.goatdroid.fourgoats.javascriptinterfaces;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.activities.DoComment;
import org.owasp.goatdroid.fourgoats.activities.ViewCheckin;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.comments.CommentsRequest;

public class ViewCheckinJSInterface
{
  Context mContext;
  
  public ViewCheckinJSInterface(Context paramContext)
  {
    this.mContext = paramContext;
  }
  
  public void deleteComment(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6, String paramString7)
  {
    UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(this.mContext);
    String str = localUserInfoDBHelper.getSessionToken();
    localUserInfoDBHelper.close();
    CommentsRequest localCommentsRequest = new CommentsRequest(this.mContext);
    try
    {
      HashMap localHashMap = localCommentsRequest.removeComment(str, paramString1);
      if (((String)localHashMap.get("success")).equals("true"))
      {
        Utils.makeToast(this.mContext, "Comment has been removed!", 1);
        Intent localIntent = new Intent(this.mContext, ViewCheckin.class);
        Bundle localBundle = new Bundle();
        localBundle.putString("venueName", paramString2);
        localBundle.putString("venueWebsite", paramString3);
        localBundle.putString("dateTime", paramString4);
        localBundle.putString("latitude", paramString5);
        localBundle.putString("longitude", paramString6);
        localBundle.putString("checkinID", paramString7);
        localIntent.putExtras(localBundle);
        this.mContext.startActivity(localIntent);
        return;
      }
      Utils.makeToast(this.mContext, (String)localHashMap.get("errors"), 1);
      return;
    }
    catch (Exception localException)
    {
      Utils.makeToast(this.mContext, "Something weird happened", 1);
    }
  }
  
  public void launchDoCommentActivity(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6)
  {
    Intent localIntent = new Intent(this.mContext, DoComment.class);
    Bundle localBundle = new Bundle();
    localBundle.putString("venueName", paramString1);
    localBundle.putString("venueWebsite", paramString2);
    localBundle.putString("dateTime", paramString3);
    localBundle.putString("latitude", paramString4);
    localBundle.putString("longitude", paramString5);
    localBundle.putString("checkinID", paramString6);
    localIntent.putExtras(localBundle);
    this.mContext.startActivity(localIntent);
  }
  
  public void launchViewCheckinActivity(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5, String paramString6)
  {
    Intent localIntent = new Intent(this.mContext, ViewCheckin.class);
    Bundle localBundle = new Bundle();
    localBundle.putString("venueName", paramString1);
    localBundle.putString("venueWebsite", paramString2);
    localBundle.putString("dateTime", paramString3);
    localBundle.putString("latitude", paramString4);
    localBundle.putString("longitude", paramString5);
    localBundle.putString("checkinID", paramString6);
    localIntent.putExtras(localBundle);
    this.mContext.startActivity(localIntent);
  }
}
