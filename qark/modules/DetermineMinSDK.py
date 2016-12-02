from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import os
import re
import sys
import urllib2
import ast
import string
import ConfigParser
import logging
import plistlib

from xml.dom import minidom
from bs4 import BeautifulSoup
from distutils.version import StrictVersion
from modules.unpackAPK import unpack
from modules.unpackAPK import find_manifest_in_unpacked_apk
from modules import common
from urllib2 import HTTPError
from httplib import HTTPException

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

def find_gradle():
	version=0
	files=[]
	for (dirpath,dirname, filenames) in os.walk(common.sourceDirectory):
		for filename in filenames:
			if filename=='build.gradle':
				files.append(os.path.join(dirpath,filename))
	if len(files)>0:
		matches=common.text_scan(files,r'def\s_compileSdkVersion\s*=\s*[0-9]+')
		#TODO - fix this so we don't have to account for the empty first element
		#We skip it if there are multiple build.gradle files, since manual input is unavoidable at that point
		if len(matches)==2:
			for m in matches:
				if len(m)>0:
					version=re.compile('\d+')
					version=version.findall(str(m[0]))[0]
	return version

def determine_min_sdk():
	"""
	Determines the minimum SDK version supported by the vulnerable application\n
	As a fallback, it allows the user to search Google PlayStore to identify the minimum SDK version if the data is unavailable in manifest.xml
	"""
	#determine minimum supported versions
	common.minSdkVersion=0
	common.sdk = common.xmldoc.getElementsByTagName("uses-sdk")
	determineSdk=''

	if len(common.sdk)>0:
		if 'android:minSdkVersion' in common.sdk[0].attributes.keys():
			try:
				common.minSdkVersion = common.sdk[0].attributes['android:minSdkVersion'].value
				logger.info(common.config.get('qarkhelper', 'MIN_SDK_VERSION') + str(common.minSdkVersion))
			except Exception as e:
				common.logger.error("Something went wrong trying to determine the version from the manifest: " + str(e))



	if common.minSdkVersion==0:
		if common.source_or_apk==2:
			common.minSdkVersion=find_gradle()
			if common.minSdkVersion==0:
				common.logger.info("We were unable to find the minimum SDK version in your source.")
				determineSdk='m'
			else:
				logger.info(common.config.get('qarkhelper', 'MIN_SDK_VERSION') + str(common.minSdkVersion))
		else:
			common.compare(common.sdk.length,1,common.config.get('qarkhelper', 'USESDK_MISS'), 'false')
			print common.config.get('qarkhelper', 'GEN_OUTPUT_WARN')
			while True:
				determineSdk=raw_input("Which option would you prefer? (P)lay, (M)anual")
				if determineSdk.lower() in ('p','m'):
					break;
				else:
					determineSdk=raw_input("Please enter either (p) or (m):")

		if determineSdk.lower() == 'p':
			#get package name from manifest if possible
			#make call to Play store
			#determine API version from https://play.google.com/store/apps/details?id=<package name>
			# will need to adjust the sdk[0] value for the checks below
			for a in common.xmldoc.getElementsByTagName('manifest'):
				if 'package' in a.attributes.keys():
					print common.config.get('qarkhelper', 'PACK_FOUND')
					package_name=a.attributes['package'].value
					print package_name
				else:
					package_name=raw_input(common.config.get('qarkhelper', 'NO_PACK_NAME'))

			try:
				logger.info(common.config.get('qarkhelper', 'DETERMINING_SDK_VERSION'))
				play_url="https://play.google.com/store/apps/details?id="
				play_url+=package_name
				print play_url
				page=urllib2.urlopen(play_url)
				html=BeautifulSoup(page.read())
				play_version=html.find(itemprop="operatingSystems")
				plat_version=re.findall('\d+.\d+', play_version.contents[0])
				if plat_version:
					plat_version=[str(item) for item in plat_version]
					api_plat_map=[]
					api_plat_map.append(['1','1.0'])
					api_plat_map.append(['2','1.1'])
					api_plat_map.append(['3','1.5'])
					api_plat_map.append(['4','1.6'])
					api_plat_map.append(['5','2.0'])
					api_plat_map.append(['6','2.0.1'])
					api_plat_map.append(['7','2.1'])
					api_plat_map.append(['8','2.2'])
					api_plat_map.append(['9','2.3'])
					api_plat_map.append(['10','2.3.3'])
					api_plat_map.append(['11','3.0'])
					api_plat_map.append(['12','3.1'])
					api_plat_map.append(['13','3.2'])
					api_plat_map.append(['14','4.0'])
					api_plat_map.append(['15','4.0.3'])
					api_plat_map.append(['16','4.1'])
					api_plat_map.append(['17','4.2'])
					api_plat_map.append(['18','4.3']) #Webviews have critical vuln, no more patches from Google
					api_plat_map.append(['19','4.4'])
					api_plat_map.append(['20','4.4']) # This is actually 4.4W, a wearable only build, I'm assuming it is the same as 4.4 for our purposes
					api_plat_map.append(['21','5.0'])
					api_plat_map.append(['22','5.1']) # This is latest version, we'll assume this for newer, until update
					#TODO - double check this, adding 5.1 may have broken it
					for a in api_plat_map:
						if StrictVersion(str(plat_version[0]))>=StrictVersion(str(a[1])):
							common.minSdkVersion=a[0]
					logger.info(common.config.get('qarkhelper', 'MIN_SDK_VERSION') + str(common.minSdkVersion))
					manual=raw_input(common.config.get('qarkhelper', 'SDK_VALUE_MANUAL'))
				else:
					print common.config.get('qarkhelper', 'CANT_DET_PLAY')
					#BUG - not processing the cases of wanting to enter if manually, if the retrieval of the play version is broken
			except HTTPError, e:
				print str(e);
				logger.error(common.config.get('qarkhelper', 'MIN_SDK_PLAY_STORE_FAILED'))
		elif (determineSdk.lower()=='m' or common.minSdkVersion==0):
			#does not actually become 1, just needs a value, since it wasn't found, so we assume worst case
			print common.term.cyan + common.term.bold + str(common.config.get('qarkhelper','NO_MIN_SDK')).decode('string-escape').format(t=common.term)
			enterSdk = raw_input(common.config.get('qarkhelper','PROMPT_MIN_SDK'))
			if enterSdk.lower() == 'y':
				sdkinput=0
				while True:
					sdkinput = int(raw_input(common.config.get('qarkhelper', 'PROMPT_VER')+common.config.get('qarkhelper','MAX_API_VERSION')+common.config.get('qarkhelper','PROMPT_VER2')))
					if 0 < int(sdkinput) <= int(common.config.get('qarkhelper','MAX_API_VERSION')):
						common.minSdkVersion = int(sdkinput)
						break
			else:
				common.minSdkVersion = 7
	else:
		# there are some notes about if this is not defined http://developer.android.com/guide/topics/manifest/uses-sdk-element.html
		if len(common.sdk)>0:
			if 'android:minSdkVersion' in common.sdk[0].attributes.keys():
				common.minSdkVersion = common.sdk[0].attributes['android:minSdkVersion'].value
			else:
				common.minSdkVersion = 1
		else:
			common.minSdkVersion = 1
			logger.info(common.config.get('qarkhelper', 'DEF_SDK'))

		if int(common.minSdkVersion) < 16:
			logger.warning(common.config.get('qarkhelper', 'LOGS_WR'))
			logWR = "true"

		if len(common.sdk)>0:
			if 'android:common.targetSdkVersion' in common.sdk[0].attributes.keys():
				common.targetSdkVersion = common.sdk[0].attributes['android:common.targetSdkVersion'].value
			else:
				common.targetSdkVersion = common.minSdkVersion
		else:
			common.targetSdkVersion = common.minSdkVersion

		if len(common.sdk)>0:
			if 'android:maxSdkVersion' in common.sdk[0].attributes.keys():
				logger.info(common.config.get('qarkhelper', 'MAX_VER_INFO'))
				maxSdkVersion = common.sdk[0].attributes['android:maxSdkVersion'].value
	return

