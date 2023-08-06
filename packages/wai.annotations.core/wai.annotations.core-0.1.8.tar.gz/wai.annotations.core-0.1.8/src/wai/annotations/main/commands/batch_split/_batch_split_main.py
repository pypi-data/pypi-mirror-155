"""
Module containing the main entry point function for getting information about
domains registered with wai.annotations.
"""
import os
import re
from itertools import chain
from random import Random
from typing import Dict, Tuple, Optional, Iterable, List

from wai.bynning.operations import split as bynning_split_op
from wai.common.cli import OptionsList

from ...logging import get_app_logger
from ._help import batch_split_help
from ._BatchSplitOptions import BatchSplitOptions, OUTPUT_NAMING_INPUT_DIR, OUTPUT_NAMING_ENUMERATE
from wai.annotations.core.util import chain_map, recursive_iglob, InstanceState, gcd


def batch_split_main(options: OptionsList):
    """
    Main method which handles the 'batch-split' sub-command.
    Splits batches of annotations into subsets individually.

    :param options:
                The options to the sub-command.
    """
    # Parse the options
    try:
        batch_split_options = BatchSplitOptions(options)
    except ValueError:
        get_app_logger().exception("Couldn't parse options to 'batch-split' command")
        print(batch_split_help())
        raise

    perform_batch_split(batch_split_options)


def load_file_names(direct_files: Iterable[str], seed: int = None) -> List[str]:
    """
    Loads the files and randomizes them, if a seed has been supplied.

    :param direct_files: the files with glob syntax (eg /some/where/*.xml or /else/where/**/*.report)
    :param seed: the seed value to use for randomizing the files, keeping order if None
    :return: the list of files
    """
    result = []
    for file_name in chain(chain_map(recursive_iglob, direct_files)):
        result.append(file_name)
    if (seed is not None) and (len(result) > 0):
        rnd = Random(seed)
        rnd.shuffle(result)
    return result


class Splitter(object):
    """
    Helper class for performing splits from a list of filenames.
    Based on code from wai.annotations.core.util.SplitSink
    """

    def __init__(self, names: List[str], ratios: List[int], file_names: List[str], regexp: str = None, groups: List[int] = None, verbose:bool = False):
        """
        Initializes the splitter with the names/ratios of the splits.

        :param names: the list of split names
        :param ratios: the list of split ratios
        :param file_names: the file names to split
        :param regexp: the regular expression to use for grouping file names into units that stay together
        :param groups: the list of group indices (starting at 1) to use for generating a unit of file names
        :param verbose: whether to output some debugging information
        """
        self.split_names = names
        self.split_ratios = ratios
        self.split_index = 0
        self.file_names = file_names
        self.regexp = regexp
        self.groups = groups
        self.verbose = verbose

    @InstanceState
    def _split_table(self) -> Dict[Optional[str], int]:
        """
        Table from split name to split ratio.
        """
        # Create a table from split-name to split-ratio
        table = {
            split_name: split_ratio
            for split_name, split_ratio
            in zip(self.split_names, self.split_ratios)
        }

        # Reduce each ratio to its lowest form
        table_gcd = gcd(*table.values())
        for split_name in table:
            table[split_name] //= table_gcd

        return table

    @InstanceState
    def _split_schedule(self) -> Tuple[str, ...]:
        """
        Creates a schedule of which split to assign elements to
        in order of discovery.
        """
        # If we're not splitting, return an empty schedule
        # Calculate a range over the length of the schedule
        schedule_range = range(sum(self._split_table.values()))

        # Create a mapping from split-name to schedule indices
        split_indices_by_name = {
            split_name: set(split_indices)
            for split_name, split_indices
            in bynning_split_op(schedule_range, **self._split_table).items()
        }

        return tuple(
            split_name
            for split_name, split_indices in split_indices_by_name.items()
            for index in schedule_range
            if index in split_indices
        )

    @property
    def _split_label(self) -> Optional[str]:
        """
        Retrieves the split label according to the schedule.
        """
        return self._split_schedule[self.split_index]

    def _move_to_next_split(self):
        """
        Increments the split index.
        """
        self.split_index = (self.split_index + 1) % len(self._split_schedule)

    def _group_file_names(self):
        """
        Groups the filenames into units, if necessary.

        :return: the grouped filenames
        :rtype: list
        """
        if (self.regexp is None) or (self.groups is None):
            return self.file_names

        units = {}
        for file_name in self.file_names:
            res = re.search(self.regexp, file_name)
            group_str = ""
            for i in range(len(self.groups)):
                if i > 0:
                    group_str += "\t"
                group_str += str(res.group(self.groups[i]))
            if group_str not in units:
                units[group_str] = []
            units[group_str].append(file_name)

        keys = list(units.keys())
        keys.sort()

        result = []
        for key in keys:
            result.append(units[key])

        return result

    def _ungroup_unit(self, unit):
        """
        Ungroups units of filenames.

        :param unit: the unit to ungroup
        :return: the ungrouped file names
        :rtype: list
        """
        if (self.regexp is None) or (self.groups is None):
            return [unit]
        else:
            return unit

    @InstanceState
    def splits(self) -> Dict[str, List[str]]:
        """
        Calculates and returns the splits.
        """
        if self.verbose:
            get_app_logger().debug("# files: %d" % len(self.file_names))
        result = dict()
        for split_name in self.split_names:
            result[split_name] = []
        units = self._group_file_names()
        if self.verbose and (self.regexp is not None):
            get_app_logger().debug("# units: %d" % len(units))
        for unit in units:
            label = self._split_label
            result[label].extend(self._ungroup_unit(unit))
            self._move_to_next_split()
        if self.verbose:
            for split_name in self.split_names:
                get_app_logger().debug("# files in split '%s': %d" % (split_name, len(result[split_name])))

        return result


