from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re, sys
import logging

import lib.plyj.model as m
import lib.plyj.parser as plyj
from modules import common
from modules import filters
from modules import findBoundServices
from modules import findExtras
from modules import externalMethodDeclarations
from modules import localMethodDeclarations
from modules.common import ReportIssue, Severity
from modules.createExploit import ExploitType
from modules import report
from modules import findSupers

parser = plyj.Parser()
tracker = []
component_type = ''
tree = ''
entries = []
taint_list = ['getIntent']
current_entry = ''
current_file = ''
local_meth_decls = []
class_name = ''
classList = []

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)


def map_from_manifest(component_list, comp_type):
	"""
	map from manifest
	"""
	global component_type
	global taint_list
	global current_file
	global class_name

	component_type = comp_type
	for j in common.java_files:
		taint_list = ['getIntent']
		file_name = re.search(r'[A-Za-z0-9_]+\.java', j)
		if file_name:
			class_name = re.sub(r'\.java', '', file_name.group())
			for c in component_list:
				if len(c) > 0:
					if type(c) is list:
						c = str(c[0])
					man_item = re.search(r'[A-Za-z0-9_]+$', str(c))
					if man_item:
						man_item = man_item.group()
						if str(man_item) == str(class_name):
							print "=" * 100
							logger.info("This class is exported from a manifest item: " + str(class_name))
							current_file = j
							tree_parser(j, comp_type)
	return


def tree_parser(j, comp_type):
	"""
	tree parser - parses Java files and creates a readable tree of elements which can be iterated over
	"""
	global tree
	global parser

	try:
		tree = parser.parse_file(j)
	except Exception as e:
		common.logger.error("Tree exception: " + str(e))
	if tree is None:
		common.logger.error("Unable to create tree for parsing")
		common.logger.error("File: " + str(j) + " could not be parsed properly, which will negatively impact results")
	else:
		common.logger.info("Checking this file for vulns: " + str(j))
		try:
			find_local_method_declarations(tree)
			find_entry(tree, comp_type)
		except Exception as e:
			if common.source_or_apk == 2:
				common.logger.error("---Oh Snap. Parsing error >.<" + str(e))
			else:
				common.logger.error("Bad file: this is not uncommon")
	return


def find_local_method_declarations(tree):
	'''
	Iterates over tree passing each object to recursive_method_finder
	'''
	global component_type

	if tree is None:
		common.logger.error("Tree type is None for find_local_method_declarations in findMethods.py")
	else:
		try:
			#TODO - verify the other branches are needed here, is m.ClassDeclaration check enough?
			for type_decl in tree.type_declarations:
				if type(type_decl) is m.ClassDeclaration:
					for t in type_decl.body:
						recursive_method_finder(t)
						#possibly redundant
						if str(component_type) == 'activity':
							find_set_result(t)
				elif type(type_decl) is list:
					for y in t:
						recursive_method_finder(y)
						#possibly redundant
						if str(component_type) == 'activity':
							find_set_result(y)
				elif hasattr(t, '_fields'):
					for f in t._fields:
						recursive_method_finder(getattr(t, f))
						#possibly redundant
						if str(component_type) == 'activity':
							find_set_result(f)
		except Exception as e:
			common.logger.error("Problem with find_local_method_declarations in findMethods.py: " + str(e))
	return


def recursive_method_finder(t):
	'''
	Looks for any locally declared methods. All entry points should be captured in this list
	'''
	#TODO - take another look at this, it might not be as complete as I first thought
	global local_meth_decls

	if type(t) is m.MethodDeclaration:
		#TODO - Add declaration names to list for later reference (uniqueness could become an issue later)
		if hasattr(t, 'name'):
			if t.name not in local_meth_decls:
				local_meth_decls.append(t.name)
	elif type(t) is list:
		for i in t:
			if type(i) is m.MethodDeclaration:
				if hasattr(i, 'name'):
					if i.name not in local_meth_decls:
						local_meth_decls.append(i.name)
			elif type(i) is list:
				for y in i:
					recursive_method_finder(i)
	elif hasattr(t, '_fields'):
		for f in t._fields:
			recursive_method_finder(getattr(t, f))
	return


def find_entry(tree, comp_type):
	"""
	find entry points into each class, by looking for component lifecycle methods
	"""
	global entries
	global current_file

	try:
		#Create list of entry points, based on component type
		'''
		if comp_type == 'activity':
			entry = ['onCreate', 'onStart']
		elif comp_type == 'activity-alias':
			entry = ['onCreate', 'onStart']
		elif comp_type == 'receiver':
			entry = ['onReceive']
		elif comp_type == 'service':
			entry = ['onCreate', 'onBind', 'onStartCommand', 'onHandleIntent']
		#TODO - The provider is a unicorn and needs more work
		elif comp_type == 'provider':
			entry = ['onReceive']
		'''
		entry=common.get_entry_for_component(comp_type)
		#Search the tree to see if there is a matching entry point
		if tree is not None:
			for type_decl in tree.type_declarations:
				if type(type_decl) is m.ClassDeclaration:
					entries = []
					for t in type_decl.body:
						if type(t) is m.MethodDeclaration:
							#Checks whether the discovered MethodDeclaration is a component entry point (lifecycle method)
							for e in entry:
								if hasattr(t, 'name'):
									if str(t.name) == str(e):
										common.logger.debug("--Found entry point: " + str(t.name))
										entries.append(str(e))
										'''
										try:
											if str(t.name)=='onBind':
												findBoundServices.main(t,tree)
										except Exception as e:
											common.logger.error("Error in findMethods.py trying to trace bound service: " + str(e))
										'''
										if hasattr(t, 'parameters'):
											for p in t.parameters:
												if hasattr(p, 'type'):
													if hasattr(p.type, 'name'):
														#TODO - This potentially needs to be expanded
														if str(p.type.name.value) == 'Intent':
															taint_list.append(p.variable.name)
					print "entries: "
					for q in entries:
						print str(q)
						findExtras.find_extras(current_file,q)
					if len(entries) < 1:
						if ((comp_type == 'activity') or (comp_type == 'activity-alias')):
							common.logger.debug("This may be a fragment")
						else:
							common.logger.debug("ERROR: Unable to find entry point in this class")
					else:
						common.logger.debug("Walking the class!")
						try:
							walk_the_class_from_entry(tree, entries, comp_type)
						except Exception as e:
							common.logger.error("Unable to walk the class in findMethods.py: " + str(e))
	except Exception as e:
		common.logger.error("Problem in find_entry in findMethods.py" + str(e))
	return


