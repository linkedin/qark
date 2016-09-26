package org.owasp.goatdroid.fourgoats.rest.login;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.AuthenticatedRestClient;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;
import org.owasp.goatdroid.fourgoats.requestresponse.RestClient;

public class LoginRequest
{
  Context context;
  String destinationInfo;
  
  public LoginRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public boolean isSessionValid(String paramString)
    throws Exception
  {
    RestClient localRestClient = new RestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/login/check_session");
    localRestClient.AddHeader("Cookie", "SESS=" + paramString);
    localRestClient.Execute(RequestMethod.GET, this.context);
    return LoginResponse.isSuccess(localRestClient.getResponse());
  }
  
  public HashMap<String, String> logOut(String paramString)
    throws Exception
  {
    AuthenticatedRestClient localAuthenticatedRestClient = new AuthenticatedRestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/login/sign_out", paramString);
    localAuthenticatedRestClient.Execute(RequestMethod.POST, this.context);
    return LoginResponse.parseStatusAndErrors(localAuthenticatedRestClient.getResponse());
  }
  
  public HashMap<String, String> validateCredentials(String paramString1, String paramString2)
    throws Exception
  {
    RestClient localRestClient = new RestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/login/authenticate");
    localRestClient.AddParam("userName", paramString1);
    localRestClient.AddParam("password", paramString2);
    localRestClient.Execute(RequestMethod.POST, this.context);
    return LoginResponse.parseLoginResponse(localRestClient.getResponse());
  }
  
  public HashMap<String, String> validateCredentialsAPI(String paramString1, String paramString2)
    throws Exception
  {
    RestClient localRestClient = new RestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/login/validate_api");
    localRestClient.AddParam("userName", paramString1);
    localRestClient.AddParam("password", paramString2);
    localRestClient.Execute(RequestMethod.POST, this.context);
    return LoginResponse.parseAPILoginResponse(localRestClient.getResponse());
  }
}
