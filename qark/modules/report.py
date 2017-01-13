from __future__ import absolute_import
'''Copyright 2015 LinkedIn Corp. Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
 You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.'''

import os
import sys
import re
import logging
import shutil

from modules.common import Severity, ReportIssue
from bs4 import BeautifulSoup
from modules import common
import modules.webviews

common.logger = logging.getLogger()
logger = logging.getLogger(__name__)

pre_rendered_html = ""

class Section():
    """
    Enum type for exploitatin category
    """
    WEBVIEW, X509, PERMISSIONS, SERVICES, BROADCASTS, PENDING_INTENTS, FILE_PERMISSIONS, CRYPTO_BUGS, ACTIVITY, APPCOMPONENTS, ADB, PLUGIN = range(12)

section = {}
section[Section.WEBVIEW] = "webview"
section[Section.X509] = "x509"
section[Section.PERMISSIONS] = "permission"
section[Section.SERVICES] = "service"
section[Section.BROADCASTS] = "broadcast"
section[Section.PENDING_INTENTS] = "pendingintent"
section[Section.FILE_PERMISSIONS] = "filepermission"
section[Section.CRYPTO_BUGS] = "crypto"
section[Section.ACTIVITY] = "activity"
section[Section.APPCOMPONENTS] = "appcomponents"
section[Section.ADB] = "adbcommands"
section[Section.PLUGIN] = "plugin"

labels = {}
labels[Severity.VULNERABILITY] = "label label-danger"
labels[Severity.INFO] = "label label-info"
labels[Severity.WARNING] = "label label-warning"
labels[Severity.ERROR] = "label label-error"

badger = {}
badger[Severity.VULNERABILITY] = "badger-div badger-left badger-danger"
badger[Severity.INFO] = "badger-div badger-left badger-success"
badger[Severity.WARNING] = "badger-div badger-left badger-warning"
badger[Severity.ERROR] = "badger-div badger-left badger-info"

severity = {}
severity[Severity.VULNERABILITY] = "Potential Vulnerability"
severity[Severity.INFO] = "Info"
severity[Severity.WARNING] = "Warning"
severity[Severity.ERROR] = "Error"


