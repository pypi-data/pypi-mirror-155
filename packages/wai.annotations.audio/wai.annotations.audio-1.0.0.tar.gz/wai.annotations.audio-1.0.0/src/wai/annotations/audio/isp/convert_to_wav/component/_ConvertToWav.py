import os

from wai.common.cli.options import TypedOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.audio import AudioInstance, Audio, AudioFormat


class ConvertToWav(
    RequiresNoFinalisation,
    ProcessorComponent[AudioInstance, AudioInstance]
):
    """
    Stream processor which converts mp3/flac/ogg to wav.
    """

    sample_rate: int = TypedOption(
        "-s", "--sample-rate",
        type=int,
        default=None,
        help="the sample rate to use for the audio data, for overriding the native rate."
    )

    def process_element(
            self,
            element: AudioInstance,
            then: ThenFunction[AudioInstance],
            done: DoneFunction
    ):
        filename_new = os.path.splitext(element.data.filename)[0] + "." + AudioFormat.WAV.get_default_extension()
        audio = Audio(
            filename_new,
            data=None,
            format=AudioFormat.WAV,
            sample_rate=element.data.audio_data[1],
            audio_data=element.data.audio_data)
        then(element.__class__(audio, element.annotations))
