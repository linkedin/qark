from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import re

from modules import common
from modules import findExtras
from modules import report

def show_adb_commands(component,compType,packageName):
	#Print ADB commands for exploitation
	cmd_list=[]
	cmd_list.append([])
	#BUG - THIS PRINTS DUPS
	extra_parameters=[]
	extra_parameters.append('[-e|--es <EXTRA_KEY> <EXTRA_STRING_VALUE> ...]')
	extra_parameters.append('[--esn <EXTRA_KEY> ...]')
	extra_parameters.append('[--ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE> ...]')
	extra_parameters.append('[--ei <EXTRA_KEY> <EXTRA_INT_VALUE> ...]')
	extra_parameters.append('[--el <EXTRA_KEY> <EXTRA_LONG_VALUE> ...]')
	extra_parameters.append('[--ef <EXTRA_KEY> <EXTRA_FLOAT_VALUE> ...]')
	extra_parameters.append('[--eu <EXTRA_KEY> <EXTRA_URI_VALUE> ...]')
	extra_parameters.append('[--ecn <EXTRA_KEY> <EXTRA_COMPONENT_NAME_VALUE>]')
	extra_parameters.append('[--eia <EXTRA_KEY> <EXTRA_INT_VALUE>[,<EXTRA_INT_VALUE...]]')
	extra_parameters.append('[--ela <EXTRA_KEY> <EXTRA_LONG_VALUE>[,<EXTRA_LONG_VALUE...]]')
	extra_parameters.append('[--efa <EXTRA_KEY> <EXTRA_FLOAT_VALUE>[,<EXTRA_FLOAT_VALUE...]]')
	extra_parameters.append('[--esa <EXTRA_KEY> <EXTRA_STRING_VALUE>[,<EXTRA_STRING_VALUE...]]')

	type_list=['String','StringArray','StringArrayList','Boolean','BooleanArray','Int','Float','Long','LongArray','[]','','IntArray','IntegerArrayList','FloatArray','Double','Char','CharArray','CharSequence','CharSequenceArray','CharSequenceArrayList','Byte','ByteArray', 'Bundle','Short','ShortArray','Serializable','Parcelable','ParcelableArrayList','ParcelableArray','unknownType']

	#TODO - Need to add 
	#TODO - -d for data uri
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
							extras_list.append([])
							entries=common.get_entry_for_component('activity')
							output=False
							for n in entries:
								tmp_extra=findExtras.find_extras(str(c[1]),n)
								if tmp_extra not in extras_list:
									extras_list+=tmp_extra
							if len(extras_list)>2:
								for t in range(1,(len(extras_list)-1)):
									if str(extras_list[t]) not in type_list:
										if re.match(r'^\..*',str(c[1])):
											baseIntent =  "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+packageName+str(c[1])+"\""
										else:
											baseIntent =  "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+str(c[1])+"\""
										simple_type=True
										if extras_list[t+1]=='String':
											baseIntent+=" --es "
										elif extras_list[t+1]=='Boolean':
											baseIntent+=" --ez "
										elif extras_list[t+1]=='Int':
											baseIntent+=" --ei "
										elif extras_list[t+1]=='Long':
											baseIntent+=" --el "
										elif extras_list[t+1]=='Float':
											baseIntent+=" --ef "
										else:
											simple_type=False

										if simple_type:
											extra_type=str(extras_list[t+1])
											print baseIntent+"\""+str(extras_list[t])+"\" \"Insert"+extra_type+"Here\""
											output=True
											#TODO, Need to think of a better way to do this
											#This is excluding all the known types, because every second element is type
										elif str(extras_list[t]) not in type_list:
											common.logger.info("Extra: " + str(extras_list[t])+" is not a simple type, or could not be determined. You'll need to append the parameter which corresponds with the correct data type, followed by a key and value, both in quotes.")
											print "Example: "+baseIntent+str(" --es \"YOURKEYHERE\" \"YOURVALUEHERE\"")
											print "Here are your options for different data types: "
											for x in extra_parameters:
												print str(x)
											print "\n"
											output=True
										report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "activity")
								extras_list=[]
							if not output:
								if re.match(r'^\..*',str(c[1])):
									baseIntent =  "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+packageName+str(c[1])+"\""
								else:
									baseIntent =  "adb shell am start -a \"" + c[0] + "\" -n \""+packageName+"/"+str(c[1])+"\""
								print baseIntent
				else:
					common.logger.debug("No intent filter on:  " + str(component))
					extras_list=[]
					entries=common.get_entry_for_component('activity')
					output=False
					last_extra=''
					for n in entries:
						tmp_extra=findExtras.find_extras(str(component),n)
						if tmp_extra not in extras_list:
							if str(tmp_extra)!=str(last_extra):
								extras_list+=tmp_extra
								last_extra=str(tmp_extra)
					if len(extras_list)>0:
						for t in range(1,(len(extras_list)-1)):
							if str(extras_list[t]) not in type_list:
								if re.match(r'^\..*',str(component)):
									baseIntent =  "adb shell am start -n \""+packageName+"/"+packageName+str(component)+"\""
								else:
									baseIntent =  "adb shell am start -n \""+packageName+"/"+str(component)+"\""
								simple_type=True
								if extras_list[t+1]=='String':
									baseIntent+=" --es "
								elif extras_list[t+1]=='Boolean':
									baseIntent+=" --ez "
								elif extras_list[t+1]=='Int':
									baseIntent+=" --ei "
								elif extras_list[t+1]=='Long':
									baseIntent+=" --el "
								elif extras_list[t+1]=='Float':
									baseIntent+=" --ef "
								elif extras_list[t+1]=='Uri':
									baseIntent+=" -d "
								else:
									simple_type=False

								if simple_type:
									extra_type=str(extras_list[t+1])
									print baseIntent+str(extras_list[t])+" \"Insert"+extra_type+"Here\""
									output=True
									#TODO, Need to think of a better way to do this
									#This is excluding all the known types, because every second element is type
								elif str(extras_list[t]) not in type_list:
									common.logger.info("Extra: " + str(extras_list[t])+" is not a simple type, or could not be determined. You'll need to append the parameter which corresponds with the correct data type, followed by a key and value, both in quotes.")
									print "Example: "+baseIntent+str(" --es \"YOURKEYHERE\" \"YOURVALUEHERE\"")
									print "Here are your options for different data types: "
									for x in extra_parameters:
										print str(x)
									print "\n"
									ouput=True
								report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "activity")
						extras_list=[]
					if not output:
						if re.match(r'^\..*',str(component)):
							baseIntent =  "adb shell am start -n \""+packageName+"/"+packageName+str(component)+"\""
						else:
							baseIntent =  "adb shell am start -n \""+packageName+"/"+str(component)+"\""
						print baseIntent

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
							output=False
							extras_list=[]
							entries=common.get_entry_for_component('service')
							for n in entries:
								tmp_extra=findExtras.find_extras(str(c[1]),n)
								if tmp_extra not in extras_list:
									extras_list+=tmp_extra
							if len(extras_list)>0:
								for t in range(1,(len(extras_list)-1)):
									if str(extras_list[t]) not in type_list:
										if re.match(r'^\..*',str(c[1])):
											baseIntent =  "adb shell am startservice -n \"" +packageName+"/"+packageName+str(c[1])+"\""+" -a \""+str(c[0])+"\""
										else:
											baseIntent =  "adb shell am startservice -n \"" +packageName+"/"+str(c[1])+"\""+" -a \""+str(c[0])+"\""
										simple_type=True
										if extras_list[t+1]=='String':
											baseIntent+=" --es "
										elif extras_list[t+1]=='Boolean':
											baseIntent+=" --ez "
										elif extras_list[t+1]=='Int':
											baseIntent+=" --ei "
										elif extras_list[t+1]=='Long':
											baseIntent+=" --el "
										elif extras_list[t+1]=='Float':
											baseIntent+=" --ef "
										elif extras_list[t+1]=='Uri':
											baseIntent+=" -d "
										else:
											simple_type=False

										if simple_type:
											extra_type=str(extras_list[t+1])
											print baseIntent+str(extras_list[t])+" \"Insert"+extra_type+"Here\""
											output=True
											#TODO, Need to think of a better way to do this
											#This is excluding all the known types, because every second element is type
										elif str(extras_list[t]) not in type_list:
											common.logger.info("Extra: " + str(extras_list[t])+" is not a simple type, or could not be determined. You'll need to append the parameter which corresponds with the correct data type, followed by a key and value, both in quotes.")
											print "Example: "+baseIntent+str(" --es \"YOURKEYHERE\" \"YOURVALUEHERE\"")
											print "Here are your options for different data types: "
											for x in extra_parameters:
												print str(x)
											print "\n"
											output=True
										report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "service")
								extras_list=[]
							if not output:
								if re.match(r'^\..*',str(c[1])):
									baseIntent =  "adb shell am startservice -n \"" +packageName+"/"+packageName+str(c[1])+"\""
								else:	
									baseIntent =  "adb shell am startservice -n \"" +packageName+"/"+str(c[1])+"\""
								print baseIntent
								report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "service")

	elif str(compType)=='receiver':
		for node in common.xmldoc.getElementsByTagName('receiver'):
			if node.attributes['android:name'].value==component:
				if len(node.getElementsByTagName('intent-filter'))>0:
					for x in node.getElementsByTagName('intent-filter'):
						for a in node.getElementsByTagName('action'):
							cmd_list.append([a.attributes['android:name'].value,component])
						try:
							cmd_list=common.dedup(cmd_list)
						except Exception as e:
							common.logger.error("Error de-duplicating command list in adb.py while processing receivers: " + str(e))
						for c in cmd_list:
							if len(c)>0:
								output=False
								extras_list=[]
								try:
									entries=common.get_entry_for_component('receiver')
								except Exception as e:
									common.logger.error("Error getting entry point for receivers in adb.py: " + str(e) )
								for n in entries:
									try:
										tmp_extra=findExtras.find_extras(str(c[1]),n)
									except Exception as e:
										common.logger.error("Error finding extras for receivers in adb.py: " + str(e))
									if tmp_extra not in extras_list:
										extras_list+=tmp_extra
								if len(extras_list)>0:
									for t in range(1,(len(extras_list)-1)):
										if str(extras_list[t]) not in type_list:
											baseIntent="adb shell am broadcast -a \""+str(c[0])+"\""
											simple_type=True
											if extras_list[t+1]=='String':
												baseIntent+=" --es "
											elif extras_list[t+1]=='Boolean':
												baseIntent+=" --ez "
											elif extras_list[t+1]=='Int':
												baseIntent+=" --ei "
											elif extras_list[t+1]=='Long':
												baseIntent+=" --el "
											elif extras_list[t+1]=='Float':
												baseIntent+=" --ef "
											elif extras_list[t+1]=='Uri':
												baseIntent+=" -d "
											else:
												simple_type=False
											if simple_type:
												extra_type=str(extras_list[t+1])
												print baseIntent+"\""+str(extras_list[t])+"\" \"Insert"+extra_type+"Here\""
												output=True
												#TODO, Need to think of a better way to do this
												#This is excluding all the known types, because every second element is type
											elif str(extras_list[t]) not in type_list:
												common.logger.info("Extra: " + str(extras_list[t])+" is not a simple type, or could not be determined. You'll need to append the parameter which corresponds with the correct data type, followed by a key and value, both in quotes.")
												print "Example: "+baseIntent+str(" --es \"YOURKEYHERE\" \"YOURVALUEHERE\"")
												print "Here are your options for different data types: "
												for x in extra_parameters:
													print str(x)
												print "\n"
												output=True
											report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "receiver")
								extras_list=[]
								if not output:
									baseIntent = "adb shell am broadcast -a \""+str(c[0])+"\""
									print baseIntent
									report.write_adb_commands("adbcommands-issues-list", common.Severity.VULNERABILITY, baseIntent, None, "receiver")

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
