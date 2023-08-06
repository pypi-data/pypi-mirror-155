"""
Provides the help information for the 'batch-split' sub-command.
"""
from ....core.help import MainUsageFormatter
from ._BatchSplitOptions import BatchSplitOptions


def batch_split_help() -> str:
    """
    Gets the help text for the 'batch-split' sub-command.
    """
    return BatchSplitOptions.get_configured_parser(
        prog="wai-annotations batch-split",
        description="When datasets contain multiple batches, it is recommended to get the same distribution "
                    "of each batch when generating train/test/validation datasets. The 'batch-split' command "
                    "allows you to generate these splits for each batch separately, outputting .list files "
                    "that can be used as input for conversion plugins (using '-I' instead of '-i'). "
                    "Furthermore, it is possible to group files within a batch that should stay together, "
                    "e.g.,images that depict the same object(s) and can be distinguished via a prefix "
                    "or suffix. The grouping is achieved via regular expression groups.",
        formatter_class=MainUsageFormatter).format_help()
