from wai.annotations.core.component import SinkComponent
from wai.common.cli.options import TypedOption

from wai.annotations.generic.core import initialize_user_class

METHOD_NAME_CONSUME = "consume_element"
METHOD_NAME_FINISH = "finish"


class BaseSink(SinkComponent):
    """
    Base class for generic sinks.
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

    def consume_element(self, element):
        """
        Consumes instances.
        """
        if not hasattr(self, "_wrapped"):
            self._wrapped = initialize_user_class(self.user_class, self.user_options, SinkComponent)
            if not hasattr(self._wrapped, METHOD_NAME_CONSUME):
                raise Exception("Class %s is missing method '%s'!" % (self.user_class, METHOD_NAME_CONSUME))

        self._wrapped.consume_element(element)

    def finish(self):
        if hasattr(self._wrapped, METHOD_NAME_FINISH):
            self._wrapped.finish()
