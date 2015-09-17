"""
Top-level functionality related to message listeners. 
"""

"""
:copyright: Copyright since 2006 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE_BSD_Simple.txt for details.
"""

from .callables import (
    getID, 
    getArgs, 
    getRawFunction,
    ListenerMismatchError, 
    CallArgsInfo
)

from .listenerimpl import (
    Listener, 
    ListenerValidator
)

class IListenerExcHandler:
    """
    Interface class base class for any handler given to pub.setListenerExcHandler()
    Such handler is called whenever a listener raises an exception during a 
    pub.sendMessage(). Example::

        from pubsub import pub
        
        class MyHandler(pub.IListenerExcHandler):
            def __call__(self, listenerID, topicObj):
                ... do something with listenerID ...
                
        pub.setListenerExcHandler(MyHandler())
    """
    def __call__(self, listenerID, topicObj):
        raise NotImplementedError('%s must override __call__()' % self.__class__)


