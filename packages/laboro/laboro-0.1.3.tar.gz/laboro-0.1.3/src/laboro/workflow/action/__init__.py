import logging
from laboro.logic.processor import Processor
from laboro.workflow.method import Method


class Action:
  """The ``laboro.workflow.action.Action`` object is a representation of a   ``laboro.workflow.step.Step`` action.

  Arguments:
    context: The ``laboro.context.Context`` instance used by the workflow.
    name: A string, specifying the action name.
    instance: A dictionary representation of ``instance`` as specified in the ``laboro.workflow.Workflow`` specification.
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

  def __init__(self, context, name, instance, when=None, loop=None):
    self.ctx = context
    self.name = name
    self.when = when
    self.loop = loop
    self.instance = instance

  def __enter__(self):
    return self

  def __exit__(self, kind, value, traceback):
    pass

  def _get_instance_args(self, instance):
    if "args" in instance:
      interpolated = instance["args"].copy()
      for key, value in interpolated.items():
        interpolated[key] = Processor().process_arg(self.ctx, str(value))
      return interpolated
    return dict()

  def run(self):
    """Run the action.
    If the ``runnable`` property evaluate to ``True``, calling the ``run()`` method will instantiate the instance when needed and run all ``methods`` within the instance methods list.
    The methods within instance methods list will be executed for each item in the ``iterable`` property.
    """
    for item in self.iterable:
      self.ctx.store.action_item = item
      if self.runnable:
        logging.getLogger().log_section("ACTION", self.name)
        cls = self.instance["class"]
        cls_args = self._get_instance_args(self.instance)
        if self.instance["instantiate"]:
          instance = self.ctx.instantiate(module=self.instance["module"],
                                          cls=cls,
                                          args=cls_args)
          self.ctx.put(self.instance["name"], instance)
        else:
          instance = self.ctx.get(self.instance["name"])
        for action_method in self.instance["methods"]:
          with Method(self.ctx, instance, **action_method) as method:
            method.run()
      else:
        msg = f"Skipping {self.name}: Condition not met: {self.when}"
        logging.getLogger().log_section("STEP", msg, level=logging.WARNING)
