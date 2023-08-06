from typing import Type, Tuple

from ....core.component import ProcessorComponent
from ....core.domain import DomainSpecifier
from ....core.specifier import ProcessorStageSpecifier


class FilterMetadataISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the filter-labels ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Filters detected objects based on their meta-data."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from ....domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        if input_domain is ImageObjectDetectionDomainSpecifier:
            return ImageObjectDetectionDomainSpecifier
        else:
            raise Exception(
                f"FilterMetadata only handles the "
                f"{ImageObjectDetectionDomainSpecifier.name()} domain"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from ...filter_metadata.component import FilterMetadata
        return FilterMetadata,
