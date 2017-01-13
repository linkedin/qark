from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import os
import re
from xml.dom import minidom

import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules import common

tree=''
currentFile=''

def start(path):
	common.logger.warning("Please use the exploit APK to manually test for TapJacking until we have a chance to complete this module. The impact should be verified manually anyway, so have fun...")
	return


def find_layout(path):
	foundButtons=[]
	foundButtons.append([])
	for (dirpath, dirnames, filenames) in os.walk(path):
		for dirname in dirnames:
			if dirname == 'layout':
				xml_files=common.find_xml(path+"/"+dirname)
	if common.source_or_apk==1:
		for x in xml_files:
			try:
				common.readLayoutFiles(x)
			except Exception as e:
				common.logger.warning("There was a problem trying to read the xml resource files, during the TapJacking checking. If you're using a decompiled APK, we're still working on this feature. You can still check manually by building our exploit APK.")
	else:
		for x in xml_files:
			button=minidom.parse(x)
			for node in button.getElementsByTagName('Button'):
				if 'android:FilterTouchesWhenObscured' in node.attributes.keys():
					if node.attributes['android:FilterTouchesWhenObscured'].value == 'true':
						continue
					else:
						foundButtons.append([str(x),node.toxml()])
				else:
					foundButtons.append([str(x),node.toxml()])
			imageButton=minidom.parse(x)
			for node in button.getElementsByTagName('ImageButton'):
				if 'android:FilterTouchesWhenObscured' in node.attributes.keys():
					if node.attributes['android:FilterTouchesWhenObscured'].value == 'true':
						continue
					else:
						try:
							if 'android:id' in node.attributes.keys():
								buttonId=node.attributes['android:id'].value
								buttonId=re.sub(r'.*id\/','',buttonId)
								foundButtons.append([str(x),buttonId])
						except Exception as e:
							common.logger.error("Unable to extract id for Button from layout's xml: " + str(e))
				else:
					try:
						if 'android:id' in node.attributes.keys():
							buttonId=node.attributes['android:id'].value
							buttonId=re.sub(r'.*id\/','',buttonId)
							foundButtons.append([str(x),buttonId])
					except Exception as e:
						common.logger.error("Unable to extract id for Button from layout's xml: " + str(e))
	if len(foundButtons) > 0:
		print "Hey, I found these buttons in xml layouts:"
		#BUG - This is an ugly hack basically "if fail - assume string"
		print "LENGTH: " + str(len(foundButtons))
		for b in foundButtons:
			try:
				print b.encode('utf-8')
			except Exception as e:
				print str(b)
	else:
		print "No buttons found in xml layouts"
	return

def find_java_buttons(xmlFile,buttonId):
	# Need find all the Buttons declared in the Java classes
	global tree
	global currentFile

	for j in common.java_files:
		currentFile=j
		common.logger.debug("FILE: " + str(j))
		tree=parser.parse_file(j)
	return
