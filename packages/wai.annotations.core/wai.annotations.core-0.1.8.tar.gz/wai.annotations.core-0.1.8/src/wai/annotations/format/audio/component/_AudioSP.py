from wai.common.cli.options import TypedOption

from wai.annotations.core.component import SinkComponent
from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription


class AudioReaderSP(AnnotationFileProcessor[SpeechInstance]):
    """
    Dummy reader that turns a list of audio files into a speech dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(
            SpeechInstance(
                Audio.from_file(filename),
                Transcription("")
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(
            SpeechInstance(
                Audio.from_file(filename),
                None
            )
        )


class AudioWriterSP(
    SinkComponent[SpeechInstance]
):
    """
    Writes the audio files to the specified output directory.
    """

    output_dir: str = TypedOption(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="the directory to write the audio files to"
    )

    def consume_element(self, element: SpeechInstance):
        element.data.write_data_if_present(self.output_dir)

    def finish(self):
        pass

