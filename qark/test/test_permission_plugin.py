from modules import common
from plugins.permission_plugin import PermissionPlugin

manifest_loc = './fixtures/app_manifest'
permissionPlugin = PermissionPlugin()


def setup():
    with open(manifest_loc, 'r') as f:
        common.manifest = f.read()


def testGetUserCreatedPermissions():
    setup()
    permissions = permissionPlugin.getUserCreatedPermissions()
    assert len(permissions) == 4


def testGetDangerousPermissions():
    setup()
    permissions = permissionPlugin.getUserCreatedPermissions()
    count = 0
    expected = [True, False, False, True]
    for permission in permissions:
        assert permissionPlugin.isDangerousPermission(permission) == expected[count]
        count += 1


if __name__ == '__main__':
    testGetUserCreatedPermissions()
    testGetDangerousPermissions()