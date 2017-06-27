from __future__ import absolute_import

'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''
import re, sys
import logging

import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules import common
from modules import report
from modules import filters
from modules.report import ReportIssue
from modules.common import Severity, ReportIssue
from modules.createExploit import ExploitType
from lib.pubsub import pub
from modules.common import terminalPrint

parser = plyj.Parser()
tree = ''


def main(queue):
    global parser
    global tree
    results = []
    count = 0

    if common.minSdkVersion < 19:
        weak_rng_warning(results)
    find_key_files(results)
    for j in common.java_files:
        count = count + 1
        pub.sendMessage('progress', bar='Crypto issues', percent=round(count * 100 / common.java_files.__len__()))
        try:
            tree = parser.parse_file(j)
            if tree is not None:
                # if re.search(r'\.getInstance\(',str(tree)):
                #	print "YES"
                for type_decl in tree.type_declarations:
                    if type(type_decl) is m.ClassDeclaration:
                        for t in type_decl.body:
                            try:
                                recursive_ecb_check(t, j, results)
                            # fixedSeedCheck(t,j)
                            except Exception as e:
                                common.logger.debug("Error running recursive_ecb_check in cryptoFlaws.py: " + str(e))
                                report.write("parsingerror-issues-list",
                                             "Error running recursive_ecb_check in cryptoFlaws.py: " + str(e), "strong")

                            # Using a fixed seed with SecureRandom
                for import_decl in tree.import_declarations:
                    try:
                        if 'SecureRandom' in import_decl.name.value:
                            if "setSeed" in str(tree):
                                issue = ReportIssue()
                                issue.setCategory(ExploitType.CRYPTO)
                                issue.setDetails(
                                    "setSeed should not be called with SecureRandom, as it is insecure. Specifying a fixed seed will cause the instance to return a predictable sequence of numbers. This may be useful for testing but it is not appropriate for secure use.")
                                issue.setFile(str(j))
                                issue.setSeverity(Severity.VULNERABILITY)
                                results.append(issue)

                                issue = terminalPrint()
                                issue.setLevel(Severity.VULNERABILITY)
                                issue.setData(
                                    "setSeed should not be called with SecureRandom, as it is insecure. Specifying a fixed seed will cause the instance to return a predictable sequence of numbers. This may be useful for testing but it is not appropriate for secure use.")
                                results.append(issue)

                            if "generateSeed" in str(tree):
                                issue = ReportIssue()
                                issue.setCategory(ExploitType.CRYPTO)
                                issue.setDetails(
                                    "generateSeed should not be called with SecureRandom, as it is insecure. Specifying a fixed seed will cause the instance to return a predictable sequence of numbers. This may be useful for testing but it is not appropriate for secure use.")
                                issue.setFile(str(j))
                                issue.setSeverity(Severity.VULNERABILITY)
                                results.append(issue)

                                issue = terminalPrint()
                                issue.setLevel(Severity.VULNERABILITY)
                                issue.setData(
                                    "generateSeed should not be called with SecureRandom, as it is insecure. Specifying a fixed seed will cause the instance to return a predictable sequence of numbers. This may be useful for testing but it is not appropriate for secure use. ")
                                results.append(issue)
                    except Exception as e:
                        common.logger.debug("Error checking insecure used of SecureRandom in cryptoFlaws.py: " + str(e))
                        report.write("parsingerror-issues-list",
                                     "Error checking insecure used of SecureRandom in cryptoFlaws.py: " + str(e))

        except Exception as e:
            common.logger.debug("Unable to create tree for " + str(j))
            report.write("parsingerror-issues-list", "Unable to create tree for " + str(j), "strong")
    queue.put(results)
    return


def weak_rng_warning(results):
    # TODO - check for any actual use of RNG
    # common.logger.warning("Key generation, signing, encryption, and random number generation may not receive cryptographically strong values due to improper initialization of the underlying PRNG on Android 4.3 (API level 18) and below. If your application relies on cryptographically secure random number generation you should apply the workaround described in https://android-developers.blogspot.com/2013/08/some-securerandom-thoughts.htm. More information: https://android-developers.blogspot.com/2013/08/some-securerandom-thoughts.html")
    return


