from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import logging

from modules import report
from modules import common
from modules.IssueType import IssueType, IssueSeverity
from modules.report import ReportIssue
from modules.common import Severity, ReportIssue
from modules.createExploit import ExploitType
from lib.progressbar import *
from lib.pubsub import pub
from modules.common import terminalPrint

def start(queue,height):
	results = []
	count = 0
	#TODO - add check for getSharedPreferences specifically, to run before these more generalized ones
	#Check for world readable files
	file_wr=r'MODE_WORLD_READABLE'
	for i in text_scan(common.java_files,file_wr):
		if len(i)>0:
			report.write(IssueType.FileSystem, IssueSeverity.High, common.config.get('qarkhelper', 'WR_FILE') + str(i[0])
			+"<br>" + str(i[1]))
			issue = ReportIssue()
			issue.setCategory(ExploitType.PERMISSION)
			issue.setDetails(common.config.get('qarkhelper', 'WR_FILE') + str(i[0]) + str(i[1]))
			issue.setFile(str(i[1]))
			issue.setSeverity(Severity.WARNING)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.WARNING)
			issue.setData(common.config.get('qarkhelper', 'WR_FILE') + str(i[0]) + str(i[1]))
			results.append(issue)
	#Check for world writable files

	file_ww=r'MODE_WORLD_WRITEABLE'
	for i in text_scan(common.java_files,file_ww):
		if len(i)>0:
			report.write(IssueType.FileSystem, IssueSeverity.High, common.config.get('qarkhelper', 'WW_FILE') + str(i[0])
			+"<br>" + str(i[1]))
			issue = ReportIssue()
			issue.setCategory(ExploitType.PERMISSION)
			issue.setDetails(common.config.get('qarkhelper', 'WW_FILE') + str(i[0]) + " in file: " + str(i[1]))
			issue.setFile(str(i[1]))
			issue.setSeverity(Severity.WARNING)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.WARNING)
			issue.setData(common.config.get('qarkhelper', 'WW_FILE') + str(i[0]) + " in file: " + str(i[1]))
			results.append(issue)
	queue.put(results)
	'''
	More checks from Android Lint to implement

	WorldReadableFiles
	------------------
	Summary: openFileOutput() call passing MODE_WORLD_READABLE

	Priority: 4 / 10
	Severity: Warning
	Category: Security

	There are cases where it is appropriate for an application to write world
	readable files, but these should be reviewed carefully to ensure that they
	contain no private data that is leaked to other applications.


	WorldWriteableFiles
	-------------------
	Summary: openFileOutput() call passing MODE_WORLD_WRITEABLE

	Priority: 4 / 10
	Severity: Warning
	Category: Security

	There are cases where it is appropriate for an application to write world
	writeable files, but these should be reviewed carefully to ensure that they
	contain no private data, and that if the file is modified by a malicious
	application it does not trick or compromise your application.
	'''
	return

#look for text
def text_scan(file_list,rex_n):
	"""
	Given a list of files, search content of each file by the regular expression and return a list of matches
	"""
	count = 0
	result_list=[]
	result_list.append([])
	for x in file_list:
		count = count + 1
		#pbar.update(round(count*100/common.java_files.__len__()))
		pub.sendMessage('progress', bar='File Permissions', percent=round(count*100/common.java_files.__len__()))
		result=common.read_files(x,rex_n)
		if len(result)>0:
			result_list.append([result,x])
	return result_list
