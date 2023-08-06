import numpy as np
import soundfile

from io import BytesIO
from wai.annotations.domain.audio import AudioFormat


def convert_audio_format(data: np.ndarray, sample_rate: int, audio_format: AudioFormat):
    """
    Converts the audio data into the specified format.
    """
    if audio_format == AudioFormat.MP3:
        raise Exception("Cannot convert to MP3!")
    data_new = BytesIO()
    soundfile.write(data_new, data, sample_rate, format=audio_format.soundfile_format_string)
    data_new.seek(0)
    return data_new.read()
