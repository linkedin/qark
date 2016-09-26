package org.owasp.goatdroid.fourgoats.rest.friends;

import java.util.ArrayList;
import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.owasp.goatdroid.fourgoats.base.ResponseBase;

public class FriendResponse
  extends ResponseBase
{
  public FriendResponse() {}
  
  public static ArrayList<HashMap<String, String>> parseListFriendsResponse(String paramString)
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
          JSONArray localJSONArray2 = localJSONObject1.getJSONArray("friends");
          k = 0;
          if (k >= localJSONArray2.length()) {
            return localArrayList;
          }
          HashMap localHashMap4 = new HashMap();
          localHashMap4.put("success", "true");
          HashMap localHashMap5 = new HashMap();
          if (localJSONArray2.getJSONObject(k).has("userID")) {
            localHashMap5.put("userID", (String)localJSONArray2.getJSONObject(k).get("userID"));
          }
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
            break label628;
          }
          localArrayList.add(localHashMap5);
          break label628;
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
          if (localJSONObject2.getJSONObject("friends").has("userID")) {
            localHashMap2.put("userID", (String)localJSONObject2.getJSONObject("friends").get("userID"));
          }
          if (localJSONObject2.getJSONObject("friends").has("userName")) {
            localHashMap2.put("userName", (String)localJSONObject2.getJSONObject("friends").get("userName"));
          }
          if (localJSONObject2.getJSONObject("friends").has("firstName")) {
            localHashMap2.put("firstName", (String)localJSONObject2.getJSONObject("friends").get("firstName"));
          }
          if (localJSONObject2.getJSONObject("friends").has("lastName")) {
            localHashMap2.put("lastName", (String)localJSONObject2.getJSONObject("friends").get("lastName"));
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
      label628:
      k++;
    }
  }
  
  public static ArrayList<HashMap<String, String>> parsePendingFriendRequestsResponse(String paramString)
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
          JSONArray localJSONArray2 = localJSONObject1.getJSONArray("pendingFriendRequests");
          k = 0;
          if (k >= localJSONArray2.length()) {
            return localArrayList;
          }
          HashMap localHashMap4 = new HashMap();
          localHashMap4.put("success", "true");
          HashMap localHashMap5 = new HashMap();
          if (localJSONArray2.getJSONObject(k).has("requestId")) {
            localHashMap5.put("requestId", (String)localJSONArray2.getJSONObject(k).get("requestId"));
          }
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
            break label628;
          }
          localArrayList.add(localHashMap5);
          break label628;
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
          if (localJSONObject2.getJSONObject("pendingFriendRequests").has("requestID")) {
            localHashMap2.put("requestID", (String)localJSONObject2.getJSONObject("pendingFriendRequests").get("requestID"));
          }
          if (localJSONObject2.getJSONObject("pendingFriendRequests").has("userName")) {
            localHashMap2.put("userName", (String)localJSONObject2.getJSONObject("pendingFriendRequests").get("userName"));
          }
          if (localJSONObject2.getJSONObject("pendingFriendRequests").has("firstName")) {
            localHashMap2.put("firstName", (String)localJSONObject2.getJSONObject("pendingFriendRequests").get("firstName"));
          }
          if (localJSONObject2.getJSONObject("pendingFriendRequests").has("lastName")) {
            localHashMap2.put("lastName", (String)localJSONObject2.getJSONObject("pendingFriendRequests").get("lastName"));
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
      label628:
      k++;
    }
  }
  
  public static HashMap<String, String> parseProfileResponse(String paramString)
  {
    localHashMap = new HashMap();
    Object localObject = "";
    try
    {
      JSONObject localJSONObject = new JSONObject(paramString);
      if (localJSONObject.getString("success").equals("false"))
      {
        localHashMap.put("success", "false");
        try
        {
          localJSONArray2 = localJSONObject.getJSONArray("errors");
          j = 0;
          int k = localJSONArray2.length();
          if (j < k) {
            break label78;
          }
        }
        catch (JSONException localJSONException2)
        {
          for (;;)
          {
            JSONArray localJSONArray2;
            int j;
            localObject = localObject + localJSONObject.getString("errors");
          }
        }
        localHashMap.put("errors", localObject);
      }
      for (;;)
      {
        return localHashMap;
        label78:
        String str = localObject + localJSONArray2.getString(j).toString() + "\n\n";
        localObject = str;
        j++;
        break;
        localHashMap.put("success", "true");
        JSONArray localJSONArray1 = localJSONObject.getJSONObject("profile").getJSONArray("entry");
        for (int i = 0; i < localJSONArray1.length(); i++) {
          localHashMap.put(localJSONArray1.getJSONObject(i).getString("key"), localJSONArray1.getJSONObject(i).getString("value"));
        }
      }
      return localHashMap;
    }
    catch (JSONException localJSONException1)
    {
      localHashMap.put("success", "false");
      localHashMap.put("errors", "Something weird happened");
    }
  }
}
