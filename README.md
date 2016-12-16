# QARK

[![Build Status](https://travis-ci.org/linkedin/qark.svg?branch=master)](https://travis-ci.org/linkedin/qark)

**Q**uick **A**ndroid **R**eview **K**it - This tool is designed to look for several security related Android application vulnerabilities, either in source code or packaged APKs. The tool is also capable of creating "Proof-of-Concept" deployable APKs and/or ADB commands, capable of exploiting many of the vulnerabilities it finds. There is no need to root the test device, as this tool focuses on vulnerabilities that can be exploited under otherwise secure conditions.


## Usage

To run in interactive mode:
```
$ python qarkMain.py
```

To run in headless mode:
```
$ python qarkMain.py --source 1 --pathtoapk /Users/foo/qark/sampleApps/goatdroid/goatdroid.apk --exploit 1 --install 1
or
$ python qarkMain.py --source 2 -c /Users/foo/qark/sampleApps/goatdroid/goatdroid --manifest /Users/foo/qark/sampleApps/goatdroid/goatdroid/AndroidManifest.xml --exploit 1 --install 1
```

The sampleApps folder contains sample APKs that you can test against QARK


##Requirements
- python 2.7.6
- JRE 1.6+ (preferably 1.7+)
- OSX or RHEL6.6 (Others may work, but not fully tested)

##Documentation

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

##Roadmap
Things that are coming soon:
- Rewrite of code to support extensibility
- Bound Service vulnerability detection and exploitation
- Content Provider vulnerability detection and exploitation
- Additional WebView configuration demonstrations
- Static Tapjacking mitigation detection
- File browser capable of using root permissions


##Notice

Note: QARK decompiles Android applications back to raw source code. Please do not use this tool if this may be considered illegal in your juristdiction. If you are unsure, seek legal counsel.

If you run into issues on OSX, especially relating to the outbound call to the Play Store, or the downloading of the SDK, it is 
likely due to your Python/OpenSSL configuration and the fact that recent changes in OSX impacted Python installed via brew. Nuking your
Python installation(s) and re-installing from source may fix your issues.


##License
Copyright 2015 LinkedIn Corp.  All rights reserved.

Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software  distributed under the License is distributed on an "AS IS" BASIS,  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

##Recent Updates
Qark has recently been refactored. qark.py has been renamed to qarkMain.py and is now packagable and runnable from other processes via the runAutomated function in qarkMain.py
