package org.owasp.goatdroid.fourgoats.rest.checkin;

public class CheckinResponse
{
  public CheckinResponse() {}
  
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
    //   49: astore 18
    //   51: iconst_0
    //   52: istore 19
    //   54: aload 18
    //   56: invokevirtual 52	org/json/JSONArray:length	()I
    //   59: istore 20
    //   61: iload 19
    //   63: iload 20
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
    //   89: aload 18
    //   91: iload 19
    //   93: invokevirtual 62	org/json/JSONArray:getString	(I)Ljava/lang/String;
    //   96: invokevirtual 66	java/lang/String:toString	()Ljava/lang/String;
    //   99: invokevirtual 70	java/lang/StringBuilder:append	(Ljava/lang/String;)Ljava/lang/StringBuilder;
    //   102: ldc 72
    //   104: invokevirtual 70	java/lang/StringBuilder:append	(Ljava/lang/String;)Ljava/lang/StringBuilder;
    //   107: invokevirtual 73	java/lang/StringBuilder:toString	()Ljava/lang/String;
    //   110: astore 21
    //   112: aload 21
    //   114: astore_2
    //   115: iinc 19 1
    //   118: goto -64 -> 54
    //   121: astore 16
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
    //   159: aload_1
    //   160: ldc 77
    //   162: aload_3
    //   163: ldc 77
    //   165: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   168: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   171: pop
    //   172: aload_1
    //   173: ldc 79
    //   175: aload_3
    //   176: ldc 79
    //   178: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   181: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   184: pop
    //   185: aload_1
    //   186: ldc 81
    //   188: aload_3
    //   189: ldc 81
    //   191: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   194: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   197: pop
    //   198: aload_3
    //   199: ldc 83
    //   201: invokevirtual 87	org/json/JSONObject:getJSONObject	(Ljava/lang/String;)Lorg/json/JSONObject;
    //   204: ldc 89
    //   206: invokevirtual 46	org/json/JSONObject:getJSONArray	(Ljava/lang/String;)Lorg/json/JSONArray;
    //   209: astore 12
    //   211: iconst_0
    //   212: istore 13
    //   214: iload 13
    //   216: aload 12
    //   218: invokevirtual 52	org/json/JSONArray:length	()I
    //   221: if_icmpge -145 -> 76
    //   224: aload_1
    //   225: aload 12
    //   227: iload 13
    //   229: invokevirtual 92	org/json/JSONArray:getJSONObject	(I)Lorg/json/JSONObject;
    //   232: ldc 94
    //   234: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   237: aload 12
    //   239: iload 13
    //   241: invokevirtual 92	org/json/JSONArray:getJSONObject	(I)Lorg/json/JSONObject;
    //   244: ldc 96
    //   246: invokevirtual 28	org/json/JSONObject:getString	(Ljava/lang/String;)Ljava/lang/String;
    //   249: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   252: pop
    //   253: iinc 13 1
    //   256: goto -42 -> 214
    //   259: astore 4
    //   261: aload_1
    //   262: ldc 24
    //   264: ldc 30
    //   266: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   269: pop
    //   270: aload_1
    //   271: ldc 42
    //   273: ldc 98
    //   275: invokevirtual 40	java/util/HashMap:put	(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;
    //   278: pop
    //   279: aload_1
    //   280: areturn
    //   281: astore 11
    //   283: aload_1
    //   284: areturn
    // Local variable table:
    //   start	length	slot	name	signature
    //   0	285	0	paramString	String
    //   7	277	1	localHashMap	java.util.HashMap
    //   10	137	2	localObject	Object
    //   19	180	3	localJSONObject	org.json.JSONObject
    //   259	1	4	localJSONException1	org.json.JSONException
    //   281	1	11	localJSONException2	org.json.JSONException
    //   209	29	12	localJSONArray1	org.json.JSONArray
    //   212	42	13	i	int
    //   121	1	16	localJSONException3	org.json.JSONException
    //   49	41	18	localJSONArray2	org.json.JSONArray
    //   52	64	19	j	int
    //   59	7	20	k	int
    //   110	3	21	str	String
    // Exception table:
    //   from	to	target	type
    //   43	51	121	org/json/JSONException
    //   54	61	121	org/json/JSONException
    //   78	112	121	org/json/JSONException
    //   11	43	259	org/json/JSONException
    //   68	76	259	org/json/JSONException
    //   123	147	259	org/json/JSONException
    //   150	198	259	org/json/JSONException
    //   198	211	281	org/json/JSONException
    //   214	253	281	org/json/JSONException
  }
}
