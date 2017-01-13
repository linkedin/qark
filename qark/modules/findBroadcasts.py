from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re
import logging

import lib.plyj.model as m
import lib.plyj.parser as plyj
from modules import common
from modules import report
from modules.report import ReportIssue
from modules.common import Severity, ReportIssue
from modules.createExploit import ExploitType
from lib.pubsub import pub
from modules.common import terminalPrint

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

parser = plyj.Parser()
current_file=''
tree=''
importFound='False'

def main(queue):
	global current_file
	global parser
	global tree
	results = []
	count = 0

	common.logger.debug("Checking for any broadcasts sent from this app......")
	for j in common.java_files:
		count = count + 1
		pub.sendMessage('progress', bar="Broadcast issues", percent=round(count*100/common.java_files.__len__()))
		current_file=j
		try:
			tree=parser.parse_file(j)
			if type(tree) is not None:
				if hasattr(tree,'type_declarations'):
					for type_decl in tree.type_declarations:
						if type(type_decl) is m.ClassDeclaration:
							for t in type_decl.body:
								try:
									recursive_broadcast_finder(t,results)
								except Exception as e:
									common.parsingerrors.add(str(j))
									common.logger.debug("Unable to process recursive_broadcast_finder in findBroadcasts.py: " + str(e))
						elif type(type_decl) is list:
							for y in type_decl:
								recursive_broadcast_finder(y,results)
						elif hasattr(type_decl,'_fields'):
							for d in type_decl._fields:
								recursive_broadcast_finder(getattr(type_decl,d),results)
			else:								
				common.logger.debug("Unable to create tree for " + str(j))
		except Exception as e:
			common.logger.debug("Tree exception during broadcast processing: " + str(e))
			common.parsingerrors.add(str(j))
	queue.put(results)
	return

def local_broadcast_manager_imported():
	'''
	Need to ensure sendBroadcast is not the method from LocalBroadcastManager, which is not insecure
	'''
	#To be thorough,we need to run through the whole import dance, but we'll save that for planned refactor
	#This will have to do for now

	global tree
	global importFound

	for imp_decl in tree.import_declarations:
		if str(imp_decl.name.value)=="android.support.v4.content.LocalBroadcastManager":
			importFound=True
		elif str(imp_decl.name.value)=="android.support.v4.content.*":
			importFound=True
		elif str(imp_decl.name.value)=="android.support.v4.*":
			importFound=True
		elif str(imp_decl.name.value)=="android.support.*":
			importFound=True
		elif str(imp_decl.name.value)=="android.*":
			importFound=True
	return importFound


