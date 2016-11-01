package org.owasp.goatdroid.fourgoats.rest.addvenue;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class AddVenueRequest
{
  Context context;
  String destinationInfo;
  
  public AddVenueRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> doAddVenue(String paramString1, String paramString2, String paramString3, String paramString4, String paramString5)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/venues/add", paramString1);
    localAuthenticatedRestClient.AddParam("venueName", paramString2);
    localAuthenticatedRestClient.AddParam("venueWebsite", paramString3);
    localAuthenticatedRestClient.AddParam("latitude", paramString4);
    localAuthenticatedRestClient.AddParam("longitude", paramString5);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return AddVenueResponse.parseAddVenueResponse(localAuthenticatedRestClient.getResponse());
  }
}
