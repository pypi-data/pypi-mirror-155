import importlib
import shlex

from wai.common.cli import CLIInstantiable


def initialize_user_class(class_name, options, super_class):
    """
    Initializes the user supplied class, lets it parse its options and ensures
    that it is a subclass of the specified super class.

    :param class_name: the name of the class to instantiate (dot notation)
    :type class_name: str
    :param options: the command-line options to parse, can be None or empty
    :type options: str
    :param super_class: the super class the user class must be derived from
    :return: the instantiate class or Exception if failed to instantiate or not of the correct type
    :rtype: object
    """
    if class_name is None:
        raise Exception("No classname of user class provided!")
    if (options is None) or (len(options.strip()) == 0):
        option_list = []
    else:
        option_list = shlex.split(options)
    module_name, cls_name = class_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    if issubclass(cls, CLIInstantiable):
        result = cls(option_list)
    else:
        result = cls()
    if not isinstance(result, super_class):
        raise Exception("%s is not of type %s!" % (class_name, type(cls)))
    return result