def writeSection(sec,data_list):
    try:
        pre_rendered = open(common.reportDir + "/report.html",'r').read()
        pre_rendered_html2 = BeautifulSoup(pre_rendered,'html5lib')

        list_of_files = []
        #Gather unique files
        for item in data_list:
            if isinstance(item, ReportIssue):
                if item.getFile() in list_of_files:
                    pass
                else:
                    list_of_files.append(item.getFile())

        #Consolidate issues by filename
        for file in list_of_files:
            issues = {}
            details = []
            file_name = "No Filename provided"
            for item in data_list:
                if isinstance(item, ReportIssue):
                    if file == item.getFile():
                        file_name = str(item.getFile())
                        if item.getDetails() is not None:
                            details.append(item.getDetails())
                            for key, value in item.getExtras().iteritems():
                                issues[key]=value

            #Construct HTML blob
            new_tag_webview_issue = pre_rendered_html2.new_tag("div")

            new_tag_webview_issue['class']=str(section[sec] + "-issue")

            new_div_image_tag = pre_rendered_html2.new_tag("div")
            new_div_image_tag['class']="blockquote-box clearfix"

            new_div_image_square_tag = pre_rendered_html2.new_tag("div")
            new_div_image_square_tag['class']="square pull-left"

            new_glyphicon_tag = pre_rendered_html2.new_tag("span")
            new_glyphicon_tag['class']="glyphicon glyphicon-list-alt white"

            new_div_image_square_tag.append(new_glyphicon_tag)

            new_div_image_tag.append(new_div_image_square_tag)

            new_tag_h4 = pre_rendered_html2.new_tag("h6")

            new_div_image_tag.append(new_tag_h4)

            new_code_tag = pre_rendered_html2.new_tag("code")

            new_p_class = pre_rendered_html2.new_tag("p")
            new_p_class['class']="clip-ellipsis"
            if len(file_name)>85:
                trim = 75
            else:
                trim = 0
            new_code_tag.string = '...{}'.format(file_name[-trim:])
            new_p_class.append(new_code_tag)
            new_div_image_tag.append(new_p_class)

            br_tag = pre_rendered_html2.new_tag("br")
            new_div_image_tag.append(br_tag)
            new_div_image_tag.append(br_tag)

            new_tag_div = pre_rendered_html2.new_tag("div")
            new_tag_div['class']="span4 collapse-group"

            new_br_tag_1 = pre_rendered_html2.new_tag("br/")

            new_tag_div.insert(0, new_br_tag_1)

            new_tag_p = pre_rendered_html2.new_tag("p")
            new_tag_div.append(new_tag_p)
            new_div_image_tag.append(new_tag_div)

            new_tag_a = pre_rendered_html2.new_tag("a")
            new_tag_a['class']="collapse-button"
            new_tag_a.string = "View details >>"


            new_tag_p.append(new_tag_a)

            new_tag_p_details = pre_rendered_html2.new_tag("div")
            new_tag_p_details['class']="collapse"
            new_strong_tag = pre_rendered_html2.new_tag("strong")
            new_strong_tag.string = "File: "
            new_code_tag = pre_rendered_html2.new_tag("code")
            new_code_tag.string = file_name
            new_strong_tag.append(new_code_tag)


            new_br_tag_1.append(new_strong_tag)



            new_h4_tag = pre_rendered_html2.new_tag("h4")
            #new_small_tag = pre_rendered_html2.new_tag("small")
            new_strong_tag = pre_rendered_html2.new_tag("strong")
            new_strong_tag['class']="details"
            new_ul_tag = pre_rendered_html2.new_tag("ul")
            new_div_tag = pre_rendered_html2.new_tag("div")
            data = ""
            count = 0
            for item in details:

                new_br_tag = pre_rendered_html2.new_tag("br/")

                new_li_tag = pre_rendered_html2.new_tag("li")
                new_li_tag.string = item
                if count % 2 == 0:
                    new_li_tag['class'] = "row-even"
                else:
                    new_li_tag['class'] = "row-odd"
                count = count + 1
                new_ul_tag.append(new_li_tag)
                new_div_tag.append(new_ul_tag)

                new_strong_tag.append(new_div_tag)
                #new_small_tag.append(new_strong_tag)
                new_h4_tag.append(new_strong_tag)



            new_div_tag_1 = pre_rendered_html2.new_tag("div")
            new_div_tag_1['class'] = badger[Severity.INFO]
            new_div_tag_1['data-badger'] = severity[Severity.INFO]

            new_div_tag_1.append(new_br_tag_1)
            new_div_tag_1.append(new_h4_tag)

            new_tag_p_details.append(new_div_tag_1)


            new_tag_div.append(new_tag_p_details)
            new_div_image_tag.append(new_tag_div)

            pre_rendered_html2.find("div", id=str(section[sec] + "-issues-list")).append(new_div_tag_1)

            with open(common.reportDir + "/report.html", "w") as fh:
                fh.write(str(pre_rendered_html2.prettify()))
            fh.close()
    except Exception as e:
        logger.debug(e.message)
        logger.debug(e)

def write_manifest(data):
    """
    Writes an issue to the report. Takes in the section to which the data is to be written, the severity of the data and finally the actual vulnerability to be reported
    """
    if common.reportInitSuccess:
        try:
            if os.path.exists(common.reportDir + "/report.html"):
                pre_rendered = open(common.reportDir + "/report.html",'r').read()
                pre_rendered_html = BeautifulSoup(pre_rendered,'html5lib')

                new_code_div = pre_rendered_html.new_tag("code")
                new_code_div['class'] = "xml"
                new_code_div.string = data
                pre_rendered_html.find("pre", id="rawmanifest").append(new_code_div)

            with open(common.reportDir + "/report.html", "w") as fh:
                fh.write(str(pre_rendered_html.prettify()))
            fh.close()
        except Exception as e:
            common.logger.debug("Error writing manifest: " + str(e))
