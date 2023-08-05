import re
import uuid
import logging


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

  def _swap_stored_args(self, args):
    pattern = re.compile(r"^\$store\$")
    for key, value in args.items():
      if re.match(pattern, str(value)) is not None:
        args[key] = self.ctx.get(re.sub(pattern, "", value))

  def run(self):
    """Run the workflow."""
    for step in self.ctx.configmgr.get_parameter("workflow", "$.steps"):
      for action in step["actions"]:
        logging.getLogger().log_section("STEP",
                                        f"{step['name']} / { action['name']}")
        instance_name = action["object"]["name"]
        module = action["object"]["module"]
        cls = action["object"]["class"]
        cls_args = dict()
        if action["object"]["instantiate"]:
          cls_args = action["object"]["args"] or dict()
          self._swap_stored_args(cls_args)
          instance = self.ctx.instantiate(module, cls, cls_args)
          self.ctx.put(instance_name, instance)
        else:
          instance = self.ctx.get(instance_name)
        for method in action["object"]["methods"]:
          method_args = method["args"] or dict()
          self._swap_stored_args(method_args)
          method_name = method["name"]
          logging.getLogger().log_section("ACTION",
                                          f"{action['name']} / {instance_name}.{method_name}")
          self.ctx.register_method_secrets(instance,
                                           method_name,
                                           method_args)
          result = getattr(instance, method_name)(**method_args)
          if method["output"] is not None:
            self.ctx.put(method["output"], result)