def walk_the_class_from_entry(tree, entries, comp_type):
	"""
	Walk the class beginning from the entry point(s)
	"""
	global current_entry

	# If it's an entry point method, we need to investigate it, otherwise ignore
	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			for e in entries:
				current_entry = e
				for t in type_decl.body:
					if type(t) is m.MethodDeclaration:
						#located an entry point
						if hasattr(t, 'name'):
							if t.name == str(e):
								track(None, True)
								if type(t.body) is list:
									#print "T.BODY: " + str(t.body)
									for b in t.body:
										token_mapper(b)
								else:
									token_mapper(t.body)
	return


def find_set_result(t):
	global component_type
	#This is used to find if the incoming triggering this Activity is going to cause data to be returned
	#TODO - it would be nicer if we actually tracked the flow, but since the exploit APK already parses returned data, it really doesn't matter
	if type(t) is m.MethodInvocation:
		if str(t.name) == 'setResult':
			common.logger.warning("It appears the Activity defined in this class : " + str(
				current_file) + " may return a result via \"setResult\". The exploit APK will automatically parse any returned values, but you should manually inspect this to determine the significance of the returned value.")
			return True
		elif hasattr(t, '_fields'):
			for y in t._fields:
				find_set_result(getattr(t, y))
	elif type(t) is list:
		for i in t:
			if type(i) is m.MethodInvocation:
				find_set_result(i)
			elif type(i) is list:
				for j in i:
					find_set_result(j)
			elif hasattr(i, '_fields'):
				for k in i._fields:
					find_set_result(getattr(i, k))
				#Need to add has fields
	elif hasattr(t, '_fields'):
		for x in t._fields:
			find_set_result(getattr(t, x))
	else:
		return False

