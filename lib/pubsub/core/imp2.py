"""
The _resolve_name and _import_module were taken from the backport of 
importlib.import_module from 3.x to 2.7. Thanks to the Python developers
for making this available as a standalone module. This makes it possible
to have an import module that mimics the "import" statement more
closely.
"""

import sys
from .. import py2and3

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in py2and3.xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def _import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.
    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

    
def load_module(moduleName, searchPath):
    """Try to import moduleName. If this doesn't work, use the "imp" module
    that is part of Python. """
    try: 
        module = _import_module(moduleName) 
        
    except:
        import imp
        fp, pathname, description = imp.find_module(moduleName, searchPath)
        try:
            module = imp.load_module(moduleName, fp, pathname, description)
            
        finally:
            # Since we may exit via an exception, close fp explicitly.
            if fp:
                fp.close()
                
    return module
