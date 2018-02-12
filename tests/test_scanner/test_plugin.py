from qark.scanner.plugin import get_plugins, get_plugin_source

import pytest


@pytest.mark.parametrize("category, num_plugins", [
    (None, 0),
    ("manifest", 0),
])
def test_get_plugins(category, num_plugins):
    assert len(get_plugins(category=category)) > num_plugins
    assert len(get_plugins(category="non_existant_category")) == 0


def test_get_plugin_source():
    assert 0 < len(get_plugin_source(category="manifest").list_plugins())
    assert 0 < len(get_plugin_source().list_plugins())
    assert 0 == len(get_plugin_source(category="does_not_exist").list_plugins())
