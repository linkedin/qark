Downloading the v2 branch
#########################
::

  ~ git clone -b v2 https://github.com/linkedin/qark


Installation
############

With pip (no security checks on requirements)
#############################################
::

  ~ pip install qark
  ~ qark --help


With `requirements.txt` (security checks on requirements)
#########################################################

::

  ~ wget https://raw.githubusercontent.com/linkedin/qark/v2/requirements.txt
  ~ pip install -r requirements.txt
  ~ pip install .
  ~ qark --help


Exploit APK
###########
QARK can generate a basic exploit APK for a few of the vulnerabilities that have been found.

To generate the exploit APK there are a few steps to follow. You need to have the Android SDK v21 and build-tools v21.1.2

1. Install the android SDK, you can get it under the 'command line tools': https://developer.android.com/studio/#downloads
2. Unzip the android SDK
3. Go into the new directory and generate the licenses with `bin/sdkmanager --licenses`
4. Make sure the generated licenses are in the android SDK directory.
5. Install the SDK and the proper build-tools version: `bin/sdkmanager --install "platforms;android-21" "sources;android-21" "build-tools;21.1.2"`