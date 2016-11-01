package org.owasp.goatdroid.fourgoats.rest.login;

import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.owasp.goatdroid.fourgoats.base.ResponseBase;

public class LoginResponse
  extends ResponseBase
{
  public LoginResponse() {}
  
  public static HashMap<String, String> parseAPILoginResponse(String paramString)
  {
    HashMap localHashMap = new HashMap();
    try
    {
      JSONObject localJSONObject = new JSONObject(paramString);
      if (localJSONObject.getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        return localHashMap;
      }
      localHashMap.put("success", "true");
      localHashMap.put("sessionToken", localJSONObject.getString("sessionToken"));
      return localHashMap;
    }
    catch (JSONException localJSONException)
    {
      localHashMap.put("success", "false");
    }
    return localHashMap;
  }
  
  public static HashMap<String, String> parseLoginResponse(String paramString)
  {
    localHashMap = new HashMap();
    try
    {
      JSONObject localJSONObject = new JSONObject(paramString);
      if (localJSONObject.getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        return localHashMap;
      }
      localHashMap.put("success", "true");
      localHashMap.put("sessionToken", localJSONObject.getString("sessionToken"));
      localHashMap.put("userName", localJSONObject.getString("userName"));
      JSONArray localJSONArray = localJSONObject.getJSONObject("preferences").getJSONArray("entry");
      for (int i = 0; i < localJSONArray.length(); i++) {
        localHashMap.put(localJSONArray.getJSONObject(i).getString("key"), localJSONArray.getJSONObject(i).getString("value"));
      }
      return localHashMap;
    }
    catch (JSONException localJSONException)
    {
      localHashMap.put("errors", localJSONException.getMessage());
      localHashMap.put("success", "false");
    }
  }
}