def write(identity, data, tag=None):
    try:
        if os.path.exists(common.reportDir + "/report.html"):
            pre_rendered = open(common.reportDir + "/report.html",'r').read()
            pre_rendered_html = BeautifulSoup(pre_rendered,'html5lib')

            if tag is not None:
                new_span_tag = pre_rendered_html.new_tag(tag)
                new_span_tag['class'] = "debug-level"
            else:
                new_span_tag = pre_rendered_html.new_tag("span")
            new_span_tag.string = str(data)
            pre_rendered_html.find("span", id=identity).append(new_span_tag)

        with open(common.reportDir + "/report.html", "w") as fh:
            fh.write(str(pre_rendered_html.prettify()))
        fh.close()
    except Exception as e:
        common.reportInitSuccess=False
        common.logger.debug("Report writing error: " + str(e))

def write_counters():
    try:
        if os.path.exists(common.reportDir + "/report.html"):
            pre_rendered = open(common.reportDir + "/report.html",'r').read()
            pre_rendered_html = BeautifulSoup(pre_rendered,'html5lib')
            warnings =  len(re.findall(r'badger-warning', str(pre_rendered_html)))
            information =  len(re.findall(r'badger-success', str(pre_rendered_html)))
            vulnerabilities =  len(re.findall(r'badger-danger', str(pre_rendered_html)))
            debug =  len(re.findall(r'debug-level', str(pre_rendered_html)))

            new_div_tag = pre_rendered_html.new_tag("div")
            new_div_tag.string = str(vulnerabilities)
            pre_rendered_html.find("h1", id="vulnerability_count").append(new_div_tag)

            new_div_tag1 = pre_rendered_html.new_tag("div")
            new_div_tag1.string = str(warnings)
            pre_rendered_html.find("h1", id="warning_count").append(new_div_tag1)

            new_div_tag2 = pre_rendered_html.new_tag("div")
            new_div_tag2.string = str(information)
            pre_rendered_html.find("h1", id="information_count").append(new_div_tag2)

            new_div_tag3 = pre_rendered_html.new_tag("div")
            new_div_tag3.string = str(debug)
            pre_rendered_html.find("h1", id="debug_count").append(new_div_tag3)

            with open(common.reportDir + "/report.html", "w") as fh:
                fh.write(str(pre_rendered_html.prettify()))
            fh.close()
    except Exception as e:
        common.logger.debug("Error in write_counters: " + str(e))

def write_badger(identity, sev, data, extra=None):
    if common.reportInitSuccess:
        try:
            if os.path.exists(common.reportDir + "/report.html"):
                pre_rendered = open(common.reportDir + "/report.html",'r').read()
                pre_rendered_html = BeautifulSoup(pre_rendered,'html5lib')

                new_div_tag = pre_rendered_html.new_tag("div")
                new_div_tag['class'] = badger[sev]
                new_div_tag['data-badger'] = severity[sev]
                new_strong_tag = pre_rendered_html.new_tag("strong")
                new_strong_tag.string = data

                new_ul_tag = pre_rendered_html.new_tag("ul")

                if extra is not None:
                    if isinstance(extra, dict):
                        for key,val in extra.items():
                                for i in extra[key]:
                                    if isinstance(i, list) :
                                        if len(i)>0:
                                            firstelement = True
                                            new_ul_tag_depth_1 = pre_rendered_html.new_tag("ul")
                                            new_li_tag = pre_rendered_html.new_tag("li")
                                            for j in i:
                                                if firstelement:
                                                    new_li_tag.string = j
                                                    firstelement = False
                                                else:
                                                    new_li_tag_depth_1 = pre_rendered_html.new_tag("li")
                                                    new_li_tag_depth_1.string = j
                                                    new_ul_tag_depth_1.append(new_li_tag_depth_1)
                                            new_li_tag.append(new_ul_tag_depth_1)
                                            new_ul_tag.append(new_li_tag)
                                    else:
                                        new_li_tag = pre_rendered_html.new_tag("li")
                                        new_li_tag.string = i
                                        new_ul_tag.append(new_li_tag)
                    elif isinstance(extra, list):
                        for i in extra:
                            new_li_tag = pre_rendered_html.new_tag("li")
                            new_li_tag.string = i
                            new_ul_tag.append(new_li_tag)
                    elif isinstance(extra, str):
                        new_li_tag = pre_rendered_html.new_tag("li")
                        new_li_tag.string = extra
                        new_ul_tag.append(new_li_tag)
                    else:
                        logger.debug("Not a valid type of object in terminalPrint extras")

                new_div_tag.append(new_strong_tag)
                new_div_tag.append(new_ul_tag)
                pre_rendered_html.find("div", id=identity).insert(0, new_div_tag)

            with open(common.reportDir + "/report.html", "w") as fh:
                fh.write(str(pre_rendered_html.prettify()))
            fh.close()
        except Exception as e:
            common.logger.debug("Error badger don't care: " + str(e))

