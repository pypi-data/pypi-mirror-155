from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class AudioSPInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for turning audio files into a speech dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy reader that turns audio files into a speech dataset."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from wai.annotations.format.audio.component import AudioReaderSP
        return LocalFilenameSource, AudioReaderSP

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
