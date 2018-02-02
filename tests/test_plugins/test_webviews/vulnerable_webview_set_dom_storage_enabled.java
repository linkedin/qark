class vulnerable_webview_set_dom_storage_enabled extends WebViewClient {
  public void vulnerableMethodSetDomStorageEnabled() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.getSettings().setDomStorageEnabled(true);
  }
  public void vulnerableMethodSetAllowFileAccess2(WebView web) {
    web.setDomStorageEnabled(true);
  }
  public void nonVulnerableMethodSetAllowFileAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
  }
}
