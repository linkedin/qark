from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import zipfile
import os
from genericpath import isdir
import subprocess
import logging
import shlex
import threading
import re
import shutil
import time
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict
from multiprocessing import Process
from threading import Thread, Lock

from lib.progressbar import *
from lib import blessings
from modules.common import logger
from modules import report
from modules import common
from lib.pubsub import pub


lock = Lock()
progresswriter1 = common.Writer((0, common.term.height-10))
progressbar1 = ProgressBar(widgets=['JD CORE ', Percentage(), Bar()], maxval=100, fd=progresswriter1)
progresswriter2 = common.Writer((0, common.term.height-8))
progressbar2 = ProgressBar(widgets=['Procyon ', Percentage(), Bar()], maxval=100, fd=progresswriter2)
progresswriter3 = common.Writer((0, common.term.height-6))
progressbar3 = ProgressBar(widgets=['CFR ', Percentage(), Bar()], maxval=100, fd=progresswriter3)

def unpack():
	"""
	APK to DEX
	"""
	logger.info('Unpacking %s', common.apkPath)
	#Get the directory to unpack to
	try:
		dirname, extension = common.apkPath.rsplit(".",1)
		#workaround for cases where path may include whitespace
		file_temp = open(common.apkPath,'r')
		zf = zipfile.ZipFile(file_temp)
		logger.info('Zipfile: %s', zf)
		for filename in [ zf.namelist()]:
			logger.info('UnpackAPK: in for loop file: %s', filename)
			if not os.path.exists(dirname + "/"):
				os.makedirs(dirname + "/")
			zf.extractall(dirname + "/", zf.namelist(), )
			logger.info('Extracted APK to %s', dirname + '/')
			common.pathToDEX = dirname + "/classes.dex"
			common.pathToUnpackedAPK = dirname + '/'
			return True
	except Exception as e:
		print(e)
		if not common.interactive_mode:
				logger.error(common.args.pathtoapk + common.config.get('qarkhelper', 'NOT_A_VALID_APK'))
				exit()
		logger.error(common.config.get('qarkhelper', 'NOT_A_VALID_APK_INTERACTIVE'))
		raise

def get_apk_info(pathToAPK):
	package = defaultdict(list)
	print "starting"
	aapt = Popen(['aapt', 'dump', 'badging', pathToAPK], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1)
	for line in aapt.stdout:
		print line,
		if line.startswith("package"):
			package['application-name'] = line.split(" ")[1].split("'")[1]
			package['application-version'] = line.split(" ")[3].split("'")[1]
		if line.startswith("sdkVersion"):
			package['application-sdkversion'] = line.split("'")[1]
		if line.startswith("targetSdkVersion"):
			package['application-targetSdkVersion'] = line.split("'")[1]
		if line.startswith("application-label"):
			package['application-label'] = line.split("'")[1]
		if "application-debuggable" in line:
			package['application-debuggable'] = True
		if line.startswith("uses-permission"):
			package['application-permissions'].append(line.split("'")[1])
	return package

def find_manifest_in_unpacked_apk(path, name):
	"""
	Finds manifest.xml from the unpacked APK
	"""
	pathFromAPK = path.rsplit(".",1)[0]
	common.sourceDirectory=pathFromAPK
	logger.info('Finding %s in %s', name,pathFromAPK)
	common.logger.debug(pathFromAPK, name)
	for root, dirs, files in os.walk(pathFromAPK):
		for file in files:
			if name in file:
				logger.info('%s found', name)
				return os.path.join(root, name)

def grep_1(path, regex):
	"""
	wrapper around grep functionality
	"""
	regObj = re.compile(regex)
	res = []
	for root, dirs, fnames in os.walk(path):
		for fname in fnames:
			if not fname.startswith("."):
				with open (root+"/"+fname, "r") as f:
					data=f.read()
					if re.search(regObj, data,):
						res.append(os.path.join(root, fname))
					f.close()
	return res

