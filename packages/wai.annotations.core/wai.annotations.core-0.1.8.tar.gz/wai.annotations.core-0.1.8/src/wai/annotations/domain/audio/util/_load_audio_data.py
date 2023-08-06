import os
import librosa
import numpy as np
import tempfile
import time

from typing import Tuple
from wai.annotations.domain.audio import AudioFormat


def _load_from_disk(data: bytes, audio_format: AudioFormat, sample_rate: int = None) -> Tuple[np.ndarray, int]:
    """
    Dumps the data on disk in a temp file and loads it from there.

    :param data: the data to load from disk
    :param audio_format: the obtain the file extension from
    :param sample_rate: the sample rate to load the data with
    :return: tuple of audio time series and sample rate
    """
    filename_tmp = os.path.join(tempfile.gettempdir(), "waiann-%d.%s" % (round(time.time()), audio_format.get_default_extension()))
    with open(filename_tmp, "wb") as fp:
        fp.write(data)
        fp.close()
    data, sample_rate = librosa.load(filename_tmp, sr=sample_rate, mono=False)
    try:
        os.remove(filename_tmp)
    except:
        pass
    return data, sample_rate


def load_audio_data(data: bytes, audio_format: AudioFormat, sample_rate: int = None) -> Tuple[np.ndarray, int]:
    """
    Loads the audio data from the file data.

    :param data: the audio file data
    :param audio_format: the format of the audio data
    :param sample_rate: the sample_rate to use if other than native
    :return: the tuple of audio time series and sample rate
    """
    # mp3 files cannot be loaded from bytes
    if audio_format == AudioFormat.MP3:
        return _load_from_disk(data, audio_format, sample_rate=sample_rate)
    else:
        try:
            return librosa.load(data, sr=sample_rate, mono=False)
        except:
            # unfortunately, not all wav files can be loaded from bytes, so need reloading from disk
            return _load_from_disk(data, audio_format, sample_rate=sample_rate)
