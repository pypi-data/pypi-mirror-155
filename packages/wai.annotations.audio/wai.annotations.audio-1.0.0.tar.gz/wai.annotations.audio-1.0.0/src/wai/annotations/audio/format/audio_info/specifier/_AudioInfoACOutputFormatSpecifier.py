from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._AudioInfoOutputFormatSpecifier import AudioInfoOutputFormatSpecifier


class AudioInfoACOutputFormatSpecifier(AudioInfoOutputFormatSpecifier):
    """
    Specifier for audio-info in the audio classification domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        return AudioClassificationDomainSpecifier
