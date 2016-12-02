from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, 
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

"""
Module for common functions and common variables that are then used elsewhere in the code
"""
import fileinput
import os
import re
import sys
import pprint
import ConfigParser
import logging
from collections import defaultdict
import glob
import subprocess

from xml.dom import minidom
from modules.IssueType import IssueType, IssueSeverity
from lib import colorama
from lib.blessed import *
from modules.createExploit import ExploitType


VULNERABILITY_LEVEL = 60
logging.addLevelName(VULNERABILITY_LEVEL, "POTENTIAL VULNERABILITY")

HEADER_ISSUES_LEVEL = 55
logging.addLevelName(HEADER_ISSUES_LEVEL, "ISSUES")

exploitdata = defaultdict(list)
logger = logging.getLogger()
sploitparams=defaultdict(list)

#Define common variables here
args = []
xmldoc = minidom.parseString('<myxml>initialize</myxml>')
targetSdkVersion = 1
sdk = xmldoc.getElementsByTagName("uses-sdk")
pathToDEX = ""
pathToJar = ""
pathToUnpackedAPK = ""
manifestName = "AndroidManifest.xml"
apkPath = ""
pathToManifest = ""
config = ConfigParser.RawConfigParser()
script_location=os.path.dirname(__file__)
script_location+='/config.properties'
config.read(script_location)
manifest = ""
java_files = []
xml_files = []
keyFiles=[]
minSdkVersion = 1
rootDir = ""
reportDir = ""
interactive_mode = True
source_or_apk = 1
exploitLocation = ""
apkPathChoice = 0
apkList = []
aapt = ""
count = 0
counter0 = 0
counter1 = 0
counter2 = 0
badVerifiers = ['ALLOW_ALL_HOSTNAME_VERIFIER']
sourceDirectory=""
parsingerrors = set()
file_not_found=[]

