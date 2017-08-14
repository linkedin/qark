import subprocess


def test_autodiscover_regression():
    result = subprocess.call("python ../qarkMain.py --source 2 --manifest testData/goatdroid/goatdroid/AndroidManifest.xml -a 1 --exploit 0 --install 1 -t ACCEPTTERMS".split())
    assert 0 == result
