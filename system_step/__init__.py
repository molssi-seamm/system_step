# -*- coding: utf-8 -*-

"""
system_step
A step for working with the molecular/crystal system in SEAMM
"""

# Bring up the classes so that they appear to be directly in
# the system_step package.

from system_step.system import System  # noqa: F401, E501
from system_step.system_parameters import SystemParameters  # noqa: F401, E501
from system_step.system_step import SystemStep  # noqa: F401, E501
from system_step.tk_system import TkSystem  # noqa: F401, E501

# The metadata
from system_step.metadata import properties  # noqa: F401

# Handle versioneer
from ._version import get_versions

__author__ = """Paul Saxe"""
__email__ = 'psaxe@molssi.org'
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
