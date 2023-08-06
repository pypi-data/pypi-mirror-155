from random import Random

import librosa
from wai.annotations.domain.audio import AudioInstance, Audio, AudioFormat
from wai.common.cli.options import TypedOption

from wai.annotations.audio.isp.base_augmentation import BaseAudioAugmentation
from wai.annotations.audio.isp.resample.component import RESAMPLE_TYPE_DEFAULT, RESAMPLE_TYPES


class TimeStretch(BaseAudioAugmentation):
    """
    Stream processor to randomly stretching the audio.
    """

    rate_from: float = TypedOption(
        "-f", "--from-rate",
        type=float,
        help="the minimum stretch factor (<1: slow down, 1: same, >1: speed up)"
    )

    rate_to: float = TypedOption(
        "-t", "--to-rate",
        type=float,
        help="the maximum stretch factor (<1: slow down, 1: same, >1: speed up)"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-stretched"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.rate_from is not None) and (self.rate_to is not None)

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

        # determine rate
        rate = None
        if (self.rate_from is not None) and (self.rate_to is not None):
            if self.rate_from == self.rate_to:
                rate = self.rate_from
            else:
                rnd = Random(aug_seed)
                rate = rnd.random() * (self.rate_to - self.rate_from) + self.rate_from
            if self.verbose:
                self.logger.info("rate: %f" % rate)

        if rate is None:
            return element
        else:
            # apply stretch
            data, sample_rate = element.data.audio_data
            data = librosa.effects.time_stretch(data, rate=rate)
            audio = Audio(element.data.filename, format=AudioFormat.WAV, sample_rate=sample_rate, audio_data=(data, sample_rate))
            return element.__class__(audio, element.annotations)
