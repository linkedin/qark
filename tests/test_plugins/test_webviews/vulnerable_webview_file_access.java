class WebviewJavascript extends WebViewClient {
  public void vulnerableMethodSetAllowFileAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
  }
  public void vulnerableMethodSetAllowFileAccess2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings webSettings = web.getSettings();
    webSettings.setAllowFileAccess(true);
  }
  public void nonVulnerableMethodSetAllowFileAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.getSettings().setAllowFileAccess(false);
  }
  public void nonVulnerableMethodSetAllowFileAccess2() {
    WebView web = (WebView) findViewById(R.id.webview);
    WebSettings web_settings = web.getSettings();
    web_settings.setAllowFileAccess(false);
  }
}
