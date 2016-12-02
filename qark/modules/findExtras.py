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
import re
from xml.dom import minidom

from lib.plyj import parser as plyj
import lib.plyj.model as m
from modules import constantResolver
from modules import common

parser = plyj.Parser()
tree=''
extras=[]
extras.append([])

#find Intent Extras
#TODO - At some point we need to consolidate the finding of extras to one function
def find_extras(stub_file_name,entry):
	"""
	Find all extras given a filename
	"""
	global tree
	global extras

	extras=[]
	extras.append([])

	common.logger.info("Checking for extras in this file: " + str(stub_file_name) + " from this entry point: " + str(entry))
	unmatched=True

	#TODO add data types to the extras, so we can provide better suggestions
	for j in common.java_files:
		dots=stub_file_name.split('.')
		dot_length=dots.__len__()
		if dots[dot_length-1] !='java':
			stub_file_name+='.java'
		if re.search(r''+str(stub_file_name)+r'$',str(j)):
			unmatched=False
			try:
				tree = parser.parse_file(j)
			except Exception as e:
				common.logger.error("Tree exception: " + str(e))
			if tree is not None:
				for type_decl in tree.type_declarations:
					if type(type_decl) is m.ClassDeclaration:
						entries = []
						for t in type_decl.body:
							if type(t) is m.MethodDeclaration:
								#Checks whether the discovered MethodDeclaration is a component entry point (lifecycle method)
								if type(entry) is list:
									for n in entry:
										if hasattr(t, 'name'):
											if str(t.name) == str(n):
												#This branch never appears to get excercised
												#Now I need to recurse over this mdecl to find methods, then check if they match any of the extra strings above
												try:
													find_methods_for_extras(t,j,entry)
												except Exception as e:
													common.logger.error("Problem trying to find extras: " + str(e))

								else:
									if str(t.name) == str(entry):
										if hasattr(t, 'name'):
											if str(t.name) == str(entry):
												#Now I need to recurse over this mdecl to find methods, then check if they match any of the extra strings above
												try:
													find_methods_for_extras(t,j,entry)
												except Exception as e:
													common.logger.error("Problem trying to find extras: " + str(e))

			else:
				common.logger.error("Could not create a tree to find extras in : " + str(j))
				common.logger.info("Attempting fall-back method to determine extras")
				fallback_grep(j)

			if len(extras)<1:
				common.logger.debug("No extras found in " + str(j) + " to suggest.\n")
				common.parsingerrors.add(str(j))

	if unmatched:
		if str(j) not in common.file_not_found:
			common.file_not_found.append(str(j))
			#BUG - seems like a flow can come here without the fname; Ex: Flagship S - 4
			try:
				common.logger.error("Sorry, we could not find/parse a file named: " + str(j) + " while looking for extras\n")
			except Exception as e:
				common.logger.error("String printing issue in findExtras: " + str(e))
	#Trying to get rid of empty first element
	return extras

def find_methods_for_extras(t,file_name,entry):
	'''
	Looks for any method invocations which extract data from Intents or Bundles
	'''
	rextras=[]
	#These pull extras
	#TODO - Need to add extra types
	rextras.append('getExtras')
	rextras.append('getStringExtra')
	rextras.append('getIntExtra')
	rextras.append('getIntArrayExtra')
	rextras.append('getFloatExtra')
	rextras.append('getFloatArrayExtra')
	rextras.append('getDoubleExtra')
	rextras.append('getDoubleArrayExtra')
	rextras.append('getCharExtra')
	rextras.append('getCharArrayExtra')
	rextras.append('getByteExtra')
	rextras.append('getByteArrayExtra')
	rextras.append('getBundleExtra')
	rextras.append('getBooleanExtra')
	rextras.append('getBooleanArrayExtra')
	rextras.append('getCharSequenceArrayExtra')
	rextras.append('getCharSequenceArrayListExtra')
	rextras.append('getCharSequenceExtra')
	rextras.append('getIntegerArrayListExtra')
	rextras.append('getLongArrayExtra')
	rextras.append('getLongExtra')
	rextras.append('getParcelableArrayExtra')
	rextras.append('getParcelableArrayListExtra')
	rextras.append('getParcelableExtra')
	rextras.append('getSerializableExtra')
	rextras.append('getShortArrayExtra')
	rextras.append('getShortExtra')
	rextras.append('getStringArrayExtra')
	rextras.append('getStringArrayListExtra')
	#These pull data from extras
	rextras.append('getString')
	rextras.append('getInt')
	rextras.append('get')

	if type(t) is m.MethodInvocation:
		if str(t.name) in rextras:
			extras_from_vars(t,rextras,file_name)
		for a in t.arguments:
			find_methods_for_extras(a,file_name,entry)
		find_methods_for_extras(t.target,file_name,entry)
	elif type(t) is m.VariableDeclarator:
		extras_from_vars(t,rextras,file_name)

	elif type(t) is m.InstanceCreation:
		extras_from_instances(t,rextras,file_name)
	elif type(t) is list:
		for l in t:
			find_methods_for_extras(l,file_name,entry)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			find_methods_for_extras(getattr(t,f),file_name,entry)
	return

