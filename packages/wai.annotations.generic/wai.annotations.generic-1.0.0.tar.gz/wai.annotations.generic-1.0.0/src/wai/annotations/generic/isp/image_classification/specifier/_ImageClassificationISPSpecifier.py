from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class ImageClassificationISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the generic image classification ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic image classification ISP."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.classification import ImageClassificationDomainSpecifier
        if input_domain is ImageClassificationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Generic IC ISP only handles the following domains: "
                f"{ImageClassificationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.generic.isp.base.component import BaseISP
        return BaseISP,
