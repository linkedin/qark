Quick Android Review Kit
========================
This tool is designed to look for several security related Android application vulnerabilities, either in source code or packaged APKs. The tool is also capable of creating "Proof-of-Concept" deployable APKs and/or ADB commands, capable of exploiting many of the vulnerabilities it finds. There is no need to root the test device, as this tool focuses on vulnerabilities that can be exploited under otherwise secure conditions.


Requirements
============
Tested on Python 2.7.13 and 3.6
Tested on OSX, Linux, and Windows

Usage
=====
For more options please see the ``--help`` command.

APK::

  ~ qark --apk path/to/my.apk

Java source code files::

  ~ qark --java path/to/parent/java/folder
  ~ qark --java path/to/specific/java/file.java


Results
=======
A report is generated in JSON and can be built into other format types, to change the report type please use the ``--report-type`` flag.

Installation
============
With pip (no security checks on requirements)::

  ~ pip install --user qark  # --user is only needed if not using a virtualenv
  ~ qark --help


With `requirements.txt` (security checks on requirements)::

  ~ git clone https://github.com/linkedin/qark
  ~ cd qark
  ~ pip install -r requirements.txt
  ~ pip install . --user  # --user is only needed if not using a virtualenv
  ~ qark --help


Exploit APK
===========
QARK can generate a basic exploit APK for a few of the vulnerabilities that have been found.

To generate the exploit APK there are a few steps to follow. You need to have the Android SDK v21 and build-tools v21.1.2

1. Install the android SDK, you can get it under the 'command line tools': https://developer.android.com/studio/#downloads
2. Unzip the android SDK
3. Go into the new directory and generate the licenses with `bin/sdkmanager --licenses`
4. Make sure the generated licenses are in the android SDK directory.
5. Install the SDK and the proper build-tools version: `bin/sdkmanager --install "platforms;android-21" "sources;android-21" "build-tools;21.1.2"`

Checks
======
QARK is an easy to use tool capable of finding common security vulnerabilities in Android applications. Unlike commercial products, it is 100% free to use. QARK features educational information allowing security reviewers to locate precise, in-depth explanations of the vulnerabilities. QARK automates the use of multiple decompilers, leveraging their combined outputs, to produce superior results, when decompiling APKs. Finally, the major advantage QARK has over traditional tools, that just point you to possible vulnerabilities, is that it can produce ADB commands, or even fully functional APKs, that turn hypothetical vulnerabilities into working "POC" exploits.

Included in the types of security vulnerabilities this tool attempts to find are:

- Inadvertently exported components
- Improperly protected exported components
- Intents which are vulnerable to interception or eavesdropping
- Improper x.509 certificate validation
- Creation of world-readable or world-writeable files
- Activities which may leak data
- The use of Sticky Intents
- Insecurely created Pending Intents
- Sending of insecure Broadcast Intents
- Private keys embedded in the source
- Weak or improper cryptography use
- Potentially exploitable WebView configurations
- Exported Preference Activities
- Tapjacking
- Apps which enable backups
- Apps which are debuggable
- Apps supporting outdated API versions, with known vulnerabilities


Notice
======
Note: QARK decompiles Android applications back to raw source code. Please do not use this tool if this may be considered illegal in your juristdiction. If you are unsure, seek legal counsel.

If you run into issues on OSX, especially relating to the outbound call to the Play Store, or the downloading of the SDK, it is
likely due to your Python/OpenSSL configuration and the fact that recent changes in OSX impacted Python installed via brew. Nuking your
Python installation(s) and re-installing from source may fix your issues.


License
=======
Copyright 2015 LinkedIn Corp.  All rights reserved.

Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. 
You may obtain a copy of the License `here <http://www.apache.org/licenses/LICENSE-2.0/>`_.
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.