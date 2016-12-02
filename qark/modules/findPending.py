from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re,sys
import logging
import lib.plyj.parser as plyj
import lib.plyj.model as m
from lib.progressbar import *
from lib.pubsub import pub
from modules.report import ReportIssue
from modules.common import Severity, ReportIssue
from modules.createExploit import ExploitType
from modules import common
from modules import report
from modules.common import terminalPrint

common.logger = logging.getLogger()

tree=''
current_file=''
parser = plyj.Parser()
method_list=[]
#These methods create instances of Pending Intents
method_list.append('getActivities')
method_list.append('getService')
method_list.append('getActivity')
method_list.append('getBroadcast')


def start(queue,height):
	"""
	Start finding pending intents
	"""
	results = []
	global tree
	global current_file
	count = 0

	#TODO - Look for use of fillIn method which can make this a much more exploitable condition
	for j in common.java_files:
		count = count + 1
		pub.sendMessage('progress', bar='Pending Intents', percent=round(count*100/common.java_files.__len__()))
		current_file=j
		try:
			tree=parser.parse_file(j)
		except ValueError as e:
			continue
		#TODO - Need to add scanning of the imports, to see if Intent or PendingIntent is extended, was working on it, 
		#but the one issue where it arose was non-trivial, so I gave up for now
		if hasattr(tree,'type_declarations'):
			for type_decl in tree.type_declarations:
				if type(type_decl) is m.ClassDeclaration:
					for t in type_decl.body:
						for f in t._fields:
							#dynamically parse each token where is f is the field and t is the token
							try:
								recurse(f,t,results)
							except Exception as e:
								common.logger.debug("Problem in recurse function of findPending.py: " + str(e))
								common.parsingerrors.add(str(current_file))

		else:
			common.logger.debug("No type declarations: " + str(j))
			report.write("parsingerror-issues-list", str(current_file), "strong")
	queue.put(results)
	return

def recurse(f,t,results):
	"""
	Recurse
	"""
	#Looking for pending intents
	global method_list
	current=getattr(t,f)
	if type(current) is str:
		for e in method_list:
			if str(type(current)) == str(e):
				#TODO - Remove this (never seems to be hit)
				report.write("parsingerror-issues-list", str(current_file), "strong")
				common.logger.debug("Please report the following error, if you see this")
				common.logger.debug("INCOMPLETE CODE BRANCH REACHED findPending.py #0 (results may be incomplete)")
	elif type(current) is list:
		for l in current:
			#TODO - There might be a way to get rid of this block and just use recurse
			if type(l) is m.MethodInvocation:
				for i in method_list:
					if str(l.name) == str(i):
						if hasattr(current,'target'):
							if hasattr(current.target,'value'):
								if str(current.target.value) == "PendingIntent":
									#TODO - the interesting ones seem to be of type Name only
									#The intent is always the third parameter, for getActivities it is an array
									try:
										parse_args(current.arguments[2],results)
									except Exception as e:
										report.write("parsingerror-issues-list", str(current_file), "strong")
										common.logger.debug("Problem in parse_args function of findPending.py: " + str(e))
			elif l is None:
				pass
			else:
				if type(l) is not str:
					for n in l._fields:
						try:
							recurse(n,l,results)
						except Exception as e:
							report.write("parsingerror-issues-list", str(current_file), "strong")
							common.logger.debug("Problem in recurse function of findPending.py: " + str(e))
				else:
					for g in method_list:
						if str(g) == str(l):
							#TODO - Remove this (never seems to be hit)
							report.write("parsingerror-issues-list", str(current_file), "strong")
							common.logger.debug("Please report the following error, if you see this")
							common.logger.debug("INCOMPLETE CODE BRANCH REACHED findPending.py #2 - Press any key to continue (results may be incomplete)")
	elif type(current) is m.MethodInvocation:
		for j in method_list:
			if str(current.name) == str(j):
				if hasattr(current,'target'):
					if hasattr(current.target,'value'):
						if str(current.target.value) == "PendingIntent":
							#TODO - the interesting ones seem to be of type Name only
							#The intent is always the third parameter, for getActivities it is an array
							try:
								parse_args(current.arguments[2],results)
							except Exception as e:
								report.write("parsingerror-issues-list", str(current_file), "strong")
								common.logger.debug("Problem in recurse function of findPending.py: " + str(e))
	elif type(current) is m.VariableDeclaration:
		if hasattr(current,'type'):
			if type(current.type) is m.Type:
				if hasattr(current.type,'name'):
					if type(current.type.name) is not str:
						if hasattr(current.type.name,'value'):
							if str(current.type.name.value) == "PendingIntent":
								report.write("parsingerror-issues-list", str(current_file), "strong")
								common.logger.debug("findPending - recurse, found PendingIntent, but not handled: " + str(current))
							else:
								report.write("parsingerror-issues-list", str(current_file), "strong")
								common.logger.debug("findPending - recurse, can't find PendingIntent: " + str(current))
	elif hasattr(current,'_fields'):
		for q in current._fields:
			try:
				recurse(q,current,results)
			except Exception as e:
				report.write("parsingerror-issues-list", str(current_file), "strong")
				common.logger.debug("Problem in recurse function of findPending.py: " + str(e))
	return

