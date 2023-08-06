from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class ObjectDetectionSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the generic object detection sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic object detection sink."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.generic.sink.base.component import BaseSink
        return BaseSink,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.image.object_detection import ImageObjectDetectionDomainSpecifier
        return ImageObjectDetectionDomainSpecifier
