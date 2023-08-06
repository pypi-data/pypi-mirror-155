from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class SpeechSinkSpecifier(SinkStageSpecifier):
    """
    Specifies the generic speech sink.
    """
    @classmethod
    def description(cls) -> str:
        return "Generic speech sink."

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.generic.sink.base.component import BaseSink
        return BaseSink,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