def parse_args(arg,results):
	"""
	Checking to see whether the setClass method is called on the arguments of a pending intent, if it is a new instance of an Intent
	"""
	if type(arg) is m.MethodInvocation:
		if type(arg.target) is m.InstanceCreation:
			#If the intent only has one argument, it must be implicit
			if len(arg.target.arguments) > 1:
				if type(arg.target.arguments[1]) is m.Name:
					#At this point, I need to go through the tree and see if this arg is a class, making this explicit and safe
					#If the argument is not a name, what is it?
					if hasattr(arg.target.arguments[1],'value'):
						try:
							if find_class(arg.target.arguments[1].value,results):
								return
							else:
								report.write("parsingerror-issues-list", str(current_file), "strong")
								common.logger.debug("ERROR: CAN'T FIND THE CLASS in parse_args")
						except Exception as e:
							report.write("parsingerror-issues-list", str(current_file), "strong")
							common.logger.debug("Problem in find_class function of findPending.py: " + str(e))
				else:
					report.write("parsingerror-issues-list", str(current_file), "strong")
					common.logger.debug("ERROR: UNEXPECTED Type " + str(type(arg.target.arguments[1])))
			else:
				#TODO - need to add details here
				issue = ReportIssue()
				issue.setCategory(ExploitType.INTENT)
				issue.setDetails("PendingIntent created with implicit intent. File: " + str(current_file))
				issue.setFile(current_file)
				issue.setSeverity(Severity.VULNERABILITY)
				results.append(issue)

				issue = terminalPrint()
				issue.setLevel(Severity.VULNERABILITY)
				issue.setData("PendingIntent created with implicit intent. File: " + str(current_file))
				results.append(issue)
		else:
			#TODO - Remove this (never seems to be hit)
			report.write("parsingerror-issues-list", str(current_file), "strong")
			common.logger.debug("Please report the following error, if you see this")
			common.logger.debug("ERROR: INCOMPLETE CODE BRANCH REACHED findPending.py #4 - Press any key to continue (results may be incomplete)")
	elif type(arg) is m.Name:
		if hasattr(arg,'value'):
			try:
				find_intent(arg.value,results)
			except Exception as e:
				report.write("parsingerror-issues-list", str(current_file), "strong")
				common.logger.debug("Problem in find_intent function of findPending.py: " + str(e))
	else:
		#TODO - Remove this (never seems to be hit)
		report.write("parsingerror-issues-list", str(current_file), "strong")
		common.logger.debug("Please report the following error, if you see this")
		common.logger.debug("ERROR: INCOMPLETE CODE BRANCH REACHED findPending.py #5 - Press any key to continue (results may be incomplete)")
	return

def find_class(classname,results):
	found=False
	"""
	Find the class name
	"""

	if hasattr(tree,'type_declarations'):
		for type_decl in tree.type_declarations:
			if type(type_decl) is m.ClassDeclaration:
				if str(type_decl.name) == str(classname):
					found=True
					return found
				else:
					if recurse_class(classname,type_decl,results):
						return True
			elif type(type_decl) is m.VariableDeclaration:
				if hasattr(type_decl,'type'):
					if hasattr(type_decl.type,'name'):
						if hasattr(type_decl.type.name,'value'):
							if str(type_decl.type.name.value) == str(classname):
								return True
			else:
				if recurse_class(classname,type_decl,results):
					return True
	return found

