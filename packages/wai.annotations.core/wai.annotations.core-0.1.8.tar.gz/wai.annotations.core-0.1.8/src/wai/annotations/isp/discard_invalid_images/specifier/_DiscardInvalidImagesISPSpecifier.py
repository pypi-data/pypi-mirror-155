from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class DiscardInvalidImagesISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the discard-invalid-images ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Discards images that cannot be loaded (e.g., corrupt image file or annotations with no image)"

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.image import Image
        if input_domain.data_type() is Image:
            return input_domain
        else:
            raise Exception(f"DiscardInvalidImages only handles the image-based domains")

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...discard_invalid_images.component import DiscardInvalidImages
        return DiscardInvalidImages,