def perform_batch_split(options: BatchSplitOptions):
    """
    Performs the batch split.

    :param options:
                The split options.
    """
    # If the help option is selected, print the usage and quit
    if options.HELP:
        print(batch_split_help())
        exit()

    # collate input patterns
    input_files = list(options.INPUTS)[:]
    for _dir in options.DIRS:
        input_files.append(os.path.join(_dir, options.GLOB))

    # locate/process files
    if options.GROUPING_GROUPS is None:
        groups = None
    else:
        groups = [int(x) for x in options.GROUPING_GROUPS.split(",")]
    for _input_index, _input in enumerate(input_files):
        # load files
        if options.VERBOSE:
            get_app_logger().debug("Processing: %s" % _input)
        all_file_names = load_file_names([_input], seed=options.SEED)
        if options.VERBOSE:
            get_app_logger().debug("# files found: %d" % len(all_file_names))

        # split files
        splitter = Splitter(names=options.SPLIT_NAMES, ratios=options.SPLIT_RATIOS, file_names=all_file_names,
                            regexp=options.GROUPING_REGEXP, groups=groups, verbose=options.VERBOSE)
        splits = splitter.splits

        # save splits
        for label in splits:
            file_names = splits[label]
            if options.VERBOSE:
                get_app_logger().debug("%s: %d" % (label, len(file_names)))

            # output file
            if options.OUTPUT_NAMING == OUTPUT_NAMING_ENUMERATE:
                name = str(_input_index+1)
            elif options.OUTPUT_NAMING == OUTPUT_NAMING_INPUT_DIR:
                name = os.path.basename(os.path.dirname(_input))
            else:
                raise Exception("Unhandled output naming: %s" % options.OUTPUT_NAMING)

            # create output dir if necessary
            if not os.path.exists(options.OUTPUT_DIR):
                if options.VERBOSE:
                    get_app_logger().debug("Creating output dir: %s" % options.OUTPUT_DIR)
                os.mkdir(options.OUTPUT_DIR)

            # save files
            out_file = os.path.join(options.OUTPUT_DIR, name + "-" + label + options.OUTPUT_EXT)
            if options.VERBOSE:
                get_app_logger().debug("Saving split to: %s" % out_file)
            with open(out_file, "w") as fp:
                for file_name in file_names:
                    fp.write(file_name)
                    fp.write("\n")
