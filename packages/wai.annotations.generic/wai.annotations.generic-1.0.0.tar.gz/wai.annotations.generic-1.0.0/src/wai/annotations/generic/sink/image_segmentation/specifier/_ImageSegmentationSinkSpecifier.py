from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ImageSegmentationSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the generic image segmentation sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic image segmentation sink."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.generic.sink.base.component import BaseSink
        return BaseSink,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.segmentation import ImageSegmentationDomainSpecifier
        return ImageSegmentationDomainSpecifier
