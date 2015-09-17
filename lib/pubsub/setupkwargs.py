"""
Setup pubsub for the kwargs message protocol. In a default installation
this is the default protocol so this module is only needed if setupkargs
utility functions are used, or in a custom installation where kwargs 
is not the default messaging protocol (such as in some versions of 
wxPython). 

This module must be imported before the first ``from pubsub import pub``
statement in the application. Once :mod:pub has been imported, the messaging 
protocol cannot be changed (i.e., importing it after the first 
``from pubsub import pub`` statement has undefined behavior). 
"""

"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from . import policies
policies.msgDataProtocol = 'kwargs'


def transitionFromArg1(commonName):
    """Utility function to assist migrating an application from using 
    the arg1 messaging protocol to using the kwargs protocol. Call this 
    after having run and debugged your application with ``setuparg1.enforceArgName(commonName)``. See the migration docs
    for more detais. 
    """
    policies.setMsgDataArgName(2, commonName)
