from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class AudioACOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing audio files from from a classification dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy writer that just outputs audio files from classification datasets."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.format.audio.component import AudioWriterAC
        return AudioWriterAC,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        return AudioClassificationDomainSpecifier
