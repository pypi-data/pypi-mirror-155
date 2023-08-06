from typing import Type

from wai.annotations.core.domain import DomainSpecifier

from ._AudioInfoOutputFormatSpecifier import AudioInfoOutputFormatSpecifier


class AudioInfoSPOutputFormatSpecifier(AudioInfoOutputFormatSpecifier):
    """
    Specifier for audio-info in the speech domain.
    """
    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
