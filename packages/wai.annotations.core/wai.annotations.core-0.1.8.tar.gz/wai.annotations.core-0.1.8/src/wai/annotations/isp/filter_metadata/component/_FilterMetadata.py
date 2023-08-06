from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.cli.options import TypedOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image.object_detection import ImageObjectDetectionInstance


TYPE_BOOL = "bool"
TYPE_NUMERIC = "numeric"
TYPE_STRING = "string"
TYPES = [
    TYPE_BOOL,
    TYPE_NUMERIC,
    TYPE_STRING,
]
TYPE_BOOL_ID = 0
TYPE_NUMERIC_ID = 1
TYPE_STRING_ID = 2
TYPE_IDS = {
    TYPE_BOOL: TYPE_BOOL_ID,
    TYPE_NUMERIC: TYPE_NUMERIC_ID,
    TYPE_STRING: TYPE_STRING_ID,
}

COMPARISON_L = 0
COMPARISON_LEQ = 1
COMPARISON_EQ = 2
COMPARISON_NEQ = 3
COMPARISON_GEQ = 4
COMPARISON_G = 5
COMPARISONS = {
    "=": COMPARISON_EQ,
    "==": COMPARISON_EQ,
    "!=": COMPARISON_NEQ,
    "<>": COMPARISON_NEQ,
    "<": COMPARISON_L,
    "<=": COMPARISON_LEQ,
    ">": COMPARISON_G,
    ">=": COMPARISON_GEQ,
}


class FilterMetadata(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, ImageObjectDetectionInstance]
):
    """
    Processes a stream of image object-detection instances,
    filtering out labels.
    """
    key: str = TypedOption("-k", "--key",
                      type=str,
                      help="the key of the meta-data value to use for the filtering")

    value_type: str = TypedOption("-t", "--value-type",
                        type=str,
                        help="the data type that the value represents, available options: %s" % "|".join(TYPES))

    comparison: str = TypedOption("-c", "--comparison",
                        type=str,
                        help="the comparison to apply to the value: for bool/numeric/string '=OTHER' and '!=OTHER' can be used, " 
                             "for numeric furthermore '<OTHER', '<=OTHER', '>=OTHER', '>OTHER'. "
                             "E.g.: '<3.0' for numeric types will discard any annotations that have a value of 3.0 or larger")

    def _initialize(self):
        """
        Initializes the state.
        """
        comparison = self.comparison
        if "=" in comparison:
            self._comparison_str = comparison[0:comparison.index("=") + 1]
        elif comparison.startswith("<"):
            self._comparison_str = comparison[0]
        elif comparison.startswith(">"):
            self._comparison_str = comparison[0]
        else:
            raise Exception("Unhandled comparison: %s" % self.comparison)

        self._comparison = COMPARISONS[self._comparison_str]
        value = comparison[len(self._comparison_str):]

        self._value_type = TYPE_IDS[self.value_type]
        if self._value_type == TYPE_BOOL_ID:
            self._comparison_value = bool(value)
        elif self._value_type == TYPE_NUMERIC_ID:
            self._comparison_value = float(value)
        else:
            self._comparison_value = value

    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        if not hasattr(self, "_comparison"):
            self._initialize()

        to_remove = []
        for i, lobj in enumerate(element.annotations):
            if self.key not in lobj.metadata:
                to_remove.append(i)
            else:
                value = lobj.metadata[self.key]
                try:
                    # bool
                    if self._value_type == TYPE_BOOL_ID:
                        value = bool(value)
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    # numeric
                    elif self._value_type == TYPE_NUMERIC_ID:
                        value = float(value)
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_L:
                            if not (value < self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_LEQ:
                            if not (value <= self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_G:
                            if not (value > self._comparison_value):
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_GEQ:
                            if not (value >= self._comparison_value):
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    # string
                    elif self._value_type == TYPE_STRING_ID:
                        if self._comparison == COMPARISON_EQ:
                            if value != self._comparison_value:
                                to_remove.append(i)
                        elif self._comparison == COMPARISON_NEQ:
                            if value == self._comparison_value:
                                to_remove.append(i)
                        else:
                            self.logger.error("Invalid comparison type: %s" % self._comparison_str)
                    else:
                        self.logger.error("Unhandled value type: %s" % self.value_type)
                        then(element)
                        return
                except:
                    self.logger.error("Failed to compare: %s" % str(value), exc_info=True)
                    to_remove.append(i)

        # remove objects that didn't meet criteria
        if len(to_remove) > 0:
            to_remove.reverse()
            for i in to_remove:
                element.annotations.pop(i)
            # no annotations left? -> mark as negative
            if len(element.annotations) == 0:
                element = ImageObjectDetectionInstance(data=element.data, annotations=None)

        then(element)
