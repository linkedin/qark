package org.owasp.goatdroid.fourgoats.rest.history;

import android.content.Context;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class HistoryRequest
{
  Context context;
  String destinationInfo;
  
  public HistoryRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public ArrayList<HashMap<String, String>> getHistory(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/history/list", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return HistoryResponse.parseHistoryResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public ArrayList<HashMap<String, String>> getUserHistory(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/history/get_user_history/" + paramString2, paramString1);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return HistoryResponse.parseHistoryResponse(localAuthenticatedRestClient.getResponse());
  }
}
