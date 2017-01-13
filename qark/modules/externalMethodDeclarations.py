from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re,os

import lib.plyj.model as m
import lib.plyj.parser as plyj
from modules import common
from modules import report

parser = plyj.Parser()

localMethodDecls=[]
matchFound=False
numMatches=0
thorough=False

def main(token,tree,current_file):
	global matchFound
	global thorough
	android_classes=[]
	java_classes=[]

	#Check to ensure something other than standard libraries are included,which we won't traverse
	customImportCount=0
	for imp_decl in tree.import_declarations:
		if not re.match(r'android\..*',imp_decl.name.value):
				if not re.match(r'com.android\..*',imp_decl.name.value):
					if not re.match(r'java\..*',imp_decl.name.value):
						if not re.match(r'org\.apache\..*',imp_decl.name.value):
							customImportCount+=1
	#No need to process if there are no custom imports
	if customImportCount==0:
		common.logger.info("No custom imports to investigate. The method is assumed to be in the standard libraries")
		return

	for imp_decl in tree.import_declarations:
		if not thorough:
			if re.match(r'android\..*',imp_decl.name.value):
				android_classes.append(imp_decl.name.value)
			elif re.match(r'com.android\..*',imp_decl.name.value):
				android_classes.append(imp_decl.name.value)
			elif re.match(r'java\..*',imp_decl.name.value):
				java_classes.append(imp_decl.name.value)
			else:
				if not re.search(r'\*',imp_decl.name.value):
					packagePath=common.sourceDirectory
					subPath=re.sub(r'\.','/',str(imp_decl.name.value))
					subPath=str(packagePath)+"/"+str(subPath)
					classFile=subPath+".java"
					if os.path.isfile(classFile):
						try:
							importTree=parser.parse_file(classFile)
						except Exception as e:
							common.logger.error("Could not create tree for "+str(classFile) +" in externalMethodDeclarations.py" )
							continue
						if hasattr(importTree,'type_declarations'):
							for type_decl in importTree.type_declarations:
								if type(type_decl) is m.ClassDeclaration:
									for t in type_decl.body:
										try:
											recursive_method_finder(t,token)
										except Exception as e:
											common.logger.error("Problem running recursive_method_finder for m.ClassDeclaration in externalMethodDeclarations.py: " + str(e))
								elif type(type_decl) is list:
									for y in t:
										try:
											recursive_method_finder(y,token)
										except Exception as e:
											common.logger.error("Problem running recursive_method_finder for lists in externalMethodDeclarations.py: " + str(e))
								elif hasattr(t,'_fields'):
									for f in t._fields:
										try:
											recursive_method_finder(getattr(t,f),token)
										except Exception as e:
											common.logger.error("Problem running recursive_method_finder for _fields in externalMethodDeclarations.py: " + str(e))
						else:
							common.logger.error("There was a problem reading the imported class: " + str(classFile) + ". Results may be negatively impacted if the class contains security relevant methods. This may be due to a de-compilation error.")
							continue
					else:
						if common.source_or_apk==1:
							#TODO check against *every* standard class to see if it's likely from a standard library?
							common.logger.debug("Imported class file not found: " + str(imp_decl.name.value)+". This may be due to a de-compilation error. The results may be degraded if a significant method declaration cannot be resolved.")
							common.parsingerrors.add(str(current_file))
						else:
							#TODO - allow for including source from multiple directories
							common.parsingerrors.add(str(current_file))
							common.logger.debug("The imported class: "+str(imp_decl.name.value)+", was not found. We are still working on integrating imports from different directories. Please either try scanning the built APK, check for updates or contribute your own code. This can be safely ignored if this class is defined in standard Java or Android libraries.")
				else:
					common.parsingerrors.add(str(current_file))
					common.logger.info("Your developer used a lazy import (*). So for now we'll be lazy developers and refuse to chase it down. Check for updates soon. Sorry, but they started it...")
					common.logger.debug("WILDCARD Import Path - We have not yet implemented the code for hunting these down, sorry!")
		else:
			break
	if numMatches>0:
		process_matches(token,tree)
	else:
		if common.source_or_apk==1:
			common.parsingerrors.add(str(current_file))
			common.logger.debug("Unable to locate the definition of the " + str(token.name)+" method from the imports in "+str(current_file)+". This will negatively impact results if this is not part of the standard Java/Android libraries and is a security relevant method.")
		else:
			common.parsingerrors.add(str(current_file))
			common.logger.debug("Unable to locate the definition of the " + str(token.name)+" method from the imports in "+str(current_file)+". This will negatively impact results if this is not part of the standard Java/Android libraries and is a security relevant method. We are still working on ignoring safe standard methods. Please check back for updates or contribute your own code.")
	return

