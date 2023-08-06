import librosa

from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.audio import AudioInstance, Audio, AudioFormat


class TrimAudio(
    RequiresNoFinalisation,
    ProcessorComponent[AudioInstance, AudioInstance]
):
    """
    Stream processor to trim silence from audio.
    """

    top_db: int = TypedOption(
        "--top-db",
        type=int,
        default=60,
        help="the threshold (in decibels) below reference to consider as silence."
    )

    frame_length: int = TypedOption(
        "--frame-length",
        type=int,
        default=2048,
        help="the number of samples per analysis frame."
    )

    hop_length: int = TypedOption(
        "--hop-length",
        type=int,
        default=512,
        help="the number of samples between analysis frames"
    )

    verbose: bool = FlagOption(
        "-v", "--verbose",
        help="whether to output some debugging output"
    )

    def process_element(
            self,
            element: AudioInstance,
            then: ThenFunction[AudioInstance],
            done: DoneFunction
    ):
        data, sample_rate = element.data.audio_data
        if self.verbose:
            self.logger.info("before trim: %s" % str(data.shape))
        data, index = librosa.effects.trim(data, top_db=self.top_db, frame_length=self.frame_length, hop_length=self.hop_length)
        if self.verbose:
            self.logger.info("after trim: %s" % str(data.shape))
        audio = Audio(element.data.filename, format=AudioFormat.WAV, sample_rate=sample_rate, audio_data=(data, sample_rate))
        then(element.__class__(audio, element.annotations))
