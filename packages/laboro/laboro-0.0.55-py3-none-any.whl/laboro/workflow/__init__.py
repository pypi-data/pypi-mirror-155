import re
import uuid
import logging
from laboro.logic.processor import Processor


class Workflow:
  """The ``laboro.workflow.Workflow`` object is the main class for the workflow representation.
  It load all configuration needed, set alk objects such History, Vault and workspace and run according to its configuration.

  The Workflow object provides a runtime context that will handle log, history, vault, and workspace, etc.

  Arguments:
    name: A string representing the workflow name.
    context: A ``laboro.context.Context`` instance.

  Returns:
    ``laboro.workflow.Workflow``: A Workflow object.

  ..  code-block:: python

      from laboro.vault import Vault()
      from laboro.log.manager import Manager as LogMgr
      from laboro.context import Context
      from laboro.workflow import Workflow

      logmgr = LogMgr(vault=Vault())
      context = Context(logger=logmgr)
      with Workflow(name="my_workflow", context=context) as wkf:
        wkf.run()
        ...
  """
  def __init__(self, name, context):
    self.name = name
    self.session = str(uuid.uuid4())
    self.ctx = context.reset(self.name, self.session)

  def __enter__(self):
    return self

  def __exit__(self, kind, value, traceback):
    self.ctx.exit(self.name, self.session, kind, value)

  def _is_runnable(self, obj):
    if "when" in obj.keys():
      return Processor().process(self.ctx, obj["when"])
    return True

  def _get_iterable(self, obj):
    return Processor().process(self.ctx, obj["loop"])

  # def _interpolated(self, args):
  #   for key, value in args.items():
  #     args[key] = Processor().process_arg(self.ctx, str(value))

  def _interpolate(self, args):
    interpolated = args.copy()
    for key, value in interpolated.items():
      interpolated[key] = Processor().process_arg(self.ctx, str(value))
    return interpolated

  def _do_step(self, step):
    step_name = step['name']
    if not self._is_runnable(step):
      msg = f"Skipping {step_name}: Condition not met: {step['when']}"
      logging.getLogger().log_section("STEP", msg, level=logging.WARNING)
      return
    logging.getLogger().log_section("STEP", f"{step_name}")
    for action in step["actions"]:
      if "loop" in action.keys():
        iterable = self._get_iterable(action)
        for item in iterable:
          self.ctx.store.action_item = item
          self._do_action(step_name, action)
      else:
        self.ctx.store.action_item = None
        self._do_action(step_name, action)

  def _do_action(self, step_name, action):
    action_name = action["name"]
    if not self._is_runnable(action):
      msg = f"Skipping {step_name} / {action_name}: Condition not met: {action['when']}"
      logging.getLogger().log_section("STEP", msg, level=logging.WARNING)
      return
    instance_name = action["object"]["name"]
    logging.getLogger().log_section("STEP", f"{step_name} / { action_name}")
    module = action["object"]["module"]
    cls = action["object"]["class"]
    cls_args = dict()
    if action["object"]["instantiate"]:
      cls_args = action["object"]["args"] or dict()
      cls_args = self._interpolate(cls_args)
      instance = self.ctx.instantiate(module, cls, cls_args)
      self.ctx.put(instance_name, instance)
    else:
      instance = self.ctx.get(instance_name)
    for method in action["object"]["methods"]:
      if "loop" in method.keys():
        iterable = self._get_iterable(method)
        for item in iterable:
          self.ctx.store.method_item = item
          self._do_method(action_name, instance, instance_name, method)
      else:
        self.ctx.store.method_item = None
        self._do_method(action_name, instance, instance_name, method)

  def _do_method(self, action_name, instance, instance_name, method):
    method_name = method["name"]
    if not self._is_runnable(method):
      msg = f"Skipping {action_name} / {instance_name}.{method_name}: Condition not met: {method['when']}"
      logging.getLogger().log_section("ACTION", msg, level=logging.WARNING)
      return
    method_args = method["args"] or dict()
    method_args = self._interpolate(method_args)
    logging.getLogger().log_section("ACTION",
                                    f"{action_name} / {instance_name}.{method_name}")
    self.ctx.register_method_secrets(instance,
                                     method_name,
                                     method_args)
    result = getattr(instance, method_name)(**method_args)
    if method["output"] is not None:
      self.ctx.put(method["output"], result)

  def run(self):
    """Run the workflow."""
    for step in self.ctx.configmgr.get_parameter("workflow", "$.steps"):
      if "loop" in step.keys():
        iterable = self._get_iterable(step)
        for item in iterable:
          self.ctx.store.step_item = item
          self._do_step(step)
      else:
        self.ctx.store.step_item = None
        self._do_step(step)
