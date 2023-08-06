from typing import Type

from .._AudioInstance import AudioInstance
from ...classification import Classification


class AudioClassificationInstance(AudioInstance[Classification]):
    """
    An instance in the audio classification domain.
    """
    @classmethod
    def annotations_type(cls) -> Type[Classification]:
        return Classification
