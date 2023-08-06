import librosa

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.audio import AudioInstance, Audio, AudioFormat


class ConvertToMono(
    RequiresNoFinalisation,
    ProcessorComponent[AudioInstance, AudioInstance]
):
    """
    Stream processor to turn audio into monophonic.
    """

    def process_element(
            self,
            element: AudioInstance,
            then: ThenFunction[AudioInstance],
            done: DoneFunction
    ):
        data, sample_rate = element.data.audio_data
        data = librosa.to_mono(data)
        audio = Audio(element.data.filename, format=AudioFormat.WAV, sample_rate=sample_rate, audio_data=(data, sample_rate))
        then(element.__class__(audio, element.annotations))
