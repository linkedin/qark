'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''


import lib.plyj.parser as plyj
from modules import common
import lib.plyj.model as m
import logging

parser = plyj.Parser()
#Until we can match types, we can only match name and param count
closeEnough=''
localTree=''
found=False

def main(token,tree,current_file):
	global closeEnough
	global localTree

	localTree=tree
	closeEnough=False

	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			for t in type_decl.body:
				recursiveMethodFinder(t,token)
	return closeEnough

def recursiveMethodFinder(t,token):
	global closeEnough

	if type(t) is m.MethodDeclaration:
		if str(t.name)==str(token.name):
			if len(t.parameters)==len(token.arguments):
				closeEnough=True
				if sinksEncountered(t):
					common.logger.log(common.VULNERABILITY_LEVEL,"It appears a vulnerability was found here, but unfortunately we haven't completed this branch yet.")
	elif type(t) is list:
		for l in t:
			recursiveMethodFinder(l,token)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			recursiveMethodFinder(getattr(t,f),token)

	return

def sinksEncountered(t):
	global localTree
	global found

	if type(t) is m.MethodInvocation:
		# raw_input()
		try:
			found=common.sink_list_check(t,localTree)
		except Exception as e:
			common.logger.error("Problem in call to common.sink_list_check from localMethodDeclarations.py: " + str(e))
	elif type(t) is list:
		for l in t:
			sinksEncountered(l)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			sinksEncountered(f)
	return found