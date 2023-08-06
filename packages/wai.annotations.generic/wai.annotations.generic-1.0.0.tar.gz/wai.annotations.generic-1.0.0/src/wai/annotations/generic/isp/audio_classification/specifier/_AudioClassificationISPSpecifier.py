from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class AudioClassificationISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the generic audio classification ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic audio classification ISP."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.classification import AudioClassificationDomainSpecifier
        if input_domain is AudioClassificationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Generic AC ISP only handles the following domains: "
                f"{AudioClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.generic.isp.base.component import BaseISP
        return BaseISP,
