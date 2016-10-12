package org.owasp.goatdroid.fourgoats.rest.admin;

import android.content.Context;
import java.util.ArrayList;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class AdminRequest
{
  Context context;
  String destinationInfo;
  
  public AdminRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> deleteUser(String paramString1, String paramString2)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/admin/delete_user", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return AdminResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public ArrayList<HashMap<String, String>> getUsers(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/admin/get_users", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.GET, this.context);
    return AdminResponse.parseGetUsersResponse(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> resetUserPassword(String paramString1, String paramString2, String paramString3)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/admin/reset_password", paramString1);
    localAuthenticatedRestClient.AddParam("userName", paramString2);
    localAuthenticatedRestClient.AddParam("newPassword", paramString3);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return AdminResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
}
