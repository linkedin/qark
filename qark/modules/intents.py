from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''
from genericpath import isdir

import zipfile
import os
import subprocess
import logging
import shlex
import re

import modules.common

#find Intent Extras
def find_extras(stub_file_name,path):
	"""
	Find all extras given a filename
	"""
	#TODO - This needs to be gutted and re-writtten
	extras=[]
	filename=re.search(r'\w+$',stub_file_name)
	filename=filename.group()
	fname=common.grep(path,r''+str(filename)+'\.java')
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
	if len(fname)>0:
		x_tmp=[]
		x_tmp.append([])
		for r in rextras:
			x_tmp=common.text_scan(fname,r)
			for m in x_tmp:
				if len(m)>0:
					i=0
					for l in m:
						if type(l) is list:
							sigh=[]
							for s in l:
								sigh.append(re.sub(r'.*\(','',str(s)))
								sigh[i]=re.sub(r'\).*','',sigh[i])
								sigh[i]=re.sub(r'\s*,.*','',sigh[i])
								extras+=sigh
								i+=1
				extras=common.dedup(extras)
		if len(extras)<1:
			common.logger.debug("No extras found in " + str(fname[0]) + " to suggest.\n")
			common.parsingerrors.add(str(fname[0]))
	else:
		#BUG - seems like a flow can come here without the fname; Ex: Flagship S - 4
		common.logger.error("Sorry, we could not find a filename while looking for extras\n")
	#Trying to get rid of empty first element
	return extras