def recursive_method_finder(t,token):
	'''
	Looks for any locally declared methods. All entry points should be captured in this list
	'''
	global matchFound
	global numMatches
	global thorough

	if type(t) is m.MethodDeclaration:
		try:
			if hasattr(t,'name'):
				if str(token.name)==str(t.name):
					if len(t.parameters)==len(token.arguments):
						try:
							thorough=True
							for p in range(0,len(t.parameters)):
								#TODO - from here, we need to go resolve each argument to ensure type matching
								#TODO - It'll have to wait for now as we'll likely have problems with Android specific types
								#TODO - Due to plyj limitations
								#TODO - Another option would be to see if there are any other matches
								#TODO - If it's unique, we'll assume it's a match until we can devise a better solution
								if not type(t.parameters[p])==type(token.arguments[p]):
									thorough=False
							numMatches+=1
						except Exception as e:
							common.logger.error("Problem during parameter type matching in externalMethodDeclaration.py's recursive_method_finder method: " + str(e))

		except Exception as e:
			common.logger.error("Problem in recursive_method_finder, trying to traverse m.MethodDeclaration: " + str(e))
	elif type(t) is list:
		try:
			for i in t:
				if type(i) is m.MethodDeclaration:
					recursive_method_finder(i,token)
				elif type(i) is list:
					for y in i:
						recursive_method_finder(i,token)
				elif hasattr(i,'_fields'):
					try:
						for z in i._fields:
							recursive_method_finder(getattr(i,z),token)
					except Exception as e:
						common.logger.error("Problem in recursive_method_finder, trying to iterate fields on list branch: " + str(e))
		except Exception as e:
			common.logger.error("Problem in recursive_method_finder, trying to traverse list: " + str(e))
	elif hasattr(t,'_fields'):
		try:
			for f in t._fields:
				recursive_method_finder(getattr(t,f),token)
		except Exception as e:
			common.logger.error("Problem in recursive_method_finder, trying to iterate over fields: " + str(e))
	return

def process_matches(token,tree):
	global numMatches
	global thorough
	try:
		if thorough:
			common.logger.debug("Located method declaration for: " + str(token.name))
			sinks_encountered(token,tree)
		elif numMatches==1:
			common.logger.info("Only one match was found for this method: " + str(token.name)+",but cannot be confirmed 100% accurate.")
			sinks_encountered(token,tree)
		else:
			common.logger.warning("A number of potentially matching method declarations were found for : " + str(token.name)+". QARK cannot currently provide a 100% positive match, so false positives could arise from this.")
			sinks_encountered(token,tree)
	except Exception as e:
		common.logger.error("Problem running sinks_encountered in externalMethodDeclarations.py: " + str(e))
	numMatches=0
	thorough=False
	return

def sinks_encountered(token,tree):
	found=False
	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			for t in type_decl.body:
				if type(t) is m.MethodInvocation:
					if str(t.name)==str(token.name):
						if len(t.arguments)==len(token.arguments):
							found=common.sink_list_check(token,tree)
		elif type(type_decl) is list:
			for l in type_decl:
				sinks_encountered(type_decl,tree)
		elif hasattr(type_decl,'_fields'):
			for f in type_decl._fields:
				sinks_encountered(getattr(type_decl,f),tree)
	if found:
		common.logger.log(common.VULNERABILITY_LEVEL,"It appears a vulnerablity was found here, but unfortunately we haven't completed this branch yet.")
		# raw_input()
	return found
