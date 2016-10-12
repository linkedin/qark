package org.owasp.goatdroid.fourgoats.rest.rewards;

import android.content.Context;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class RewardsRequest
{
  Context context;
  String destinationInfo;
  
  public RewardsRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public ArrayList<HashMap<String, String>> getAllRewards(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/rewards/all_rewards", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return RewardsResponse.parseRewardsResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public ArrayList<HashMap<String, String>> getMyRewards(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/rewards/my_rewards", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return RewardsResponse.parseRewardsResponse(localAuthenticatedRestClient.getResponse());
  }
}
