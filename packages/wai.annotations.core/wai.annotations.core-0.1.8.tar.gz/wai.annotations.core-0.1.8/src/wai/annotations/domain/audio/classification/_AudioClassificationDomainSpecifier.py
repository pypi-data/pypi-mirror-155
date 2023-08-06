from typing import Type

from ....core.domain import DomainSpecifier
from .._Audio import Audio
from ._AudioClassificationInstance import AudioClassificationInstance
from ...classification import Classification

DESCRIPTION = """Transcriptions of recorded speech.

The speech domain covers audio data of people speaking natural languages, annotated with text transcribing the verbal
contents of the audio. Instances in this domain are an audio file and a string containing the transcription.
"""


class AudioClassificationDomainSpecifier(DomainSpecifier[Audio, Classification]):
    """
    Domain specifier for audio recordings annotated with a label.
    """
    @classmethod
    def name(cls) -> str:
        return "Audio classification domain"
    
    @classmethod
    def description(cls) -> str:
        return DESCRIPTION
    
    @classmethod
    def data_type(cls) -> Type[Audio]:
        return Audio
    
    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification

    @classmethod
    def instance_type(cls) -> Type[AudioClassificationInstance]:
        return AudioClassificationInstance
