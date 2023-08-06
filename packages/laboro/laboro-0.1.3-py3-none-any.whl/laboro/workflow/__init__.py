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
    name: A string specifying the name of the workflow
    packages: A list of package names.
    workspace: A dictionary representation of a workspace configuration (see ``laboro.workspace.Workspace`` for further dertails).
    steps: A list of dictionary representation of ``laboro.workflow.Step``

  Returns:
    ``laboro.workflow.Workflow``: A Workflow object.

  ..  code-block:: python

      from laboro.vault import Vault()
      from laboro.log.manager import Manager as LogMgr
      from laboro.context import Context
      from laboro.workflow import Workflow

      cfg_mgr = CfgMgr(main_config="/etc/laboro/laboro.yml")
      context = Context(logger=LogMgr(Vault()), config_mgr=cfg_mgr)
      logging.getLogger().log_section("LABORO", "Bootstrapping")
      logging.getLogger().vault.clear()
      cfg_mgr.workflow_config = "my_workflow.yml"
      workflow = cfg_mgr.workflow_config
      with Workflow(context=context, **workflow) as wkf:
        wkf.run()
        ...
  """
  def __init__(self, context, name, packages, workspace, steps):
    self.name = name.replace(" ", "_")
    self.packages = packages
    self.workspace = workspace
    self.steps = steps
    self.ctx = context.reset(session=str(uuid.uuid4()),
                             workspace_cfg=self.workspace)

  def __enter__(self):
    return self

  def __exit__(self, kind, value, traceback):
    self.ctx.exit(kind, value)

  def run(self):
    """Run the workflow."""
    for wkf_step in self.steps:
      with Step(self.ctx, **wkf_step) as step:
        step.run()
    logging.getLogger().log_line()
