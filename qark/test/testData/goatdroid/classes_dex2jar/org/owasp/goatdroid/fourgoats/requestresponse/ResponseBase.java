package org.owasp.goatdroid.fourgoats.requestresponse;

import java.util.HashMap;
import org.json.JSONException;
import org.json.JSONObject;

public class ResponseBase
{
  public ResponseBase() {}
  
  public static HashMap<String, String> getSuccessAndErrors(String paramString)
  {
    HashMap localHashMap = new HashMap();
    try
    {
      if (new JSONObject(paramString).getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        return localHashMap;
      }
      localHashMap.put("success", "true");
      return localHashMap;
    }
    catch (JSONException localJSONException)
    {
      localHashMap.put("success", "false");
    }
    return localHashMap;
  }
}
