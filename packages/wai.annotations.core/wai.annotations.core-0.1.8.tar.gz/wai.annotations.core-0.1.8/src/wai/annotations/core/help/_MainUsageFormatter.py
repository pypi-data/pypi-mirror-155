from argparse import ArgumentDefaultsHelpFormatter


class MainUsageFormatter(ArgumentDefaultsHelpFormatter):
    """
    Helper class for formatting the main usage message.
    """
    def _format_usage(self, *args, **kwargs):
        return super()._format_usage(*args, **kwargs)[:-2] + " [STAGE [STAGE ...]]\n\n"
