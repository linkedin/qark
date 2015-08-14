"""
Setup pubsub for the *arg1* message protocol. In a default pubsub installation
the default protocol is *kargs*.

This module must be imported before the first ``from pubsub import pub``
statement in the application. Once :mod:pub has been imported, the messaging
protocol must not be changed (i.e., importing it after the first
``from pubsub import pub`` statement has undefined behavior).
::

    from .. import setuparg1
    from .. import pub

The *arg1* protocol is identical to the legacy messaging protocol from
first version of pubsub (when it was still part of wxPython) and
is *deprecated*. This module is therefore *deprecated*.
"""

"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from . import policies
policies.msgDataProtocol = 'arg1'

import sys
sys.stdout.write("""

======================================================================
          ***    ATTENTION   ***
This messaging protocol is deprecated. This module, and hence arg1
messaging protocol, will be removed in v3.4 of PyPubSub. Please make
the necessary changes to your code so that it no longer requires this 
module. The pypubsub documentation provides steps that may be useful 
to minimize the chance of introducing bugs in your application.
======================================================================

""")


def enforceArgName(commonName):
    """This will configure pubsub to require that all listeners use
    the same argument name (*commonName*) as first parameter. This
    is a ueful first step in migrating an application that has been
    using *arg1* protocol to the more powerful *kwargs* protocol. """
    policies.setMsgDataArgName(1, commonName)
