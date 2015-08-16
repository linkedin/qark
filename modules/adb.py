'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

from modules import common,intents,report
import re

def showAdbCommands(component,compType,packageName):
	#Print ADB commands for exploitation
	cmd_list=[]
	cmd_list.append([])
	#BUG - THIS PRINTS DUPS
	#TODO - re-implement the extras, just want to make sure it looks good first
	#suggest_extras=raw_input("Would you like us to suggest extras to add? (y/n) ")
	if str(compType)=='activity':
		for node in common.xmldoc.getElementsByTagName('activity'):
			if node.attributes['android:name'].value == component:
				if len(node.getElementsByTagName('intent-filter'))>0:
					for x in node.getElementsByTagName('intent-filter'):
						for a in node.getElementsByTagName('action'):
							cmd_list.append([a.attributes['android:name'].value,component])
						cmd_list=common.dedup(cmd_list)
					for c in cmd_list:
						if len(c)>0:
						#find extra suggestions for the intents in c[1], if any
							extras_list=[]
							extras_list+=intents.find_extras(str(c[1]),common.sourceDirectory)
							if len(extras_list)>0:
								for t in extras_list:
									if re.match(r'^\..*',str(c[1])):
										command = "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+packageName+str(c[1])+"\""+" --es "+str(t)+" \"EXTRA_VALUE_IN_QUOTES\""
									else:
										command = "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+str(c[1])+"\""+" --es "+str(t)+" \"EXTRA_VALUE_IN_QUOTES\""
									print command
									report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "activity")
							else:
								if re.match(r'^\..*',str(c[1])):
									command = "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+packageName+str(c[1])+"\""
								else:
									command = "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+str(c[1])+"\""
								print command
								report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "activity")
				else:
					common.logger.debug("No intent filter on:  " + str(component))
					extras_list=[]
					extras_list+=intents.find_extras(str(component),common.sourceDirectory)
					if len(extras_list)>0:
						if re.match(r'^\..*',str(component)):
							command =  "adb shell am start -n \""+packageName+"/"+packageName+component+"\""
						else:
							command =  "adb shell am start -n \""+packageName+"/"+component+"\""
						print command
						extras = []
						for e in extras_list:
							extras.append("Possible extras to send: " + str(e))
							print "Possible extras to send: " + str(e)
						report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, extras, "activity")
					else:
						if re.match(r'^\..*',str(component)):
							command =  "adb shell am start -n \""+packageName+"/"+packageName+component+"\""
						else:
							command =  "adb shell am start -n \""+packageName+"/"+component+"\""
						print command
						report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "activity")
	elif str(compType)=='service':
		#BUG - THIS PRINTS DUPS without the below
		for node in common.xmldoc.getElementsByTagName('service'):
			if node.attributes['android:name'].value == component:
				if len(node.getElementsByTagName('intent-filter'))>0:
					for x in node.getElementsByTagName('intent-filter'):
						for a in node.getElementsByTagName('action'):
							cmd_list.append([a.attributes['android:name'].value,component])
						cmd_list=common.dedup(cmd_list)
					for c in cmd_list:
						if len(c)>0:
							extras_list=[]
							extras_list+=intents.find_extras(str(c[1]),common.sourceDirectory)
							if len(extras_list)>0:
								for t in extras_list:
									if re.match(r'^\..*',str(c[1])):
										command =  "adb shell am startservice " +packageName+"/"+packageName+str(c[1])+" --es "+str(t)
									else:
										command =  "adb shell am startservice " +packageName+"/"+str(c[1])+" --es "+str(t)
									print command
									report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "service")
							else:
								if re.match(r'^\..*',str(c[1])):
									command =  "adb shell am startservice " +packageName+"/"+packageName+str(c[1])
								else:	
									command =  "adb shell am startservice " +packageName+"/"+str(c[1])
								print command
								report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "service")
	elif str(compType)=='receiver':
		for node in common.xmldoc.getElementsByTagName('receiver'):
			if node.attributes['android:name'].value==component:
				for x in node.getElementsByTagName('intent-filter'):
					for a in node.getElementsByTagName('action'):
						cmd_list.append([a.attributes['android:name'].value,component])
					cmd_list=common.dedup(cmd_list)
					for c in cmd_list:
						if len(c)>0:
							extras_list=[]
							extras_list+=intents.find_extras(str(c[1]),common.sourceDirectory)
							if len(extras_list)>0:
								for t in extras_list:
									baseIntent="adb shell am broadcast -a \""+str(c[0])+"\""
									print "Possible Extra: " + str(t)
									baseIntent+=" --es "+str(t)+" \"YOURDATAHERE\""
									print baseIntent
									report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "receiver")

									common.logger.info("Sorry, the dynamic extra suggestions is still a work in progress. In the mean time, know that the --es flag is used for sending key/value pairs which are strings.")
									common.logger.info("If the suggested extra does not appear quoted, it is either a CONSTANT or String variable, it should not be used literally as shown")
							else:
								command = "adb shell am broadcast -a \""+str(c[0])+"\""
								print command
								report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, command, None, "receiver")

	elif str(compType)=='provider':
		for node in common.xmldoc.getElementsByTagName('provider'):
			if node.attributes['android:name'].value == component:
				print "TO INSERT DATA:"
				print "adb shell content insert --uri <URI> [--user <USER_ID>] --bind <BINDING> [--bind <BINDING>...]"
				print "TO UPDATE DATA:"
				print "adb shell content update --uri <URI> [--user <USER_ID>] [--where <WHERE>]"
				print "TO DELETE DATA:"
				print "adb shell content delete --uri <URI> [--user <USER_ID>] --bind <BINDING> [--bind <BINDING>...]" \
					  "[--where <WHERE>]"
				print "TO QUERY DATA: "
				print "adb shell content query --uri <URI> [--user <USER_ID>] [--projection <PROJECTION>]" \
					  "[--where <WHERE>] [--sort <SORT_ORDER>]"
				print "TO CALL THE PROVIDER DIRECTLY"
				print "adb shell content call --uri <URI> --method <METHOD> [--arg <ARG>]"
	return