#TODO - Double check this list against : https://android.googlesource.com/platform/frameworks/base/+/master/core/res/AndroidManifest.xml
#This is a list of broadcasts that only system apps should be able to send. If the attacker already has system level access, it's game over...
#TODO For readability, break this into multiple lines using \
#TODO - This pages lists system-only Intents: http://developer.android.com/reference/android/content/Intent.html, which all seem to be included in the list below, but when we're not lazy, we shoudl verify this and break them out
#TODO - Need to double check that we're checking for protected Intents in all the right places below
protected_broadcasts=['android.intent.action.SCREEN_OFF','android.intent.action.SCREEN_ON','android.intent.action.USER_PRESENT','android.intent.action.TIME_TICK','android.intent.action.TIMEZONE_CHANGED','android.intent.action.BOOT_COMPLETED','android.intent.action.PACKAGE_INSTALL','android.intent.action.PACKAGE_ADDED','android.intent.action.PACKAGE_REPLACED','android.intent.action.MY_PACKAGE_REPLACED','android.intent.action.PACKAGE_REMOVED','android.intent.action.PACKAGE_FULLY_REMOVED','android.intent.action.PACKAGE_CHANGED','android.intent.action.PACKAGE_RESTARTED','android.intent.action.PACKAGE_DATA_CLEARED','android.intent.action.PACKAGE_FIRST_LAUNCH','android.intent.action.PACKAGE_NEEDS_VERIFICATION','android.intent.action.PACKAGE_VERIFIED','android.intent.action.UID_REMOVED','android.intent.action.QUERY_PACKAGE_RESTART','android.intent.action.CONFIGURATION_CHANGED','android.intent.action.LOCALE_CHANGED','android.intent.action.BATTERY_CHANGED','android.intent.action.BATTERY_LOW','android.intent.action.BATTERY_OKAY','android.intent.action.ACTION_POWER_CONNECTED','android.intent.action.ACTION_POWER_DISCONNECTED','android.intent.action.ACTION_SHUTDOWN','android.intent.action.DEVICE_STORAGE_LOW','android.intent.action.DEVICE_STORAGE_OK','android.intent.action.DEVICE_STORAGE_FULL','android.intent.action.DEVICE_STORAGE_NOT_FULL','android.intent.action.NEW_OUTGOING_CALL','android.intent.action.REBOOT','android.intent.action.DOCK_EVENT','android.intent.action.MASTER_CLEAR_NOTIFICATION','android.intent.action.USER_ADDED','android.intent.action.USER_REMOVED','android.intent.action.USER_STOPPED','android.intent.action.USER_BACKGROUND','android.intent.action.USER_FOREGROUND','android.intent.action.USER_SWITCHED','android.app.action.ENTER_CAR_MODE','android.app.action.EXIT_CAR_MODE','android.app.action.ENTER_DESK_MODE','android.app.action.EXIT_DESK_MODE','android.appwidget.action.APPWIDGET_UPDATE_OPTIONS','android.appwidget.action.APPWIDGET_DELETED','android.appwidget.action.APPWIDGET_DISABLED','android.appwidget.action.APPWIDGET_ENABLED','android.backup.intent.RUN','android.backup.intent.CLEAR','android.backup.intent.INIT','android.bluetooth.adapter.action.STATE_CHANGED','android.bluetooth.adapter.action.SCAN_MODE_CHANGED','android.bluetooth.adapter.action.DISCOVERY_STARTED','android.bluetooth.adapter.action.DISCOVERY_FINISHED','android.bluetooth.adapter.action.LOCAL_NAME_CHANGED','android.bluetooth.adapter.action.CONNECTION_STATE_CHANGED','android.bluetooth.device.action.FOUND','android.bluetooth.device.action.DISAPPEARED','android.bluetooth.device.action.CLASS_CHANGED','android.bluetooth.device.action.ACL_CONNECTED','android.bluetooth.device.action.ACL_DISCONNECT_REQUESTED','android.bluetooth.device.action.ACL_DISCONNECTED','android.bluetooth.device.action.NAME_CHANGED','android.bluetooth.device.action.BOND_STATE_CHANGED','android.bluetooth.device.action.NAME_FAILED','android.bluetooth.device.action.PAIRING_REQUEST','android.bluetooth.device.action.PAIRING_CANCEL','android.bluetooth.device.action.CONNECTION_ACCESS_REPLY','android.bluetooth.headset.profile.action.CONNECTION_STATE_CHANGED','android.bluetooth.headset.profile.action.AUDIO_STATE_CHANGED','android.bluetooth.headset.action.VENDOR_SPECIFIC_HEADSET_EVENT','android.bluetooth.a2dp.profile.action.CONNECTION_STATE_CHANGED','android.bluetooth.a2dp.profile.action.PLAYING_STATE_CHANGED','android.bluetooth.input.profile.action.CONNECTION_STATE_CHANGED','android.bluetooth.pan.profile.action.CONNECTION_STATE_CHANGED','android.hardware.display.action.WIFI_DISPLAY_STATUS_CHANGED','android.hardware.usb.action.USB_STATE','android.hardware.usb.action.USB_ACCESSORY_ATTACHED','android.hardware.usb.action.USB_ACCESSORY_ATTACHED','android.hardware.usb.action.USB_DEVICE_ATTACHED','android.hardware.usb.action.USB_DEVICE_DETACHED','android.intent.action.HEADSET_PLUG','android.intent.action.ANALOG_AUDIO_DOCK_PLUG','android.intent.action.DIGITAL_AUDIO_DOCK_PLUG','android.intent.action.HDMI_AUDIO_PLUG','android.intent.action.USB_AUDIO_ACCESSORY_PLUG','android.intent.action.USB_AUDIO_DEVICE_PLUG','android.net.conn.CONNECTIVITY_CHANGE','android.net.conn.CONNECTIVITY_CHANGE_IMMEDIATE','android.net.conn.DATA_ACTIVITY_CHANGE','android.net.conn.BACKGROUND_DATA_SETTING_CHANGED','android.net.conn.CAPTIVE_PORTAL_TEST_COMPLETED','android.nfc.action.LLCP_LINK_STATE_CHANGED','com.android.nfc_extras.action.RF_FIELD_ON_DETECTED','com.android.nfc_extras.action.RF_FIELD_OFF_DETECTED','com.android.nfc_extras.action.AID_SELECTED','android.nfc.action.TRANSACTION_DETECTED','android.intent.action.CLEAR_DNS_CACHE','android.intent.action.PROXY_CHANGE','android.os.UpdateLock.UPDATE_LOCK_CHANGED','android.intent.action.DREAMING_STARTED','android.intent.action.DREAMING_STOPPED','android.intent.action.ANY_DATA_STATE','com.android.server.WifiManager.action.START_SCAN','com.android.server.WifiManager.action.DELAYED_DRIVER_STOP','android.net.wifi.WIFI_STATE_CHANGED','android.net.wifi.WIFI_AP_STATE_CHANGED','android.net.wifi.WIFI_SCAN_AVAILABLE','android.net.wifi.SCAN_RESULTS','android.net.wifi.RSSI_CHANGED','android.net.wifi.STATE_CHANGE','android.net.wifi.LINK_CONFIGURATION_CHANGED','android.net.wifi.CONFIGURED_NETWORKS_CHANGE','android.net.wifi.supplicant.CONNECTION_CHANGE','android.net.wifi.supplicant.STATE_CHANGE','android.net.wifi.p2p.STATE_CHANGED','android.net.wifi.p2p.DISCOVERY_STATE_CHANGE','android.net.wifi.p2p.THIS_DEVICE_CHANGED','android.net.wifi.p2p.PEERS_CHANGED','android.net.wifi.p2p.CONNECTION_STATE_CHANGE','android.net.wifi.p2p.PERSISTENT_GROUPS_CHANGED','android.net.conn.TETHER_STATE_CHANGED','android.net.conn.INET_CONDITION_ACTION','android.intent.action.EXTERNAL_APPLICATIONS_AVAILABLE','android.intent.action.EXTERNAL_APPLICATIONS_UNAVAILABLE','android.intent.action.AIRPLANE_MODE','android.intent.action.ADVANCED_SETTINGS','android.intent.action.BUGREPORT_FINISHED','android.intent.action.ACTION_IDLE_MAINTENANCE_START','android.intent.action.ACTION_IDLE_MAINTENANCE_END','android.intent.action.SERVICE_STATE','android.intent.action.RADIO_TECHNOLOGY','android.intent.action.EMERGENCY_CALLBACK_MODE_CHANGED','android.intent.action.SIG_STR','android.intent.action.ANY_DATA_STATE','android.intent.action.DATA_CONNECTION_FAILED','android.intent.action.SIM_STATE_CHANGED','android.intent.action.NETWORK_SET_TIME','android.intent.action.NETWORK_SET_TIMEZONE','android.intent.action.ACTION_SHOW_NOTICE_ECM_BLOCK_OTHERS','android.intent.action.ACTION_MDN_STATE_CHANGED','android.provider.Telephony.SPN_STRINGS_UPDATED','android.provider.Telephony.SIM_FULL','com.android.internal.telephony.data-restart-trysetup','com.android.internal.telephony.data-stall']

'''
This is here specifically because we saw an issue with the import of html5lib in python on some machines
Better to have a scan and no html report, than no scan
'''
reportInitSuccess=True

term = Terminal()
height = 0

class terminalPrint():

	level = logging.INFO
	data = ""
	extra = {}

	def __init__(self):
		self.level = logging.INFO
		self.data = ""
		self.extra = {}

	def setLevel(self, level):
		self.level = level

	def getLevel(self):
		return self.level

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

	def getExtras(self):
		return self.extra

	def setExtras(self, key, value):
		self.extra[key] = value


def enterFullScreen():
	print term.enter_fullscreen
	print term.clear

def exitClean():
	print term.exit_fullscreen
	exit()

