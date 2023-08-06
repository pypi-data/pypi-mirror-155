from random import Random

import librosa
from wai.annotations.domain.audio import AudioInstance, Audio, AudioFormat
from wai.common.cli.options import TypedOption

from wai.annotations.audio.isp.base_augmentation import BaseAudioAugmentation
from wai.annotations.audio.isp.resample.component import RESAMPLE_TYPE_DEFAULT, RESAMPLE_TYPES


class PitchShift(BaseAudioAugmentation):
    """
    Stream processor to randomly change the pitch.
    """

    steps_from: float = TypedOption(
        "-f", "--from-steps",
        type=float,
        help="the minimum (fractional) steps to shift"
    )

    steps_to: float = TypedOption(
        "-t", "--to-steps",
        type=float,
        help="the maximum (fractional) steps to shift"
    )

    bins_per_octave: float = TypedOption(
        "--bins-per-octave",
        type=int,
        default=12,
        help="how many steps per octave"
    )

    resample_type: str = TypedOption(
        "--resample-type",
        type=str,
        default=RESAMPLE_TYPE_DEFAULT,
        help="the resampling type to apply (%s)" % "|".join(RESAMPLE_TYPES)
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-shifted"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.steps_from is not None) and (self.steps_to is not None)

    def _augment(self, element: AudioInstance, aug_seed: int):
        """
        Augments the audio.

        :param element: the audio to augment
        :type element: AudioInstance
        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :return: the potentially updated audio
        :rtype: AudioInstance
        """

        # determine steps
        steps = None
        if (self.steps_from is not None) and (self.steps_to is not None):
            if self.steps_from == self.steps_to:
                steps = self.steps_from
            else:
                rnd = Random(aug_seed)
                steps = rnd.random() * (self.steps_to - self.steps_from) + self.steps_from
            if self.verbose:
                self.logger.info("steps: %f" % steps)

        if steps is None:
            return element
        else:
            # apply shift
            data, sample_rate = element.data.audio_data
            data = librosa.effects.pitch_shift(data, sr=sample_rate, n_steps=steps, bins_per_octave=self.bins_per_octave, res_type=self.resample_type)
            audio = Audio(element.data.filename, format=AudioFormat.WAV, sample_rate=sample_rate, audio_data=(data, sample_rate))
            return element.__class__(audio, element.annotations)
