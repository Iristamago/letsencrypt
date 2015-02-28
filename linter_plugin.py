"""Let's Encrypt ACME PyLint plugin.

http://docs.pylint.org/plugins.html

"""
from astroid import MANAGER
from astroid import nodes


def register(unused_linter):
    """Register this module as PyLint plugin."""

def _transform(cls):
    # fix the "no-member" error on instances of
    # letsencrypt.acme.util.ImmutableMap subclasses (instance
    # attributes are initialized dynamically based on __slots__)
    if (('Message' in cls.basenames or 'ImmutableMap' in cls.basenames or
         'util.ImmutableMap' in cls.basenames) and (cls.slots() is not None)):
        for slot in cls.slots():
            cls.locals[slot.value] = [nodes.EmptyNode()]


MANAGER.register_transform(nodes.Class, _transform)
