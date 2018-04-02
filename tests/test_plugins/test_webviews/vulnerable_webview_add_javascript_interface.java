class JsObject {
  @JavascriptInterface
  public String toString() { return "injectedObject"; }
}

class vulnerable_webview_add_javascript_interface extends WebViewClient {
  public void vulnerableMethodSetAllowFileAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.addJavascriptInterface(new JsObject(), "injectedObject");
  }
  public void vulnerableMethodSetAllowFileAccess2(WebView web) {
    web.addJavascriptInterface(new JsObject(), "injectedObject");
  }
  public void nonVulnerableMethodSetAllowFileAccess(WebView web) {
    pass;
  }
}
