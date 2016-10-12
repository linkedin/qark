"""
Aggregates policies for pubsub. Mainly, related to messaging protocol. 

:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

msgProtocolTransStage = None

msgDataProtocol    = 'kwargs'
msgDataArgName     = None
senderKwargNameAny = False


def setMsgDataArgName(stage, listenerArgName, senderArgNameAny=False):
    global senderKwargNameAny
    global msgDataArgName
    global msgProtocolTransStage
    senderKwargNameAny = senderArgNameAny
    msgDataArgName = listenerArgName
    msgProtocolTransStage = stage
    #print `policies.msgProtocolTransStage`, `policies.msgDataProtocol`, \
    #      `policies.senderKwargNameAny`, `policies.msgDataArgName`
    #print 'override "arg1" protocol arg name:', argName