def extras_from_instances(t,methods,file_name):
	global tree

	if tree is not None:
		for type_decl in tree.type_declarations:
			if type(type_decl) is m.ClassDeclaration:
				for b in type_decl.body:
					if type(b) is m.ClassDeclaration:
						for c in b.body:
							extras_from_instance_methods(c,methods,file_name)

	return

def extras_from_instance_methods(c,methods,file_name):
	if type(c) is m.MethodInvocation:
		if str(c.name) in methods:
			extras_from_vars(c,methods,file_name)
		for a in c.arguments:
			extras_from_instance_methods(a,methods,file_name)
	elif type(c) is list:
		for l in c:
			extras_from_instance_methods(l,methods,file_name)
	elif hasattr(c,'_fields'):
		for f in c._fields:
			extras_from_instance_methods(getattr(c,f),methods,file_name)
	return

def extras_from_vars(token,methods,file_name):
	'''
	Looks for where data may be extracted from variables, which originated as extras, to derive key names
	'''
	global tree
	global extras

	single_extra=['getBooleanExtra']

	resolved_constant=''

	try:
		if hasattr(token,'initializer'):
			if type(token.initializer) is m.MethodInvocation:
				for n in methods:
					if str(token.initializer.name) == str(n):
						var=token.variable.name
						#This is for Intents
						var_type=re.sub(r'^get','',str(n))
						var_type=re.sub(r'Extra$','',str(var_type))
						#This is for Bundles
						var_type=re.sub(r'Extras$','',str(var_type))
						#TODO - still false positives from .get on strings which are not derived from extras
						if len(var_type)>0:
							common.logger.info("Possible Extra: " + str(var) + " of type: " + str(var_type))
							if var not in extras:
								extras.append(var)
								extras.append(var_type)
							if token.initializer.name in single_extra:
								break
						else:
							common.logger.info("Possible Extra: " + str(var) + " of unknown type")
							if var not in extras:
								extras.append(var)
								extras.append("unknownType")
							if token.initializer.name in single_extra:
								break

		elif type(token) is m.MethodInvocation:
			for n in methods:
				if str(token.name) == str(n):
					var=token.name
					#This is for Intents
					var_type=re.sub(r'^get','',str(n))
					var_type=re.sub(r'Extra$','',str(var_type))
					#This is for Bundles
					var_type=re.sub(r'Extras$','',str(var_type))
					#TODO - still false positives from .get on strings which are not derived from extras
					if len(var_type)>0:
						for a in token.arguments:
							if type(a) is m.Literal:
								if a.value not in extras:
									extras.append(a.value)
									extras.append(var_type)
									common.logger.info("Possible Extra: " + str(a.value) + " of type: " + str(var_type))
								if token.name in single_extra:
									break
							elif len(resolved_constant)==0:
								if type(a) is m.Name:
									try:
										resolved_constant=constantResolver.main(file_name,a.value)
									except Exception as e:
										common.logger.error("Problem trying to resolve constants: " + str(e))
								if resolved_constant is not None:
									if len(resolved_constant)>0:
										if resolved_constant not in extras:
											extras.append(resolved_constant)
											extras.append(var_type)
											common.logger.info("Possible Extra: " + str(resolved_constant) + " of type: " + str(var_type))
										if token.name in single_extra:
											break
									else:
										if re.match(r'R\.[A-Za-z0-9_\$\.]+',a.value):
											continue
										else:
											try:
												resolved_constant=constantResolver.string_finder(tree,a.value)
											except Exception as e:
												common.logger.error("Problem trying to resolve constants: " + str(e))
											if resolved_constant is not None:
												if len(resolved_constant)>0:
													if resolved_constant not in extras:
														extras.append(resolved_constant)
														extras.append(var_type)
														common.logger.info("Possible Extra: " + str(resolved_constant) + " of type: " + str(var_type))
													if token.name in single_extra:
														break
												else:
													common.logger.warning("Unable to resolve constant: " + str(a.value)+". You should review this manually.")
								if resolved_constant is not None:
									if len(resolved_constant)==0:
										common.logger.warning("Unable to resolve constant: " + str(a.value) + ". You should review this manually.")
	except Exception as e:
		common.logger.error("Problem trying to resolve constants or variables for extra keys: " + str(e))
	return