def recurse_class(classname,treeObject,results):
	found=False
	if hasattr(treeObject,'_fields'):
		for x in treeObject._fields:
			if type(getattr(treeObject,x)) is list:
				for y in getattr(treeObject,x):
					if type(y) is m.ClassDeclaration:
						if str(y.name) == str(classname):
							found=True
							return found
					elif type(y) is m.VariableDeclaration:
						if hasattr(y,'type'):
							if hasattr(y.type,'name'):
								if hasattr(y.type.name,'value'):
									if str(y.type.name.value) == "Class":
										for v in y.variable_declarators:
											if str(v.variable.name) == str(classname):
												found=True
												return found
					else:
						if recurse_class(classname,y,results):
							return True
			elif type(getattr(treeObject,x)) is m.ClassDeclaration:
				if x.name == str(classname):
					found=True
					return found
				else:
					if recurse_class(classname,x,results):
						return True

			elif type(getattr(treeObject,x)) is m.VariableDeclaration:
				if hasattr(getattr(treeObject,x),'type'):
					if hasattr(getattr(treeObject,x).type,'name'):
						if hasattr(getattr(treeObject,x).type.name,'value'):
							if str(getattr(treeObject,x).type.name.value) == str(classname):
								found=True
								return found

			elif hasattr(getattr(treeObject,x),'_fields'):
				for z in getattr(treeObject,x)._fields:
					if recurse_class(classname,getattr(getattr(treeObject,x),z),results):
						return True
	elif type(treeObject) is list:
		for a in treeObject:
			if recurse_class(classname,a,results):
				return True
	return found

def find_intent(intent,results):
	"""
	Find Intent 
	"""
	#TODO - This section is ugly and needs to be refactored
	#Looking for the intent used in the pending intent
	global tree
	found=False
	explicit=False
	if hasattr(tree,'type_declarations'):
		for type_decl in tree.type_declarations:
			if type(type_decl) is m.ClassDeclaration:
				for t in type_decl.body:
					if not found:
						if type(t) is m.VariableDeclaration:
							if hasattr(t,'type'):
								if type(t.type) is not str:
									report.write("parsingerror-issues-list", str(current_file), "strong")
									common.logger.debug("Please report the following error, if you see this")
									common.logger.debug("ERROR: INCOMPLETE CODE BRANCH REACHED findPending.py #6 - Press any key to continue (results may be incomplete)")
									if str(t.type) == "Intent":
										common.logger.error("FOUND Intent Variable 0: " + str(t))
									else: 
										if hasattr(t.type,'name'):
											if hasattr(t.type.name,'value'):
												if str(t.type.name.value) == "Intent":
													common.logger.debug("FOUND Intent Variable 1: " + str(t))
						else:
							try:
								temp=intent_digger(t,intent)
							except Exception as e:
								common.logger.debug("Error in intent_digger function of findPending.py: " + str(e))
							found=temp[0]
							explicit=temp[1]
							if found:
								if not explicit:
									#See if the intent is explicit
									if type(t) is m.MethodInvocation:
										if str(t.name) == "setClass":
											explicit=True
										elif str(t.name) == "setPackage":
											explicit=True
									elif type(t) is m.MethodDeclaration:
										for f in t._fields:
											if type(getattr(t,f)) is list:
												for x in getattr(t,f):
													if type(x) is m.MethodInvocation:
														if str(x.name) == "setClass":
															explicit=True
														elif str(x.name) == "setPackage":
															explicit=True
													else:
														if hasattr(x,'_fields'):
															for y in x._fields:
																if type(getattr(x,y)) is m.MethodInvocation:
																	if str(getattr(x,y).name) == "setClass":
																		if hasattr(getattr(x,y).target,'value'):
																			if str(getattr(x,y).target.value) == str(intent):
																				explicit=True
																			elif str(getattr(x,y).name) == "setPackage":
																				if str(getattr(x,y).target.value) == str(intent):
																					explicit=True
																		else:
																			common.logger.debug("Something went wrong in findPending, when determining if the Intent was explicit")
														elif type(x) is list:
															common.logger.debug("ERROR: UNEXPECTED CODE PATH in find_intent - 1")
											elif type(getattr(t,f)) is m.MethodInvocation:
												common.logger.debug("ERROR: UNEXPECTED CODE PATH in find_intent - 2")
									else:
										for f in t._fields:
											if type(getattr(t,f)) is list:
												for x in getattr(t,f):
													if type(x) is m.MethodInvocation:
														if str(x.name) =="setClass":
															explicit=True
														elif str(x.name) =="setPackage":
															explicit=True
								else:
									break
	else:
		common.logger.debug("NO TYPE DECLARATIONS")
	if not explicit:
		if found:
			issue = ReportIssue()
			issue.setCategory(ExploitType.INTENT)
			issue.setDetails("Implicit Intent: " + str(intent) + " used to create instance of PendingIntent. A malicious application could potentially intercept, redirect and/or modify (in a limited manner) this Intent. Pending Intents retain the UID of your application and all related permissions, allowing another application to act as yours.  File: " + str(current_file) + " More details: https://www.securecoding.cert.org/confluence/display/android/DRD21-J.+Always+pass+explicit+intents+to+a+PendingIntent")
			issue.setFile(current_file)
			issue.setSeverity(Severity.VULNERABILITY)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData("Implicit Intent: " + str(intent) + " used to create instance of PendingIntent. A malicious application could potentially intercept, redirect and/or modify (in a limited manner) this Intent. Pending Intents retain the UID of your application and all related permissions, allowing another application to act as yours.  File: " + str(current_file) + " More details: https://www.securecoding.cert.org/confluence/display/android/DRD21-J.+Always+pass+explicit+intents+to+a+PendingIntent")
			results.append(issue)
		else:
			#TO DO - ensure we can resolve custom intents to avoid this error
			common.logger.debug("ERROR: COULDN'T FIND THE INTENT: " + str(intent) + " This may either be due to a custom Intent class or other error")
	return

