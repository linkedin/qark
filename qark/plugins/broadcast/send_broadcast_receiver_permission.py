from qark.plugins.helpers import get_min_sdk
from qark.scanner.plugin import BasePlugin
from qark.issue import Severity, Issue

import logging
import re
from xml.dom import minidom

import javalang
from javalang.tree import MethodInvocation


log = logging.getLogger(__name__)

BROADCAST_METHODS = (
    "sendBroadcast",
    "sendBroadcastAsUser",
    "sendOrderedBroadcast",
    "sendOrderedBroadcastAsUser",
    "sendStickyBroadcast",
    "sendStickyBroadcastAsUser",
    "sendStickyOrderedBroadcast",
    "sendStickyOrderedBroadcastAsUser",
)
STICKY_BROADCAST_METHODS = (
    "sendStickyBroadcast",
    "sendStickyBroadcastAsUser",
    "sendStickyOrderedBroadcast",
    "sendStickyOrderedBroadcastAsUser",
)
LOCAL_BROADCAST_IMPORTS = (
    "android.support.v4.content.LocalBroadcastManager",
    "android.support.v4.content.*",
    "android.support.v4.*",
    "android.support.*",
    "android.*",
)
BROADCAST_WITHOUT_RECEIVER = (
    "A broadcast, {broadcast_type}, is sent from this file {file_name}, which does not specify the receiverPermission. "
    "This means any application on the device can receive this broadcast. You should investigate this "
    "for potential data leakage."
)
BROADCAST_WITH_RECEIVER = (
    "A broadcast, {broadcast_type}, is sent from this file {file_name}, which specifies the receiverPermission, "
    "but depending on the protection level of the permission (on the receiving app side), may "
    "still be vulnerable to interception, if the protection level of the permission is not set "
    "to signature or signatureOrSystem. You should investigate this for potential data leakage."
)
BROADCAST_WITH_RECEIVER_UNDER_21 = (
    "A broadcast, {broadcast_type}, is sent from this class: {file_name}, which specifies the "
    "receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability "
    "in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device "
    "can potentially receive this broadcast. You should investigate this for potential data leakage."
)
STICKY_BROADCAST = (
    "A sticky broadcast, {broadcast_type}, is sent from this class: {file_name}. These should not be used, as they "
    "rovide no security (anyone can access them), no protection (anyone can modify them), and many other problems. "
    "For more info: http://developer.android.com/reference/android/content/Context.html"
)


class SendBroadcastReceiverPermission(BasePlugin):
    def __init__(self):
        BasePlugin.__init__(self, category="broadcast")
        self.severity = Severity.WARNING
        self.current_file = None
        self.manifest_xml = None
        self.below_min_sdk_21 = False

    def run(self, files, apk_constants=None):
        try:
            self.below_min_sdk_21 = apk_constants["min_sdk"] < 21
        except (KeyError, TypeError):
            for decompiled_file in files:
                if decompiled_file.lower().endswith("androidmanifest.xml"):
                    self.below_min_sdk_21 = get_min_sdk(manifest_xml=minidom.parse(decompiled_file)) < 21
                else:
                    self.below_min_sdk_21 = False

        java_files = (decompiled_file for decompiled_file in files if decompiled_file.lower().endswith(".java"))
        for java_file in java_files:
            with open(java_file, "r") as java_file_to_read:
                file_contents = java_file_to_read.read()

                # really simple check to see if the file has the methods we are interested in before parsing the AST
                if not re.search("({broadcasts})".format(broadcasts="|".join(BROADCAST_METHODS)), file_contents):
                    continue

            try:
                parsed_tree = javalang.parse.parse(file_contents)
            except javalang.parser.JavaSyntaxError:
                log.debug("Error parsing file %s, continuing", java_file)
                continue
            self.current_file = java_file
            for method_invocation in parsed_tree.filter(MethodInvocation):
                self._check_method_invocation(method_invocation, parsed_tree.imports)

    def _check_method_invocation(self, method_invocation, imports):
        method_name = method_invocation[1].member
        num_arguments = len(method_invocation[1].arguments)
        if method_invocation[1].member in BROADCAST_METHODS:
            name = None
            description = None

            if method_name == "sendBroadcast":
                if num_arguments == 1 and not has_local_broadcast_imported(import_tree=imports):
                    name = "Broadcast sent without receiverPermission"
                    description = BROADCAST_WITHOUT_RECEIVER
                elif num_arguments == 2:
                    if self.below_min_sdk_21:
                        name = "Broadcast sent with receiverPermission with minimum SDK under 21"
                        description = BROADCAST_WITH_RECEIVER_UNDER_21
                    else:
                        name = "Broadcast sent with receiverPermission"
                        description = BROADCAST_WITH_RECEIVER

            elif method_name == "sendBroadcastAsUser":
                if num_arguments == 2:
                    name = "Broadcast sent as specific user without receiverPermission"
                    description = BROADCAST_WITH_RECEIVER_UNDER_21
                elif num_arguments == 3:
                    if self.below_min_sdk_21:
                        name = ("Broadcast sent as specific user with receiverPermission with minimum SDK "
                                      "under 21")
                        description = BROADCAST_WITH_RECEIVER_UNDER_21
                    else:
                        name = "Broadcast sent as specific user with receiverPermission"
                        description = BROADCAST_WITH_RECEIVER

            elif method_name == "sendOrderedBroadcast":
                if num_arguments in (2, 7):
                    if self.below_min_sdk_21:
                        name = "Ordered broadcast sent with receiverPermission with minimum SDK under 21"
                        description = BROADCAST_WITH_RECEIVER_UNDER_21
                    else:
                        name = "Ordered broadcast sent with receiverPermission"
                        description = BROADCAST_WITH_RECEIVER

            elif method_name == "sendOrderedBroadcastAsUser":
                if num_arguments == 7:
                    if self.below_min_sdk_21:
                        name = "Ordered broadcast sent with receiverPermission with minimum SDK under 21"
                        description = BROADCAST_WITH_RECEIVER_UNDER_21
                    else:
                        name = "Ordered broadcast sent with receiverPermission"
                        description = BROADCAST_WITH_RECEIVER

            elif method_name in STICKY_BROADCAST_METHODS:
                self._add_issue(name="Sticky broadcast sent", description=STICKY_BROADCAST,
                                broadcast_type=method_name, severity=Severity.VULNERABILITY)

            if name is not None and description is not None:
                # create vulnerabilities for everything that is not a sticky broadcast
                self._add_issue(name=name, description=description,
                                broadcast_type=method_name)

    def _add_issue(self, name, description, broadcast_type, severity=Severity.WARNING):
        self.issues.append(Issue(
            category=self.category, severity=severity, name=name,
            description=description.format(file_name=self.current_file,
                                           broadcast_type=broadcast_type),
            file_object=self.current_file)
        )


def has_local_broadcast_imported(import_tree):
    return any([import_declaration.path in LOCAL_BROADCAST_IMPORTS for import_declaration in import_tree])


plugin = SendBroadcastReceiverPermission()
