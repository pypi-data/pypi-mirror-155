"""
Provides the help information for the 'plugins' sub-command.
"""
from ....core.help import MainUsageFormatter
from ._PluginsOptions import PluginsOptions


def plugins_help() -> str:
    """
    Gets the help text for the 'plugins' sub-command.
    """
    return PluginsOptions.get_configured_parser(
        prog="wai-annotations plugins",
        description="Outputs command-line help information on one or more plugins, in plain text or markdown.",
        formatter_class=MainUsageFormatter).format_help()
