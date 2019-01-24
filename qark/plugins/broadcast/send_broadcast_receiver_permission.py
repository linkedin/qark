import logging
import re

import javalang
from javalang.tree import MethodInvocation

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin, ManifestPlugin

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
    "A broadcast, {broadcast_type} which does not specify the receiverPermission. "
    "This means any application on the device can receive this broadcast. You should investigate this "
    "for potential data leakage."
)
BROADCAST_WITH_RECEIVER = (
    "A broadcast, {broadcast_type} which specifies the receiverPermission, "
    "but depending on the protection level of the permission (on the receiving app side), may "
    "still be vulnerable to interception, if the protection level of the permission is not set "
    "to signature or signatureOrSystem. You should investigate this for potential data leakage."
)
BROADCAST_WITH_RECEIVER_UNDER_21 = (
    "A broadcast, {broadcast_type} which specifies the "
    "receiverPermission, but may still be vulnerable to interception, due to the permission squatting vulnerability "
    "in API levels before 21. This means any application, installed prior to the expected receiver(s) on the device "
    "can potentially receive this broadcast. You should investigate this for potential data leakage."
)
STICKY_BROADCAST = (
    "A sticky broadcast, {broadcast_type}. These should not be used, as they "
    "rovide no security (anyone can access them), no protection (anyone can modify them), and many other problems. "
    "For more info: http://developer.android.com/reference/android/content/Context.html"
)


class SendBroadcastReceiverPermission(CoroutinePlugin, ManifestPlugin):
    """
    This plugin checks certain broadcast methods to see if they are using an insecure version,
    based on number of arguments.
    """
    def __init__(self):
        super(SendBroadcastReceiverPermission, self).__init__(category="broadcast",
                                                              name="Send Broadcast Receiver Permission")
        self.severity = Severity.WARNING
        self.current_file = None
        self.manifest_xml = None
        self.below_min_sdk_21 = False

    def run_coroutine(self):
        while True:
            _, method_invocation = (yield)

            if not isinstance(method_invocation, javalang.tree.MethodInvocation):
                continue

            self._check_method_invocation(method_invocation, self.java_ast.imports)

    def can_run_coroutine(self):
        self.below_min_sdk_21 = self.min_sdk < 21
        self.current_file = self.file_path
        return re.search("({broadcasts})".format(broadcasts="|".join(BROADCAST_METHODS)),
                         self.file_contents) is not None

    def _check_method_invocation(self, method_invocation, imports):
        """
        Checks the type of method that is being called and the amount of arguments and adds it to the issues list if it
        results in a warning or vulnerability.

        :param javalang.tree.MethodInvocation method_invocation: method being called
        :param list imports: list of imports
        """
        method_name = method_invocation.member
        num_arguments = len(method_invocation.arguments)
        if method_name in BROADCAST_METHODS:
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
                        name = "Broadcast sent as specific user with receiverPermission with minimum SDK under 21"
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
                                broadcast_type=method_name, severity=Severity.VULNERABILITY,
                                line_number=method_invocation.position)

            if name is not None and description is not None:
                # create vulnerabilities for everything that is not a sticky broadcast
                self._add_issue(name=name, description=description,
                                broadcast_type=method_name, line_number=method_invocation.position)

    def _add_issue(self, name, description, broadcast_type, severity=Severity.WARNING, line_number=None):
        """
        Helper method to append issues to the plugin.

        :param str name: issue name
        :param str description: issue description
        :param str broadcast_type: type of broadcast from `BROADCAST_METHODS`
        :param Severity severity: issue severity
        """
        self.issues.append(Issue(
            category=self.category, severity=severity, name=name,
            description=description.format(broadcast_type=broadcast_type),
            file_object=self.current_file,
            line_number=line_number)
        )


def has_local_broadcast_imported(import_tree):
    """
    Helper function to determine if the import tree contains any broadcast import.

    :param list import_tree: `javalang` import tree
    :return: True if import tree has broadcast import, else False
    :rtype: bool
    """
    return any(import_declaration.path in LOCAL_BROADCAST_IMPORTS for import_declaration in import_tree)


plugin = SendBroadcastReceiverPermission()
