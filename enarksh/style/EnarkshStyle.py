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

# ----------------------------------------------------------------------------------------------------------------------
