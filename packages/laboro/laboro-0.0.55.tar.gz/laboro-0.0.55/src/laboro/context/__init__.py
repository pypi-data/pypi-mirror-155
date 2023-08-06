import os
import logging
from laboro.error import LaboroError
from laboro.history import History
from laboro.workspace import Workspace
from laboro.context.store import Store
from laboro.config.manager import Manager as ConfigMgr
from laboro.module.manager import Manager as ModuleMgr
from laboro.error.handler import Handler as ErrorHandler


class Context:
  """The ``laboro.context.Context`` object manages all low level tasks for ``laboro.workflow.Workflow`` instances. It is instantiated once by the main **Laboro** process in a **Laboro** execution ans is passed from **Workflow** instances to **Workflow** instances.

  It loads the main **Laboro** configuration file ``/etc/laboro/laboro.yml`` and initiate all needed **Laboro** submodules.

  Arguments:
    logger: A ``laboro.logger.manager.Manager`` instance.

  Raises:
    ``laboro.error.LaboroError``: If the main **Laboro** configuration file is not found or invalid.

  Returns:
    ``laboro.context.Context``
  """
  def __init__(self, logger):
    self.delete_workspace_on_exit = True
    self.logger = logger
    self.store = Store()
    self.history = None
    self.modulemgr = ModuleMgr()
    self.configmgr = ConfigMgr("/etc/laboro/laboro.yml")
    self.workspacedir = self.configmgr.get_parameter("main",
                                                     "$.laboro.workspacedir")
    self.histdir = self.configmgr.get_parameter("main",
                                                "$.laboro.histdir")
    self.workflowdir = self.configmgr.get_parameter("main",
                                                    "$.laboro.workflowdir")
    self.logdir = self.configmgr.get_parameter("main",
                                               "$.laboro.log.dir")
    self.loglevel = self.configmgr.get_parameter("main",
                                                 "$.laboro.log.level")
    self.workspace = None
    logging.getLogger().vault.clear()

  def reset(self, workflow_name, session):
    """Reset the ``laboro.context.Context`` instance with the new workflow configuration and session.

    Arguments:
      workflow_name: A string specifying the workflow name. The ``workflow_name`` will be used to retrieve the workflow configuration file in the``laboro.workflowdir`` specified in the main configuration file.
      session: A unique string defining a workflow session. Usually a string representation of a uuid.uuid4() instance.

    Raises:
      ``laboro.error.LaboroError``: For various reasons linked to the submodules instantiations.

    Returns:
      ``laboro.context.Context``: The ``Context`` instance reseted with the new parameters.
    """
    try:
      logging.getLogger().log_section("WORKFLOW",
                                      f"Started {workflow_name} / {session}")
      logging.getLogger().vault.clear()
      self.store.clear()
      self._configure_logger(workflow_name, session)
      self._set_workflow_config(workflow_name)
      self.delete_workspace_on_exit = self.configmgr.get_parameter("workflow", "$.workspace.delete_on_exit")
      self.workspace = Workspace(workspacedir=self.workspacedir,
                                 workflow=workflow_name,
                                 session=session)
      history_path = os.path.join(self.histdir, f"{workflow_name}.db")
      self.history = History(filename=history_path,
                             workflow=workflow_name,
                             session=session,
                             params=self.configmgr.workflow_config)
      self.history.enter()
      self.install_packages()
      return self
    except Exception as err:
      ErrorHandler().handle_error(workflow_name,
                                  session,
                                  err.__class__,
                                  str(err))

  def exit(self, name, session, kind, value):
    """Exit the ``Context`` instance.
    When the instance exit, it triggers the ``laboro.workspace.Workspace``, ``laboro.history.History`` instances exit and close the log linked to the ``laboro.workflow.Workflow`` instance associated with the ``Context`` instance. It also register the exit/error code.

    Arguments:
      name: A string specifying the ``Workflow`` name to close.
      session: A string specifying the ``Workflow`` session to close.
      kind: The kind of event that triggered the ``Context`` instance exit.
      value: The `value` of the event that triggered the ``Context`` instance exit.
    """
    if self.delete_workspace_on_exit:
      self.workspace.delete()
    self.history.exit(kind, value)
    ErrorHandler().handle_error(name, session, kind, value)
    self.logger.remove_file_handler(session)

  def _configure_logger(self, workflow_name, session):
    self.logger.add_file_handler(self.logdir, workflow_name, session)
    self.logger.set_log_level(self.loglevel)

  def _set_workflow_config(self, workflow_name):
    config_file_name = os.path.join(self.workflowdir, f"{workflow_name}.yml")
    logging.info(f"[+] Loading workflow_config: {config_file_name}")
    self.configmgr.workflow_config = config_file_name

  def install_packages(self):
    """Install all packages listed in the workflow configuration file.
    """
    packages = self.configmgr.get_parameter("workflow", "$.packages")
    for pkg in packages:
      self.modulemgr.install_package(pkg)

  def put(self, prop, value):
    """Store the ``prop`` variable and its value in the ``Context.store`` ``laboro.context.Store`` instance.

    Arguments:
      prop: A string representing the variable name.
      value: Any type, the value to store.

    Raises:
      ``TypeError``: When ``prop`` is not a string.
    """
    self.store.put(prop, value)

  def get(self, prop):
    """Retrieve the ``prop`` value from the ``Context.store`` ``laboro.context.Store`` instance.

    Arguments:
      prop: A string representing the variable name.

    Raises:
      ``TypeError``: When ``prop`` is not a string.
      ``AttributeError``: When ``prop`` does not exist within the Store instance.
    """
    return self.store.get(prop)

  def _register_class(self, module, cls):
    self.modulemgr.register_class_from_module(cls, module)

  def _register_instance_secrets(self, instance, args):
    if args is not None:
      class_args = instance.specification["args"]
      secret_keys = [arg["name"] for arg in class_args if arg["secret"]]
      secrets = [args[key] for key in args.keys() if key in secret_keys]
      list(map(logging.getLogger().vault.add, secrets))

  def _instantiate(self, module, cls, args):
    logging.info(f"[+] Object instantiation: {module}.{cls}")
    mod = self.modulemgr.get_class_from_module(cls=cls, module=module)
    instance = mod(context=self, args=args)
    self._register_instance_secrets(instance, args)
    return mod(context=self, args=args)

  def instantiate(self, module, cls, args):
    """Register the class to the ``laboro.module.ModuleMgr`` instance and return an instance of the class.

    Arguments:
      module: A string specifying the *Python* module name from each retrieve the class.
      cls: A string specifying the class name to instantiate.
      args: A `kwargs` that will be used to instantiate the class.

    Returns:
      An instance of the class ``module``.``cls`` instantiated with the ``args`` `kwargs` as init parameters.

    Raises:
      ``laboro.error.LaboroError``: When the specified module or class ar not available and when the specified ``args`` are incompatibles with the class constructor.
    """
    self._register_class(module, cls)
    return self._instantiate(module, cls, args)

  def register_method_secrets(self, instance, method, args):
    """Register the secrets from the specified arguments ``args``.
    Retrieve the name of the ``instance``'s ``method`` declared as *secret* and register their value in the ``laboro.Vault.vault`` embedded in the ``laboro.logger.LaboroLogger``.

    Arguments:
      instance: An instance of an object derived from the ``laboro.module.Module``.
      method: The ``instance`` method name from which retrieve the secret arguments list.
      args: A kwargs from which retrieve the secret value.

    Raises:
      ``laboro.error.LaboroError`` when the specified ``method `` does not exists.
    """
    if args is not None:
      try:
        method_args = [meth for meth in instance.specification["methods"] if meth["name"] == method][0]["args"]
        secret_keys = [arg["name"] for arg in method_args if arg["secret"]]
        secrets = [args[key] for key in args.keys() if key in secret_keys]
        list(map(logging.getLogger().vault.add, secrets))
      except IndexError as err:
        raise LaboroError(f"UnknownMethodError: Unknown method {instance.__class__.__name__}.{method}") from err
