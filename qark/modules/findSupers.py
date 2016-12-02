from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''
import re

import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules import common
from modules import findExtras

parser = plyj.Parser()
name=''
list_of_supers=[]
checked_for_extras=''
vuln_found=False

def find_extensions(tree,token):
	'''
	Locates classes this class extends, to track down super calls
	'''
	global name
	global vuln_found

	name = token.name

	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			common.logger.info("This class extends and calls a method in : " + str(type_decl.extends.name.value))
			for j in common.java_files:
				if re.search(r'/'+str(type_decl.extends.name.value)+'.java',str(j)):
					common.logger.info("Checking this file for issues: " + str(j))
					create_tree(j)
	return vuln_found

def create_tree(filename):

	global parser

	local_tree=parser.parse_file(filename)
	if local_tree is not None:	
		for type_decl in local_tree.type_declarations:
			if type(type_decl) is m.ClassDeclaration:
				for t in type_decl.body:
					try:
						search_mdecl(t,local_tree,filename)
					except Exception as e:
						common.logger.error("Problem calling search_mdecl from create_tree in findSupers.py: " + str(e))
	else:
		common.logger.error("Unable to create tree for parsing: " + str(filename))

	return

def search_mdecl(t,local_tree,filename):
	
	global name
	global checked_for_extras

	try:
		if type(t) is m.MethodDeclaration:
			if t.name==name:
				#TODO - Do you call locally defined methods?
				#TODO - Do you call methods I need to track down from other places?
				process_mdecl(t,local_tree,filename)
				#TODO - This might spew out extras when not needed
				if checked_for_extras!=str(filename):
					checked_for_extras=str(filename)
					findExtras.find_extras(filename,t.name)
		elif type(t) is list:
			for l in t:
				search_mdecl(l,local_tree,filename)
		elif hasattr(t,'_fields'):
			for f in t._fields:
				search_mdecl(getattr(t,f),local_tree,filename)
	except Exception as e:
		common.logger.error("Problem in search_mdecl function in findSupers.py: " +str(e))
	return

def process_mdecl(t,local_tree,filename):
	
	global vuln_found

	try:
		for b in t.body:
			if type(b) is m.MethodInvocation:
				if common.sink_list_check(b,local_tree):
					common.logger.warning("This subclass extends a superclass, potentially via another superclass, which contains a sensitive method invocation: " + str(b.name) + ", but does not appear to be tainted by user input. You should review this manually to determine whether the execution of this method by itself represents an issue. Extended class: " + str(filename))
					vuln_found=True
				elif b.target == 'super':
					find_extensions(local_tree,t)
				#TODO - potentially add setResult check here
			elif type(b) is list:
				for l in b:
					process_mdecl_body(l,local_tree,filename)
			elif hasattr(b,'_fields'):
				for f in b._fields:
					process_mdecl_body(getattr(b,f),local_tree,filename)
	except Exception as e:
		common.logger.error("Problem in process_mdecl function of findSupers.py: "+str(e))
	return

def process_mdecl_body(t,local_tree,filename):
	
	global vuln_found
	try:
		if type(t) is m.MethodInvocation:
			#TODO - This might spew out extras when not needed
			#findExtras.find_extras(filename,t.name)
			try:
				if common.sink_list_check(t,local_tree):
					common.logger.warning("This subclass extends a superclass, potentially via another superclass, which contains a sensitive method invocation: " + str(t.name) + ", but does not appear to be tainted by user input. You should review this manually to determine whether the execution of this method by itself represents an issue. Extended class: " + str(filename))
					vuln_found=True
				elif t.target == 'super':
					try:
						find_extensions(local_tree,t)
					except Exception as e:
						common.logger.error("Problem calling find_extensions from process_mdecl_body in findSupers.py: " +str(e))
			except Exception as e:
				common.logger.error("Problem processing MethodInvocation in process_mdecl_body: " +str(e))
		elif type(t) is list:
			for l in t:
				try:
					process_mdecl_body(l,local_tree,filename)
				except Exception as e:
					common.logger.error("Problem recursively calling process_mdecl_body for list from itself in findSupers.py: " +str(e))
		elif hasattr(t,'_fields'):
			for f in t._fields:
				try:
					process_mdecl_body(getattr(t,f),local_tree,filename)
				except Exception as e:
					common.logger.error("Problem recursively calling process_mdecl_body for fields from itself in findSupers.py: " +str(e))
	except Exception as e:
		common.logger.error("Problem in process_mdecl_body function of findSupers.py "+str(e))
	return


