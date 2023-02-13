"""
Utilities

This module contains other miscellaneous helpful things that don't seem to
have a home anywhere else.  The flags defined here can be used to help code
adapt depending on which OS it is running.
"""

import platform

is_linux = (platform.system() == 'Linux')
is_windows = (platform.system() == 'Windows')
