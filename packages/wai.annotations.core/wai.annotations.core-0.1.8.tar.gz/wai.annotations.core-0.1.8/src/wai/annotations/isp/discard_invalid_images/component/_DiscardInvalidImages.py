from wai.common.cli.options import FlagOption

from ....core.component import ProcessorComponent
from ....core.stream import ThenFunction, DoneFunction
from ....core.stream.util import RequiresNoFinalisation
from ....domain.image import ImageInstance


class DiscardInvalidImages(
    RequiresNoFinalisation,
    ProcessorComponent[ImageInstance, ImageInstance]
):
    """
    Processes a stream of image-based instances, discarding invalid images
    (eg corrupt files or annotations with not file attached).
    """

    verbose = FlagOption(
        "-v", "--verbose",
        help="whether to output debugging information"
    )

    def process_element(
            self,
            element: ImageInstance,
            then: ThenFunction[ImageInstance],
            done: DoneFunction
    ):
        # no data?
        if (element.data.data is None) or (len(element.data.data) == 0):
            if self.verbose:
                self.logger.info("No image data, skipping!")
            return

        # try reading the data
        try:
            img = element.data.pil_image
            if img is None:
                return
        except:
            if self.verbose:
                self.logger.info("Failed to read image data, skipping!")
            return

        then(element)
