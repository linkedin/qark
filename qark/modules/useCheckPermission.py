from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

from modules import common

def use_check_permission():
	common.logger.info("Sorry, we haven't completed the check for use_check_permission yet. Check for updates soon.")
	'''
	From Android Lint:

		UseCheckPermission
	------------------
	Summary: Using the result of check permission calls

	Priority: 6 / 10
	Severity: Warning
	Category: Security

	You normally want to use the result of checking a permission; these methods
	return whether the permission is held; they do not throw an error if the
	permission is not granted. Code which does not do anything with the return
	value probably meant to be calling the enforce methods instead, e.g. rather
	than Context#checkCallingPermission it should call
	Context#enforceCallingPermission.
	'''
	return