def extras_for_attack(token_type, method):
	'''
	Identifies any extras to be included in the exploit app
	'''

	bundle_extras = []
	bundle_extras.append("get")
	bundle_extras.append("getBoolean")
	bundle_extras.append("getBooleanArray")
	bundle_extras.append("getDouble")
	bundle_extras.append("getDoubleArray")
	#TODO - more than one
	bundle_extras.append("getInt")
	bundle_extras.append("getIntArray")
	bundle_extras.append("getLong")
	bundle_extras.append("getLongArray")
	#TODO - more than one
	bundle_extras.append("getString")
	bundle_extras.append("getStringArray")
	bundle_extras.append("getIntArray")

	intent_extras = []
	intent_extras.append("getBooleanArrayExtra")
	intent_extras.append("getBundleExtra")
	intent_extras.append("getByteArrayExtra")
	intent_extras.append("getByteExtra")
	intent_extras.append("getCharArrayExtra")
	intent_extras.append("getCharExtra")
	intent_extras.append("getCharSequenceArrayExtra")
	intent_extras.append("getCharSequenceArrayListExtra")
	intent_extras.append("getCharSequenceExtra")
	intent_extras.append("getDoubleArrayExtra")
	intent_extras.append("getDoubleExtra")
	intent_extras.append("getExtras")
	intent_extras.append("getFloatArrayExtra")
	intent_extras.append("getFloatExtra")
	intent_extras.append("getIntArrayExtra")
	intent_extras.append("getIntExtra")
	intent_extras.append("getIntegerArrayListExtra")
	intent_extras.append("getLongArrayExtra")
	intent_extras.append("getLongExtra")
	intent_extras.append("getParcelableArrayExtra")
	intent_extras.append("getParcelableArrayListExtra")
	intent_extras.append("getParcelableExtra")
	intent_extras.append("getSerializableExtra")
	intent_extras.append("getShortArrayExtra")
	intent_extras.append("getShortExtra")
	intent_extras.append("getStringArrayExtra")
	intent_extras.append("getStringArrayListExtra")
	intent_extras.append("getStringExtra")

	#TODO - Need to deal with non-Extra data pulled from intents

	extra = []

	if str(token_type) == "Bundle":
		for b in bundle_extras:
			if str(b) == str(method.name):
				if str(b) not in extra:
					extra.append(str(b))
				for a in method.arguments:
					if type(a) is m.Literal:
						if str(a.value) not in extra:
							extra.append(a.value)
	elif str(token_type) == "Intent":
		for i in intent_extras:
			if str(i) == str(method.name):
				if str(i) not in extra:
					extra.append(str(i))
				for a in method.arguments:
					if type(a) is m.Literal:
						if str(a.value) not in extra:
							extra.append(a.value)
	else:
		pass
	return extra

def fallback_grep(file_name):

	"""
	Used for finding extras when parser fails to create tree
	"""
	global extras

	rextras=[]
	rextras.append(r'getExtras\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getStringExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getIntExtra\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getIntArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getFloatExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getFloatArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getDoubleExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getDoubleArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getCharExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getCharArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getByteExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getByteArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getBundleExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getBooleanExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getBooleanArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getCharSequenceArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getCharSequenceArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getCharSequenceExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getInterArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getLongArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getLongExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getParcelableArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getParcelableArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getParcelableExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getSeriablizableExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getShortArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getShortExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getStringArrayExtra\(\s*[0-9A-Za-z_\"\'.]+')
	rextras.append(r'getStringArrayListExtra\(\s*[0-9A-Za-z_\"\'.]+')
	#These are not necessarily Intent extras, but may contain them
	rextras.append(r'getString\(\s*[0-9A-Za-z_\"\'.]+')

	#TODO add data types to the extras, so we can provide better suggestions
	for r in rextras:
		x_tmp=common.text_scan_single(file_name,r)
		for x in x_tmp:
			for r in rextras:
				match=re.search(r,str(x))
				if match is not None:
					match=re.sub(r'get.*\(','',str(match.group(0)))
					if match not in extras:
						extras.append(match)
						var_type=str(r)
						var_type=re.sub(r'^get','',var_type)
						var_type=re.sub(r'\\.*','',var_type)
						var_type=re.sub(r'Extra.*','',var_type)
						extras.append(var_type)
	if len(extras)<1:
		common.logger.debug("No extras found in " + str(file_name) + " to suggest.\n")
	return extras
