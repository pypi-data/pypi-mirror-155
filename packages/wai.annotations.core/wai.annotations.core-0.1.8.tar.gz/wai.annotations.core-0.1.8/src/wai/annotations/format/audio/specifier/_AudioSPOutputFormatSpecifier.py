from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class AudioSPOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing audio files from from a speech dataset.
    """
    @classmethod
    def description(cls) -> str:
        return "Dummy writer that just outputs audio files from speech datasets."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.format.audio.component import AudioWriterSP
        return AudioWriterSP,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