#TODO - many of these can likely be generalized down to just a handful too
def token_mapper(token):
	"""
	Token Mapper
	"""
	try:
		if type(token) is m.FieldDeclaration:
			try:
				parse_field_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.MethodInvocation:
			try:
				parse_method_invocation(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.VariableDeclaration:
			try:
				parse_variable_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.VariableDeclarator:
			try:
				parse_variable_declarator(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.MethodDeclaration:
			try:
				parse_method_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ClassInitializer:
			try:
				parse_class_initializer(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ConstructorDeclaration:
			try:
				parse_constructor_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.EnumDeclaration:
			try:
				parse_enum_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.InterfaceDeclaration:
			try:
				parse_interface_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ExpressionStatement:
			try:
				parse_expression_statement(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.IfThenElse:
			try:
				parse_if_then_else(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Return:
			try:
				parse_return(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Try:
			try:
				parse_try(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Catch:
			try:
				parse_catch(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ForEach:
			try:
				parse_for_each(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.For:
			try:
				parse_for(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Switch:
			try:
				parse_switch(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.SwitchCase:
			try:
				parse_switch_case(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Block:
			try:
				parse_block(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Synchronized:
			try:
				parse_synchronized(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Variable:
			try:
				parse_variable(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.EmptyDeclaration:
			common.logger.debug("OOPS - EmptyDeclaration: " + str(type(token)))
		elif type(token) is type(None):
			try:
				parse_none()
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ClassDeclaration:
			try:
				parse_class_declaration(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Assignment:
			try:
				parse_assignment(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Literal:
			try:
				parse_literal(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ClassLiteral:
			try:
				parse_class_literal(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.InstanceCreation:
			try:
				parse_instance_creation(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Cast:
			try:
				parse_cast(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Unary:
			try:
				parse_unary(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Additive:
			try:
				parse_additive(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Type:
			try:
				parse_type(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Equality:
			try:
				parse_equality(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ConditionalAnd:
			try:
				parse_conditional_and(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Conditional:
			try:
				parse_conditional(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ArrayCreation:
			try:
				parse_array_creation(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.While:
			try:
				parse_while(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is bool:
			try:
				parse_bool(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Break:
			try:
				parse_break(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ArrayInitializer:
			try:
				parse_array_initializer(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Annotation:
			try:
				parse_annotation(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.FormalParameter:
			try:
				parse_formal_parameter(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.ConditionalOr:
			try:
				parse_conditional_or(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Wildcard:
			try:
				parse_wildcard(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is str:
			try:
				parse_string(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is int:
			try:
				parse_int(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Relational:
			try:
				parse_relational(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.Name:
			try:
				parse_name(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		elif type(token) is m.FieldAccess:
			try:
				parse_field_access(token)
			except Exception as e:
				common.logger.error("Problem in findMethods.py parsing token type: " + str(type(token)) + ". " +str(e))
		else:
			common.logger.debug("NOT COVERED IN TOKEN MAPPER: ")
			common.logger.debug(type(token))
			common.logger.debug(str(token))
			common.logger.debug(str(tracker))
	except Exception as e:
		common.logger.error("Problem with token_mapper in findMethods.py: " + str(e))
	return


def track(token, reset):
	"""
	Tracks the token
	"""
	global tracker
	if reset:
		tracker = []
	else:
		tracker.append(token)
	return


def wtf_is(token):
	"""
	Identifies the type of token
	"""
	global tree
	global current_entry
	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			common.logger.debug("Checking for token definition: " + str(token))
			for t in type_decl.body:
				if type(t) is m.FieldDeclaration:
					if len(t.variable_declarators) > 0:
						for v in t.variable_declarators:
							if hasattr(v.variable, 'name'):
								if str(v.variable.name) == str(token):
									token_type = str(t.type)
				elif type(t) is m.MethodDeclaration:
					for v in t.body:
						if type(v) is m.VariableDeclaration:
							for d in v.variable_declarators:
								if hasattr(d.variable, 'name'):
									if str(d.variable.name) == str(token):
										token_type = v.type.name.value
	return token_type


def is_global(token):
	"""
	Checks if a given token is global in context
	"""
	foundglobal = False
	for type_decl in tree.type_declarations:
		for t in type_decl.body:
			if type(t) is m.FieldDeclaration:
				for f in t.variable_declarators:
					if str(token) == str(f.variable.name):
						foundglobal = True
					#TODO NOTHING IS ACTUALLY checking the return value, it's just a placeholder for now
					#From here, we want to go and see if this is used in any
	return foundglobal


def generic_tainted(token, tainted):
	'''
	Finds whether any generic object is tainted
	'''
	global taint_list
	if hasattr(token, '_fields'):
		for f in token._fields:
			try:
				if is_tainted(getattr(token, f)):
					tainted = True
					if str(token) not in taint_list:
						common.logger.debug("TAINTED " + str(type(token)) + ": " + str(token))
			except Exception as e:
				common.logger.error("Problem calling is_tainted, from generic_tainted in findMethods.py: " + str(e))

	return tainted


def is_tainted(token):
	"""
	Identifies if a given token is tainted or not
	"""
	tainted = False
	global taint_list
	try:
		if type(token) is m.Assignment:
			if hasattr(token, '_fields'):
				for f in token._fields:
					if hasattr(token, str(f)):
						if is_tainted(getattr(token, str(f))):
							tainted = True
							if str(token) not in taint_list:
								if type(token.lhs) is m.FieldAccess:
									if str(token.lhs.target) == "this":
										if type(token.lhs.name) is str:
											if token.lhs.name not in taint_list:
												taint_list.append(token.lhs.name)
								elif type(token.lhs.value) is str:
									if str(token.lhs.value) not in taint_list:
										taint_list.append(str(token.lhs.value))
									is_global(token.lhs.value)
							else:
								common.logger.debug("Token already in taint_list : " + str(token))
		elif type(token) is m.MethodInvocation:
			for f in token._fields:
				if is_tainted(getattr(token, f)):
					tainted = True
					if str(f) == 'arguments':
						if hasattr(token.target, 'value'):
							taint_list.append(token.target.value)
						#TODO - Verify the class for the package found actually is imported by this class
		elif type(token) is m.VariableDeclaration:
			for f in token._fields:
				if is_tainted(getattr(token, f)):
					tainted = True
					if str(token) not in taint_list:
						for v in token.variable_declarators:
							taint_list.append(v.variable.name)
						#CAN THIS EVER BE > 1 ?

		elif type(token) is m.EmptyDeclaration:
			common.logger.debug("Reached an EmptyDeclaration: " + str(type(token)) + " in findMethods.py")

		elif type(token) is type(None):
			#no-op
			parse_none()

		elif type(token) is str:
			for t in taint_list:
				if str(t) == str(token):
					tainted = True
					if str(token) not in taint_list:
						common.logger.debug("TAINTED String: " + str(token))
					track(None, True)

		elif type(token) is int:
			parse_int(token)

		elif type(token) is list:
			for x in token:
				tainted = generic_tainted(x, tainted)

		elif type(token) is bool:
			parse_bool(token)

		else:
			tainted = generic_tainted(token, tainted)
	except Exception as e:
		common.logger.error("Problem with is_tainted method in findMethods.py: " + str(e))
	return tainted

def tainted_sink_processor(sink, token):
	"""
	Tainted sink processor
	"""
	result = None
	#STUFF THAT TAKES ACTION
	final_sink = []
	final_sink.append([])
	final_sink.append(['android.util.Log', 'int', 'd', ['java.lang.String', 'java.lang.String']])
	final_sink.append(['android.util.Log', 'int', 'd', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'e', ['java.lang.String', 'java.lang.String']])
	final_sink.append(['android.util.Log', 'int', 'e', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'i', ['java.lang.String', 'java.lang.String']])
	final_sink.append(['android.util.Log', 'int', 'i', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'v', ['java.lang.String', 'java.lang.String']])
	final_sink.append(['android.util.Log', 'int', 'v', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.String']])
	final_sink.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.String']])
	final_sink.append(
		['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	final_sink.append(['java.io.OutputStream', 'void', 'write', ['byte[]']])
	#final_sink.append(['java.io.OutputStream','void','write',['byte[]'','int','int']])
	final_sink.append(['java.io.OutputStream', 'void', 'write', ['int']])
	final_sink.append(['java.io.FileOutputStream', 'void', 'write', ['byte[]']])
	#final_sink.append(['java.io.FileOutputStream','void','write',['byte[]'','int','int']])
	final_sink.append(['java.io.FileOutputStream', 'void', 'write', ['int']])
	final_sink.append(['java.io.Writer', 'void', 'write', ['char[]']])
	#final_sink.append(['java.io.Writer','void','write',['char[]'','int','int']])
	final_sink.append(['java.io.Writer', 'void', 'write', ['int']])
	final_sink.append(['java.io.Writer', 'void', 'write', ['java.lang.String']])
	final_sink.append(['java.io.Writer', 'void', 'write', ['java.lang.String', 'int', 'int']])
	final_sink.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent']])
	final_sink.append(
		['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	final_sink.append(['android.media.MediaRecorder', 'void', 'setVideoSource', ['int']])
	final_sink.append(['android.media.MediaRecorder', 'void', 'setPreviewDisplay', ['android.view.Surface']])
	#final_sink.append(['android.media.MediaRecorder','void','start',[]'])
	final_sink.append(['android.content.Context', 'android.content.Intent', 'registerReceiver',
					   ['android.content.BroadcastReceiver', 'android.content.IntentFilter']])
	final_sink.append(['android.content.Context', 'android.content.Intent', 'registerReceiver',
					   ['android.content.BroadcastReceiver', 'android.content.IntentFilter', 'java.lang.String',
						'android.os.Handler']])
	final_sink.append(['android.telephony.SmsManager', 'void', 'sendTextMessage',
					   ['java.lang.String', 'java.lang.String', 'java.lang.String', 'android.app.PendingIntent',
						'android.app.PendingIntent']])
	final_sink.append(['android.telephony.SmsManager', 'void', 'sendDataMessage',
					   ['java.lang.String', 'java.lang.String', 'short', 'byte[]', 'android.app.PendingIntent',
						'android.app.PendingIntent']])
	final_sink.append(['android.telephony.SmsManager', 'void', 'sendMultipartTextMessage',
					   ['java.lang.String', 'java.lang.String', 'java.util.ArrayList', 'java.util.ArrayList',
						'java.util.ArrayList']])
	final_sink.append(['java.net.Socket', 'void', 'connect', ['java.net.SocketAddress']])
	final_sink.append(['android.os.Handler', 'boolean', 'sendMessage', ['android.os.Message']])
	final_sink.append(
		['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putBoolean',
		 ['java.lang.String', 'boolean']])
	final_sink.append(
		['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putFloat',
		 ['java.lang.String', 'float']])
	final_sink.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putInt',
					   ['java.lang.String', 'int']])
	final_sink.append(
		['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putLong',
		 ['java.lang.String', 'long']])
	final_sink.append(
		['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putString',
		 ['java.lang.String', 'java.lang.String']])
	final_sink.append(['org.apache.http.impl.client.DefaultHttpClient', 'org.apache.http.HttpResponse', 'execute',
					   ['org.apache.http.client.methods.HttpUriRequest']])
	final_sink.append(['org.apache.http.client.HttpClient', 'org.apache.http.HttpResponse', 'execute',
					   ['org.apache.http.client.methods.HttpUriRequest']])
	final_sink.append(['android.content.Context', 'void', 'startActivity', ['android.content.Intent']])
	final_sink.append(
		['android.content.Context', 'void', 'startActivity', ['android.content.Intent', 'android.os.Bundle']])
	final_sink.append(['android.content.Context', 'void', 'startActivities', ['android.content.Intent[]']])
	final_sink.append(
		['android.content.Context', 'void', 'startActivities', ['android.content.Intent[]', 'android.os.Bundle']])
	final_sink.append(
		['android.content.Context', 'android.content.ComponentName', 'startService', ['android.content.Intent']])
	final_sink.append(['android.content.Context', 'boolean', 'bindService',
					   ['android.content.Intent', 'android.content.ServiceConnection', 'int']])
	final_sink.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent']])
	final_sink.append(
		['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	final_sink.append(['android.app.Activity', 'void', 'setResult', ['int', 'android.content.Intent']])
	final_sink.append(['android.app.Activity', 'void', 'startActivity', ['android.content.Intent']])
	final_sink.append(
		['android.app.Activity', 'void', 'startActivity', ['android.content.Intent', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivities', ['android.content.Intent[]']])
	final_sink.append(
		['android.app.Activity', 'void', 'startActivities', ['android.content.Intent[]', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityForResult', ['android.content.Intent', 'int']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityForResult',
					   ['android.content.Intent', 'int', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityFromChild',
					   ['android.app.Activity', 'android.content.Intent', 'int', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityFromChild',
					   ['android.app.Activity', 'android.content.Intent', 'int']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityFromFragment',
					   ['android.app.Fragment', 'android.content.Intent', 'int', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityFromFragment',
					   ['android.app.Fragment', 'android.content.Intent', 'int']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityIfNeeded',
					   ['android.content.Intent', 'int', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'startActivityIfNeeded', ['android.content.Intent', 'int']])
	final_sink.append(
		['android.app.Activity', 'android.content.ComponentName', 'startService', ['android.content.Intent']])
	final_sink.append(['android.app.Activity', 'boolean', 'bindService',
					   ['android.content.Intent', 'android.content.ServiceConnection', 'int']])
	final_sink.append(['android.app.Activity', 'void', 'sendBroadcast', ['android.content.Intent']])
	final_sink.append(['android.app.Activity', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	final_sink.append(
		['android.app.Activity', 'void', 'sendBroadcastAsUser', ['android.content.Intent', 'android.os.UserHandle']])
	final_sink.append(['android.app.Activity', 'void', 'sendBroadcastAsUser',
					   ['android.content.Intent', 'android.os.UserHandle', 'java.lang.String']])
	final_sink.append(['android.app.Activity', 'void', 'sendOrderedBroadcast',
					   ['android.content.Intent', 'java.lang.String', 'android.content.BroadcastReceiver',
						'android.os.Handler', 'int', 'java.lang.String', 'android.os.Bundle']])
	final_sink.append(
		['android.app.Activity', 'void', 'sendOrderedBroadcast', ['android.content.Intent', 'java.lang.String']])
	final_sink.append(['android.app.Activity', 'void', 'sendOrderedBroadcastAsUser',
					   ['android.content.Intent', 'android.os.UserHandle', 'java.lang.String',
						'android.content.BroadcastReceiver', 'android.os.Handler', 'int', 'java.lang.String',
						'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'sendStickyBroadcast', ['android.content.Intent']])
	final_sink.append(['android.app.Activity', 'void', 'sendStickyBroadcastAsUser',
					   ['android.content.Intent', 'android.os.UserHandle']])
	final_sink.append(['android.app.Activity', 'void', 'sendStickyOrderedBroadcast',
					   ['android.content.Intent', 'android.content.BroadcastReceiver', 'android.os.Handler', 'int',
						'java.lang.String', 'android.os.Bundle']])
	final_sink.append(['android.app.Activity', 'void', 'sendStickyOrderedBroadcastAsUser',
					   ['android.content.Intent', 'android.os.UserHandle', 'android.content.BroadcastReceiver',
						'android.os.Handler', 'int', 'java.lang.String', 'android.os.Bundle']])
	final_sink.append(['android.content.ContentResolver', 'android.net.Uri', 'insert',
					   ['android.net.Uri', 'android.content.ContentValues']])
	final_sink.append(['android.content.ContentResolver', 'int', 'delete',
					   ['android.net.Uri', 'java.lang.String', 'java.lang.String[]']])
	final_sink.append(['android.content.ContentResolver', 'int', 'update',
					   ['android.net.Uri', 'android.content.ContentValues', 'java.lang.String', 'java.lang.String[]']])
	#final_sink.append(['android.content.ContentResolver','android.database.Cursor','query',['android.net.Uri','java.lang.String[]'','java.lang.String','java.lang.String[]'','java.lang.String']])
	#final_sink.append(['android.content.ContentResolver','android.database.Cursor','query',['android.net.Uri','java.lang.String[]'','java.lang.String','java.lang.String[]'','java.lang.String','android.os.CancellationSignal']])
	#final_sink.append(['java.lang.ProcessBuilder','java.lang.Process','start',[]']
	final_sink.append(['android.app.NotificationManager', 'void', 'notify', ['int', 'android.app.Notification']])
	#Not in SOOT SINK LIST
	final_sink.append(['android.webkit.WebView','void','loadUrl',['java.lang.String']])
	#The second param is java.util.Map<K,V>
	final_sink.append(['android.webkit.WebView','void','loadUrl',['java.lang.String','java.util.Map']])


	#STUFF THAT GETS TAINTED
	intermediate_sink = []
	intermediate_sink.append([])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putBinder', ['java.lang.String', 'android.os.IBinder']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putBoolean', ['java.lang.String', 'boolean']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putBooleanArray', ['java.lang.String', 'boolean[]']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putBundle', ['java.lang.String', 'android.os.Bundle']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putByte', ['java.lang.String', 'byte']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putByteArray', ['java.lang.String', 'byte[]']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putChar', ['java.lang.String', 'char']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putCharArray', ['java.lang.String', 'char[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putCharSequence', ['java.lang.String', 'java.lang.CharSequence']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putCharSequenceArray', ['java.lang.String', 'java.lang.CharSequence[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putCharSequenceArrayList', ['java.lang.String', 'java.util.ArrayList']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putDouble', ['java.lang.String', 'double']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putDoubleArray', ['java.lang.String', 'double[]']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putFloat', ['java.lang.String', 'float']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putFloatArray', ['java.lang.String', 'float[]']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putInt', ['java.lang.String', 'int']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putIntArray', ['java.lang.String', 'int[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putIntegerArrayList', ['java.lang.String', 'java.util.ArrayList']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putLong', ['java.lang.String', 'long']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putLongArray', ['java.lang.String', 'long[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putParcelable', ['java.lang.String', 'android.os.Parcelable']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putParcelableArray', ['java.lang.String', 'android.os.Parcelable[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putParcelableArrayList', ['java.lang.String', 'java.util.ArrayList']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putSerializable', ['java.lang.String', 'java.io.Serializable']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putShort', ['java.lang.String', 'short']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putShortArray', ['java.lang.String', 'short[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putSparseParcelableArray', ['java.lang.String', 'android.util.SparseArray']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putString', ['java.lang.String', 'java.lang.String']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putStringArray', ['java.lang.String', 'java.lang.String[]']])
	intermediate_sink.append(
		['android.os.Bundle', 'void', 'putStringArrayList', ['java.lang.String', 'java.util.ArrayList']])
	intermediate_sink.append(['android.os.Bundle', 'void', 'putAll', ['android.os.Bundle']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'double[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'int']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'putExtra',
							  ['java.lang.String', 'java.lang.CharSequence']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'char']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'android.os.Bundle']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'putExtra',
							  ['java.lang.String', 'android.os.Parcelable[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.io.Serializable']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'int[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'float']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'byte[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'long[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'android.os.Parcelable']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'float[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'long']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.lang.String[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'boolean']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'boolean[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'short']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'double']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'short[]']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.lang.String']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'byte']])
	intermediate_sink.append(
		['org.apache.http.message.BasicNameValuePair', 'void', '<init>', ['java.lang.String', 'java.lang.String']])
	intermediate_sink.append(
		['java.net.URL', 'void', '<init>', ['java.lang.String', 'java.lang.String', 'int', 'java.lang.String']])
	intermediate_sink.append(
		['java.net.URL', 'void', '<init>', ['java.lang.String', 'java.lang.String', 'java.lang.String']])
	intermediate_sink.append(['java.net.URL', 'void', '<init>',
							  ['java.lang.String', 'java.lang.String', 'int', 'java.lang.String',
							   'java.net.URLStreamHandler']])
	intermediate_sink.append(['java.net.URL', 'void', '<init>', ['java.lang.String']])
	intermediate_sink.append(['java.net.URL', 'void', '<init>', ['java.net.URL', 'java.lang.String']])
	intermediate_sink.append(
		['java.net.URL', 'void', '<init>', ['java.net.URL', 'java.lang.String', 'java.net.URLStreamHandler']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'char[]']])
	intermediate_sink.append(['java.net.URL', 'void', 'set',
							  ['java.lang.String', 'java.lang.String', 'int', 'java.lang.String', 'java.lang.String']])
	intermediate_sink.append(['java.net.URL', 'void', 'set',
							  ['java.lang.String', 'java.lang.String', 'int', 'java.lang.String', 'java.lang.String',
							   'java.lang.String', 'java.lang.String', 'java.lang.String']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'putExtra',
							  ['java.lang.String', 'java.lang.CharSequence[]']])
	intermediate_sink.append(
		['java.net.URLConnection', 'void', 'setRequestProperty', ['java.lang.String', 'java.lang.String']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'setAction', ['java.lang.String']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'setClassName',
							  ['android.content.Context', 'java.lang.Class']])
	intermediate_sink.append(['android.content.Intent', 'android.content.Intent', 'setClassName',
							  ['android.content.Context', 'java.lang.String']])
	intermediate_sink.append(
		['android.content.Intent', 'android.content.Intent', 'setComponent', ['android.content.ComponentName']])
	intermediate_sink.append(['android.content.IntentFilter', 'void', 'addAction', ['java.lang.String']])

	for i in intermediate_sink:
		if len(i) > 0:
			if str(i[2]) == str(sink):
				if len(i[3]) == len(token.arguments):
					result = import_checker(i[0], token, i[2], len(i[3]))
				break
	if result == None:
		for f in final_sink:
			if len(f) > 0:
				if str(f[2]) == str(sink):
					if len(f[3]) == len(token.arguments):
						#TODO - need to validate the type of each parameter in the sink vs. the type in the token
						#I'll take the FP dings for now, since it's probably not going to be too many any way
						result = import_checker(f[0], token, f[2], len(f[3]))
					break
	return result


def import_checker(imp, token, method, argslength):
	"""
	Import checker
	"""
	global tree
	global current_file
	new_taint_list = []
	first_pass = True
	again = True
	confirmed = False
	#Another way to approach this could be to simply look for where the method name is declared and see if any of the possibilities are in the sink list
	#or, just check if any of the imports along the tree are a match, then go from there
	#Does the file containing the tainted sink, import the class containing the "actual" sink?
	for imp_decl in tree.import_declarations:
		if hasattr(token.target, 'value'):
			#May be able to remove this assignment, if only used once
			obj_inst = obj_instance_of(token)
			#Exclude android classes
			android_class = re.match(r'android\..*', imp_decl.name.value)
			#Ignoring Android classes, because if this is the match, we already know that
			if not android_class:
				#Check if the token is a class that is imported
				match = re.search(r'' + str(token.target.value) + '$', str(imp_decl.name.value))
				#Check if the token is instead a variable, of the sink class
				if not match:
					match = re.search(r'' + str(obj_inst) + '$', str(imp_decl.name.value))
				if match:
				#Find if the matched sink is an instance of one of the imported classes
					#See if the file here imports the vulnerable class
					#To do this, I need to know to which file I'm going to open, then open it and loop the imports
					#This will break on Windows
					imported_file_name = re.sub('\.', '/', str(imp_decl.name.value))
					for j in common.java_files:
						filename_match = re.search(imported_file_name, str(j))
						if filename_match:
							localtree = parser.parse_file(j)
							#Looking to see if this file imports the class for this sink
							#TODO - This could be made recursive
							for local_imp_decl in localtree.import_declarations:
								if str(imp) == str(local_imp_decl.name.value):
									for type_decl in localtree.type_declarations:
										if type(type_decl) is m.ClassDeclaration:
											for t in type_decl.body:
												if type(t) is m.MethodDeclaration:
													if str(t.name) == str(token.name):
														objclass = re.sub(r'.*\.', '', imp)
														for b in t.body:
															if hasattr(b, '_fields'):
																for f in b._fields:
																	sink_method_finder(getattr(b, f), argslength,
																					   objclass)
																#TODO - Need to go into a parsing routine to get to whether this method is
																#wrapping the method we're looking for, then whether the number of arguments
																#it expects is the same as the one we're looking for
			else:
				match = re.search(r'' + str(obj_inst) + '$', str(imp_decl.name.value))
				if match:

					if type(token) is m.MethodInvocation:
						if again:
							issue = ReportIssue()
							issue.setCategory(ExploitType.RECEIVER)
							issueExtras = []
							for a in token.arguments:
								if type(a) is m.MethodInvocation:
									#deduping list
									for i in taint_list:
										if i not in new_taint_list:
											new_taint_list.append(i)


									for t in new_taint_list:
										if str(a.target.value) == str(t):

											issue.setDetails("The " + str(token.name) + " method, imported from " + str(
														imp_decl.name.value) + " is tainted by " + str(
														a.target.value) + " on object " + token.target.value + " of type " + str(
														obj_inst))
											issue.setFile(str(current_file))
											issue.setSeverity(Severity.VULNERABILITY)

											#This should probably be moved elsewhere
											if first_pass:
												common.logger.log(common.VULNERABILITY_LEVEL,
													"The " + str(token.name) + " method, imported from " + str(
														imp_decl.name.value) + " is tainted by " + str(
														a.target.value) + " on object " + token.target.value + " of type " + str(
														obj_inst))
												first_pass = False
												confirmed = True
												#create a list containing the data needed to build exploit
												class_tmp = []
												#TODO - ensure class_name is pulling the correct value, since it is not declared as global
												class_tmp.append(str(class_name))
												common.sploitparams = class_tmp
												intent_action = []
												intent_action = (filters.find_comp_type(current_file))

											#Need to figure out what the type of the tainting object is, so that we can see what parameters are passed in
											token_type = wtf_is(a.target.value)
											extras = findExtras.extras_for_attack(token_type, a)
											common.logger.log(common.VULNERABILITY_LEVEL,
												"To exploit, you will need to send an intent with the key: " + str(
													extras[1]) + " of type: " + str(re.sub(r'get', '', extras[0])))
											issueExtras.append("To exploit, you will need to send an intent with the key: " + str(
													extras[1]) + " of type: " + str(re.sub(r'get', '', extras[0])))
											extras_tmp = [extras[1], extras[0]]
											common.sploitparams.append(extras_tmp)

											common.logger.log(common.VULNERABILITY_LEVEL,
												"To exploit, you will need to send an intent with the action: " + str(
													intent_action))
										#TODO - Need to send this information to an API that builds the APK

								again = False
							issue.setExtras("list", issueExtras)
							report.write_badger("appcomponents", issue.getSeverity(), issue.getDetails(), issueExtras)
					else:
						common.logger.warning("Uncategorized Vulnerability: " + str(token))
	return confirmed

def obj_instance_of(token):
	"""
	Identifies the class of token
	"""
	i_of = None
	#This is to determine what type this object is
	for type_decl in tree.type_declarations:
		if type(type_decl) is m.ClassDeclaration:
			for t in type_decl.body:
				if hasattr(t, 'body'):
					for a in t.body:
						if type(a) is m.VariableDeclaration:
							for v in a.variable_declarators:
								if str(v.variable.name) == str(token.target.value):
									if type(v.initializer) is m.MethodInvocation:
										i_of = v.initializer.target.value
	return i_of


def sink_method_finder(field, length, method):
	"""
	Master sink finder
	"""
	confirmed = False
	if type(field) is list:
		for x in field:
			sink_method_finder(x, length, method)
	if hasattr(field, '_fields'):
		for q in field._fields:
			if hasattr(field, 'target'):
				if hasattr(field.target, 'value'):
					if str(field.target.value) == str(method):
						#BUG - SOMETHING IS WRONG HERE WITH THE ARGUMENT COUNT CHECKING
						if len(field.arguments) == length:
							confirmed = True
		else:
			if hasattr(field, '_fields'):
				for f in field._fields:
					sink_method_finder(getattr(field, f), length, method)
	return confirmed


def list_checker(token, q):
	"""
	List checker
	"""
	try:
		tainted = False
		if type(q) is list:
			try:
				track(q, False)
				for i in q:
					token_mapper(i)
			except Exception as e:
				common.logger.error("Problem with list parsing in list_checker method of findMethods.py: " + str(e))
		else:
			try:
				if is_tainted(token):
					tainted = True
				try:
					check = getattr(token, str(q))
				except Exception as e:
					common.logger.error("attribute error: " + str(e))
				if type(check) is list:
					tainted = list_checker(token, check)
				else:
					if is_tainted(check):
						tainted = True
					token_mapper(check)
			except Exception as e:
				common.logger.error(
					"Problem with non-list handling in list_checker method of findMethods.py: " + str(e))
	except Exception as e:
		common.logger.error("Problem with list_checker in findMethods.py: " + str(e))
	return tainted


def parse_expression_statement(token):
	"""
	Parse token type - statement
	"""
	try:
		track(token.expression, False)
		if hasattr(token, '_fields'):
			for t in token._fields:
				list_checker(token, t)
	except Exception as e:
		common.logger.error("Problem with parse_expression_statement in findMethods.py: " + str(e))
	return


def parse_class_literal(token):
	"""
	Parse token type - literal
	"""
	try:
		track(token, False)
		if hasattr(token, '_fields'):
			for f in token._fields:
				track(f, False)
				if is_tainted(getattr(token, f)):
					common.logger.debug("TAINTED: " + str(token))
				else:
					if list_checker(token, f):
						common.logger.debug("TAINTED: " + str(token))
	except Exception as e:
		common.logger.error("Problem with parse_class_literal in findMethods.py: " + str(e))
	return


def parse_relational(token):
	"""
	Parse token type - relational
	"""
	try:
		track(token, False)
		if hasattr(token, '_fields'):
			for f in token._fields:
				track(f, False)
				if is_tainted(getattr(token, f)):
					common.logger.debug("TAINTED: " + str(token))
				else:
					if list_checker(token, f):
						common.logger.debug("TAINTED: " + str(token))
	except Exception as e:
		common.logger.error("Problem with parse_relational in findMethods.py: " + str(e))
	return


def parse_while(token):
	"""
	Parse token type - While
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_array_initializer(token):
	"""
	Parse token type - ArrayInitializer
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_wildcard(token):
	"""
	Parse token type - Wildcard
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_int(token):
	"""
	Parse token type - Integer
	"""
	return


def parse_bool(token):
	"""
	Parse token type - Boolean
	"""
	return


def parse_formal_parameter(token):
	"""
	Parse token type - formal parameter
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_equality(token):
	"""
	Parse token type - equality
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_unary(token):
	"""
	Parse token type - unary
	"""
	return


def parse_none():
	"""
	Parse token type - None
	"""
	return


def parse_field_access(token):
	"""
	Parse token type - FieldAccess
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
	return


def parse_array_creation(token):
	"""
	Parse token type - ArrayCreation
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_conditional_and(token):
	"""
	Parse token type - Conditional AND
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_conditional(token):
	"""
	Parse token type - Conditional
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_type(token):
	"""
	Parse token type - Type
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_string(token):
	"""
	Parse token type - String
	"""
	track(token, False)
	if is_tainted(token):
		common.logger.debug("TAINTED STRING: " + str(tracker[len(tracker) - 2]))
	#BUG - This may be causing me to miss a second getIntent in the path
	#It might make sense to traverse the tree backwards until is not longer tainted, but then how to move forward
	#Should I really get down to the string level? Wouldn't this cause a string "getIntent" to be misunderstood
	return


def parse_additive(token):
	"""
	Parse token type - Additive
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_assignment(token):
	"""
	Parse token type - assignment
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))

	return

def is_super(token):
	match=False
	if hasattr(token,'target'):
		if token.target =='super':
			match=True
	return match


def parse_method_invocation(token):
	"""
	Parse token type - Method invocation
	"""
	global tree
	global local_meth_decls
	global entries
	global component_type
	global current_file

	if is_super(token):
		#Returns a bool of whether a sensitive method was encountered
		try:
			if findSupers.find_extensions(tree,token):
				#Need filename and current entry point
				try:
					findExtras.find_extras(current_file,current_entry)
				except Exception as e:
					common.logger.error("Problem with findExtras in parse_method_invocation for supers: " +str(e))
				#Need to deliver the results from the two calls above to the exploit and report
			if component_type == 'activity':
				try:
					find_set_result(token)
				except Exception as e:
					common.logger.error("Problem calling find_set_result in parse_method_invocation for supers: " +str(e))
		except Exception as e:
				common.logger.error("Problem parsing supers in parse_method_invocation: " +str(e))
	else:
		#TODO - This call may now be redundant
		if str(component_type) == 'activity':
			try:
				find_set_result(token)
			except Exception as e:
				common.logger.error("Problem calling find_set_result in parse_method_invocation: " +str(e))
		if hasattr(token, 'name'):
			if token.name not in local_meth_decls:
			#BUG - Problem with this logic is it assumes the entire class has already been parsed
			#To avoid this, we use an ugly hack that should cause the whole class to be parsed
				recursive_method_finder(tree)
				#Yes this could be re-ordered, but seems more efficient, since it saves the recursion time
		if token.name not in entries:
			if type(tree) is not None:
				closeEnough=False
			#From here we need to create the call tree in the local file
				try:
					common.logger.debug("Parsing local method declarations")
					closeEnough=localMethodDeclarations.main(token, tree, current_file)
				except Exception as e:
					common.logger.error("Problem trying to look for locally declared methods in findMethods.py: " + str(e))
				if not closeEnough:
					try:
						common.logger.debug("Parsing external method declarations")
						externalMethodDeclarations.main(token, tree, current_file)
					except Exception as e:
						common.logger.error('Problem running externalMethodDeclarations module from findMethods.py: ' + str(e))
			else:
				common.logger.error("Tried to pass None type tree to externalMethodDeclarations in findMethods.py")

			try:
				track(token, False)
				if hasattr(token, '_fields'):
					for f in token._fields:
						if type(f) is m.MethodInvocation:
							#TODO possibly redundant
							if str(component_type) == 'activity':
								find_set_result(f)
						track(f, False)
						if is_tainted(getattr(token, f)):
							common.logger.debug("TAINTED: " + str(token))
							try:
								sink = common.sink_list_check(token,tree)
							except Exception as e:
								common.logger.error("Problem trying to find sink: " + str(e))
							if sink != None:
								if tainted_sink_processor(sink, token):
									break
						elif list_checker(token, f):
							common.logger.debug("TAINTED: " + str(token))
			except Exception as e:
				common.parsingerrors.add(str(current_file))
				common.logger.error("Problem in parse_method_invocation of findMethods.py, when trying to match sinks: " + str(e))
	return


def parse_conditional_or(token):
	"""
	Parse token type - Conditional OR
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_field_declaration(token):
	"""
	Parse token type - Field Declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_name(token):
	"""
	Parse token type - Name
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_cast(token):
	"""
	Parse token type - Cast
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_variable_declaration(token):
	"""
	Parse token type - variable declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_catch(token):
	"""
	Parse token type - Catch
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_switch(token):
	"""
	Parse token type - switch
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_switch_case(token):
	"""
	Parse token type - switchCase
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_variable_declarator(token):
	"""
	Parse token type - variable declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_method_declaration(token):
	"""
	Parse token type - method declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_class_initializer(token):
	"""
	Parse token type - Class Initializer
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_constructor_declaration(token):
	"""
	Parse token type - constructor declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_enum_declaration(token):
	"""
	Parse token type - enum declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_interface_declaration(token):
	"""
	Parse token type - interface declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_if_then_else(token):
	"""
	Parse token type - IfThenElse
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_return(token):
	"""
	Parse token type - return
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_try(token):
	"""
	Parse token type - try
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_for_each(token):
	"""
	Parse token type - For each
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_for(token):
	"""
	Parse token type - For
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_block(token):
	"""
	Parse token type - Block
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_synchronized(token):
	"""
	Parse token type - Synchronized
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_variable(token):
	"""
	Parse token type - Variable
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_class_declaration(token):
	"""
	Parse token type - Class declaration
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_annotation(token):
	"""
	Parse token type - annotation
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_literal(token):
	"""
	Parse token type - Literal
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_break(token):
	"""
	Parse token type - break
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return


def parse_instance_creation(token):
	"""
	Parse token type - Instance creation
	"""
	track(token, False)
	if hasattr(token, '_fields'):
		for f in token._fields:
			track(f, False)
			if is_tainted(getattr(token, f)):
				common.logger.debug("TAINTED: " + str(token))
			else:
				if list_checker(token, f):
					common.logger.debug("TAINTED: " + str(token))
	return
