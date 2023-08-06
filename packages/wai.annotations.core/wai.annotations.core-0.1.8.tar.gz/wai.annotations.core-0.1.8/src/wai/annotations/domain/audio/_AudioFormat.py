import os
from enum import Enum
from typing import Optional, FrozenSet
from itertools import chain

from wai.common.cli import CLIRepresentable


class AudioFormat(CLIRepresentable, Enum):
    """
    Class enumerating the types of audio files we can work with. Each enumeration's
    value is the set of possible file extensions for that audio type, followed
    by its soundfile format string.
    """
    WAV = frozenset({"wav", "WAV"}), "WAV"
    OGG = frozenset({"ogg", "OGG"}), "OGG"
    FLAC = frozenset({"flac", "FLAC"}), "FLAC"
    MP3 = frozenset({"mp3", "MP3"}), "MP3"

    @property
    def possible_extensions(self) -> FrozenSet[str]:
        """
        Gets the set of possible extensions for this format.
        """
        return self.value[0]

    @property
    def soundfile_format_string(self) -> str:
        """
        Gets the soundfile format string for this format.
        """
        return self.value[1]

    @classmethod
    def for_filename(cls, filename: str) -> Optional["AudioFormat"]:
        """
        Gets the audio format for a given audio filename.

        :param filename:    The audio filename.
        :return:            The audio format, or none if no format matched.
        """
        # Get the extension from the filename
        extension: str = os.path.splitext(filename)[1][1:]

        # Search for a format with this extension
        audio_format = cls.for_extension(extension)

        # If a format was found, return it
        if audio_format is not None:
            return audio_format

        # Otherwise it is an error
        raise ValueError(f"'{filename}' does not end in a recognised extension "
                         f"({', '.join(chain(*(audio_format.possible_extensions for audio_format in AudioFormat)))})")

    def replace_extension(self, filename: str) -> str:
        """
        Replaces the extension of an audio filename with the
        default extension for this format.

        :param filename:    The filename to modify.
        :return:            The new filename.
        """
        # Get the extension from the filename
        extension: str = os.path.splitext(filename)[1][1:]

        # Remove the extension from the filename
        filename = filename[:-len(extension)]

        # Choose a new extension for the filename
        extension = self.get_default_extension().upper() if extension.isupper() else self.get_default_extension()

        return filename + extension

    @classmethod
    def for_extension(cls, extension: str) -> Optional["AudioFormat"]:
        """
        Gets the audio format for the given extension.

        :param extension:   The extension.
        :return:            The audio format.
        """
        # Remove a leading dot if applicable
        if extension.startswith("."):
            extension = extension[1:]

        # Lowercase the extension
        extension = extension.lower()

        # Try find a format for the extension
        for audio_format in AudioFormat:
            if extension in audio_format.possible_extensions:
                return audio_format

        return None

    def get_default_extension(self) -> str:
        """
        Gets the default extension for the audio format.
        """
        return self.name.lower()

    def __str__(self) -> str:
        return self.get_default_extension()

    def cli_repr(self) -> str:
        return self.get_default_extension()

    @classmethod
    def from_cli_repr(cls, cli_string: str) -> 'AudioFormat':
        # The CLI representation is any known extension
        audio_format = cls.for_extension(cli_string)

        # If the extension is unknown, raise an issue
        if audio_format is None:
            raise ValueError(f"Unrecognised audio format '{cli_string}'")

        return audio_format
