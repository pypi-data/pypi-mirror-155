import os

from random import Random
from wai.common.cli.options import TypedOption, FlagOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.audio import AudioInstance

MIN_RAND = 0
MAX_RAND = 1000


AUG_MODE_REPLACE = "replace"
AUG_MODE_ADD = "add"
AUG_MODES = [
    AUG_MODE_REPLACE,
    AUG_MODE_ADD,
]


class BaseAudioAugmentation(
    RequiresNoFinalisation,
    ProcessorComponent[AudioInstance, AudioInstance]
):
    """
    Base class for stream processors that augment audios.
    """

    aug_mode: str = TypedOption(
        "-m", "--mode",
        type=str,
        default=AUG_MODE_REPLACE,
        help="the audio augmentation mode to use, available modes: %s" % ", ".join(AUG_MODES)
    )

    aug_suffix: str = TypedOption(
        "--suffix",
        type=str,
        help="the suffix to use for the file names in case of augmentation mode %s" % AUG_MODE_ADD
    )

    seed: int = TypedOption(
        "-s", "--seed",
        type=int,
        help="the seed value to use for the random number generator; randomly seeded if not provided"
    )

    seed_augmentation: bool = FlagOption(
        "-a", "--seed-augmentation",
        help="whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value from %d to %d for the augmentation." % (MIN_RAND, MAX_RAND)
    )

    threshold: float = TypedOption(
        "-T", "--threshold",
        type=float,
        help="the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)"
    )

    verbose: bool = FlagOption(
        "-v", "--verbose",
        help="whether to output debugging information"
    )

    def _default_suffix(self):
        """
        Returns the default suffix to use for audios when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        raise NotImplementedError()

    def _get_suffix(self):
        """
        Returns the suffix to use when using imgaug mode "add".

        :return: the suffix to use
        :rtype: str
        """
        if self.aug_suffix is None:
            return self._default_suffix()
        else:
            return self.aug_suffix

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return True

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
        raise NotImplementedError()

    def process_element(
            self,
            element: AudioInstance,
            then: ThenFunction[AudioInstance],
            done: DoneFunction
    ):
        # can we augment?
        if not self._can_augment():
            then(element)
            return

        threshold = 0.0 if self.threshold is None else self.threshold
        if (threshold < 0) or (threshold > 1):
            raise Exception("Threshold must satisfy x >= 0 and x <= 1, supplied: %f" % threshold)

        if not hasattr(self, "_random"):
            self._random = Random(self.seed)

        if self._random.random() < threshold:
            then(element)
            return

        # augment
        if self.seed_augmentation:
            aug_seed = self._random.randint(MIN_RAND, MAX_RAND)
        else:
            aug_seed = None
        element_out = self._augment(element, aug_seed)

        if self.aug_mode == AUG_MODE_ADD:
            then(element)
            # update filename for additional audio
            # TODO less hacky?
            parts = os.path.splitext(element_out.data.filename)
            element_out.data._filename = parts[0] + self._get_suffix() + parts[1]
            then(element_out)
        elif self.aug_mode == AUG_MODE_REPLACE:
            then(element_out)
        else:
            raise Exception("Unknown augmentation mode: %s" + self.aug_mode)
