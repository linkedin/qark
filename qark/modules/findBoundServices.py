from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import lib.plyj.parser as plyj
import lib.plyj.model as m
from modules import common

def main(t,tree):
	for b in t.body:
		if type(b) is m.Return:
			if hasattr(b,'result'):
				if type(b.result) is m.MethodInvocation:
					print "b.result: " + str(b.result)
					if hasattr(b.result,'name'):
						print "b.result.name: " + str(b.result.name)
						if b.result.name=='getIBinder':
							if hasattr(b.result,'target'):
								print "b.result.target: " + str(b.result.target)
								if hasattr(b.result.target,'value'):
									print "b.result.target.value: " + str(b.result.target.value)
									targetName=b.result.target.value
									print "B Target: " + str(b.result.target)
									raw_input()
									what_is_this(targetName,tree)
				elif type(b.result) is list:
					for l in b.result:
						if type(l) is m.MethodInvocation:
							if hasattr(l,'result'):
								if hasattr(l.result,'name'):
									if l.result.name=='getIBinder':
										if hasattr(l.result,'target'):
											if hasattr(l.result.target,'value'):
												targetName=l.result.target.value
												print "L Target: " + str(l.result.target)
												raw_input()
												what_is_this(targetName,tree)
				elif hasattr(b.result,'_fields'):
					for f in b.result._fields:
						if type(f) is m.MethodInvocation:
							if hasattr(f,'result'):
								if hasattr(f.result,'name'):
									if f.result.name=='getIBinder':
										print "Found a nested one: " + str(f)
										if hasattr(f.result,'target'):
											print "F Target: " + str(f.result.target)
											if hasattr(f.result.target,'value'):
												targetName=f.result.target.value
												what_is_this(targetName,tree)
												raw_input()
	return

def what_is_this(targetName,tree):
	for x in tree.body:
		if type(x) is m.VariableDeclaration:
			print "X: " + str(x)
			raw_input()
		else:
			print "TREE: " + str(tree)
	return
