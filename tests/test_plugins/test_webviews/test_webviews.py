import os

import pytest

from qark.issue import Severity
from qark.plugins.webview.add_javascript_interface import AddJavascriptInterface, ADD_JAVASCRIPT_INTERFACE_DESCRIPTION
from qark.plugins.webview.javascript_enabled import JavascriptEnabled, JAVASCRIPT_ENABLED_DESCRIPTION
from qark.plugins.webview.load_data_with_base_url import LoadDataWithBaseURL, LOAD_DATA_WITH_BASE_URL_DESCRIPTION
from qark.plugins.webview.set_allow_content_access import SetAllowContentAccess, SET_ALLOW_CONTENT_ACCESS_DESCRIPTION
from qark.plugins.webview.set_allow_file_access import SetAllowFileAccess, SET_ALLOW_FILE_ACCESS_DESCRIPTION
from qark.plugins.webview.set_allow_universal_access_from_file_urls import (
    SetAllowUniversalAccessFromFileURLs,
    SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION,
)
from qark.plugins.webview.set_dom_storage_enabled import SetDomStorageEnabled, SET_DOM_STORAGE_ENABLED_DESCRIPTION
from qark.scanner.plugin import ManifestPlugin

VULNERABLE_WEBVIEW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "vulnerable_webview.java")
VULNERABLE_FILE_ACCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "vulnerable_webview_file_access.java")
VULNERABLE_CONTENT_ACCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "vulnerable_webview_content_access.java")
VULNERABLE_UNIVERSAL_ACCESS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "vulnerable_webview_universal_access_from_urls.java")
VULNERABLE_JAVASCRIPT_INTERFACE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "vulnerable_webview_add_javascript_interface.java")
VULNERABLE_DOM_STORAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "vulnerable_webview_set_dom_storage_enabled.java")


def test_javascript_enabled():
    plugin = JavascriptEnabled()
    plugin.update(VULNERABLE_WEBVIEW_PATH)
    plugin.run()
    assert 1 == len(plugin.issues)
    issue = plugin.issues[0]
    assert plugin.name == issue.name
    assert "webview" == issue.category
    assert JAVASCRIPT_ENABLED_DESCRIPTION == issue.description
    assert Severity.WARNING == issue.severity


def test_load_data_with_base_url():
    plugin = LoadDataWithBaseURL()
    plugin.update(VULNERABLE_WEBVIEW_PATH)
    plugin.run()
    assert 1 == len(plugin.issues)
    issue = plugin.issues[0]
    assert plugin.name == issue.name
    assert "webview" == issue.category
    assert LOAD_DATA_WITH_BASE_URL_DESCRIPTION == issue.description
    assert Severity.WARNING == issue.severity


def test_set_allow_file_access():
    plugin = SetAllowFileAccess()
    plugin.update(VULNERABLE_FILE_ACCESS)
    plugin.run()
    assert 2 == len(plugin.issues)
    for issue in plugin.issues:
        assert "webview" == issue.category
        assert SET_ALLOW_FILE_ACCESS_DESCRIPTION == issue.description
        assert "Webview enables file access" == issue.name
        assert Severity.WARNING == issue.severity


def test_set_allow_content_access():
    plugin = SetAllowContentAccess()
    plugin.update(VULNERABLE_CONTENT_ACCESS)
    plugin.run()
    assert 2 == len(plugin.issues)
    for issue in plugin.issues:
        assert "webview" == issue.category
        assert SET_ALLOW_CONTENT_ACCESS_DESCRIPTION == issue.description
        assert "Webview enables content access" == issue.name
        assert Severity.WARNING == issue.severity


@pytest.mark.parametrize("min_sdk, num_issues", [
    (1, 2),
    (14, 2),
    (15, 2),
    (16, 1),
    (30, 1),
])
def test_set_allow_universal_access_from_file_urls(min_sdk, num_issues):
    ManifestPlugin.min_sdk = min_sdk
    plugin = SetAllowUniversalAccessFromFileURLs()
    plugin.update(VULNERABLE_UNIVERSAL_ACCESS)
    plugin.run()
    assert num_issues == len(plugin.issues)
    for issue in plugin.issues:
        assert "webview" == issue.category
        assert SET_ALLOW_UNIVERSAL_ACCESS_FROM_FILE_URLS_DESCRIPTION == issue.description
        assert "Webview enables universal access for JavaScript" == issue.name
        assert Severity.WARNING == issue.severity


@pytest.mark.parametrize("min_sdk, num_issues", [
    (1, 2),
    (15, 2),
    (16, 2),
    (17, 0),
    (30, 0),
])
def test_set_add_javascript_interface(min_sdk, num_issues):
    ManifestPlugin.min_sdk = min_sdk
    plugin = AddJavascriptInterface()
    plugin.update(file_path=VULNERABLE_JAVASCRIPT_INTERFACE)
    plugin.run()
    assert num_issues == len(plugin.issues)
    for issue in plugin.issues:
        assert "webview" == issue.category
        assert ADD_JAVASCRIPT_INTERFACE_DESCRIPTION == issue.description
        assert "Webview uses addJavascriptInterface pre-API 17" == issue.name
        assert Severity.WARNING == issue.severity


def test_set_dom_storage_enabled():
    plugin = SetDomStorageEnabled()
    plugin.update(VULNERABLE_DOM_STORAGE)

    plugin.run()
    assert 2 == len(plugin.issues)
    for issue in plugin.issues:
        assert "webview" == issue.category
        assert SET_DOM_STORAGE_ENABLED_DESCRIPTION == issue.description
        assert "Webview enables DOM Storage" == issue.name
        assert Severity.WARNING == issue.severity
