package org.owasp.goatdroid.fourgoats.rest.rewards;

import java.util.ArrayList;
import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.owasp.goatdroid.fourgoats.base.ResponseBase;

public class RewardsResponse
  extends ResponseBase
{
  public RewardsResponse() {}
  
  public static ArrayList<HashMap<String, String>> parseRewardsResponse(String paramString)
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
          JSONArray localJSONArray2 = localJSONObject1.getJSONArray("rewards");
          k = 0;
          if (k >= localJSONArray2.length()) {
            return localArrayList;
          }
          HashMap localHashMap4 = new HashMap();
          localHashMap4.put("success", "true");
          HashMap localHashMap5 = new HashMap();
          if (localJSONArray2.getJSONObject(k).has("rewardName")) {
            localHashMap5.put("rewardName", (String)localJSONArray2.getJSONObject(k).get("rewardName"));
          }
          if (localJSONArray2.getJSONObject(k).has("rewardDescription")) {
            localHashMap5.put("rewardDescription", (String)localJSONArray2.getJSONObject(k).get("rewardDescription"));
          }
          if (localJSONArray2.getJSONObject(k).has("venueName")) {
            localHashMap5.put("venueName", (String)localJSONArray2.getJSONObject(k).get("venueName"));
          }
          if (localJSONArray2.getJSONObject(k).has("checkinsRequired")) {
            localHashMap5.put("checkinsRequired", (String)localJSONArray2.getJSONObject(k).get("checkinsRequired"));
          }
          if (localJSONArray2.getJSONObject(k).has("latitude")) {
            localHashMap5.put("latitude", (String)localJSONArray2.getJSONObject(k).get("latitude"));
          }
          if (localJSONArray2.getJSONObject(k).has("longitude")) {
            localHashMap5.put("longitude", (String)localJSONArray2.getJSONObject(k).get("longitude"));
          }
          if (localJSONArray2.getJSONObject(k).has("timeEarned")) {
            localHashMap5.put("timeEarned", (String)localJSONArray2.getJSONObject(k).get("timeEarned"));
          }
          localArrayList.add(localHashMap4);
          if (localHashMap5.size() <= 0) {
            break label856;
          }
          localArrayList.add(localHashMap5);
          break label856;
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
          HashMap localHashMap2 = new HashMap();
          if (localJSONObject2.getJSONObject("rewards").has("rewardName")) {
            localHashMap2.put("rewardName", (String)localJSONObject2.getJSONObject("rewards").get("rewardName"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("rewardDescription")) {
            localHashMap2.put("rewardDescription", (String)localJSONObject2.getJSONObject("rewards").get("rewardDescription"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("venueName")) {
            localHashMap2.put("venueName", (String)localJSONObject2.getJSONObject("rewards").get("venueName"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("checkinsRequired")) {
            localHashMap2.put("checkinsRequired", (String)localJSONObject2.getJSONObject("rewards").get("checkinsRequired"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("latitude")) {
            localHashMap2.put("latitude", (String)localJSONObject2.getJSONObject("rewards").get("latitude"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("longitude")) {
            localHashMap2.put("longitude", (String)localJSONObject2.getJSONObject("rewards").get("longitude"));
          }
          if (localJSONObject2.getJSONObject("rewards").has("timeEarned")) {
            localHashMap2.put("timeEarned", (String)localJSONObject2.getJSONObject("rewards").get("timeEarned"));
          }
          localArrayList.add(localHashMap1);
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
      label856:
      k++;
    }
  }
}
