from argparse import ArgumentDefaultsHelpFormatter


class PluginUsageFormatter(ArgumentDefaultsHelpFormatter):
    """
    Helper class for formatting the usage options of plugin components.
    """
    def __init__(self,
                 prog,
                 indent_increment=2,
                 max_help_position=24,
                 width=100,
                 start_indent=0):
        super().__init__(prog,
                         indent_increment=indent_increment,
                         max_help_position=max_help_position,
                         width=width)

        self._current_indent = start_indent
