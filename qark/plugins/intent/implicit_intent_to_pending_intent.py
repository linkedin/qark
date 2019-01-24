import logging
import re

from javalang.tree import MethodInvocation, ClassCreator, ReferenceType

from qark.issue import Severity, Issue
from qark.scanner.plugin import CoroutinePlugin

log = logging.getLogger(__name__)


PENDING_INTENT_METHODS = ("getActivities",
                          "getService",
                          "getActivity",
                          "getBroadcast",
                          )
PENDING_INTENT_REGEX = re.compile(
    "({pending_intent_method})".format(pending_intent_method="|".join(PENDING_INTENT_METHODS)))


class ImplicitIntentToPendingIntent(CoroutinePlugin):
    """
    This plugin checks if a `new Intent` is passed into any of the `PENDING_INTENT_METHODS`.
    If there is, a Vulnerability is created.
    """
    def __init__(self):
        super(ImplicitIntentToPendingIntent, self).__init__(category="intent", name="Empty pending intent found",
                                                            description=(
                                                                "For security reasons, the Intent you supply here should almost always"
                                                                " be an explicit intent that is specify an explicit component to be delivered"
                                                                " to through Intent.setClass. A malicious application could potentially"
                                                                " intercept, redirect and/or modify this Intent. Pending Intents retain the"
                                                                " UID of your application and all related permissions, allowing another"
                                                                " application to act as yours. Reference: "
                                                                "https://developer.android.com/reference/android/app/PendingIntent.html"))
        self.severity = Severity.VULNERABILITY
        self.current_file = None

    def can_run_coroutine(self):
        # simple search to avoid files that are not vulnerable
        if re.search("new Intent", self.file_contents) is None or re.search(PENDING_INTENT_REGEX, self.file_contents) is None:
            return False

        if not any("PendingIntent" in imported_declaration.path for imported_declaration in self.java_ast.imports):
            # if PendingIntent is never imported the file is not vulnerable
            return False

        return True

    def run_coroutine(self):
        while True:
            _, pending_intent_invocation = (yield)

            if not isinstance(pending_intent_invocation,
                              MethodInvocation) or pending_intent_invocation.member not in PENDING_INTENT_METHODS:
                continue

            # iterate over every argument in the pending intent call, looking for a "new Intent()"
            for method_argument in pending_intent_invocation.arguments:
                for _, creation in method_argument.filter(ClassCreator):
                    if len(creation.arguments) in (0, 1):  # remove any intents created with arguments
                        for _, reference_declaration in creation.filter(ReferenceType):
                            if reference_declaration.name == "Intent":
                                self.issues.append(Issue(category=self.category, severity=self.severity,
                                                         name=self.name, description=self.description,
                                                         file_object=self.file_path))


plugin = ImplicitIntentToPendingIntent()
