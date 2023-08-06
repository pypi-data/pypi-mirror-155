from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class ConvertToMonoISPSpecifier(ProcessorStageSpecifier):
    """
    Converts audio files to monophonic.
    """
    @classmethod
    def description(cls) -> str:
        return "Converts audio files to monophonic."

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
                f"ConvertToMonoISPSpecifier only handles the following domains: "
                f"{AudioClassificationDomainSpecifier.name()}"
                f"{SpeechDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.audio.isp.convert_to_mono.component import ConvertToMono
        return ConvertToMono,
