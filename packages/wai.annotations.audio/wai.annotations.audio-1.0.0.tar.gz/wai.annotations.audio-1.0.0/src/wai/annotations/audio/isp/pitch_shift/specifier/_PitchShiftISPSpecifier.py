from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class PitchShiftISPSpecifier(ProcessorStageSpecifier):
    """
    Augmentation method for shifting the pitch of audio files.
    """
    @classmethod
    def description(cls) -> str:
        return "Augmentation method for shifting the pitch of audio files."

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
                f"PitchShiftISPSpecifier only handles the following domains: "
                f"{AudioClassificationDomainSpecifier.name()}"
                f"{SpeechDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.audio.isp.pitch_shift.component import PitchShift
        return PitchShift,
