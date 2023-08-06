from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class AudioACInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for turning audio files into a classification dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy reader that turns audio files into a classification dataset."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from wai.annotations.format.audio.component import AudioReaderAC
        return LocalFilenameSource, AudioReaderAC

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        return AudioClassificationDomainSpecifier