def recursive_broadcast_finder(t,results):

	if type(t) is m.MethodDeclaration:
		if str(t.name) == 'sendBroadcast':
			common.logger.debug("It appears the sendBroadcast method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendBroadcastAsUser':
			common.logger.debug("It appears the sendBroadcastAsUser method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendOrderedBroadcast':
			common.logger.debug("It appears the sendOrderedBroadcast method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendOrderedBroadcastAsUser':
			common.logger.debug("It appears the sendOrderedBroadcastAsUser method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendStickyBroadcast':
			common.logger.debug("It appears the sendStickyBroadcast method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendStickyBroadcastAsUser':
			common.logger.debug("It appears the sendStickyBroadcastAsUser method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendStickyOrderedBroadcast':
			common.logger.debug("It appears the sendStickyOrderedBroadcast method may be overridden in this class. The following findings for this class may be false positives")
		if str(t.name) == 'sendStickyOrderedBroadcastAsUser':
			common.logger.debug("It appears the sendStickyOrderedBroadcastAsUser method may be overridden in this class. The following findings for this class may be false positives")
	if type(t) is m.MethodInvocation:
		if str(t.name) == 'sendBroadcast':
			if len(t.arguments)==1:
				#We need to ensure this isn't a local broadcast
				#TODO - There is a lot more we need to do to fully qualify this, but should be good enough for now
				if local_broadcast_manager_imported()==True:
					common.logger.debug(tree)
				else:
					report.write_badger("manifest-issues", modules.common.Severity.INFO, "NO IMPORT")
					common.logger.debug("FOUND A sendBroadcast")
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("A broadcast is sent from this class: " + str(current_file) + ", which does not specify the receiverPermission. This means any application on the device can receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("A broadcast is sent from this class: " + str(current_file) + ", which does not specify the receiverPermission. This means any application on the device can receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)

			elif len(t.arguments)==2:
				if common.minSdkVersion<21:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("A broadcast is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("A broadcast is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)
				else:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("A broadcast is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("A broadcast is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					results.append(issue)
		elif str(t.name) == 'sendBroadcastAsUser':
			if len(t.arguments)==2:
				issue = ReportIssue()
				issue.setCategory(ExploitType.BROADCAST_INTENT)
				issue.setDetails("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which does not specify the receiverPermission. This means any application on the device can receive this broadcast. You should investigate this for potential data leakage.")
				issue.setFile(str(current_file))
				issue.setSeverity(Severity.WARNING)
				results.append(issue)

				issue = terminalPrint()
				issue.setLevel(Severity.WARNING)
				issue.setData("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which does not specify the receiverPermission. This means any application on the device can receive this broadcast. You should investigate this for potential data leakage.")
				results.append(issue)
			elif len(t.arguments)==3:
				if common.minSdkVersion<21:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)
				else:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("A broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					results.append(issue)
		elif str(t.name) == 'sendOrderedBroadcast':
			if ((len(t.arguments)==2) or (len(t.arguments)==7)):
				if common.minSdkVersion<21:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)
				else:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)
		elif str(t.name) == 'sendOrderedBroadcastAsUser':
			if len(t.arguments)==7:
				if common.minSdkVersion<21:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device can potentially receive this broadcast. You should investigate this for potential data leakage.")
					results.append(issue)
				else:
					issue = ReportIssue()
					issue.setCategory(ExploitType.BROADCAST_INTENT)
					issue.setDetails("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					issue.setFile(str(current_file))
					issue.setSeverity(Severity.WARNING)
					results.append(issue)

					issue = terminalPrint()
					issue.setLevel(Severity.WARNING)
					issue.setData("An ordered broadcast, as a specific user, is sent from this class: " + str(current_file) + ", which specifies the receiverPermission, but depending on the protection level of the permission (on the receiving app side), may still be vulnerable to interception, if the protection level of the permission is not set to signature or signatureOrSystem. You should investigate this for potential data leakage.")
					results.append(issue)
		elif str(t.name) == 'sendStickyBroadcast':
			issue = ReportIssue()
			issue.setCategory(ExploitType.BROADCAST_INTENT)
			issue.setDetails("A sticky broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			issue.setFile(str(current_file))
			issue.setSeverity(Severity.VULNERABILITY)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData("A sticky broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			results.append(issue)
		elif str(t.name) == 'sendStickyBroadcastAsUser':
			issue = ReportIssue()
			issue.setCategory(ExploitType.BROADCAST_INTENT)
			issue.setDetails("A sticky user broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			issue.setFile(str(current_file))
			issue.setSeverity(Severity.VULNERABILITY)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData("A sticky user broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			results.append(issue)
		elif str(t.name) == 'sendStickyOrderedBroadcast':
			issue = ReportIssue()
			issue.setCategory(ExploitType.BROADCAST_INTENT)
			issue.setDetails("A sticky ordered broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			issue.setFile(str(current_file))
			issue.setSeverity(Severity.VULNERABILITY)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData("A sticky ordered broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			results.append(issue)
		elif str(t.name) == 'sendStickyOrderedBroadcastAsUser':
			issue = ReportIssue()
			issue.setCategory(ExploitType.BROADCAST_INTENT)
			issue.setDetails("A sticky ordered user broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			issue.setFile(str(current_file))
			issue.setSeverity(Severity.VULNERABILITY)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData("A sticky ordered user broadcast is sent from this class: " + str(current_file) + ". These should not be used, as they provide no security (anyone can access them), no protection (anyone can modify them), and many other problems. For more info: http://developer.android.com/reference/android/content/Context.html")
			results.append(issue)
		elif hasattr(t,'_fields'):
			for g in t._fields:
				recursive_broadcast_finder(getattr(t,g),results)
	elif type(t) is list:
		for l in t:
			recursive_broadcast_finder(l,results)
	elif hasattr(t,'_fields'):
		for f in t._fields:
			if type(getattr(t,f)) is not str:
				recursive_broadcast_finder(getattr(t,f),results)
	return
