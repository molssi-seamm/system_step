===========
System Step
===========

| |pull| |CI| |docs| |coverage| |lgtm| |PyUp|
| |Release| |PyPi|

A plug-in working with the system (molecular, periodic...) in a SEAMM flowchart

* Free software: BSD-3-Clause
* Developer Documentation: https://system-step.readthedocs.io
* User Documentation: https://molssi-seamm.github.io

.. |pull| image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/system_step
   :target: https://github.com/molssi-seamm/system_step/pulls
   :alt: GitHub pull requests

.. |CI| image:: https://github.com/molssi-seamm/system_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/system_step/actions?query=workflow%3ACI
   :alt: CI status

.. |docs| image:: https://readthedocs.org/projects/system-step/badge/?version=latest
   :target: https://system-step.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |coverage| image:: https://codecov.io/gh/molssi-seamm/system_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/system_step
   :alt: Code coverage

.. |lgtm| image:: https://img.shields.io/lgtm/grade/python/g/molssi-seamm/system_step.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/molssi-seamm/system_step/context:python
   :alt: Code Quality

.. |PyUp| image:: https://pyup.io/repos/github/molssi-seamm/system_step/shield.svg
   :target: https://pyup.io/repos/github/molssi-seamm/system_step/
   :alt: Updates for requirements

.. |Release| image:: https://github.com/molssi-seamm/system_step/workflows/Release/badge.svg
   :target: https://github.com/molssi-seamm/system_step/actions?query=workflow%3ARelease
   :alt: CI status for releases

.. |PyPi| image:: https://img.shields.io/pypi/v/system_step.svg
   :target: https://pypi.python.org/pypi/system_step
   :alt: Release version

Features
--------

This plug-in to the `SEAMM environment`_ provides an interface to the
simulation system. The system is the molecular or periodic
(crystalline) structure for the simulations. SEAMM allows you to work
with multiple systems, each of which may have more than one conformer
or configuration. This plug-in lets you choose which system and which
configuration of that system to use for the current simulation, and to
switch between them.

This plug-in currently supports

* Adding new systems
* Selecting with system to work with
* Adding conformers/configurations to a system
* Selecting which conformer/configuration to work with

.. _SEAMM environment: https://github.com/molssi-seamm

Credits
---------

This package was created with Cookiecutter_ and the
`molssi-seamm/cookiecutter-seamm-plugin`_ project template.

Developed by the Molecular Sciences Software Institute (MolSSI_),
which receives funding from the National Science Foundation under
award ACI-1547580

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin
.. _MolSSI: https://molssi.org
