from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re
from modules import common

def find_intent_files():
	"""
	Find all files declaring or using intents in the application
	"""
	common.logger.info("Attempting to trace Intent Sources to Sinks")
	int_files=[]
	int_dec_list=[]
	int_dec_list.append([])
	int_rex=r'import\sandroid\.content\.Intent'
	#This syntax is deprecated
	int_assign_rex1=r'Intent\s*[A-Za-z0-9_$]+\s*[=;]\s+getIntent\('
	int_assign_rex2=r'[A-Za-z0-9_$]+\s*[=;]\s*Intent\.parseUri\('
	int_assign_rex3=r'Intent\s*[A-Za-z0-9_$]+\s*[=;]\s*new\s+Intent\('
	int_files+=common.text_scan(common.java_files,int_rex)
	for i in int_files:
		if len(i)>0:
			tmp=[i[1]]
			int_dec_list+=common.text_scan(tmp,int_assign_rex1)
			int_dec_list+=common.text_scan(tmp,int_assign_rex2)
			int_dec_list+=common.text_scan(tmp,int_assign_rex3)
	common.logger.info("Intent Declarations:")
	int_dec_list=filter(None,int_dec_list)
	for d in int_dec_list:
		if len(d)>0:
			d[0]=re.sub(r'\s*[=;]\s*new\s*Intent\(.*','',str(d[0]))
			d[0]=re.sub(r'(final)?\s*Intent\s+','',str(d[0]))
			d[0]=re.sub(r'[=;]\s*getIntent\(.*','',str(d[0]))
			d[0]=re.sub(r'\'','',str(d[0]))
			d[0]=re.sub(r'\"','',str(d[0]))
			d[0]=re.sub(r'\s+','',str(d[0]))
			d[0]=re.sub(r'\[','',str(d[0]))
			d[0]=re.sub(r'\\\\\t','',str(d[0]))
			d[0]=re.sub(r'\\\t','',str(d[0]))
			d[0]=re.sub(r'\\t','',str(d[0]))
			d[0]=str(d[0]).strip('\t\n\r')
	common.logger.info(int_dec_list)
	return

def ext_intents():

	return
