class vulnerable_webview_universal_access_from_urls extends WebViewClient {
  public void vulnerableMethodSetAllowUniversalAccessFromURLs() {
    WebView web = (WebView) findViewById(R.id.webview);
  }
  public void vulnerableMethodSetAllowUniversalAccessFromURLs2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings webSettings = web.getSettings();
    webSettings.setAllowUniversalAccessFromFileURLs(true);
  }
  public void nonVulnerableMethodSetAllowUniversalAccessFromURLs() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.getSettings().setAllowUniversalAccessFromFileURLs(false);
  }
  public void nonVulnerableMethodSetAllowUniversalAccessFromURLs2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings web_settings = web.getSettings();
    web_settings.setAllowUniversalAccessFromFileURLs(false);
  }
}
