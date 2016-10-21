"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Output
from cleo import OutputFormatterStyle
from cleo.styles import CleoStyle


class EnarkshStyle(CleoStyle):
    """
    Output style for Enarksh.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, input, output):
        """
        Object constructor.

        :param cleo.inputs.input.Input input: The input object.
        :param cleo.outputs.output.Output output: The output object.
        """
        CleoStyle.__init__(self, input, output)

        # Style for file system objects (e.g. file and directory names).
        style = OutputFormatterStyle('green', None, ['bold'])
        output.get_formatter().set_style('fso', style)

        # Style for errors.
        style = OutputFormatterStyle('red', None, ['bold'])
        output.get_formatter().set_style('err', style)

        # Style for warnings.
        style = OutputFormatterStyle('yellow', None, ['bold'])
        output.get_formatter().set_style('warn', style)

        # Style for Enarksh notices.
        style = OutputFormatterStyle('yellow')
        output.get_formatter().set_style('notice', style)

    # ------------------------------------------------------------------------------------------------------------------
    def log_verbose(self, message):
        """
        Logs a message only when logging level is verbose.

        :param str|list[str] message: The message.
        """
        if self.get_verbosity() >= Output.VERBOSITY_VERBOSE:
            self.writeln(message)

    # ------------------------------------------------------------------------------------------------------------------
    def log_very_verbose(self, message):
        """
        Logs a message only when logging level is very verbose.

        :param str|list[str] message: The message.
        """
        if self.get_verbosity() >= Output.VERBOSITY_VERY_VERBOSE:
            self.writeln(message)

# ----------------------------------------------------------------------------------------------------------------------