def decompile(path):
	"""
	Converts DEX to JAR(containing class files) and then class files to near original java code using 3 different decompilers and selecting the best available decompiled code
	"""
	common.pathToDEX = path
	pathToDex2jar = common.rootDir + "/lib/dex2jar/dex2jar.sh"
	sp = subprocess.Popen([pathToDex2jar, common.pathToDEX], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output, error = sp.communicate()
	common.pathToJar = common.pathToDEX.rsplit(".",1)[0] + "_dex2jar.jar"
	dirname, extension = common.pathToJar.rsplit(".",1)
	zf = zipfile.ZipFile(common.pathToJar)

	#Total number of class files that need to be decompiled
	total_files = len(zf.namelist())
	report.write("totalfiles", total_files)
	common.count = len([s for s in zf.namelist() if ((".class" in s) and ("$" not in s))])

	pub.subscribe(decompiler_update, 'decompile')

	thread0 = Process(name='clear', target=clear, args = ())
	thread1 = Process(name='jdcore', target=jdcore, args = (zf.filename,dirname))
	thread2 = Process(name='procyon', target=cfr, args = (zf.filename,dirname))
	thread3 = Process(name='cfr', target=procyon, args = (zf.filename,dirname))

	thread0.start()
	thread0.join()

	progressbar1.start()
	progressbar2.start()
	progressbar3.start()


	thread1.start()
	thread2.start()
	thread3.start()
	thread1.join(0)
	thread2.join(0)
	thread3.join(0)

	if not common.runningAutomated:
		with common.term.cbreak():
			val = None
			while val not in (u'c', u'C'):
				with common.term.location(0,common.term.height-3):
					print "Decompilation may hang/take too long (usually happens when the source is obfuscated)."
					print "At any time," + common.term.bold_underline_red_on_white('Press C to continue') + " and QARK will attempt to run SCA on whatever was decompiled."
					val = common.term.inkey(timeout=1)
	while True:
		if not (thread1.is_alive() or thread2.is_alive() or thread3.is_alive()):
			break

	if thread1.is_alive():
		thread1.terminate()
	if thread2.is_alive():
		thread2.terminate()
	if thread3.is_alive():
		thread3.terminate()

	#Go back to the bottom of the screen
	with common.term.location(0,common.term.height):
		print ""

	g1 = grep_1(dirname, "// Byte code:")
	g2 = grep_1(dirname+"1", "// This method has failed to decompile.")
	g3 = grep_1(dirname+"2", "// This method could not be decompiled.")

	#print list(set(g1) - set(g2))
	logger.info("Trying to improve accuracy of the decompiled files")
	restored = 0
	try:
		for filename in g1:
			relative_filename = str(filename).split(dirname)[1]
			if any(relative_filename in s for s in g2):
				if any(relative_filename in s for s in g3):
					logger.debug("Failed to reconstruct: " + relative_filename)
				else:
					shutil.copy(dirname+"2"+relative_filename, filename)
					restored = restored +1
			else:
				shutil.copy(dirname+"1"+relative_filename, filename)
				restored = restored +1
	except Exception as e:
		print e.message
	report.write("restorestats","Restored " + str(restored) + " file(s) out of " + str(len(g1)) + " corrupt file(s)")
	logger.info("Restored " + str(restored) + " file(s) out of " + str(len(g1)) + " corrupt file(s)")
	logger.debug("Deleting redundant decompiled files")
	try:
		shutil.rmtree(dirname+"1")
		logger.debug("Deleted " + dirname+"1")
		shutil.rmtree(dirname+"2")
		logger.debug("Deleted " + dirname+"2")
	except Exception as e:
		logger.debug("Unable to delete redundant decompiled files (no impact on scan results): " + str(e))


def decompiler_update(cfr=None,jdcore=None,procyon=None):
	lock.acquire()
	if cfr is not None:
		if cfr<=100:
			progressbar3.update(cfr)
	if jdcore is not None:
		if jdcore<=100:
			progressbar1.update(jdcore)
	if procyon is not None:
		if procyon<=100:
			progressbar2.update(procyon)
	lock.release()

def jdcore(path,dirname):
	"""
	calls the jdcore decompiler from command line
	"""
	process = subprocess.Popen(["java","-jar", common.rootDir + "/lib/jd-core-java-1.2.jar", path, dirname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def cfr(path,dirname):
	"""
	calls the cfr decompiler from command line
	"""
	process = subprocess.Popen(["java","-jar", common.rootDir + "/lib/cfr_0_115.jar", path, "--outputdir", dirname+"1"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	try:
		while True:
			line = process.stdout.readline()
			if not line:
				break
			if "Processing" in line:
				common.counter1 = common.counter1 + 1
				pub.sendMessage('decompile', cfr=round(common.counter1*100/common.count))
				pub.sendMessage('decompile', jdcore=round(common.counter1*100/common.count))
	except Exception as e:
		logger.debug(e.message)

def procyon(path,dirname):
	"""
	calls the procyon decompiler from command line
	"""
	process = subprocess.Popen(["java","-jar", common.rootDir + "/lib/procyon/procyon-decompiler-0.5.30.jar", path, "-o ", dirname+"2"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	try:
		while True:
			line = process.stdout.readline()
			if not line:
				break
			if "Decompiling" in line:
				common.counter2 = common.counter2 + 1
				pub.sendMessage('decompile', procyon=round(common.counter2*100/common.count))
	except Exception as e:
		logger.debug(e.message)

def clear():
	"""
	Making space for progressbars
	"""
	with common.term.location():
		logger.info('Please wait while QARK tries to decompile the code back to source using multiple decompilers. This may take a while.')
		print("\n"*11)
