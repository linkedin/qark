package org.owasp.goatdroid.fourgoats.rest.preferences;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class PreferencesRequest
{
  Context context;
  String destinationInfo;
  
  public PreferencesRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> updatePreferences(String paramString1, String paramString2, String paramString3)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/preferences/modify_preferences", paramString1);
    localAuthenticatedRestClient.AddParam("isPublic", paramString2);
    localAuthenticatedRestClient.AddParam("autoCheckin", paramString3);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return PreferencesResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
}
