from typing import Type, Tuple

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import ProcessorStageSpecifier


class ImageSegmentationISPSpecifier(ProcessorStageSpecifier):
    """
    Specifies the generic image segmentation ISP.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic image segmentation ISP."

    @classmethod
    def domain_transfer_function(
            cls,
            input_domain: Type[DomainSpecifier]
    ) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        if input_domain is ImageSegmentationDomainSpecifier:
            return input_domain
        else:
            raise Exception(
                f"Generic IS ISP only handles the following domains: "
                f"{ImageSegmentationDomainSpecifier.name()}"
            )

    @classmethod
    def components(cls) -> Tuple[Type[ProcessorComponent]]:
        from wai.annotations.generic.isp.base.component import BaseISP
        return BaseISP,