def write_adb_commands(identity, sev, data, extra=None, infobartext=None):
    try:
        if os.path.exists(common.reportDir + "/report.html"):
            pre_rendered = open(common.reportDir + "/report.html",'r').read()
            pre_rendered_html = BeautifulSoup(pre_rendered,'html5lib')

            new_div_tag = pre_rendered_html.new_tag("div")
            new_div_tag['class'] = badger[sev]
            if infobartext is not None:
                new_div_tag['data-badger'] = infobartext
            else:
                new_div_tag['data-badger'] = severity[sev]
            new_strong_tag = pre_rendered_html.new_tag("kbd")
            new_strong_tag.string = data

            new_ul_tag = pre_rendered_html.new_tag("ul")

            if extra is not None:
                if isinstance(extra, dict):
                    for key,val in extra.items():
                            for i in extra[key]:
                                if isinstance(i, list) :
                                    if len(i)>0:
                                        firstelement = True
                                        new_ul_tag_depth_1 = pre_rendered_html.new_tag("ul")
                                        new_li_tag = pre_rendered_html.new_tag("li")
                                        for j in i:
                                            if firstelement:
                                                new_li_tag.string = j
                                                firstelement = False
                                            else:
                                                new_li_tag_depth_1 = pre_rendered_html.new_tag("li")
                                                new_li_tag_depth_1.string = j
                                                new_ul_tag_depth_1.append(new_li_tag_depth_1)
                                        new_li_tag.append(new_ul_tag_depth_1)
                                        new_ul_tag.append(new_li_tag)
                                else:
                                    new_li_tag = pre_rendered_html.new_tag("li")
                                    new_li_tag.string = i
                                    new_ul_tag.append(new_li_tag)
                elif isinstance(extra, list):
                    for i in extra:
                        new_li_tag = pre_rendered_html.new_tag("li")
                        new_li_tag.string = i
                        new_ul_tag.append(new_li_tag)
                elif isinstance(extra, str):
                    new_li_tag = pre_rendered_html.new_tag("li")
                    new_li_tag.string = extra
                    new_ul_tag.append(new_li_tag)
                else:
                    logger.debug("Not a valid type of object in terminalPrint extras")

            new_div_tag.append(new_strong_tag)
            new_div_tag.append(new_ul_tag)
            pre_rendered_html.find("div", id=identity).insert(0, new_div_tag)

        with open(common.reportDir + "/report.html", "w") as fh:
            fh.write(str(pre_rendered_html.prettify()))
        fh.close()
    except Exception as e:
        common.logger.debug("Error writing ADB commands to report: " + str(e))

def reset():
    """
    Flushes the contents of the report
    """
    try:
        common.reportDir = common.getConfig("rootDir") + "/report"
        if common.args.reportdir is not None :
            common.reportDir = common.args.reportdir + "/report"

        if os.path.exists(common.reportDir):
            shutil.rmtree(common.reportDir)
        shutil.copytree(common.getConfig("rootDir") + "/template3", common.reportDir)
        os.rename(common.reportDir + "/index.html", common.reportDir + "/report.html")
    except Exception as e:
        common.logger.debug("Error when trying to reset report")
