from wai.common.cli.options import TypedOption
from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.generic.core import initialize_user_class


METHOD_NAME = "process_element"


class BaseISP(
    RequiresNoFinalisation,
    ProcessorComponent
):
    """
    Base class for generic stream processors.
    """

    user_class: str = TypedOption(
        "-c", "--class",
        type=str,
        help="the user class to wrap (dot notation)"
    )

    user_options: str = TypedOption(
        "-o", "--options",
        type=str,
        help="the options for the user class to parse"
    )

    def process_element(
            self,
            element,
            then: ThenFunction,
            done: DoneFunction
    ):
        if not hasattr(self, "_wrapped"):
            self._wrapped = initialize_user_class(self.user_class, self.user_options, ProcessorComponent)
            if not hasattr(self._wrapped, METHOD_NAME):
                raise Exception("Class %s is missing method '%s'!" % (self.user_class, METHOD_NAME))

        self._wrapped.process_element(element, then, done)
