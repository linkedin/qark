from subprocess import Popen, PIPE


def test_autodiscover_regression():
    process = Popen("python ../qarkMain.py --source 2 --manifest testData/goatdroid/goatdroid/AndroidManifest.xml -a 1 --exploit 0 --install 1 -t ACCEPTTERMS".split(), stdin=PIPE)
    out,err = process.communicate('y')  # install the SDK if it asks
    print(out, err)
    assert 1 == 2
    result = process.wait()
    assert 0 == result
