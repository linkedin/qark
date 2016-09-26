/*
 * Decompiled with CFR 0_115.
 * 
 * Could not load the following classes:
 *  android.content.Context
 *  org.apache.http.HttpEntity
 *  org.apache.http.HttpHost
 *  org.apache.http.HttpResponse
 *  org.apache.http.NameValuePair
 *  org.apache.http.StatusLine
 *  org.apache.http.client.ClientProtocolException
 *  org.apache.http.client.HttpClient
 *  org.apache.http.client.entity.UrlEncodedFormEntity
 *  org.apache.http.client.methods.HttpGet
 *  org.apache.http.client.methods.HttpPost
 *  org.apache.http.client.methods.HttpUriRequest
 *  org.apache.http.conn.ClientConnectionManager
 *  org.apache.http.message.BasicNameValuePair
 *  org.apache.http.params.HttpParams
 */
package org.owasp.goatdroid.fourgoats.requestresponse;

import android.content.Context;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URLEncoder;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ClientConnectionManager;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.HttpParams;
import org.owasp.goatdroid.fourgoats.misc.Utils;
import org.owasp.goatdroid.fourgoats.requestresponse.CustomSSLSocketFactory;
import org.owasp.goatdroid.fourgoats.requestresponse.RequestMethod;

public class AuthenticatedRestClient {
    private static /* synthetic */ int[] $SWITCH_TABLE$org$owasp$goatdroid$fourgoats$requestresponse$RequestMethod;
    private ArrayList<NameValuePair> headers;
    private String message;
    private ArrayList<NameValuePair> params;
    private String response;
    private int responseCode;
    private String sessionToken;
    private String url;

    /*
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     */
    static /* synthetic */ int[] $SWITCH_TABLE$org$owasp$goatdroid$fourgoats$requestresponse$RequestMethod() {
        int[] arrn;
        int[] arrn2 = $SWITCH_TABLE$org$owasp$goatdroid$fourgoats$requestresponse$RequestMethod;
        if (arrn2 != null) {
            return arrn2;
        }
        arrn = new int[RequestMethod.values().length];
        try {
            arrn[RequestMethod.GET.ordinal()] = 1;
        }
        catch (NoSuchFieldError var2_3) {}
        try {
            arrn[RequestMethod.POST.ordinal()] = 2;
        }
        catch (NoSuchFieldError var3_2) {}
        $SWITCH_TABLE$org$owasp$goatdroid$fourgoats$requestresponse$RequestMethod = arrn;
        return arrn;
    }

    public AuthenticatedRestClient(String string2, String string3) {
        this.url = string2;
        this.sessionToken = string3;
        this.params = new ArrayList();
        this.headers = new ArrayList();
    }

