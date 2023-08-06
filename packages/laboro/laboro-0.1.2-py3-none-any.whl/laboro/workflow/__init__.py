import uuid
import logging
from laboro.workflow.step import Step


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

  def run(self):
    """Run the workflow."""
    for wkf_step in self.ctx.configmgr.get_parameter("workflow", "$.steps"):
      with Step(self.ctx, **wkf_step) as step:
        step.run()
    logging.getLogger().log_line()
