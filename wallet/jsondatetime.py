import json
import datetime
import dateutil.parser

try:
    string_types = basestring  # Python 2
except NameError:
    string_types = str  # Python 3

DEFAULT_DATE_FORMAT = '%a, %d %b %Y %H:%M:%S UTC'
DEFAULT_ARGUMENT = "datetime_format"


def iteritems(source):

    if not hasattr(source, 'items'):
        return source

    for k, v in source.items():
        if isinstance(v, list):
            for a in v:
                iteritems(a)
        elif isinstance(v, dict):
            iteritems(v)
        elif isinstance(v, string_types):
            try:
                source[k] = dateutil.parser.parse(v, ignoretz=True)
            except:
                pass

    return source