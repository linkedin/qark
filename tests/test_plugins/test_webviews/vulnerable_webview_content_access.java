class WebviewJavascript extends WebViewClient {
  public void vulnerableMethodSetAllowContentAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
  }
  public void vulnerableMethodSetAllowContentAccess2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings webSettings = web.getSettings();
    webSettings.setAllowContentAccess(true);
  }
  public void nonVulnerableMethodSetAllowFileAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.getSettings().setAllowContentAccess(false);
  }
  public void nonVulnerableMethodSetAllowFileAccess2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings web_settings = web.getSettings();
    web_settings.setAllowContentAccess(false);
  }
}
