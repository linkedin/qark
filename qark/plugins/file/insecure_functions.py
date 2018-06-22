import logging

import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration

from qark.issue import Severity, Issue
from qark.scanner.plugin import JavaASTPlugin

log = logging.getLogger(__name__)

INSECURE_FUNCTIONS_DESCRIPTION = (
    "The Content provider API provides a method call. The framework does no permission checking on this "
    "entry into the content provider besides the basic ability for the application to get access to the provider"
    " at all. Any implementation of this method must do its own permission checks on incoming calls to make sure "
    "they are allowed. Failure to do so will allow unauthorized components to interact with the content provider. "
    "Reference: https://bitbucket.org/secure-it-i/android-app-vulnerability-benchmarks/src/d5305b9481df3502e60e98fa352d5f58e4a69044/ICC/WeakChecksOnDynamicInvocation-InformationExposure/?at=master"
)

INSECURE_FUNCTIONS_NAMES = ("call",)


class InsecureFunctions(JavaASTPlugin):
    def __init__(self):
        super(InsecureFunctions, self).__init__(category="file", name="Insecure functions found",
                                                description=INSECURE_FUNCTIONS_DESCRIPTION)
        self.severity = Severity.WARNING

    def run(self):
        for _, class_declaration in self.java_ast.filter(ClassDeclaration):
            for _, method_declaration_in_class in class_declaration.filter(MethodDeclaration):

                if method_declaration_in_class.name in INSECURE_FUNCTIONS_NAMES:
                    self.issues.append(Issue(
                        category=self.category, severity=self.severity, name=self.name,
                        description=self.description,
                        file_object=self.file_path,
                        line_number=method_declaration_in_class.position)
                    )


plugin = InsecureFunctions()
