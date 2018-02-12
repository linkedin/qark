package test_plugins.test_cert_plugins;

public class testHostnameVerifier {
  public static final X509HostnameVerifier ALLOW_ALL_HOSTNAME_VERIFIER = new AllowAllHostnameVerifier();
}

public class testSetHostnameVerifier {
  public static void vulnerableMethod() {
    URL url = new URL("https://example.org/");
    HttpsURLConnection urlConnection = (HttpsURLConnection)url.openConnection();
    urlConnection.setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);
  }
  public static void nonVulnerableMethod() {
    URL url = new URL("https://example.org/");
    HttpsURLConnection urlConnection = (HttpsURLConnection)url.openConnection();
    urlConnection.setHostnameVerifier(SSLSocketFactory.SOMETHING_ELSE);
  }
}
