from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

from modules import common

import re

def find_intent_filters(name,type):
	result=''
	for node in common.xmldoc.getElementsByTagName(str(type)):
		if re.search(str(name),str(node.attributes['android:name'].value)):
			for x in node.getElementsByTagName('intent-filter'):
				for a in node.getElementsByTagName('action'):
					result=str(a.attributes['android:name'].value)
	return result

def find_package():
	result=''
	for node in common.xmldoc.getElementsByTagName("manifest"):
		return str(node.attributes['package'].value)

def find_comp_type(file_name):
	#Find the current component name
	class_name=re.sub(r'\.java','',str(file_name))
	class_name=re.sub(r'^.*\/','',str(class_name))
	type_array=['service','receiver','activity', 'provider','activity-alias']
	print str(class_name)
	for t in type_array:
		result=find_intent_filters(class_name,t)
		if result:
			return result
	return
