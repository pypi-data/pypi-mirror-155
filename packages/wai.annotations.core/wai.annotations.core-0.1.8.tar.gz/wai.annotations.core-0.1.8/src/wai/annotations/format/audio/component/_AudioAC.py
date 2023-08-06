from wai.common.cli.options import TypedOption

from wai.annotations.core.component import SinkComponent
from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.classification import AudioClassificationInstance
from wai.annotations.domain.classification import Classification


class AudioReaderAC(AnnotationFileProcessor[AudioClassificationInstance]):
    """
    Dummy reader that turns a list of audio files into a classification dataset.
    """
    def read_annotation_file(self, filename: str, then: ThenFunction[AudioClassificationInstance]):
        then(
            AudioClassificationInstance(
                Audio.from_file(filename),
                Classification("")
            )
        )

    def read_negative_file(self, filename: str, then: ThenFunction[AudioClassificationInstance]):
        then(
            AudioClassificationInstance(
                Audio.from_file(filename),
                None
            )
        )


class AudioWriterAC(
    SinkComponent[AudioClassificationInstance]
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

    def consume_element(self, element: AudioClassificationInstance):
        element.data.write_data_if_present(self.output_dir)

    def finish(self):
        pass

