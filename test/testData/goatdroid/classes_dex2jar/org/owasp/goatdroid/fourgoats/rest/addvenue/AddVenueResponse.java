package org.owasp.goatdroid.fourgoats.rest.addvenue;

import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class AddVenueResponse
{
  public AddVenueResponse() {}
  
  public static HashMap<String, String> parseAddVenueResponse(String paramString)
  {
    HashMap localHashMap = new HashMap();
    Object localObject = "";
    try
    {
      JSONObject localJSONObject = new JSONObject(paramString);
      if (localJSONObject.getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        for (;;)
        {
          try
          {
            localJSONArray = localJSONObject.getJSONArray("errors");
            i = 0;
            int j = localJSONArray.length();
            if (i < j) {
              continue;
            }
          }
          catch (JSONException localJSONException2)
          {
            JSONArray localJSONArray;
            int i;
            String str;
            localObject = localObject + localJSONObject.getString("errors");
            continue;
          }
          localHashMap.put("errors", localObject);
          return localHashMap;
          str = localObject + localJSONArray.getString(i).toString() + "\n\n";
          localObject = str;
          i++;
        }
      }
      localHashMap.put("success", "true");
      return localHashMap;
    }
    catch (JSONException localJSONException1)
    {
      localHashMap.put("success", "false");
      localHashMap.put("errors", "Something weird happened");
    }
    return localHashMap;
  }
}
