package org.owasp.goatdroid.fourgoats.rest.searchforfriends;

import android.content.Context;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class SearchForFriendsRequest
{
  Context context;
  String destinationInfo;
  
  public SearchForFriendsRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public ArrayList<HashMap<String, String>> getUsers(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/friends/search_users", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return SearchForFriendsResponse.parseSearchForFriendsResponse(localAuthenticatedRestClient.getResponse());
  }
}
