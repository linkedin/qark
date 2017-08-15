import os
import subprocess

import qark.modules.sdkManager


def test_autodiscover_regression():
    qark.sdkManager.common.rootDir = '..'

    if not os.path.exists("../settings.properties"):
        f = open("../settings.properties",'w')
        f.close()

    qark.sdkManager.common.writeKey("rootDir", "..")
    qark.modules.sdkManager.download_sdk()  # first download the sdk so that we can use it
    result = subprocess.call("python ../qarkMain.py --source 2 --manifest testData/goatdroid/goatdroid/AndroidManifest.xml -a 1 --exploit 0 --install 0".split())
    assert 0 == result
