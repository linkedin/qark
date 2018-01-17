from qark.scanner.plugin import get_plugins

import pytest


@pytest.mark.parametrize("category, num_plugins", [
    (None, 0),
    ("manifest", 0),
])
def test_plugin(category, num_plugins):
    assert len(get_plugins(category=category)) > num_plugins
    assert len(get_plugins(category="non_existant_category")) == 0
