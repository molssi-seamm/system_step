# -*- coding: utf-8 -*-
"""
Control parameters for the System step in a SEAMM flowchart
"""

import logging
import seamm
import pprint  # noqa: F401

logger = logging.getLogger(__name__)


class SystemParameters(seamm.Parameters):
    """The control parameters for System.

    The developer will add a dictionary of Parameters to this class.
    The keys are parameters for the current plugin, which themselves
    might be dictionaries.

    You need to replace the 'time' example below with one or more
    definitions of the control parameters for your plugin and application.

    Attributes
    ----------
    parameters : dict(str)
        A dictionary containing the parameters for the current step.
        Each key of the dictionary is a dictionary that contains the
        the following keys:

        kind : custom
            Specifies the kind of a variable. While the 'kind' of a
            variable might be a numeric value, it may still have
            enumerated custom values meaningful to the user. For
            instance, if the parameter is a convergence criterion for
            an optimizer, custom values like 'normal', 'precise', etc,
            might be adequate. In addition, any parameter can be set
            to a variable of expression, indicated by having '$' as
            the first character in the field. For example,
            $OPTIMIZER_CONV.
        default : str
            One of 'integer', 'float', 'string', 'boolean' or 'enum'. The
            default value of the parameter, used to reset it.
        default_units : str
            The default units, used for resetting the value.
        enumeration : tuple
            A tuple of enumerated values.
        format_string : str
            A format string for 'pretty' output.
        description : str
            A short string used as a prompt in the GUI.
        help_text : tuple
            A longer string to display as help for the user.

    See Also
    --------
    System, TkSystem, System
    SystemParameters, SystemStep

    Examples
    --------
    parameters = {
        "time": {
            "default": 100.0,
            "kind": "float",
            "default_units": "ps",
            "enumeration": tuple(),
            "format_string": ".1f",
            "description": "Simulation time:",
            "help_text": ("The time to simulate in the dynamics run.")
        },
    }
    """

    parameters = {
        "system operation": {
            "default": 'use an existing system',
            "kind": "enum",
            "default_units": None,
            "enumeration": (
                'create a new, empty system',
                'copy an existing system',
                'use an existing system'
            ),
            "format_string": "s",
            "description": "What you want to do:",
            "help_text": ("The operation for the simulation system.")
        },
        "system to copy": {
            "default": "current",
            "kind": "integer",
            "default_units": None,
            "enumeration": (
                "current",
                "new",
            ),
            "format_string": "d",
            "description": "System to copy:",
            "help_text": ("The simulation system to copy.")
        },
        "system name": {
            "default": "default",
            "kind": "string",
            "default_units": None,
            "enumeration": (
                "default",
            ),
            "format_string": "s",
            "description": "Name for the new system:",
            "help_text": ("The name for the simulation system.")
        },
        "system": {
            "default": "current",
            "kind": "integer",
            "default_units": None,
            "enumeration": (
                "current",
                "new",
            ),
            "format_string": "d",
            "description": "Which system to use:",
            "help_text": ("The simulation system to use.")
        },
        "configuration operation": {
            "default": 'use an existing configuration',
            "kind": "enum",
            "default_units": None,
            "enumeration": (
                'copy an existing configuration',
                'create a new configuration',
                'use an existing configuration'
            ),
            "format_string": "s",
            "description": "What you want to do:",
            "help_text": ("The operation for the configuration.")
        },
        "configuration to copy": {
            "default": "current",
            "kind": "integer",
            "default_units": None,
            "enumeration": (
                "current",
                "new",
            ),
            "format_string": "d",
            "description": "Configuration to copy:",
            "help_text": ("The simulation configuration to copy.")
        },
        "configuration name": {
            "default": "default",
            "kind": "string",
            "default_units": None,
            "enumeration": (
                "default",
            ),
            "format_string": "s",
            "description": "Name for the new configuration:",
            "help_text": ("The name for the configuration.")
        },
        "configuration": {
            "default": "current",
            "kind": "integer",
            "default_units": None,
            "enumeration": (
                "current",
                "new"
            ),
            "format_string": "d",
            "description": "Which configuration to use:",
            "help_text": ("The configuration to use.")
        },
    }

    def __init__(self, defaults={}, data=None):
        """
        Initialize the parameters, by default with the parameters defined above

        Parameters
        ----------
        defaults: dict
            A dictionary of parameters to initialize. The parameters
            above are used first and any given will override/add to them.
        data: dict
            A dictionary of keys and a subdictionary with value and units
            for updating the current, default values.

        Returns
        -------
        None
        """

        logger.debug('SystemParameters.__init__')

        super().__init__(
            defaults={**SystemParameters.parameters, **defaults},
            data=data
        )
