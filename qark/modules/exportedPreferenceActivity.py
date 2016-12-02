from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

from xml.dom import minidom
import re

import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules import common

parser = plyj.Parser()
preferenceClasses=['PreferenceActivity']

#TODO - Yes this is duplicate code, but we can come back later and clean it up
def main():
	#TODO - I need to figure out a way to silence this. It is outputting where I don't want it too
	common.logger.info("Checking for exported PreferenceActivity classes")
	act_priv_list, act_exp_list, act_exp_perm_list, act_prot_broad_list, report_data=common.check_export('activity',False)
	#Do I need to add a minSdkVersion check here?

	if ((len(act_exp_list)>0) or (len(act_exp_perm_list>1)) or (len(act_prot_broad_list>0))):
		find_preference_activity()
		if len(act_exp_list)>0:
			if look_for_file(act_exp_list):
				common.logger.error("This application is vulnerable to a potentially serious type of reflection issue, detailed here: http://securityintelligence.com/new-vulnerability-android-framework-fragment-injection. Unfortunately, we are still working on an automated exploit for this.")
		if len(act_exp_perm_list)>1:
			if look_for_file(act_exp_perm_list):
				common.logger.error("This application is vulnerable to a potentially serious type of reflection issue, detailed here: http://securityintelligence.com/new-vulnerability-android-framework-fragment-injection. Unfortunately, we are still working on an automated exploit for this.")
		if len(act_prot_broad_list)>0:
			if look_for_file(act_prot_broad_list):
				common.logger.error("This application is vulnerable to a potentially serious type of reflection issue, detailed here: http://securityintelligence.com/new-vulnerability-android-framework-fragment-injection. Unfortunately, we are still working on an automated exploit for this.")
	return

def look_for_file(act_list):
	global preferenceClasses
	vuln=False

	for a in act_list:
		for p in preferenceClasses:
			if str(a)==str(p):
				vuln=True
	return vuln

def find_preference_activity():
	global parser
	global preferenceClasses

	activityFiles=[]

	for j in common.java_files:
		init_len_pc=len(preferenceClasses)
		try:
			tree=parser.parse_file(j)
		except Exception as e:
			common.logger.error("Unable to create a parsing tree in exportedPreferenceActivity. ERROR: " + str(e))
			continue
		if hasattr(tree,'type_declarations'):
			for type_decl in tree.type_declarations:
				if hasattr(type_decl,'extends'):
					if hasattr(type_decl.extends,'name'):
						for p in preferenceClasses:
							if str(type_decl.extends.name.value)==str(p):
								if (str(type_decl.name) not in preferenceClasses):
									preferenceClasses.append(str(type_decl.name))
	#Trying to be recursive here, so extensions of extensions, etc are found, might require more refinement
	if len(preferenceClasses)>init_len_pc:
		find_preference_activity()

	return
