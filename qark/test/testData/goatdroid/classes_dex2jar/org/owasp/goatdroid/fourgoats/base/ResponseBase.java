package org.owasp.goatdroid.fourgoats.base;

import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ResponseBase
{
  public ResponseBase() {}
  
  public static boolean isSuccess(String paramString)
    throws JSONException
  {
    return !new JSONObject(paramString).getString("success").equals("false");
  }
  
  public static HashMap<String, String> parseStatusAndErrors(String paramString)
  {
    localHashMap = new HashMap();
    localObject1 = "";
    if (paramString == null) {}
    for (;;)
    {
      try
      {
        localObject1 = localObject1 + "Could not contact the remote service";
        localHashMap.put("success", "false");
        return localHashMap;
      }
      catch (JSONException localJSONException1)
      {
        JSONObject localJSONObject;
        localHashMap.put("success", "false");
        return localHashMap;
      }
      catch (Exception localException)
      {
        localHashMap.put("success", "false");
        return localHashMap;
      }
      finally
      {
        localHashMap.put("errors", localObject1);
      }
      localJSONObject = new JSONObject(paramString);
      if (localJSONObject.getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        try
        {
          JSONArray localJSONArray = localJSONObject.getJSONArray("errors");
          int i = 0;
          if (i >= localJSONArray.length()) {
            continue;
          }
          String str = localObject1 + "-" + localJSONArray.getString(i).toString() + "\n\n";
          localObject1 = str;
          i++;
          continue;
        }
        catch (JSONException localJSONException2)
        {
          localObject1 = localObject1 + localJSONObject.getString("errors");
        }
      }
      else
      {
        localHashMap.put("success", "true");
      }
    }
  }
}
