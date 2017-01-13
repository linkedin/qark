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

parser = plyj.Parser()
tree=''

def main(file_name,value):
	'''
	Parses file to determine where to look for constants
	'''
	global tree

	file_found=False
	var_found=''

	try:
		tree = parser.parse_file(file_name)
	except Exception as e:
		common.logger.error("Tree exception: " + str(e))
	try:
		if tree is not None:
			if var_found is not None:
				if len(var_found)==0:
					value_dots=value.split('.')
					if value_dots is not None:
						if len(value_dots)>0:
							for i in tree.import_declarations:
								import_dots=i.name.value.split('.')
								if import_dots is not None:
									if import_dots[len(import_dots)-1]==value_dots[0]:
										if len(var_found)==0:
											for j in common.java_files:
												j_slash=j.split('/')
												if j_slash is not None:
													j_dots=j_slash[len(j_slash)-1].split('.')
													if j_dots is not None:
														if j_dots[len(j_dots)-2]==value_dots[0]:
															file_found=True
															try:
																new_tree=parser.parse_file(j)
															except Exception as e:
																common.logger.error("Unable to create tree for import while looking for extras: " + str(e))
																break
															if len(var_found)==0:
																try:
																	for type_decl in new_tree.type_declarations:
																		if type(type_decl) is m.ClassDeclaration:
																			if len(var_found)==0:
																				for t in type_decl.body:
																					var_found=recursive_var_finder(t,value_dots)
																					if len(var_found)>0:
																						return var_found
																except Exception as e:
																	common.logger.error("Problem in constantResolver.main trying to process new_tree: " + str(e))
				else:	
					print "Following string_finder"
					try:
						string_finder(tree,value)
					except Exception as e:
						common.logger.error("Problem trying to find strings in tree in constantResolver.py: " + str(e))
				if var_found is not None:
					if len(var_found)==0:
						#Constant wasn't found in imports, check all files
						for j in common.java_files:
							second_tree=parser.parse_file(j)
							if second_tree is not None:
								if len(var_found)==0:
									try:
										for type_decl in second_tree.type_declarations:
											if type(type_decl) is m.ClassDeclaration:
												if len(var_found)==0:
													for t in type_decl.body:
														try:
															var_found=recursive_var_finder(t,value_dots)
														except Exception as e:
															common.logger.error("Problem trying to recursively find variables: " + str(e))
														if len(var_found)>0:
															return var_found
									except Exception as e:
										common.logger.error("Problem in constantResolver.main, processing second_tree: " + str(e))
		else:
			common.logger.error("Unable to create tree while looking for constants for : " + str(file_name))
	except Exception as e:
		common.logger.error("Problem in constantResolver.main: " + str(e))
	return var_found

def recursive_var_finder(t,local_value_dots):
	'''
	Looks for definitions of constants
	'''
	found=''
	try:
		if local_value_dots is not None:
			if len(local_value_dots)>1:
				if type(t) is m.VariableDeclarator:
					if t.variable.name==local_value_dots[1]:
						if type(t.initializer) is m.Literal:
							found=str(t.initializer.value)
							return found
				elif type(t) is list:
					for l in t:
						if found is not None:
							if len(found)>0:
								return found
							else:
								try:
									found=recursive_var_finder(l,local_value_dots)
								except Exception as e:
									common.logger.error("Problem trying to recursively find variables from list: " + str(e))
				elif hasattr(t,'_fields'):
					for f in t._fields:
						if found is not None:
							if len(found)>0:
								return found
							else:
								try:
									found=recursive_var_finder(getattr(t,f),local_value_dots)
								except Exception as e:
									common.logger.error("Problem trying to recursively find variables from fields: " + str(e))
	except Exception as e:
		common.logger.error("Problem in recursive_var_finder function of constantResolver.py: " + str(e))
	return found

def string_finder(local_tree,value):
	'''
	Parses tree to find where to look for locally declared constants
	'''
	found=''
	try:
		for type_decl in local_tree.type_declarations:
			if type(type_decl) is m.ClassDeclaration:
				for t in type_decl.body:
					try:
						found=recursive_string_finder(local_tree,t,value)
						if found is not None:
							if len(found)>0:
								return found
					except Exception as e:
						common.logger.error("Problem calling recursive_string_finder from string_finder in constantResolver.py: " + str(e))
	except Exception as e:
		common.logger.error("Problem in constantResolver.string_finder: " + str(e))
	return found

def recursive_string_finder(local_tree,t,value):
	'''
	Looks for locally declared constants
	'''
	found=''
	if type(t) is m.VariableDeclarator:
		if t.variable.name==value:
			if type(t.initializer) is m.Literal:
				found=t.initializer.value
				return found
	elif type(t) is list:
		for l in t:
			if found is not None:
				if len(found)>0:
					return found
				else:
					found=recursive_string_finder(local_tree,l,value)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			if found is not None:
				if len(found)>0:
					return found
				else:
					found=recursive_string_finder(local_tree,getattr(t,f),value)
	return found
