from argparse import ArgumentParser
from typing import List

from wai.common.cli import CLIInstantiable
from wai.common.cli.options import FlagOption, TypedOption


OUTPUT_NAMING_ENUMERATE = "enumerate"
OUTPUT_NAMING_INPUT_DIR = "input_dir"
OUTPUT_NAMING_SCHEMES = [
    OUTPUT_NAMING_ENUMERATE,
    OUTPUT_NAMING_INPUT_DIR,
]


class BatchSplitOptions(CLIInstantiable):
    """
    The options for the 'batch-split' command.
    """
    # The name of the input annotation files to read from
    INPUTS: List[str] = TypedOption(
        "-i", "--input",
        type=str,
        nargs="+",
        metavar="FILENAME",
        action="concat",
        help="each -i/--input defines a single batch that gets split separately, to be used with glob syntax, e.g., '-i /some/where/*.xml'"
    )

    # The name of the directories with annotation files (use with --glob)
    DIRS: List[str] = TypedOption(
        "-d", "--dir",
        type=str,
        nargs="+",
        metavar="DIR",
        action="concat",
        help="the batch directories to look for files using the supplied glob expression (--glob)"
    )

    # The seed to use for randomisation of the read sequence
    GLOB: str = TypedOption(
        "-g", "--glob",
        type=str,
        default=None,
        help="the glob expression to apply when looking for files in the input directories (--dir), e.g., '*.xml'"
    )

    # The seed to use for randomisation of the read sequence
    SEED: int = TypedOption(
        "-s", "--seed",
        type=int,
        help="the seed value to use for randomizing the input files"
    )

    # the names for the splits
    SPLIT_NAMES = TypedOption(
        "-n", "--split-names",
        type=str,
        metavar="SPLIT NAME",
        nargs="*",
        help="the names to use for the batch splits"
    )

    # the ratios for splitting the batches
    SPLIT_RATIOS = TypedOption(
        "-r", "--split-ratios",
        type=int,
        metavar="RATIO",
        nargs="+",
        help="the ratios to use for the batch splits"
    )

    # The directory to write the split files to
    OUTPUT_DIR: str = TypedOption(
        "-o", "--output-dir",
        type=str,
        metavar="DIR",
        default="*",
        help="the directory to store the generated splits in as files"
    )

    # how to name the output files
    OUTPUT_NAMING: str = TypedOption(
        "-O", "--output-naming",
        type=str,
        metavar="NAMING",
        default=OUTPUT_NAMING_INPUT_DIR,
        help="how the generate the name for the created split files in the output directory: %s" % "|".join(OUTPUT_NAMING_SCHEMES)
    )

    # the suffix for the split files
    OUTPUT_EXT: str = TypedOption(
        "--output-ext",
        type=str,
        metavar="EXT",
        default=".list",
        help="the extension to use for the split files (incl dot)"
    )

    # the suffix for the split files
    GROUPING_REGEXP: str = TypedOption(
        "--grouping-regexp",
        type=str,
        metavar="REGEXP",
        default=None,
        help="the regular expression with groups for combining files into groups that get treated as a unit, e.g.: '([a-z]+)(-a|-b|-c)(-[a-z]+).csv'"
    )

    # the suffix for the split files
    GROUPING_GROUPS: str = TypedOption(
        "--grouping-groups",
        type=str,
        metavar="GROUPS",
        default=None,
        help="the comma-separated list of regular expression group indices (0: all, 1: first group, etc) that will make up the string for identifying files to treat as single unit, e.g.: '1,3'"
    )

    # Override the default help option
    VERBOSE = FlagOption(
        "-v", "--verbose",
        help="outputs debugging information"
    )

    # Override the default help option
    HELP = FlagOption(
        "-h", "--help",
        help="prints this help message and exits"
    )

    @classmethod
    def get_configured_parser(cls, *, add_help=False, **kwargs) -> ArgumentParser:
        return super().get_configured_parser(add_help=add_help, **kwargs)
