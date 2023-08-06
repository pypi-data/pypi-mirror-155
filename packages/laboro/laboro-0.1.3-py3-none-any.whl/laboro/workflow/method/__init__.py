import logging
from laboro.logic.processor import Processor


class Method:
  """The ``laboro.workflow.method.Method`` object is a representation of a   ``laboro.workflow.action.Action`` method.

  Arguments:
    context: The ``laboro.context.Context`` instance used by the workflow.
    name: A string, specifying the method name.
    instance: An instance object derived from the ``laboro.module.Module`` class.
    args: A dictionary representation of the arguments that will be passed to the method call.
    output: String. A variable name in which the return value of the method will be stored for a later use within the workflow.
    when: Optional. A string representation of an expression thant can be evaluate as a boolean.
    loop: Optional. A string describing any iterable object.

  Returns:
    ``laboro.workflow.action.Action``
  """

  @property
  def iterable(self):
    """Get the *iterable* object on which loop, if any.
    This property is evaluated for each call from the ``loop`` attribute.
    """
    if self.loop is not None:
      return Processor().process(self.ctx, str(self.loop))
    return [self.loop]

  @property
  def runnable(self):
    """Get the condition in which the step is runnable.
    This property is evaluated for each call from the ``when`` attribute.
    """
    if self.when is not None:
      return Processor().process(self.ctx, str(self.when))
    return True

  def __init__(self, context, instance, name, args=None,
               output=None, when=None, loop=None):
    self.ctx = context
    self.instance = instance
    self.name = name
    self.when = when
    self.loop = loop
    self.args = args
    self.output = output

  def __enter__(self):
    return self

  def __exit__(self, kind, value, traceback):
    pass

  def _get_method_args(self):
    if self.args is not None:
      interpolated = self.args.copy()
      for key, value in interpolated.items():
        interpolated[key] = Processor().process_arg(self.ctx, str(value))
      return interpolated
    return dict()

  def run(self):
    for item in self.iterable:
      self.ctx.store.method_item = item
      if self.runnable:
        logging.getLogger().log_section("METHOD",
                                        f"{self.name}")
        method_args = self._get_method_args()
        self.ctx.register_method_secrets(self.instance,
                                         self.name,
                                         method_args)
        result = getattr(self.instance, self.name)(**method_args)
        if self.output is not None:
          self.ctx.put(self.output, result)
      else:
        msg = f"Skipping  {self.name}: Condition not met: {self.when}"
        logging.getLogger().log_section("METHOD", msg, level=logging.WARNING)
