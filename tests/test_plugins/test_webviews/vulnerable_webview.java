class WebviewJavascript extends WebViewClient {
  public void vulnerableMethodJavascriptEnabled() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    web.getSettings().setJavaScriptEnabled(true);
  }
  public void nonVulnerableMethodJavascriptEnabled() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    web.getSettings().setJavaScriptEnabled();
  }
  public void nonVulnerableMethod2JavascriptEnabled() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    web.getSettings().setJavaScriptEnabled(false);
  }
  public void vulnerableMethodLoadDataWithBaseURL() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    web.loadDataWithBaseURL("file:///android_res/drawable/", "<html></html>", "text/html", "UTF-8", null);
  }
  public void nonVulnerableMethodLoadDataWithBaseURL() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    web.loadDataWithBaseURL();
  }
  public void vulnerableMethodSetAllowFileAccessSetAllowContentAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    WebSettings webSettings = web.getSettings();
  }
  public void nonVulnerableMethodSetAllowFileAccessSetAllowContentAccess() {
    WebView web = (WebView) findViewById(R.id.webview);
    web.setWebChromeClient(new MyCustomChromeClient(this));
    web.setWebViewClient(new MyCustomWebViewClient(this));
    web.clearCache(true);
    web.clearHistory();
    WebSettings webSettings = web.getSettings();
    webSettings.setAllowFileAccess(false);
    webSettings.setAllowContentAccess(false);
  }
}