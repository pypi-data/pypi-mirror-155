from .lsi import *  # noqa

try:
    from version import version
except ImportError:
    version = "unknown"
