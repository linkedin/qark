package org.owasp.goatdroid.fourgoats.activities;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.text.Editable;
import android.view.View;
import android.widget.EditText;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.base.BaseActivity;
import org.owasp.goatdroid.fourgoats.db.UserInfoDBHelper;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.rest.comments.CommentsRequest;

public class DoComment
  extends BaseActivity
{
  Bundle bundle;
  EditText commentEditText;
  Context context;
  
  public DoComment() {}
  
  public boolean areFieldsCompleted()
  {
    return !this.commentEditText.getText().toString().equals("");
  }
  
  public void onCreate(Bundle paramBundle)
  {
    super.onCreate(paramBundle);
    setContentView(2130903072);
    this.context = getApplicationContext();
    this.commentEditText = ((EditText)findViewById(2130968639));
    this.bundle = getIntent().getExtras();
  }
  
  public void submitComment(View paramView)
  {
    if (!areFieldsCompleted())
    {
      Utils.makeToast(this.context, "All fields are required", 1);
      return;
    }
    new DoCommentAsyncTask(null).execute(new Void[] { null, null });
  }
  
  private class DoCommentAsyncTask
    extends AsyncTask<Void, Void, HashMap<String, String>>
  {
    private DoCommentAsyncTask() {}
    
    protected HashMap<String, String> doInBackground(Void... paramVarArgs)
    {
      HashMap localHashMap1 = new HashMap();
      UserInfoDBHelper localUserInfoDBHelper = new UserInfoDBHelper(DoComment.this.context);
      String str = localUserInfoDBHelper.getSessionToken();
      CommentsRequest localCommentsRequest = new CommentsRequest(DoComment.this.context);
      try
      {
        HashMap localHashMap2 = localCommentsRequest.addComment(str, DoComment.this.commentEditText.getText().toString(), DoComment.this.bundle.getString("checkinID"));
        return localHashMap2;
      }
      catch (Exception localException)
      {
        localHashMap1.put("errors", localException.getMessage());
        return localHashMap1;
      }
      finally
      {
        localUserInfoDBHelper.close();
      }
    }
    
    public void launchViewCheckin(Bundle paramBundle)
    {
      Intent localIntent = new Intent(DoComment.this.context, ViewCheckin.class);
      localIntent.putExtras(paramBundle);
      DoComment.this.startActivity(localIntent);
    }
    
    protected void onPostExecute(HashMap<String, String> paramHashMap)
    {
      if (((String)paramHashMap.get("success")).equals("true"))
      {
        Utils.makeToast(DoComment.this.context, "Your comment has been posted!", 1);
        launchViewCheckin(DoComment.this.bundle);
        return;
      }
      Utils.makeToast(DoComment.this.context, (String)paramHashMap.get("errors"), 1);
    }
  }
}