    /*
     * Loose catch block
     * Enabled aggressive block sorting
     * Enabled unnecessary exception pruning
     * Enabled aggressive exception aggregation
     * Lifted jumps to return sites
     */
    private static String convertStreamToString(InputStream inputStream) {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        StringBuilder stringBuilder = new StringBuilder();
        do {
            String string2;
            block11 : {
                string2 = bufferedReader.readLine();
                if (string2 != null) break block11;
                inputStream.close();
                return stringBuilder.toString();
            }
            stringBuilder.append(String.valueOf(string2) + "\n");
            continue;
            break;
        } while (true);
        catch (IOException iOException) {
            try {
                inputStream.close();
                return stringBuilder.toString();
            }
            catch (IOException var6_5) {
                return stringBuilder.toString();
            }
        }
        catch (Throwable throwable) {
            try {
                inputStream.close();
            }
            catch (IOException var4_7) {
                throw throwable;
            }
            throw throwable;
        }
        catch (IOException iOException2) {
            return stringBuilder.toString();
        }
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    private void executeRequest(HttpUriRequest httpUriRequest, String string2, Context context) throws KeyManagementException, NoSuchAlgorithmException {
        HttpClient httpClient = CustomSSLSocketFactory.getNewHttpClient();
        HashMap<String, String> hashMap = Utils.getProxyMap(context);
        String string3 = hashMap.get("proxyHost");
        String string4 = hashMap.get("proxyPort");
        if (!string3.equals("") && !string4.equals("")) {
            HttpHost httpHost = new HttpHost(string3, Integer.parseInt(string4));
            httpClient.getParams().setParameter("http.route.default-proxy", (Object)httpHost);
        }
        HttpResponse httpResponse = httpClient.execute(httpUriRequest);
        this.responseCode = httpResponse.getStatusLine().getStatusCode();
        this.message = httpResponse.getStatusLine().getReasonPhrase();
        HttpEntity httpEntity = httpResponse.getEntity();
        if (httpEntity == null) return;
        try {
            InputStream inputStream = httpEntity.getContent();
            this.response = AuthenticatedRestClient.convertStreamToString(inputStream);
            inputStream.close();
            return;
        }
        catch (ClientProtocolException var9_12) {
            httpClient.getConnectionManager().shutdown();
            return;
        }
        catch (IOException var8_13) {
            httpClient.getConnectionManager().shutdown();
            return;
        }
    }

    public void AddHeader(String string2, String string3) {
        this.headers.add((NameValuePair)new BasicNameValuePair(string2, string3));
    }

    public void AddParam(String string2, String string3) {
        this.params.add((NameValuePair)new BasicNameValuePair(string2, string3));
    }

    /*
     * Unable to fully structure code
     * Enabled aggressive block sorting
     * Lifted jumps to return sites
     */
    public void Execute(RequestMethod var1_1, Context var2_2) throws Exception {
        block0 : switch (AuthenticatedRestClient.$SWITCH_TABLE$org$owasp$goatdroid$fourgoats$requestresponse$RequestMethod()[var1_1.ordinal()]) {
            default: {
                return;
            }
            case 1: {
                var6_3 = "";
                if (this.params.isEmpty()) ** GOTO lbl-1000
                var6_3 = String.valueOf(var6_3) + "?";
                var10_4 = this.params.iterator();
                do {
                    if (!var10_4.hasNext()) lbl-1000: // 2 sources:
                    {
                        var7_7 = new HttpGet(String.valueOf(this.url) + var6_3);
                        var8_8 = this.headers.iterator();
                        break block0;
                    }
                    var11_5 = var10_4.next();
                    var12_6 = String.valueOf(var11_5.getName()) + "=" + URLEncoder.encode(var11_5.getValue(), "UTF-8");
                    if (var6_3.length() > 1) {
                        var6_3 = String.valueOf(var6_3) + "&" + var12_6;
                        continue;
                    }
                    var6_3 = String.valueOf(var6_3) + var12_6;
                } while (true);
            }
            case 2: {
                var3_10 = new HttpPost(this.url);
                var4_11 = this.headers.iterator();
                ** GOTO lbl33
            }
        }
        do {
            if (!var8_8.hasNext()) {
                var7_7.addHeader("Cookie", "SESS=" + this.sessionToken);
                this.executeRequest((HttpUriRequest)var7_7, this.url, var2_2);
                return;
            }
            var9_9 = var8_8.next();
            var7_7.addHeader(var9_9.getName(), var9_9.getValue());
        } while (true);
lbl33: // 1 sources:
        do {
            if (!var4_11.hasNext()) {
                if (!this.params.isEmpty()) {
                    var3_10.setEntity((HttpEntity)new UrlEncodedFormEntity(this.params, "UTF-8"));
                }
                var3_10.addHeader("Cookie", "SESS=" + this.sessionToken);
                this.executeRequest((HttpUriRequest)var3_10, this.url, var2_2);
                return;
            }
            var5_12 = var4_11.next();
            var3_10.addHeader(var5_12.getName(), var5_12.getValue());
        } while (true);
    }

    public String getErrorMessage() {
        return this.message;
    }

    public String getResponse() {
        return this.response;
    }

    public int getResponseCode() {
        return this.responseCode;
    }
}

