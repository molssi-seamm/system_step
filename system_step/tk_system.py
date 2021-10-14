# -*- coding: utf-8 -*-

"""The graphical part of a System step"""

import pprint  # noqa: F401
import tkinter as tk
import tkinter.ttk as ttk

import system_step  # noqa: F401
import seamm
from seamm_util import ureg, Q_, units_class  # noqa: F401
import seamm_widgets as sw


class TkSystem(seamm.TkNode):
    """
    The graphical part of a System step in a flowchart.

    Attributes
    ----------
    tk_flowchart : TkFlowchart = None
        The flowchart that we belong to.
    node : Node = None
        The corresponding node of the non-graphical flowchart
    namespace : str
        The namespace of the current step.
    tk_subflowchart : TkFlowchart
        A graphical Flowchart representing a subflowchart
    canvas: tkCanvas = None
        The Tk Canvas to draw on
    dialog : Dialog
        The Pmw dialog object
    x : int = None
        The x-coordinate of the center of the picture of the node
    y : int = None
        The y-coordinate of the center of the picture of the node
    w : int = 200
        The width in pixels of the picture of the node
    h : int = 50
        The height in pixels of the picture of the node
    self[widget] : dict
        A dictionary of tk widgets built using the information
        contained in System_parameters.py

    See Also
    --------
    System, TkSystem,
    SystemParameters,
    """

    def __init__(
        self,
        tk_flowchart=None,
        node=None,
        canvas=None,
        x=None,
        y=None,
        w=200,
        h=50
    ):
        """
        Initialize a graphical node.

        Parameters
        ----------
        tk_flowchart: Tk_Flowchart
            The graphical flowchart that we are in.
        node: Node
            The non-graphical node for this step.
        namespace: str
            The stevedore namespace for finding sub-nodes.
        canvas: Canvas
           The Tk canvas to draw on.
        x: float
            The x position of the nodes center on the canvas.
        y: float
            The y position of the nodes cetner on the canvas.
        w: float
            The nodes graphical width, in pixels.
        h: float
            The nodes graphical height, in pixels.

        Returns
        -------
        None
        """
        super().__init__(
            tk_flowchart=tk_flowchart,
            node=node,
            canvas=canvas,
            x=x,
            y=y,
            w=w,
            h=h
        )

    def create_dialog(self):
        """
        Create the dialog. A set of widgets will be chosen by default
        based on what is specified in the System_parameters
        module.

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkSystem.reset_dialog
        """

        super().create_dialog(title='System')
        # Shortcut for parameters
        P = self.node.parameters

        # Then create the widgets, first frames for system and configuration
        s_frame = self['system frame'] = ttk.LabelFrame(
            self['frame'],
            borderwidth=4,
            relief='sunken',
            text='Simulation System',
            labelanchor='n',
            padding=10
        )
        c_frame = self['configuration frame'] = ttk.LabelFrame(
            self['frame'],
            borderwidth=4,
            relief='sunken',
            text='Configuration/Conformer',
            labelanchor='n',
            padding=10
        )

        help_text = (
            'When choosing a system or configuration, you may use a numerical'
            '\nvalue, starting with 1, or a negative number to count back from'
            '\nthe end, starting with -1.'
            '\n'
            '\nYou can also use the name -- but if the name is not unique you '
            "\nwon't know which one you get."
            "\n"
            "\nFinally, 'current' refers to the currently selected one and"
            "\n'new' to the one just created."
        )
        w = ttk.Label(self['frame'], text=help_text, justify=tk.LEFT)

        self['use new configuration'] = ttk.Label(
            c_frame, text="The new configuration will be used."
        )

        s_frame.grid(row=0, column=0, sticky=tk.EW, pady=10)
        c_frame.grid(row=1, column=0, sticky=tk.EW, pady=10)
        w.grid(row=2, column=0, pady=10)

        for key in P:
            if key not in ('results', 'extra keywords', 'create tables'):
                if 'system' in key:
                    self[key] = P[key].widget(s_frame)
                elif 'configuration' in key:
                    self[key] = P[key].widget(c_frame)
                else:
                    self[key] = P[key].widget(self['frame'])

        # Set bindings
        for name in ('system operation', 'configuration operation', 'system'):
            combobox = self[name].combobox
            combobox.bind("<<ComboboxSelected>>", self.reset_dialog)
            combobox.bind("<Return>", self.reset_dialog)
            combobox.bind("<FocusOut>", self.reset_dialog)

        # and lay them out
        self.reset_dialog()

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog.

        The widgets are chosen by default from the information in
        System_parameter.

        This function simply lays them out row by row with
        aligned labels. You may wish a more complicated layout that
        is controlled by values of some of the control parameters.
        If so, edit or override this method

        Parameters
        ----------
        widget : Tk Widget = None

        Returns
        -------
        None

        See Also
        --------
        TkSystem.create_dialog
        """

        # Remove any widgets previously packed for the system
        frame = self['system frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        widgets = []
        widgets1 = []

        w = self['system operation']
        sysop = w.get()
        w.grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(w)
        row += 1

        if 'copy' in sysop:
            w = self['system to copy']
            w.grid(row=row, column=1, sticky=tk.EW)
            widgets1.append(w)
            row += 1

        if 'create' in sysop or 'copy' in sysop:
            w = self['system name']
            w.grid(row=row, column=1, sticky=tk.EW)
            widgets1.append(w)
            row += 1

        w = self['system']
        value = w.get()
        if 'create' in sysop or 'copy' in sysop:
            w.combobox.config(values=['current', 'new'])
        else:
            w.combobox.config(values=['current'])
            if value == 'new':
                w.set('current')
        w.grid(row=row, column=0, columnspan=2, sticky=tk.EW)
        widgets.append(w)
        row += 1

        # Align the labels
        sw.align_labels(widgets)
        sw.align_labels(widgets1)

        # Set the widths and expansion
        frame.columnconfigure(0, minsize=50)
        frame.columnconfigure(1, weight=1)

        # Remove any widgets previously packed for the configuration
        frame = self['configuration frame']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        widgets = []
        widgets1 = []

        if self['system'].get() == 'new':
            w = self['use new configuration']
            w.grid(row=row, column=0, columnspan=2, sticky=tk.W)
            widgets.append(w)
            row += 1
        else:
            w = self['configuration operation']
            operation = w.get()
            w.grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(w)
            row += 1

            if 'copy' in operation:
                w = self['configuration to copy']
                w.grid(row=row, column=1, sticky=tk.EW)
                widgets1.append(w)
                row += 1

            if 'create' in operation or 'copy' in operation:
                w = self['configuration name']
                w.grid(row=row, column=1, sticky=tk.EW)
                widgets1.append(w)
                row += 1

            w = self['configuration']
            value = w.get()
            if 'create' in operation or 'copy' in operation:
                w.combobox.config(values=['current', 'new'])
            else:
                w.combobox.config(values=['current'])
                if value == 'new':
                    w.set('current')
            w.grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            widgets.append(w)
            row += 1

        # Align the labels
        sw.align_labels(widgets)
        sw.align_labels(widgets1)

        # Set the widths and expansion
        frame.columnconfigure(0, minsize=50)
        frame.columnconfigure(1, weight=1)

    def right_click(self, event):
        """
        Handles the right click event on the node.

        Parameters
        ----------
        event : Tk Event

        Returns
        -------
        None

        See Also
        --------
        TkSystem.edit
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the System input

        Parameters
        ----------
        None

        Returns
        -------
        None

        See Also
        --------
        TkSystem.right_click
        """

        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):
        """Handle the closing of the edit dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.

        Parameters
        ----------
        result : None or str
            The value of this variable depends on what the button
            the user clicked.

        Returns
        -------
        None
        """

        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result)
            )

        self.dialog.deactivate(result)
        # Shortcut for parameters
        P = self.node.parameters

        # Get the values for all the widgets. This may be overkill, but
        # it is easy! You can sort out what it all means later, or
        # be a bit more selective.
        for key in P:
            P[key].set_from_widget()

    def handle_help(self):
        """Shows the help to the user when click on help button.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print('Help not implemented yet for System!')
