package org.owasp.goatdroid.fourgoats.rest.admin;

import java.util.ArrayList;
import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.owasp.goatdroid.fourgoats.base.ResponseBase;

public class AdminResponse
  extends ResponseBase
{
  public AdminResponse() {}
  
  public static ArrayList<HashMap<String, String>> parseGetUsersResponse(String paramString)
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
          JSONArray localJSONArray2 = localJSONObject1.getJSONArray("users");
          k = 0;
          if (k >= localJSONArray2.length()) {
            return localArrayList;
          }
          HashMap localHashMap4 = new HashMap();
          localHashMap4.put("success", "true");
          HashMap localHashMap5 = new HashMap();
          if (localJSONArray2.getJSONObject(k).has("userName")) {
            localHashMap5.put("userName", (String)localJSONArray2.getJSONObject(k).get("userName"));
          }
          if (localJSONArray2.getJSONObject(k).has("firstName")) {
            localHashMap5.put("firstName", (String)localJSONArray2.getJSONObject(k).get("firstName"));
          }
          if (localJSONArray2.getJSONObject(k).has("lastName")) {
            localHashMap5.put("lastName", (String)localJSONArray2.getJSONObject(k).get("lastName"));
          }
          localArrayList.add(localHashMap4);
          if (localHashMap5.size() <= 0) {
            break label552;
          }
          localArrayList.add(localHashMap5);
          break label552;
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
          if (localJSONObject2.getJSONObject("users").has("userName")) {
            localHashMap2.put("userName", (String)localJSONObject2.getJSONObject("users").get("userName"));
          }
          if (localJSONObject2.getJSONObject("users").has("firstName")) {
            localHashMap2.put("firstName", (String)localJSONObject2.getJSONObject("users").get("firstName"));
          }
          if (localJSONObject2.getJSONObject("users").has("lastName")) {
            localHashMap2.put("lastName", (String)localJSONObject2.getJSONObject("users").get("lastName"));
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
      label552:
      k++;
    }
  }
}
