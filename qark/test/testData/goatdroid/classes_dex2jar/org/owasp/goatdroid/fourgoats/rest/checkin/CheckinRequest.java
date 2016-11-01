package org.owasp.goatdroid.fourgoats.rest.checkin;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class CheckinRequest
{
  Context context;
  String destinationInfo;
  
  public CheckinRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> doCheckin(String paramString1, String paramString2, String paramString3)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/checkin", paramString1);
    localAuthenticatedRestClient.AddParam("latitude", paramString2);
    localAuthenticatedRestClient.AddParam("longitude", paramString3);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return CheckinResponse.parseCheckinResponse(localAuthenticatedRestClient.getResponse());
  }
}
