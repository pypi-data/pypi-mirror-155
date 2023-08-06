from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class TimeStretchISPSpecifier(ProcessorStageSpecifier):
    """
    Augmentation method for stretching the time of audio files (speed up/slow down).
    """
    @classmethod
    def description(cls) -> str:
        return "Augmentation method for stretching the time of audio files (speed up/slow down)."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        if input_domain is AudioClassificationDomainSpecifier:
            return input_domain
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        if input_domain is SpeechDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"TimeStretchISPSpecifier only handles the following domains: "
                f"{AudioClassificationDomainSpecifier.name()}"
                f"{SpeechDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.audio.isp.time_stretch.component import TimeStretch
        return TimeStretch,
