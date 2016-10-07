package org.owasp.goatdroid.fourgoats.rest.friends;

import android.content.Context;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class FriendRequest
{
  Context context;
  String destinationInfo;
  
  public FriendRequest(Context paramContext)
  {
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
    this.context = paramContext;
  }
  
  public HashMap<String, String> acceptFriendRequest(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/accept_friend_request", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return FriendResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> denyFriendRequest(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/deny_friend_request", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return FriendResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> doFriendRequest(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/request_friend", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return FriendResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public ArrayList<HashMap<String, String>> getFriends(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/list_friends", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return FriendResponse.parseListFriendsResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public ArrayList<HashMap<String, String>> getPendingFriendRequests(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/get_pending_requests", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return FriendResponse.parsePendingFriendRequestsResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> getProfile(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/view_profile/" + paramString2, paramString1);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return FriendResponse.parseProfileResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> removeFriendRequest(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/remove_friend", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return FriendResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
}
