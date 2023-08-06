from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class MelSpectrogramISPSpecifier(ProcessorStageSpecifier):
    """
    Generates a plot from a Mel spectrogram.
    """
    @classmethod
    def description(cls) -> str:
        return "Generates a plot from a Mel spectrogram."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        if input_domain is AudioClassificationDomainSpecifier:
            return ImageClassificationDomainSpecifier
        else:
            raise Exception(
                f"MelSpectrogramISPSpecifier only handles the following domains: "
                f"{AudioClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.audio.xdc.mel_spectrogram.component import MelSpectrogram
        return MelSpectrogram,
