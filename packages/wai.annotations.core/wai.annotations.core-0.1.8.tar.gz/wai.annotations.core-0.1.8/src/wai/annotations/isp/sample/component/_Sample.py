from random import Random
from ....core.component import ProcessorComponent
from ....core.domain import Instance
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from wai.common.cli.options import TypedOption


class Sample(
    RequiresNoFinalisation,
    ProcessorComponent[Instance, Instance]
):
    """
    ISP that selects a sub-sample from the stream.
    """

    seed: int = TypedOption(
        "-s", "--seed",
        type=int,
        help="the seed value to use for the random number generator; randomly seeded if not provided"
    )

    threshold: float = TypedOption(
        "-T", "--threshold",
        type=float,
        default=0.0,
        help="the threshold to use for Random.rand(): if equal or above, sample gets selected; range: 0-1; default: 0 (= always)"
    )

    def process_element(
            self,
            element: Instance,
            then: ThenFunction[Instance],
            done: DoneFunction
    ):
        threshold = 0.0 if self.threshold is None else self.threshold
        if (threshold < 0) or (threshold > 1):
            raise Exception("Threshold must satisfy x >= 0 and x <= 1, supplied: %f" % threshold)

        if self.threshold == 1.0:
            then(element)
            return

        if not hasattr(self, "_random"):
            self._random = Random(self.seed)

        if self._random.random() >= threshold:
            then(element)

