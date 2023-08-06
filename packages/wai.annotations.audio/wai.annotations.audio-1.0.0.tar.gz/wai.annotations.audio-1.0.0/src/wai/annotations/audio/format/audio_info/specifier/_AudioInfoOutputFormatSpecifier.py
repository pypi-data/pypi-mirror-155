from abc import ABC
from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.specifier import SinkStageSpecifier


class AudioInfoOutputFormatSpecifier(SinkStageSpecifier, ABC):
    """
    Base specifier for the audio-info in each known domain.
    """
    @classmethod
    def description(cls) -> str:
        return "Collates and outputs information on the audio files."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.audio.format.audio_info.component import AudioInfo
        return AudioInfo,