class Writer(object):
	"""Create an object with a write method that writes to a
	specific place on the screen, defined at instantiation.

	This is the glue between blessings and progressbar.
	"""
	def __init__(self, location):
		"""
		Input: location - tuple of ints (x, y), the position
						of the bar in the terminal
		"""
		self.location = location

	def write(self, string):
		with term.location(*self.location):
			print(string)

class ColorizingStreamHandler(logging.StreamHandler):
	color_map = {
		logging.DEBUG: colorama.Style.DIM + colorama.Fore.CYAN + colorama.Back.WHITE,
		logging.INFO: colorama.Style.DIM + colorama.Fore.BLUE + colorama.Style.BRIGHT,
		logging.WARNING: colorama.Fore.YELLOW + colorama.Style.BRIGHT,
		logging.ERROR: colorama.Fore.WHITE + colorama.Style.BRIGHT + colorama.Back.RED,
		logging.CRITICAL: colorama.Back.RED,
		60: colorama.Fore.RED + colorama.Style.BRIGHT,
		55: colorama.Fore.WHITE + colorama.Back.BLUE,
	}

	def __init__(self, stream, color_map=None):
		logging.StreamHandler.__init__(self,
									   colorama.AnsiToWin32(stream).stream)
		if color_map is not None:
			self.color_map = color_map

	@property
	def is_tty(self):
		isatty = getattr(self.stream, 'isatty', None)
		return isatty and isatty()

	def format(self, record):
		message = logging.StreamHandler.format(self, record)
		if self.is_tty:
			# Don't colorize a traceback
			parts = message.split('\n', 1)
			parts[0] = self.colorize(parts[0], record)
			message = '\n'.join(parts)
		return message

	def colorize(self, message, record):
		try:
			return (self.color_map[record.levelno] + message +
					colorama.Style.RESET_ALL)
		except KeyError:
			return message

def set_environment_variables():
	os.environ["PATH"] += os.pathsep + getConfig('AndroidSDKPath') + 'tools' + os.pathsep + getConfig(
		'AndroidSDKPath') + 'platform-tools' + os.pathsep + getConfig('AndroidSDKPath') + 'tools/lib'
	os.environ["ANDROID_HOME"] = getConfig('AndroidSDKPath')

def initialize_logger():
	logger.setLevel(logging.DEBUG)

	if not os.path.exists(rootDir + '/logs'):
		os.makedirs(rootDir + '/logs')

	# create console handler and set level to INFO
	handler = ColorizingStreamHandler(sys.stdout)
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# create error file handler and set level to INFO
	handler = logging.FileHandler(os.path.join(rootDir +"/logs/", "info.log"),"w", encoding=None, delay="true")
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(levelname)s - %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)


def readLayoutFiles(pathToLayout):
	aapt = glob.glob(getConfig("AndroidSDKPath")+ "build-tools/*/aapt*")
	process = subprocess.Popen([aapt[0], "dump", "xmltree", apkPath, pathToLayout], stdout=subprocess.PIPE)
	output, err = process.communicate()
	print output

