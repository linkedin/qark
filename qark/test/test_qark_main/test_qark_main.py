import subprocess

from qark.modules.sdkManager import download_sdk


def test_autodiscover_regression():
    download_sdk()  # first download the sdk so that we can use it
    result = subprocess.call("python ../qarkMain.py --source 2 --manifest testData/goatdroid/goatdroid/AndroidManifest.xml -a 1 --exploit 0 --install 0".split(), stdin=PIPE)
    assert 0 == result
