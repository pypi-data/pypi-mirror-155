import librosa
import numpy as np

from typing import Optional, Tuple
from ...core.domain import Data
from ._AudioFormat import AudioFormat
from .util import convert_audio_format, load_audio_data


class Audio(Data):
    """
    Contains the information about an audio file.
    """
    def __init__(
            self,
            filename: str,
            data: Optional[bytes] = None,
            format: Optional[AudioFormat] = None,
            sample_rate: Optional[int] = None,
            audio_data: Optional[Tuple[np.ndarray, int]] = None,
    ):
        super().__init__(filename, data)

        self._format: AudioFormat = (
            format if format is not None
            else AudioFormat.for_filename(filename)
        )

        self._sample_rate: int = sample_rate
        self._audio_data: [Tuple[np.ndarray, int]] = audio_data

    @property
    def data(self) -> Optional[bytes]:
        """
        The binary contents of the file, if available.
        """
        if (self._data is None) and (self._audio_data is not None):
            self._data = convert_audio_format(self._audio_data[0], self._audio_data[1], self._format)
        return self._data

    @property
    def audio_data(self):
        """
        Returns a tuple of the audio data and sample rate.

        :return: the tuple of audio data and sample rate or None if no data available
        :rtype: Tuple[np.ndarray, int]
        """
        if self._audio_data is None:
            self._audio_data = load_audio_data(self.data, self.format, self._sample_rate) if (self.data is not None) else None
        return self._audio_data

    @property
    def format(self) -> AudioFormat:
        """
        Gets the format of this audio file.
        """
        return self._format

    def get_duration(self) -> float:
        """
        Returns the duration in seconds.
        CAUTION: has to read the data if not yet converted to audio_data tuple.

        :return: the duration in seconds.
        """
        return librosa.get_duration(self.audio_data[0], self.audio_data[1])

    def convert(self, to_format: AudioFormat) -> 'Audio':
        """
        Converts this audio file into another format.

        :param to_format:   The audio format to convert to.
        :return:            The converted audio object.
        """
        # If it's the same format, just make a copy
        if to_format is self._format:
            return Audio(
                self.filename,
                self.data,
                self.format,
                self._sample_rate
            )

        return Audio(
            to_format.replace_extension(self.filename),
            convert_audio_format(self.audio_data[0], self.audio_data[1], to_format) if self.data is not None else None,
            to_format,
            self._sample_rate
        )

    @classmethod
    def from_file_data(cls, file_name: str, file_data: bytes) -> 'Audio':
        return cls(file_name, file_data)
