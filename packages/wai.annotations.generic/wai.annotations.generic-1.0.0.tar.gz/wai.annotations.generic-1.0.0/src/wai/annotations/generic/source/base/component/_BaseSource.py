from wai.annotations.core.component import SourceComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.common.cli.options import TypedOption

from wai.annotations.generic.core import initialize_user_class

METHOD_NAME = "produce"


class BaseSource(SourceComponent):
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

    def produce(self, then: ThenFunction, done: DoneFunction):
        """
        Produces
        :param then:
        :param done:
        :return:
        """
        if not hasattr(self, "_wrapped"):
            self._wrapped = initialize_user_class(self.user_class, self.user_options, SourceComponent)
            if not hasattr(self._wrapped, METHOD_NAME):
                raise Exception("Class %s is missing method '%s'!" % (self.user_class, METHOD_NAME))

        self._wrapped.produce(then, done)
