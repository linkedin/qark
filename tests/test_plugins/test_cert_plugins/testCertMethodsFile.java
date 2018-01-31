class VulnerableCheckServerTrusted {
  public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {}
}
class VulnerableCheckServerTrustedEmptyReturn {
  public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {return;}
}
class VulnerableOnReceivedSslError {
  public void onReceivedSslError(Webview view, SslErrorHandler handler, SslError error) throws CertificateException {
    handler.proceed();
  }
}
class NonVulnerableOnReceivedSslError {
  public void onReceivedSslError(Webview view, SslErrorHandler handler, SslError error) throws CertificateException {
    // this one has more logic than just handler.proceed even though it is just as vulnerable
    if( 1 > 0 ) {
      handler.proceed();
    }
  }
}