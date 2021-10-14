# -*- coding: utf-8 -*-

"""Non-graphical part of the System step in a SEAMM flowchart
"""

import logging
import pprint  # noqa: F401

import system_step
import seamm
from seamm_util import ureg, Q_  # noqa: F401
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

# In addition to the normal logger, two logger-like printing facilities are
# defined: 'job' and 'printer'. 'job' send output to the main job.out file for
# the job, and should be used very sparingly, typically to echo what this step
# will do in the initial summary of the job.
#
# 'printer' sends output to the file 'step.out' in this steps working
# directory, and is used for all normal output from this step.

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('System')


class System(seamm.Node):
    """
    The non-graphical part of a System step in a flowchart.

    Attributes
    ----------
    parser : configargparse.ArgParser
        The parser object.

    options : tuple
        It contains a two item tuple containing the populated namespace and the
        list of remaining argument strings.

    subflowchart : seamm.Flowchart
        A SEAMM Flowchart object that represents a subflowchart, if needed.

    parameters : SystemParameters
        The control parameters for System.

    See Also
    --------
    TkSystem,
    System, SystemParameters
    """

    def __init__(
        self, flowchart=None, title='System', extension=None, logger=logger
    ):
        """A step for System in a SEAMM flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Parameters
        ----------
        flowchart: seamm.Flowchart
            The non-graphical flowchart that contains this step.

        title: str
            The name displayed in the flowchart.
        extension: None
            Not yet implemented
        logger : Logger = logger
            The logger to use and pass to parent classes

        Returns
        -------
        None
        """
        logger.debug('Creating System {}'.format(self))

        super().__init__(
            flowchart=flowchart,
            title='System',
            extension=extension,
            module=__name__,
            logger=logger
        )  # yapf: disable

        self.parameters = system_step.SystemParameters()

    @property
    def version(self):
        """The semantic version of this module.
        """
        return system_step.__version__

    @property
    def git_revision(self):
        """The git version of this module.
        """
        return system_step.__git_revision__

    def description_text(self, P=None):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.

        Parameters
        ----------
        P: dict
            An optional dictionary of the current values of the control
            parameters.
        Returns
        -------
        str
            A description of the current step.
        """
        if not P:
            P = self.parameters.values_to_dict()

        text = ""

        # Handle the system
        if self.is_expr(P['system operation']):
            text += (
                "The value of '{system operation}' will determine whether "
                "a new system will be created or copied, or if we switch "
                "to another existing system."
            )
        elif 'create' in P['system operation']:
            if P['system name'] == 'default':
                text += "A new system will be created, using the default name."
            else:
                text += "A new system named '{system name}' will be created"
        elif 'copy' in P['system operation']:
            if P['system name'] == 'default':
                text += (
                    "A new system named with the default name "
                    "will be created by copying the system '{system to copy}'."
                )
            else:
                text += (
                    "A new system named '{system name}' "
                    "will be created by copying the system '{system to copy}'."
                )
        elif 'use' not in P['system operation']:
            raise RuntimeError(
                f"Don't recognize the system operation {P['system operation']}"
            )

        # Handle the configuration
        text += "\n"
        if self.is_expr(P['configuration operation']):
            text += (
                "The value of '{configuration operation}' will determine "
                "whether a new configuration will be created or copied, or if "
                "we switch to another existing configuration."
            )
        elif 'create' in P['configuration operation']:
            if P['configuration name'] == 'default':
                text += (
                    "A new configuration will be created, using the default "
                    "name."
                )
            else:
                text += (
                    "A new configuration named '{configuration name}' will be "
                    "created"
                )
        elif 'copy' in P['configuration operation']:
            if P['configuration name'] == 'default':
                text += (
                    "A new configuration named with the default name "
                    "will be created by copying the configuration "
                    "'{configuration to copy}'."
                )
            else:
                text += (
                    "A new configuration named '{configuration name}' "
                    "will be created by copying the configuration "
                    "'{configuration to copy}'."
                )
        elif 'use' not in P['configuration operation']:
            raise RuntimeError(
                "Don't recognize the configuration operation "
                f"{P['configuration operation']}"
            )

        if P['system'] == 'current':
            text += ' Subsequent steps will continue to use the current system'
        elif P['system'] == 'new':
            text += ' Subsequent steps will use the newly created system'
        else:
            text += " Subsequent steps will use the system '{system}'"

        if P['configuration'] == 'current':
            text += ' and current configuration.'
        elif P['configuration'] == 'new':
            text += ' and the newly created configuration.'
        else:
            text += " and the configuration '{configuration}'."

        return self.header + '\n' + __(text, **P, indent=4 * ' ').__str__()

    def run(self):
        """Run a System step.

        Parameters
        ----------
        None

        Returns
        -------
        seamm.Node
            The next node object in the flowchart.
        """
        next_node = super().run(printer)
        # Get the values of the parameters, dereferencing any variables
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Print what we are doing -- getting formatted values for printing
        PP = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data,
            formatted=True,
            units=False
        )
        printer.normal(__(self.description_text(PP), indent=self.indent))

        # Get the system
        system_db = self.get_variable('_system_db')
        # configuration = system_db.system.configuration

        if 'create' in P['system operation']:
            if P['system name'] == 'default':
                system = system_db.create_system()
            else:
                system = system_db.create_system(P['system name'])
        elif 'copy' in P['system operation']:
            raise NotImplementedError('Cannot copy systems yet.')
            if P['system name'] == 'default':
                text += (
                    "A new system named with the default name "
                    "will be created by copying the system '{system to copy}'."
                )
            else:
                text += (
                    "A new system named '{system name}' "
                    "will be created by copying the system '{system to copy}'."
                )
        elif 'use' not in P['system operation']:
            raise RuntimeError(
                f"Don't recognize the system operation {P['system operation']}"
            )
        
        # Analyze the results
        self.analyze()

        # Add other citations here or in the appropriate place in the code.
        # Add the bibtex to data/references.bib, and add a self.reference.cite
        # similar to the above to actually add the citation to the references.

        return next_node

    def analyze(self, indent='', **kwargs):
        """Do any analysis of the output from this step.

        Also print important results to the local step.out file using
        'printer'.

        Parameters
        ----------
        indent: str
            An extra indentation for the output
        """
        printer.normal(
            __(
                'This is a placeholder for the results from the '
                'System step',
                indent=4 * ' ',
                wrap=True,
                dedent=False
            )
        )
