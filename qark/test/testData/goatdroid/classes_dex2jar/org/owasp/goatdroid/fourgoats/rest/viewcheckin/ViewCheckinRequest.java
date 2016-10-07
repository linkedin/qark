package org.owasp.goatdroid.fourgoats.rest.viewcheckin;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class ViewCheckinRequest
{
  Context context;
  String destinationInfo;
  
  public ViewCheckinRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> getCheckin(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/comments/get/" + paramString2, paramString1);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return ViewCheckinResponse.parseCheckinResponse(localAuthenticatedRestClient.getResponse());
  }
}