def checkJavaVersion():
	process = subprocess.Popen(["java","-version"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	try:
		while True:
			line = process.stdout.readline()
			if not line:
				break
			if "java version" in line:
				majorversion = float(str(line).split(" ")[-1].replace('\"','')[0:3])
				if majorversion < 1.6:
					print "Old JRE detected. QARK requires JRE 6+ in order to run the decompilers correctly. You can still continue to scan source code"
				elif majorversion < 1.7:
					print "Procyon decompiler was not built with JRE 6 support. Decompilation results may not be optimal."
	except Exception as e:
		print "Old JRE detected. QARK requires JRE 6+ in order to run the decompilers correctly. You can still continue to scan source code"



def fcount(path):
	""" Counts the number of files in a directory """
	count = 0
	for f in os.listdir(path):
		if os.path.isfile(os.path.join(path, f)):
			count += 1

	return count

def getConfig(key):
	"""
	Function to retrieve a key
	"""
	value = ""
	for line in fileinput.input([rootDir + "/settings.properties"]):
		if key in line:
			value = line.split("=")[1]
			if "path" in str(key).lower():
				#If its a path, verify that it exists before returning the value
				value = value.rstrip()
				if value.endswith("/"):
					if not os.path.exists(value.rsplit("/",1)[0]):
						value= ""
				else:
					if not os.path.exists(value):
						value=""
			break
	fileinput.close()
	return value.rstrip()

def writeKey(key,value):
	"""
	Function to write a key to settings.properties\n
	If a value exists, this will overwrite the key
	"""
	flag=0
	for line in fileinput.input([rootDir +"/settings.properties"], inplace=True):
		if key in line:
			print line.replace(line, key + "=" + value)
			flag=1
		else:
			print line,
	if flag==0:
		fileinput.close()
		f = open(rootDir + "/settings.properties","a")
		f.write("\n" + key + "=" + value),
		print "Updated config value:: %s %s" %(key,value)
		f.close()


# Will return file names matching regex
def grep(path, regex):
	"""
	Standard wrapper around grep. Searches the contents of a file given a regular expression and returns a list of results
	"""
	regObj = re.compile(regex)
	res = []
	for root, dirs, fnames in os.walk(path):
		for fname in fnames:
			if regObj.match(fname):
				res.append(os.path.join(root,fname))
	return res

def find_java(path):
	"""
	Given an absolute path, find  and return all java files in a list

	"""
	logger.info('Finding all java files')
	list_of_files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename[-5:] == '.java':
				list_of_files.append(os.path.join(dirpath,filename))
	return list_of_files

def find_xml(path):
	"""
	Given an absolute path, find  and return all R.java files in a list

	"""
	list_of_files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename[-4:] == '.xml':
				list_of_files.append(os.path.join(dirpath,filename))
	return list_of_files

def findKeys(path):
	"""
	Given an absolute path, find  and return all key files in a list

	"""
	logger.info('Looking for private key files in project')
	list_of_files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename[-4:] == '.pem':
				list_of_files.append(os.path.join(dirpath,filename))
			elif filename[-4:] == '.key':
				list_of_files.append(os.path.join(dirpath,filename))
	return list_of_files

def find_xml(path):
	"""
	Given an absolute path, find  and return all xml files in a list

	"""
	logger.info('Finding all xml files')
	list_of_files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename[-4:] == '.xml':
				list_of_files.append(os.path.join(dirpath,filename))
	return list_of_files

def read_files(filename,rex):
	"""
	Read a file line by line, run a regular expression against the content and return list of things that require inspection
	"""
	things_to_inspect=[]
	try:
		with open(filename) as f:
			content=f.readlines()
			for y in content:
				if re.search(rex,y):
					if re.match(r'^\s*(\/\/|\/\*)',y): #exclude single-line or beginning comments
						pass
					elif re.match(r'^\s*\*',y): #exclude lines that are comment bodies
						pass
					elif re.match(r'.*\*\/$',y): #exclude lines that are closing comments
						pass
					elif re.match(r'^\s*Log\..\(',y): #exclude Logging functions
						pass
					elif re.match(r'(.*)(public|private)\s(String|List)',y): #exclude declarations
						pass
					else:
						things_to_inspect.append(y)
	except Exception as e:
		logger.error("Unable to read file: " + str(filename) + " results will be inaccurate")
	return things_to_inspect

def print_res_list(list_n,msg_n):
	"""
	Deprecated code
	"""
	if len(list_n)>1:
		print msg_n
		for x in list_n:
			if len(x)>0:
				print x

#look for text
def text_scan(file_list,rex_n):
	"""
	Given a list of files, search content of each file by the regular expression and return a list of matches
	"""
	result_list=[]
	#result_list.append([])
	for file in file_list:
		result=read_files(file,rex_n)
		if len(result)>0:
			result_list.append([result,file])
	return result_list

def text_scan_single(file_name,rex_n):
	"""
	Given a single files, search content of each file by the regular expression and return a list of matches
	"""
	result_list=[]
	result_list.append([])
	result=read_files(file_name,rex_n)
	if len(result)>0:
		result_list.append([result,file_name])
	return result_list

def compare(length, req_length, msg, bye):
	"""
	Deprecated code
	"""
	if length != req_length:
		print msg
		if bye == 'true':
			sys.exit()
	return

def dedup(L):
	"""
	Given a list, deduplicate it
	"""
	if L:
		L.sort()
		last = L[-1]
		for i in range(len(L)-2, -1, -1):
			if last == L[i]:
				del L[i]
			else:
				last = L[i]
	return L

#find clases that extend something
def find_ext(class_name):
	"""
	Function to find if a class extends any other type and return the results in a list
	"""
	extension_list=[]
	extension_list.append([])
	ext_string=r'class.*extends\s+'+re.escape(class_name)+r'\s*(<.*>)?(implements.*)?\s*{'
	extension_list=text_scan(java_files,ext_string)
	for y in extension_list:
		if len(y)>0:
			y[0]=re.sub(r';\\n','',str(y[0]).strip('[]\''))
			y[0]=re.sub(r'^.*\w+\sclass','',y[0])
			y[0]=re.sub(r'\sextends.*','',y[0])
			y[0]=re.sub(r'<.*>','',y[0])
			y[0]=str(y[0]).strip()
	return extension_list

def tree(l):
	"""
	Given a list of files, find the complete list of hierarchy of extensions and return the result as a list
	"""
	tmp_list = []
	for c in l:
		if len(c)>0:
			tmp_list+=find_ext(str(c[0]))
		else:
			tmp_list=[]
	return tmp_list

def normalizeActivityNames(activityList,package_name):
	for d in range(0,len(activityList)):
		if re.match(r'\..*',str(activityList[d])):
			activityList[d]=str(package_name)+str(activityList[d])
	return activityList

def check_export(tag,output):
	"""
	Check if the application has marked the tag as EXPORTED
	"""

	global protected_broadcasts

	report_data = []
	private_list=[]
	exported_list=[]
	exported_perm_list=[]
	exported_perm_list.append([])
	protected_broad_list=[]

	for node in xmldoc.getElementsByTagName(tag):
		if 'android:exported' in node.attributes.keys():
			if node.attributes['android:exported'].value == 'true':
				if 'android:permission' in node.attributes.keys():
					if node.getElementsByTagName('intent-filter'):
						for x in node.getElementsByTagName('intent-filter'):
							for a in node.getElementsByTagName('action'):
								if (a.attributes['android:name'].value) not in protected_broadcasts:
									exported_perm_list.append([node.attributes['android:name'].value, node.attributes['android:permission'].value])
								else:
									protected_broad_list.append(node.attributes['android:name'].value)
					else:
						exported_perm_list.append([node.attributes['android:name'].value, node.attributes['android:permission'].value])
				elif node.getElementsByTagName('intent-filter'):
					for x in node.getElementsByTagName('intent-filter'):
						for a in node.getElementsByTagName('action'):
							if (a.attributes['android:name'].value) not in protected_broadcasts:
								exported_list.append(node.attributes['android:name'].value)
							else:
								protected_broad_list.append(node.attributes['android:name'].value)
				else:
					exported_list.append(node.attributes['android:name'].value)
			elif node.attributes['android:exported'].value == 'false':
				private_list.append(node.attributes['android:name'].value)
			else:
				logger.error(config.get('qarkhelper', 'ERR_DET_EXP'))
				logger.error(node.attributes['android:exported'].value)
		elif tag == 'provider':
			if ((int(minSdkVersion) > 16) or (int(targetSdkVersion) > 16)):
				private_list.append(node.attributes['android:name'].value)
			else:
				if 'android:permission' in node.attributes.keys():
					exported_perm_list.append([node.attributes['android:name'].value, node.attributes['android:permission'].value])
				else:
					if 'action' in node.attributes.keys():
						for a in node.getElementsByTagName('action'):
							if (a.attributes['android:name'].value) not in protected_broadcasts:
								exported_list.append(node.attributes['android:name'].value)
							else:
								protected_broad_list.append(node.attributes['android:name'].value)
					else:
						exported_list.append(node.attributes['android:name'].value)
		else:
			for x in node.getElementsByTagName('intent-filter'):
				#BUG - this causes dups when more than one intent filter is present for the same element
				#should only be accessed once per element, so just need to check if it is already in list
				if 'android:permission' in node.attributes.keys():
					if (node.attributes['android:name'].value, node.attributes['android:permission'].value) not in exported_perm_list:
						if x.getElementsByTagName('action'):
							for a in node.getElementsByTagName('action'):
								if (node.attributes['android:name'].value, a.attributes['android:name'].value) not in protected_broadcasts:
									exported_perm_list.append([node.attributes['android:name'].value, node.attributes['android:permission'].value])
								else:
									protected_broad_list.append([node.attributes['android:name'].value,node.attributes['android:name'].value])
						else:
							exported_perm_list.append([node.attributes['android:name'].value, node.attributes['android:permission'].value])
					else:
						if (node.attributes['android:name'].value) not in exported_list:
							if x.getElementsByTagName('action'):
								for a in node.getElementsByTagName('action'):
									if (a.attributes['android:name'] not in protected_broadcasts):
										exported_list.append(node.attributes['android:name'].value)
									else:
										protected_broad_list.append([node.attributes['android:name'].value,a.attributes['android:name'].value])
							else:
										exported_list.append(node.attributes['android:name'].value)
				else:
					if x.getElementsByTagName('action'):
						for a in node.getElementsByTagName('action'):
							if (a.attributes['android:name'] not in protected_broadcasts):
								exported_list.append(node.attributes['android:name'].value)
							else:
								protected_broad_list.append([node.attributes['android:name'].value,a.attributes['android:name'].value])
	if output:
		results = []
		if (int(minSdkVersion) < 20 and len(exported_perm_list) > 1):
			#TODO - HACK to skip the first empty element that prints []
			exported_perm_list=dedup(exported_perm_list)
			item = []

			issue = terminalPrint()
			issue.setLevel(Severity.VULNERABILITY)
			issue.setData(config.get('qarkhelper', 'WARN_FOLL') + ' ' + tag +' ' + config.get('qarkhelper', 'PERM_SNATCH') +' ' +tag + ' ' + config.get('qarkhelper', 'VULN_MAL') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_TYPES'))
			issue.setExtras("list", exported_perm_list)
			report_data.append(issue)

			issue = ReportIssue()
			issue.setCategory(ExploitType.MANIFEST)
			issue.setDetails(config.get('qarkhelper', 'WARN_FOLL') + ' ' + tag +' ' + config.get('qarkhelper', 'PERM_SNATCH') +' ' +tag + ' ' + config.get('qarkhelper', 'VULN_MAL') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_TYPES'))
			issue.setFile(pathToManifest)
			issue.setSeverity(Severity.WARNING)
			issue.setExtras("list", exported_perm_list)
			results.append(issue)

		if len(exported_list) > 0:

			#TODO - HACK to skip the first empty element that prints []
			exported_list=dedup(exported_list)


			issue = terminalPrint()
			issue.setLevel(Severity.WARNING)
			issue.setData(config.get('qarkhelper', 'WARN_FOLL') + ' ' + tag + ' ' + config.get('qarkhelper', 'EXP_NO_PERM') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_MAL') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_TYPES'))
			issue.setExtras("list", exported_list)
			report_data.append(issue)

			issue = ReportIssue()
			issue.setCategory(ExploitType.MANIFEST)
			issue.setDetails(config.get('qarkhelper', 'WARN_FOLL') + ' ' + tag + ' ' + config.get('qarkhelper', 'EXP_NO_PERM') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_MAL') + ' ' + tag + ' ' + config.get('qarkhelper', 'VULN_TYPES'))
			issue.setFile(pathToManifest)
			issue.setSeverity(Severity.WARNING)
			issue.setExtras("list", exported_list)
			results.append(issue)

			#BUG - need to de-dupe the last returned list
		if len(protected_broad_list)>1:
			protected_broad_list=dedup(protected_broad_list)

			issue = terminalPrint()
			issue.setLevel(Severity.INFO)
			issue.setData("PROTECTED BROADCASTS")
			issue.setExtras("list", protected_broad_list)
			report_data.append(issue)

			issue = ReportIssue()
			issue.setCategory(ExploitType.MANIFEST)
			issue.setDetails("PROTECTED BROADCASTS")
			issue.setFile(pathToManifest)
			issue.setSeverity(Severity.INFO)
			issue.setExtras("list", protected_broad_list)
			results.append(issue)

			issue = terminalPrint()
			issue.setLevel(Severity.INFO)
			issue.setData("These are exported, but the associated Intents can only be sent by SYSTEM level apps. They could still potentially be vulnerable, if the Intent carries data that is tainted (2nd order injection)")
			issue.setExtras("list", protected_broad_list)
			report_data.append(issue)

			issue = ReportIssue()
			issue.setCategory(ExploitType.MANIFEST)
			issue.setDetails("These are exported, but the associated Intents can only be sent by SYSTEM level apps. They could still potentially be vulnerable, if the Intent carries data that is tainted (2nd order injection)")
			issue.setFile(pathToManifest)
			issue.setSeverity(Severity.INFO)
			issue.setExtras("list", protected_broad_list)
			results.append(issue)

	else:
		if (int(minSdkVersion) < 20 and len(exported_perm_list) > 1):
			exported_perm_list=dedup(exported_perm_list)
		if len(exported_list) > 0:
			exported_list=dedup(exported_list)
		if len(protected_broad_list)>1:
			protected_broad_list=dedup(protected_broad_list)

	return (list(set(private_list)), exported_list, exported_perm_list, protected_broad_list, report_data, results)

def sink_list_check(token,tree):
	"""
	Check against the master list of sinks
	"""
	#BUG The commented out sinks need some massaging to parse right; They are mostly breaking context
	sink_list = []
	sink_list.append([])
	sink_list.append(['android.os.Bundle', 'void', 'putBinder', ['java.lang.String', 'android.os.IBinder']])
	sink_list.append(['android.os.Bundle', 'void', 'putBoolean', ['java.lang.String', 'boolean']])
	sink_list.append(['android.os.Bundle', 'void', 'putBooleanArray', ['java.lang.String', 'boolean[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putBundle', ['java.lang.String', 'android.os.Bundle']])
	sink_list.append(['android.os.Bundle', 'void', 'putByte', ['java.lang.String', 'byte']])
	sink_list.append(['android.os.Bundle', 'void', 'putByteArray', ['java.lang.String', 'byte[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putChar', ['java.lang.String', 'char']])
	sink_list.append(['android.os.Bundle', 'void', 'putCharArray', ['java.lang.String', 'char[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putCharSequence', ['java.lang.String', 'java.lang.CharSequence']])
	sink_list.append(['android.os.Bundle', 'void', 'putCharSequenceArray', ['java.lang.String', 'java.lang.CharSequence[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putCharSequenceArrayList', ['java.lang.String', 'java.util.ArrayList']])
	sink_list.append(['android.os.Bundle', 'void', 'putDouble', ['java.lang.String', 'double']])
	sink_list.append(['android.os.Bundle', 'void', 'putDoubleArray', ['java.lang.String', 'double[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putFloat', ['java.lang.String', 'float']])
	sink_list.append(['android.os.Bundle', 'void', 'putFloatArray', ['java.lang.String', 'float[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putInt', ['java.lang.String', 'int']])
	sink_list.append(['android.os.Bundle', 'void', 'putIntArray', ['java.lang.String', 'int[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putIntegerArrayList', ['java.lang.String', 'java.util.ArrayList']])
	sink_list.append(['android.os.Bundle', 'void', 'putLong', ['java.lang.String', 'long']])
	sink_list.append(['android.os.Bundle', 'void', 'putLongArray', ['java.lang.String', 'long[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putParcelable', ['java.lang.String', 'android.os.Parcelable']])
	sink_list.append(['android.os.Bundle', 'void', 'putParcelableArray', ['java.lang.String', 'android.os.Parcelable[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putParcelableArrayList', ['java.lang.String', 'java.util.ArrayList']])
	sink_list.append(['android.os.Bundle', 'void', 'putSerializable', ['java.lang.String', 'java.io.Serializable']])
	sink_list.append(['android.os.Bundle', 'void', 'putShort', ['java.lang.String', 'short']])
	sink_list.append(['android.os.Bundle', 'void', 'putShortArray', ['java.lang.String', 'short[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putSparseParcelableArray', ['java.lang.String', 'android.util.SparseArray']])
	sink_list.append(['android.os.Bundle', 'void', 'putString', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.os.Bundle', 'void', 'putStringArray', ['java.lang.String', 'java.lang.String[]']])
	sink_list.append(['android.os.Bundle', 'void', 'putStringArrayList', ['java.lang.String', 'java.util.ArrayList']])
	sink_list.append(['android.os.Bundle', 'void', 'putAll', ['android.os.Bundle']])
	sink_list.append(['android.util.Log', 'int', 'd', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'd', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'e', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'e', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'i', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'i', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'v', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'v', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'w', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.util.Log', 'int', 'wtf', ['java.lang.String', 'java.lang.String', 'java.lang.Throwable']])
	sink_list.append(['java.io.OutputStream', 'void', 'write', ['byte[]']])
	#sink_list.append(['java.io.OutputStream','void','write',['byte[]'','int','int']])
	sink_list.append(['java.io.OutputStream', 'void', 'write', ['int']])
	sink_list.append(['java.io.FileOutputStream', 'void', 'write', ['byte[]']])
	#sink_list.append(['java.io.FileOutputStream','void','write',['byte[]'','int','int']])
	sink_list.append(['java.io.FileOutputStream', 'void', 'write', ['int']])
	sink_list.append(['java.io.Writer', 'void', 'write', ['char[]']])
	#sink_list.append(['java.io.Writer','void','write',['char[]'','int','int']])
	sink_list.append(['java.io.Writer', 'void', 'write', ['int']])
	sink_list.append(['java.io.Writer', 'void', 'write', ['java.lang.String']])
	sink_list.append(['java.io.Writer', 'void', 'write', ['java.lang.String', 'int', 'int']])
	sink_list.append(['java.net.URL', 'void', 'set',['java.lang.String', 'java.lang.String', 'int', 'java.lang.String', 'java.lang.String']])
	sink_list.append(['java.net.URL', 'void', 'set',['java.lang.String', 'java.lang.String', 'int', 'java.lang.String', 'java.lang.String','java.lang.String', 'java.lang.String', 'java.lang.String']])
	sink_list.append(['java.net.URLConnection', 'void', 'setRequestProperty', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'setAction', ['java.lang.String']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'setClassName',['android.content.Context', 'java.lang.Class']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'setClassName',['android.content.Context', 'java.lang.String']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'setComponent', ['android.content.ComponentName']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'double[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'int']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra',['java.lang.String', 'java.lang.CharSequence']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'char']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'android.os.Bundle']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra',['java.lang.String', 'android.os.Parcelable[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.io.Serializable']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'int[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'float']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'byte[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'long[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'android.os.Parcelable']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'float[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'long']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.lang.String[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'boolean']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'boolean[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'short']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'double']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'short[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'byte']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra', ['java.lang.String', 'char[]']])
	sink_list.append(['android.content.Intent', 'android.content.Intent', 'putExtra',['java.lang.String', 'java.lang.CharSequence[]']])
	sink_list.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent']])
	sink_list.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	sink_list.append(['android.media.MediaRecorder', 'void', 'setVideoSource', ['int']])
	sink_list.append(['android.media.MediaRecorder', 'void', 'setPreviewDisplay', ['android.view.Surface']])
	sink_list.append(['android.media.MediaRecorder', 'void', 'start', '[]'])
	sink_list.append(['android.content.Context', 'android.content.Intent', 'registerReceiver',['android.content.BroadcastReceiver', 'android.content.IntentFilter']])
	sink_list.append(['android.content.Context', 'android.content.Intent', 'registerReceiver',['android.content.BroadcastReceiver', 'android.content.IntentFilter', 'java.lang.String','android.os.Handler']])
	sink_list.append(['android.content.IntentFilter', 'void', 'addAction', ['java.lang.String']])
	sink_list.append(['android.telephony.SmsManager', 'void', 'sendTextMessage',['java.lang.String', 'java.lang.String', 'java.lang.String', 'android.app.PendingIntent','android.app.PendingIntent']])
	sink_list.append(['android.telephony.SmsManager', 'void', 'sendDataMessage',['java.lang.String', 'java.lang.String', 'short', 'byte[]', 'android.app.PendingIntent','android.app.PendingIntent']])
	sink_list.append(['android.telephony.SmsManager', 'void', 'sendMultipartTextMessage',['java.lang.String', 'java.lang.String', 'java.util.ArrayList', 'java.util.ArrayList', 'java.util.ArrayList']])
	sink_list.append(['java.net.Socket', 'void', 'connect', ['java.net.SocketAddress']])
	sink_list.append(['android.os.Handler', 'boolean', 'sendMessage', ['android.os.Message']])
	sink_list.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putBoolean',['java.lang.String', 'boolean']])
	sink_list.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putFloat',['java.lang.String', 'float']])
	sink_list.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putInt',['java.lang.String', 'int']])
	sink_list.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putLong',['java.lang.String', 'long']])
	sink_list.append(['android.content.SharedPreferences$Editor', 'android.content.SharedPreferences$Editor', 'putString',['java.lang.String', 'java.lang.String']])
	sink_list.append(['org.apache.http.impl.client.DefaultHttpClient', 'org.apache.http.HttpResponse', 'execute',['org.apache.http.client.methods.HttpUriRequest']])
	sink_list.append(['org.apache.http.client.HttpClient', 'org.apache.http.HttpResponse', 'execute',['org.apache.http.client.methods.HttpUriRequest']])
	sink_list.append(['android.content.Context', 'void', 'startActivity', ['android.content.Intent']])
	sink_list.append(['android.content.Context', 'void', 'startActivity', ['android.content.Intent', 'android.os.Bundle']])
	sink_list.append(['android.content.Context', 'void', 'startActivities', ['android.content.Intent[]']])
	sink_list.append(['android.content.Context', 'void', 'startActivities', ['android.content.Intent[]', 'android.os.Bundle']])
	sink_list.append(['android.content.Context', 'android.content.ComponentName', 'startService', ['android.content.Intent']])
	sink_list.append(['android.content.Context', 'boolean', 'bindService',['android.content.Intent', 'android.content.ServiceConnection', 'int']])
	sink_list.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent']])
	sink_list.append(['android.content.Context', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	sink_list.append(['android.app.Activity', 'void', 'setResult', ['int', 'android.content.Intent']])
	sink_list.append(['android.app.Activity', 'void', 'startActivity', ['android.content.Intent']])
	sink_list.append(['android.app.Activity', 'void', 'startActivity', ['android.content.Intent', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivities', ['android.content.Intent[]']])
	sink_list.append(['android.app.Activity', 'void', 'startActivities', ['android.content.Intent[]', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityForResult', ['android.content.Intent', 'int']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityForResult',['android.content.Intent', 'int', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityFromChild',['android.app.Activity', 'android.content.Intent', 'int', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityFromChild',['android.app.Activity', 'android.content.Intent', 'int']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityFromFragment',['android.app.Fragment', 'android.content.Intent', 'int', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityFromFragment',['android.app.Fragment', 'android.content.Intent', 'int']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityIfNeeded',['android.content.Intent', 'int', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'startActivityIfNeeded', ['android.content.Intent', 'int']])
	sink_list.append(['android.app.Activity', 'android.content.ComponentName', 'startService', ['android.content.Intent']])
	sink_list.append(['android.app.Activity', 'boolean', 'bindService',['android.content.Intent', 'android.content.ServiceConnection', 'int']])
	sink_list.append(['android.app.Activity', 'void', 'sendBroadcast', ['android.content.Intent']])
	sink_list.append(['android.app.Activity', 'void', 'sendBroadcast', ['android.content.Intent', 'java.lang.String']])
	sink_list.append(['android.app.Activity', 'void', 'sendBroadcastAsUser', ['android.content.Intent', 'android.os.UserHandle']])
	sink_list.append(['android.app.Activity', 'void', 'sendBroadcastAsUser',['android.content.Intent', 'android.os.UserHandle', 'java.lang.String']])
	sink_list.append(['android.app.Activity', 'void', 'sendOrderedBroadcast',['android.content.Intent', 'java.lang.String', 'android.content.BroadcastReceiver','android.os.Handler', 'int', 'java.lang.String', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'sendOrderedBroadcast', ['android.content.Intent', 'java.lang.String']])
	sink_list.append(['android.app.Activity', 'void', 'sendOrderedBroadcastAsUser',['android.content.Intent', 'android.os.UserHandle', 'java.lang.String','android.content.BroadcastReceiver', 'android.os.Handler', 'int', 'java.lang.String','android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'sendStickyBroadcast', ['android.content.Intent']])
	sink_list.append(['android.app.Activity', 'void', 'sendStickyBroadcastAsUser',['android.content.Intent', 'android.os.UserHandle']])
	sink_list.append(['android.app.Activity', 'void', 'sendStickyOrderedBroadcast',['android.content.Intent', 'android.content.BroadcastReceiver', 'android.os.Handler', 'int','java.lang.String', 'android.os.Bundle']])
	sink_list.append(['android.app.Activity', 'void', 'sendStickyOrderedBroadcastAsUser',['android.content.Intent', 'android.os.UserHandle', 'android.content.BroadcastReceiver','android.os.Handler', 'int', 'java.lang.String', 'android.os.Bundle']])
	sink_list.append(['android.content.ContentResolver', 'android.net.Uri', 'insert',['android.net.Uri', 'android.content.ContentValues']])
	sink_list.append(['android.content.ContentResolver', 'int', 'delete',['android.net.Uri', 'java.lang.String', 'java.lang.String[]']])
	sink_list.append(['android.content.ContentResolver', 'int', 'update',['android.net.Uri', 'android.content.ContentValues', 'java.lang.String', 'java.lang.String[]']])
	sink_list.append(['android.content.ContentResolver', 'android.database.Cursor', 'query',['android.net.Uri', 'java.lang.String[]', 'java.lang.String', 'java.lang.String[]','java.lang.String']])
	sink_list.append(['android.content.ContentResolver', 'android.database.Cursor', 'query',['android.net.Uri', 'java.lang.String[]', 'java.lang.String', 'java.lang.String[]','java.lang.String', 'android.os.CancellationSignal']])
	sink_list.append(['java.lang.ProcessBuilder', 'java.lang.Process', 'start', '[]'])
	sink_list.append(['android.app.NotificationManager', 'void', 'notify', ['int', 'android.app.Notification']])
	sink_list.append(['org.apache.http.message.BasicNameValuePair', 'void', '<init>', ['java.lang.String', 'java.lang.String']])
	sink_list.append(['java.net.URL', 'void', '<init>', ['java.lang.String', 'java.lang.String', 'int', 'java.lang.String']])
	sink_list.append(['java.net.URL', 'void', '<init>', ['java.lang.String', 'java.lang.String', 'java.lang.String']])
	sink_list.append(['java.net.URL', 'void', '<init>',['java.lang.String', 'java.lang.String', 'int', 'java.lang.String', 'java.net.URLStreamHandler']])
	sink_list.append(['java.net.URL', 'void', '<init>', ['java.lang.String']])
	sink_list.append(['java.net.URL', 'void', '<init>', ['java.net.URL', 'java.lang.String']])
	sink_list.append(['java.net.URL', 'void', '<init>', ['java.net.URL', 'java.lang.String', 'java.net.URLStreamHandler']])
	try:
		for s in sink_list:
			if len(s) > 0:
				#TODO - seems like this might be re-workable for efficiency
				if hasattr(token, 'name'):
					#Match sink and token method names
					if str(s[2]) == str(token.name):
						#Match token and sink parameter counts (Types will have to wait)
						if len(s[3])==len(token.arguments):
							#Confirm the class for the matched sink is in our imports
							for imp_decl in tree.import_declarations:
								if str(imp_decl.name.value)==str(s[0]):
									found=token.name
									return found
						else:
							found=None
					else:
						found=None
				else:
					logger.error("Unable to find the name of the token: " + str(token) + " when checking against sink list in findMethods.py")
					found=None
			else:
				found=None
	except Exception as e:
		logger.error("Problem in sink_list_check method of common.py: " + str(e))
		found=None
	return found


class Severity():
	"""
	Enum type for exploitatin category
	"""
	INFO, WARNING, ERROR, VULNERABILITY = range(4)

def print_terminal_header(header):
	with term.location(0,term.height):
		logger.log(HEADER_ISSUES_LEVEL, header)

def print_terminal(objectlist):
	for item in objectlist:
		if isinstance(item, terminalPrint):
			if item.getLevel() == Severity.INFO:
				logger.info(item.getData())
			if item.getLevel() == Severity.WARNING:
				logger.warning(item.getData())
			if item.getLevel() == Severity.ERROR:
				logger.error(item.getData())
			if item.getLevel() == Severity.VULNERABILITY:
				logger.log(VULNERABILITY_LEVEL,item.getData())
			if item.getExtras() is not None:
				extra_item = item.getExtras()
				if isinstance(extra_item, dict):
					for key,val in extra_item.items():
							for i in extra_item[key]:
								firstelement = True
								if isinstance(i, list):
									for j in i:
										if firstelement:
											with term.location(10,term.height):
														print j
											firstelement = False
										else:
											with term.location(20,term.height):
														print j
								else:
									with term.location(10,term.height):
										print i
				if isinstance(extra_item, list):
					for i in extra_item:
						firstelement = True
						if isinstance(i, list):
							for j in i:
								if firstelement:
									with term.location(10,term.height):
												print j
									firstelement = False
								else:
									with term.location(20,term.height):
												print j
						else:
							with term.location(10,term.height):
									print i
				if isinstance(extra_item, str):
					with term.location(10,term.height):
									print extra_item
				else:
					logger.debug("Not a valid type of object in terminalPrint extras")

def get_entry_for_component(comp_type):
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
	return entry

class ReportIssue():
	category = ""
	severity = ""
	details = ""
	file = ""
	name = ""
	extra = {}

	def __init__(self):
		self.category = ""
		self.severity = ""
		self.details = ""
		self.file = ""
		self.name = ""
		self.extra = {}


	def getCategory(self):
		return self.category

	def setCategory(self, category):
		self.category = category

	def getSeverity(self):
		return self.severity

	def setSeverity(self, severity):
		self.severity = severity

	def getDetails(self):
		return self.details

	def setDetails(self, details):
		self.details = details

	def getFile(self):
		return self.file

	def setFile(self, file):
		self.file = file

	def getName(self):
		return self.name

	def setName(self, name):
		self.name = name

	def getExtras(self):
		return self.extra

	def setExtras(self, key, value):
		self.extra[key] = value