'''
	#TODO - Need to finish this
def fixed_seed_check(t,filename):
	SecureRandom
	------------
	Summary: Using a fixed seed with SecureRandom

	Priority: 9 / 10
	Severity: Warning
	Category: Performance

	Specifying a fixed seed will cause the instance to return a predictable
	sequence of numbers. This may be useful for testing but it is not appropriate
	for secure use.

	More information: 
	http://developer.android.com/reference/java/security/SecureRandom.html
	if type(t) is m.Variable:
		if hasattr(t,'type'):
			if hasattr(t.type,'name'):
				if hasattr(t.type.name,'value'):
					if str(t.type.name.value)=='SecureRandom':
						if hasattr(t.type,'type_arguments'):
							if len(t.type.type_arguments)>0:
								print "T: " + str(t)
								print "FILE: " + str(filename)
								#raw_input("SEEDED SecureRandom")
	elif type(t) is list:
		for l in t:
			fixedSeedCheck(l,filename)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			fixedSeedCheck(getattr(t,f),filename)
	elif re.search(r'SecureRandom', str(t)):
		print "FILE: " + str(filename)
		#raw_input("T: " + str(t))
	return
'''


def recursive_ecb_check(t, filename, results):
    # TODO - review this for thoroughness
    # TODO - need to verify .getInstance is actually being invoked on a Cipher object
    # TODO - we could whittle down the possibilities by checking the imports as well
    if type(t) is m.MethodInvocation:
        if hasattr(t, 'name'):
            if str(t.name) == 'getInstance':
                if hasattr(t, 'arguments'):
                    for a in t.arguments:
                        if type(a) is m.Literal:
                            # sets mode to ECB
                            if re.search(r'.*\/ECB\/.*', str(a.value)):

                                issue = ReportIssue()
                                issue.setCategory(ExploitType.CRYPTO)
                                issue.setDetails(
                                    "getInstance should not be called with ECB as the cipher mode, as it is insecure. ")
                                issue.setFile(str(filename))
                                issue.setSeverity(Severity.VULNERABILITY)
                                results.append(issue)

                                issue = terminalPrint()
                                issue.setLevel(Severity.VULNERABILITY)
                                issue.setData(
                                    "getInstance should not be called with ECB as the cipher mode, as it is insecure. ")
                                results.append(issue)

                            # sets mode to something other than ECB
                            elif re.search(r'.*/.*/.*', str(a.value)):
                                return
                            # No mode set
                            elif str(a.value) == '':
                                issue = ReportIssue()
                                issue.setCategory(ExploitType.CRYPTO)
                                issue.setDetails(
                                    "getInstance should not be called without setting the cipher mode because the default mode on android is ECB, which is insecure. ")
                                issue.setFile(str(filename))
                                issue.setSeverity(Severity.VULNERABILITY)
                                results.append(issue)

                                issue = terminalPrint()
                                issue.setLevel(Severity.VULNERABILITY)
                                issue.setData(
                                    "getInstance should not be called without setting the cipher mode because the default mode on android is ECB, which is insecure. ")
                                results.append(issue)

    if type(t) is list:
        for l in t:
            recursive_ecb_check(l, filename, results)
    elif hasattr(t, '_fields'):
        for f in t._fields:
            recursive_ecb_check(getattr(t, f), filename, results)

    '''		GetInstance
	-----------
	Summary: Cipher.getInstance with ECB

	Priority: 9 / 10
	Severity: Warning
	Category: Security

	Cipher#getInstance should not be called with ECB as the cipher mode or without
	setting the cipher mode because the default mode on android is ECB, which is
	insecure.'''

    return


def find_key_files(results):
    '''	PackagedPrivateKey
	------------------
	Summary: Packaged private key

	Priority: 8 / 10
	Severity: Fatal
	Category: Security

	In general, you should not package private key files inside your app.
	'''
    if len(common.keyFiles) > 0:
        possibleKeyFiles = common.text_scan(common.keyFiles, r'PRIVATE\sKEY')
        if len(possibleKeyFiles) > 0:
            for f in possibleKeyFiles:
                common.logger.debug("It appears there is a private key embedded in your application: " + str(f))
                issue = ReportIssue()
                issue.setCategory(ExploitType.CRYPTO)
                issue.setDetails(
                    "It appears there is a private key embedded in your application in the following file:")
                issue.setFile(str(f))
                issue.setSeverity(Severity.VULNERABILITY)
                results.append(issue)

                issue = terminalPrint()
                issue.setLevel(Severity.VULNERABILITY)
                issue.setData("It appears there is a private key embedded in your application in the following file:")
                results.append(issue)
    return