def intent_digger(t,intent):
	"""
	Traverse the intent declaration hierarchy
	"""
	results=[False,False]
	if hasattr(t,"_fields"):
		for f in t._fields:
			current=getattr(t,f)
			if type(current) is list:
				for c in current:
					if type(c) is m.VariableDeclaration:
						if hasattr(c,'type'):
							if type(c.type) is m.Type:
								if hasattr(c.type,'name'):
									if hasattr(c.type.name,'value'):
										if c.type.name.value == "Intent":
											for v in c.variable_declarators:
												if str(v.variable.name) == str(intent):
													found=True
													if hasattr(v.initializer,'arguments'):
														for a in v.initializer.arguments:
															if type(a) is m.ClassLiteral:
																explicit=True
																results=[found,explicit]
																return results
													results=[found,False]
													return results

					elif type(c) is m.VariableDeclarator:
						if hasattr(c.initializer,'type'):
							if hasattr(c.initializer.type.name,'value'):
								if c.initializer.type.name.value == "Intent":
									if str(c.variable.name) == str(intent):
										found=True
										if hasattr(c.initializer,'arguments'):
											for a in c.initializer.arguments:
												if type(a) is m.ClassLiteral:
													explicit=True
													results=[found,explicit]
													return results
										explicit=False
										results=[found,explicit]
										return results
						else:
							results=intent_digger(c.initializer,intent)
							if results[0] == True:
								return results

					else:
						results=intent_digger(c,intent)
						if results[0] == True:
							return results

			elif type(current) is m.VariableDeclaration:
				if hasattr(current,'type'):
					if type(current.type) is m.Type:
						if hasattr(current.type.name,'value'):
							if current.type.name.value == "Intent":
								for v in current.variable_declarators:
									if str(v.variable.name) == str(intent):
										found=True
										for a in v.initializer.arguments:
											if type(a) is m.ClassLiteral:
												explicit=True
												results=[found,explicit]
												return results
			elif type(current) is m.VariableDeclarator:
				if hasattr(c.initializer,'type'):
					if hasattr(c.initializer.type.name,'value'):
						if c.initializer.type.name.value == "Intent":
							if str(c.variable.name) == str(intent):
								found=True
								for a in c.initializer.arguments:
									if type(a) is m.ClassLiteral:
										explicit=True
										results=[found,explicit]
										return results
								explicit=False
								results=[found,explicit]
								return results
			else:
				if hasattr(current,'_fields'):
					for r in current._fields:
						results=intent_digger(getattr(current,r),intent)
						if results[0] == True:
							return results
							
	elif type(t) is list:
		for y in t:
			results=intent_digger(y,intent)
			if results[0] == True:
				return results

	return results
