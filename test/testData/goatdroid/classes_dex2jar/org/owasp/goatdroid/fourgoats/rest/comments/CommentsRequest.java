package org.owasp.goatdroid.fourgoats.rest.comments;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class CommentsRequest
{
  Context context;
  String destinationInfo;
  
  public CommentsRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> addComment(String paramString1, String paramString2, String paramString3)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/comments/add", paramString1);
    localAuthenticatedRestClient.AddParam("comment", paramString2);
    localAuthenticatedRestClient.AddParam("checkinID", paramString3);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return CommentsResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> getComments(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/comments/get", paramString1);
    localAuthenticatedRestClient.AddParam("checkinID", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return CommentsResponse.parseGetCommentsResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> removeComment(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/comments/remove", paramString1);
    localAuthenticatedRestClient.AddParam("commentID", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return CommentsResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
}
