"""
Compatibility layer and utilities.
"""
import sys

PY3 = sys.version_info[0] >= 3

if PY3:
    from io import StringIO  # noqa
    import urllib.parse as urlparse

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    str_types = (str)
else:
    import urlparse
    from StringIO import StringIO  # noqa

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    str_types = (str, unicode)
