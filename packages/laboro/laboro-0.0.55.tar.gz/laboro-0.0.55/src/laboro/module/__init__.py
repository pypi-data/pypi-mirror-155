import os
import logging
from laboro.error import LaboroError
from laboro.validator import Validator


class Module:
  """The ``laboro.module.Module`` class is the base class from which each **Laboro** module must be derived from.

  It provides the ``@laboro_method`` decorator which must decorate any **public method** of a derived module.

  ..  code-block:: python

        from laboro.module import Module

        class MyModule(Module):
          def __init__(self, context, args):
            super().__init__(filepath=__file__, context=context, args=args)

        @Module.laboro_method
        def my_public_method(self, arg1, arg2):
          self._private_method(arg1)

        def _my_private_method(self, arg1):
          <do thing>

  Arguments:
    filepath: The file path of the module. From the derived class scope, it should be ``__file__``. The ``filepath`` arguement is used to retrieve the module *YAML* specification file.
    context: The ``laboro.context.Context`` associated with the ``laboro.workflow.Workflow`` instance instantiating the module. The ``context`` will be automatically provided by the workflow.
    args: A kwargs representing the module instance arguments.

  Returns:
    ``laboro.module.Module``

  Raises:
    laboro.error.LaboroError: When the ``args`` kwargs does not validate against the module specification or when the module specification does not validate the meta module specification.
  """
  def __init__(self, filepath, context, args=None):
    self.filepath = filepath
    self.context = context
    self.args = args
    self.specification = self._validate_spec()
    self._validate_args()

  @staticmethod
  def laboro_method(func):
    """The ``@laboro.module.Module.laboro_method`` decorator provides the way to validate the module methods arguments against the module method specification. All module derived from the `laboro.module.Module`` **must** decorate all their **public methods**.
    """
    def wrapper(self, *args, **kwargs):
      if len(args) > 1:
        logging.error("Using method with args instead of kwargs !")
        logging.warning("No argument checking will be done.")
        self.context.put(func.__name__, func(*args[1:]))
        return self.context.get(func.__name__)
      else:
        try:
          method = func.__name__
          methods = self.specification["methods"]
          method = [meth for meth in methods if meth["name"] == method][0]
          Validator().validate_method_args(method, kwargs)
        except IndexError as err:
          raise LaboroError(f"UnknownMethodError: Unknown method: {method}") from err
        self.context.put(func.__name__, func(self, **kwargs))
        return self.context.get(func.__name__)
    return wrapper

  def _validate_spec(self):
    """Load module specification from its YAML data file."""
    base_spec = os.path.join(os.path.dirname(__file__),
                             "schema",
                             "object.yml")
    spec_file = os.path.join(os.path.dirname(self.filepath),
                             "schema",
                             "specification.yml")
    return Validator().validate_instance(schema=base_spec,
                                         instance=spec_file)

  def _validate_args(self):
    """Validate arguments against a specification.
    """
    spec_file = os.path.join(os.path.dirname(self.filepath),
                             "schema",
                             "specification.yml")
    return Validator().validate_obj_args(specification=spec_file,
                                         args=self.args)

  def get_arg_value(self, arg):
    """Get the value of the specified argument.

    Arguments:
      arg: The argument to get the value from.

    Returns:
      The value of the searched argument. The type of the return value depend of the value of the searched argument.

    Raises:
      ``laboro.error.LaboroError``: When the specified argument is not known to the module.
    """
    if arg in self.args:
      return self.args[arg]
    msg = {"type": "UnknownModuleArgError",
           "message": f"Module argument not found: {arg}"}
    raise LaboroError(f"[{msg['type']}] {msg['message']}")

  def get_arg_value_as_string(self, arg):
    """Get the value of the specified argument as a string.

    Arguments:
      arg: The argument to get the value from.

    Returns:
      ``str``: The string representation of value of the searched argument.

    Raises:
      ``laboro.error.LaboroError``: When the specified argument is not known to the module.
    """
    if arg in self.args:
      return str(self.args[arg])
    msg = {"type": "UnknownModuleArgError",
           "message": f"Module argument not found: {arg}"}
    raise LaboroError(f"[{msg['type']}] {msg['message']}")
