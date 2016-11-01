package org.owasp.goatdroid.fourgoats.rest.viewcheckin;

public class ViewCheckinResponse
{
  public ViewCheckinResponse() {}
  
  /* Error */
  public static java.util.HashMap<String, String> parseCheckinResponse(String paramString)
  {
    // Byte code:
    //   0: new 14	java/util/HashMap
    //   3: dup
    //   4: invokespecial 15	java/util/HashMap:<init>	()V
    //   7: astore_1
    //   8: ldc 17
    //   10: astore_2
    //   11: new 19	org/json/JSONObject
    //   14: dup
    //   15: aload_0
    //   16: invokespecial 22	org/json/JSONObject:<init>	(Ljava/lang/String;)V
    //   19: astore_3
    //   20: aload_3
    //   21: ldc 24
    //   23: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   26: ldc 30
    //   28: invokevirtual 36	java/lang/String:equals	(Ljava/lang/Object;)Z
    //   31: ifeq +119 -> 150
    //   34: aload_1
    //   35: ldc 24
    //   37: ldc 30
    //   39: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   42: pop
    //   43: aload_3
    //   44: ldc 42
    //   46: invokevirtual 46	org/json/JSONObject:getJSONArray	(Ljava/lang/String;)Lorg/json/JSONArray;
    //   49: astore 15
    //   51: iconst_0
    //   52: istore 16
    //   54: aload 15
    //   56: invokevirtual 52	org/json/JSONArray:length	()I
    //   59: istore 17
    //   61: iload 16
    //   63: iload 17
    //   65: if_icmplt +13 -> 78
    //   68: aload_1
    //   69: ldc 42
    //   71: aload_2
    //   72: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   75: pop
    //   76: aload_1
    //   77: areturn
    //   78: new 54	java/lang/StringBuilder
    //   81: dup
    //   82: aload_2
    //   83: invokestatic 58	java/lang/String:valueOf	(Ljava/lang/Object;)Ljava/lang/String;
    //   86: invokespecial 59	java/lang/StringBuilder:<init>	(Ljava/lang/String;)V
    //   89: aload 15
    //   91: iload 16
    //   93: invokevirtual 62	org/json/JSONArray:getString	(I)Ljava/lang/String;
    //   96: invokevirtual 66	java/lang/String:toString	()Ljava/lang/String;
    //   99: invokevirtual 70	java/lang/StringBuilder:append	(Ljava/lang/String;)Ljava/lang/StringBuilder;
    //   102: ldc 72
    //   104: invokevirtual 70	java/lang/StringBuilder:append	(Ljava/lang/String;)Ljava/lang/StringBuilder;
    //   107: invokevirtual 73	java/lang/StringBuilder:toString	()Ljava/lang/String;
    //   110: astore 18
    //   112: aload 18
    //   114: astore_2
    //   115: iinc 16 1
    //   118: goto -64 -> 54
    //   121: astore 13
    //   123: new 54	java/lang/StringBuilder
    //   126: dup
    //   127: aload_2
    //   128: invokestatic 58	java/lang/String:valueOf	(Ljava/lang/Object;)Ljava/lang/String;
    //   131: invokespecial 59	java/lang/StringBuilder:<init>	(Ljava/lang/String;)V
    //   134: aload_3
    //   135: ldc 42
    //   137: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   140: invokevirtual 70	java/lang/StringBuilder:append	(Ljava/lang/String;)Ljava/lang/StringBuilder;
    //   143: invokevirtual 73	java/lang/StringBuilder:toString	()Ljava/lang/String;
    //   146: astore_2
    //   147: goto -79 -> 68
    //   150: aload_1
    //   151: ldc 24
    //   153: ldc 75
    //   155: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   158: pop
    //   159: aload_3
    //   160: ldc 77
    //   162: invokevirtual 81	org/json/JSONObject:getJSONObject	(Ljava/lang/String;)Lorg/json/JSONObject;
    //   165: ldc 83
    //   167: invokevirtual 46	org/json/JSONObject:getJSONArray	(Ljava/lang/String;)Lorg/json/JSONArray;
    //   170: astore 9
    //   172: iconst_0
    //   173: istore 10
    //   175: iload 10
    //   177: aload 9
    //   179: invokevirtual 52	org/json/JSONArray:length	()I
    //   182: if_icmpge -106 -> 76
    //   185: aload_1
    //   186: aload 9
    //   188: iload 10
    //   190: invokevirtual 86	org/json/JSONArray:getJSONObject	(I)Lorg/json/JSONObject;
    //   193: ldc 88
    //   195: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   198: aload 9
    //   200: iload 10
    //   202: invokevirtual 86	org/json/JSONArray:getJSONObject	(I)Lorg/json/JSONObject;
    //   205: ldc 90
    //   207: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   210: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   213: pop
    //   214: iinc 10 1
    //   217: goto -42 -> 175
    //   220: astore 4
    //   222: aload_1
    //   223: ldc 24
    //   225: ldc 30
    //   227: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   230: pop
    //   231: aload_1
    //   232: ldc 42
    //   234: ldc 92
    //   236: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   239: pop
    //   240: aload_1
    //   241: areturn
    //   242: astore 8
    //   244: aload_1
    //   245: areturn
    // Local variable table:
    //   start	length	slot	name	signature
    //   0	246	0	paramString	String
    //   7	238	1	localHashMap	java.util.HashMap
    //   10	137	2	localObject	Object
    //   19	141	3	localJSONObject	org.json.JSONObject
    //   220	1	4	localJSONException1	org.json.JSONException
    //   242	1	8	localJSONException2	org.json.JSONException
    //   170	29	9	localJSONArray1	org.json.JSONArray
    //   173	42	10	i	int
    //   121	1	13	localJSONException3	org.json.JSONException
    //   49	41	15	localJSONArray2	org.json.JSONArray
    //   52	64	16	j	int
    //   59	7	17	k	int
    //   110	3	18	str	String
    // Exception table:
    //   from	to	target	type
    //   43	51	121	org/json/JSONException
    //   54	61	121	org/json/JSONException
    //   78	112	121	org/json/JSONException
    //   11	43	220	org/json/JSONException
    //   68	76	220	org/json/JSONException
    //   123	147	220	org/json/JSONException
    //   150	159	220	org/json/JSONException
    //   159	172	242	org/json/JSONException
    //   175	214	242	org/json/JSONException
  }
}
