package org.owasp.goatdroid.fourgoats.rest.history;

import java.util.ArrayList;
import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class HistoryResponse
{
  public HistoryResponse() {}
  
  public static ArrayList<HashMap<String, String>> parseHistoryResponse(String paramString)
  {
    ArrayList localArrayList = new ArrayList();
    Object localObject = "";
    for (;;)
    {
      int k;
      try
      {
        localJSONObject1 = new JSONObject(paramString);
        if (localJSONObject1.getString("success").equals("true"))
        {
          JSONArray localJSONArray2 = localJSONObject1.getJSONArray("history");
          k = 0;
          if (k >= localJSONArray2.length()) {
            return localArrayList;
          }
          HashMap localHashMap4 = new HashMap();
          localHashMap4.put("success", "true");
          HashMap localHashMap5 = new HashMap();
          if (localJSONArray2.getJSONObject(k).has("dateTime")) {
            localHashMap5.put("dateTime", (String)localJSONArray2.getJSONObject(k).get("dateTime"));
          }
          if (localJSONArray2.getJSONObject(k).has("checkinID")) {
            localHashMap5.put("checkinID", (String)localJSONArray2.getJSONObject(k).get("checkinID"));
          }
          if (localJSONArray2.getJSONObject(k).has("latitude")) {
            localHashMap5.put("latitude", (String)localJSONArray2.getJSONObject(k).get("latitude"));
          }
          if (localJSONArray2.getJSONObject(k).has("longitude")) {
            localHashMap5.put("longitude", (String)localJSONArray2.getJSONObject(k).get("longitude"));
          }
          if (localJSONArray2.getJSONObject(k).has("venueName")) {
            localHashMap5.put("venueName", (String)localJSONArray2.getJSONObject(k).get("venueName"));
          }
          if (localJSONArray2.getJSONObject(k).has("venueWebsite")) {
            localHashMap5.put("venueWebsite", (String)localJSONArray2.getJSONObject(k).get("venueWebsite"));
          }
          localArrayList.add(localHashMap4);
          if (localHashMap5.size() <= 0) {
            break label780;
          }
          localArrayList.add(localHashMap5);
          break label780;
        }
        localHashMap3 = new HashMap();
        localHashMap3.put("success", "false");
      }
      catch (JSONException localJSONException1)
      {
        JSONObject localJSONObject1;
        JSONArray localJSONArray1;
        int i;
        try
        {
          HashMap localHashMap3;
          int j;
          JSONObject localJSONObject2 = new JSONObject(paramString);
          HashMap localHashMap1 = new HashMap();
          localHashMap1.put("success", "true");
          localArrayList.add(localHashMap1);
          HashMap localHashMap2 = new HashMap();
          if (localJSONObject2.getJSONObject("history").has("dateTime")) {
            localHashMap2.put("dateTime", (String)localJSONObject2.getJSONObject("history").get("dateTime"));
          }
          if (localJSONObject2.getJSONObject("history").has("checkinID")) {
            localHashMap2.put("checkinID", (String)localJSONObject2.getJSONObject("history").get("checkinID"));
          }
          if (localJSONObject2.getJSONObject("history").has("latitude")) {
            localHashMap2.put("latitude", (String)localJSONObject2.getJSONObject("history").get("latitude"));
          }
          if (localJSONObject2.getJSONObject("history").has("longitude")) {
            localHashMap2.put("longitude", (String)localJSONObject2.getJSONObject("history").get("longitude"));
          }
          if (localJSONObject2.getJSONObject("history").has("venueName")) {
            localHashMap2.put("venueName", (String)localJSONObject2.getJSONObject("history").get("venueName"));
          }
          if (localJSONObject2.getJSONObject("history").has("venueWebsite")) {
            localHashMap2.put("venueWebsite", (String)localJSONObject2.getJSONObject("history").get("venueWebsite"));
          }
          if (localHashMap2.size() <= 0) {
            continue;
          }
          localArrayList.add(localHashMap2);
          return localArrayList;
        }
        catch (JSONException localJSONException2)
        {
          localJSONException2.getMessage();
          return localArrayList;
        }
        String str2 = localObject + localJSONArray1.getString(i).toString() + "\n\n";
        localObject = str2;
        i++;
        continue;
        String str1;
        return localArrayList;
      }
      try
      {
        localJSONArray1 = localJSONObject1.getJSONArray("errors");
        i = 0;
        j = localJSONArray1.length();
        if (i < j) {
          continue;
        }
      }
      catch (JSONException localJSONException3)
      {
        str1 = localObject + localJSONObject1.getString("errors");
        localObject = str1;
        continue;
      }
      localHashMap3.put("errors", localObject);
      localArrayList.add(localHashMap3);
      return localArrayList;
      label780:
      k++;
    }
  }
}
