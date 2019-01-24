import logging
from copy import deepcopy

from javalang.tree import MethodInvocation, MethodDeclaration, VariableDeclaration, Type, Literal

from qark.issue import Issue, Severity
from qark.plugins.helpers import valid_method_invocation, remove_dict_entry_by_value

log = logging.getLogger(__name__)


CATEGORY = "webview"


def valid_set_method_bool(method_invocation, str_bool, method_name="setAllowFileAccess"):
    """
    Determines if the `method_invocation` has the same `method_name` and has an argument of value `str_bool`

    :param MethodInvocation method_invocation: The javalang MethodInvocation
    :param str str_bool: The value of what should be in the argument
    :param str method_name: The name of the method to be found
    :return: Whether the MethodInvocation matches the method name and has the `str_bool` value as its first argument.
    :rtype: bool
    """
    if not method_invocation.arguments or not isinstance(method_invocation.arguments[0], Literal):
        return False
    return (valid_method_invocation(method_invocation, method_name, num_arguments=1)
            and method_invocation.arguments[0].value == str_bool)


def webview_default_vulnerable(tree, method_name, issue_name, description, file_object, severity=Severity.WARNING):
    """
    A helper method for some WebView plugins that checks if a specific method is called with `method_name` and
    has a single argument that is the boolean value `false`. If so, it creates an issue with the other parameters.

    :param tree: javalang tree
    :param str method_name: method name to look for
    :param str issue_name: name of issue when it gets created
    :param str description: description for issue
    :param str file_object: current file being parsed
    :param Severity severity: severity of the issue
    :return: list of issues found in the `tree`
    :rtype: list
    """
    issues = []
    # iterate over method declarations to not go out of different scopes
    for _, method_declaration in tree.filter(MethodDeclaration):
        webviews = {}
        webview_name = None

        for _, node in method_declaration:

            if ast_type_equals(node, VariableDeclaration):
                webview = node
                # webviews are vulnerable by default
                # create a dictionary of webview and websettings objects keyed by their variable name to the
                #  AST parsed declaration
                webviews = add_webview_to_dict(webviews, webview, "WebView")

            elif ast_type_equals(node, MethodInvocation):
                method_invocation = node
                # check if method_name was called like
                # webview.getSettings().method_name("false"), which makes it not vulnerable
                if method_invocation.member == "getSettings":
                    webview_name = method_invocation.qualifier

                    # selectors are the .operators after the function, in this case `setAllowFileAccess`
                    if method_invocation.selectors is None:
                        continue

                    for selector in method_invocation.selectors:
                        if valid_set_method_bool(method_invocation=selector, str_bool="false", method_name=method_name):

                            # remove all instances of that webview from the dictionary as they are not vulnerable
                            if webviews.get(webview_name):
                                webviews = remove_dict_entry_by_value(webviews, webview_name)

                # check if method_name was called like
                # web_settings.method_name("false"), which makes it not vulnerable
                if (valid_set_method_bool(method_invocation=method_invocation, str_bool="false",
                                          method_name=method_name)
                        and webviews.get(webview_name)):
                    webviews = remove_dict_entry_by_value(webviews, webview_name)

        # any webview left in the dictionary is vulnerable,
        # and since there can be many variables for a single webview,
        # we will convert the values from the webviews dictionary into a set to create issues
        for webview in set(webviews.values()):
            issues.append(Issue(category=CATEGORY, name=issue_name, severity=severity,
                                description=description, line_number=webview.position,
                                file_object=file_object))

    return issues


def add_webview_to_dict(webviews, webview, java_type):
    """
    Takes a `webview` and adds it to the `webviews` dictionary if the type of webview is `java_type`

    :param dict webviews: dictionary of already existing webviews that are found
    :param webview: AST parsed object
    :param java_type: the type of class the webview should be
    :return: dictionary with the webview added
    :rtype: dict
    """
    webviews_return = webviews
    if isinstance(webview.type, Type) and webview.type.name == java_type:
        webviews_return = deepcopy(webviews_return)
        for declaration in webview.declarators:
            webviews_return[declaration.name] = webview

    return webviews_return


def ast_type_equals(node, pattern):
    """Small helper around how Javalang does its type checking for nodes."""
    return node == pattern or (isinstance(pattern, type) and isinstance(node, pattern))
