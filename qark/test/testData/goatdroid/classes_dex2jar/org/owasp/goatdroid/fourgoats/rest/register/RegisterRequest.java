package org.owasp.goatdroid.fourgoats.rest.register;

import android.content.Context;
import java.util.HashMap;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;
import org.owasp.goatdroid.fourgoats.requestresponse.RestClient;

public class RegisterRequest
{
  Context context;
  String destinationInfo;
  
  public RegisterRequest(Context paramContext)
  {
    this.context = paramContext;
    this.destinationInfo = Utils.getDestinationInfo(paramContext);
  }
  
  public HashMap<String, String> validateRegistration(String paramString1, String paramString2, String paramString3, String paramString4)
    throws Exception
  {
    RestClient localRestClient = new RestClient("https://" + this.destinationInfo + "/fourgoats/api/v1/register");
    localRestClient.AddParam("firstName", paramString1);
    localRestClient.AddParam("lastName", paramString2);
    localRestClient.AddParam("userName", paramString3);
    localRestClient.AddParam("password", paramString4);
    localRestClient.Execute(RequestMethod.POST, this.context);
    return RegisterResponse.parseStatusAndErrors(localRestClient.getResponse());
  }
}
