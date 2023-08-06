import os
import sys
import logging
import coloredlogs
from laboro.logger import LaboroLogger


class Manager:
  """The purpose of the ``laboro.logger.manager.Manager`` object is to configure the logger used in the whole **Laboro** package and all its subpackages.
  """

  terms = ["linux", "xterm", "xterm-256color"]
  console_fmt = '[%(asctime)s] [%(levelname)-8s] %(message)s'
  file_fmt = '[%(asctime)s] [%(levelname)-8s] %(message)s'
  datefmt = '%Y%m%d %H:%M:%S'
  c_field_styles = {'asctime': {'color': 'magenta'},
                    'hostname': {'color': 'magenta'},
                    'levelname': {'bold': True, 'color': 'white'},
                    'programname': {'color': 'cyan'},
                    'name': {'color': 'cyan'}}
  c_level_styles = {'debug': {'color': 'white'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'bold': True, 'color': 'red'}}
  f_field_styles = {'asctime': {'color': 'magenta'},
                    'hostname': {'color': 'magenta'},
                    'levelname': {'color': 'white'},
                    'programname': {'color': 'cyan'},
                    'name': {'color': 'cyan'}}
  f_level_styles = {'debug': {'color': 'white'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'color': 'red'}}

  def __init__(self, vault):
    self.handlers = {}
    self._set_default()
    self._set_logger_class(LaboroLogger)
    self._set_vault(vault)

  def _set_default(self):
    """Configure the logger default configuration to *stdout*.

    If the ``TERM`` environment variable is defined and is one of "linux", "xterm" or "xterm-256color" the default logger will use ``coloredlogs`` to enhance log readability with colors.

    The default logging level is set to ``INFO``.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    if "TERM" in os.environ and os.environ["TERM"] in self.terms:
      console_handler.setFormatter(
          coloredlogs.ColoredFormatter(fmt=self.console_fmt,
                                       datefmt=self.datefmt,
                                       level_styles=self.c_level_styles,
                                       field_styles=self.c_field_styles))
    else:
      console_handler.setFormatter(logging.Formatter(fmt=self.console_fmt,
                                                     datefmt=self.datefmt))
    logging.basicConfig(level=logging.INFO,
                        handlers=[console_handler])

  def _set_logger_class(self, cls):
    """Set the logger class to be used by the Manager.

    Arguments:
      cls: A class derived from the ``logging.logger`` class.
    """
    logging.getLogger().__class__ = cls
    logging.setLoggerClass(cls)

  def _set_vault(self, vault):
    """Set the ``laboro.vault.Vault`` instance for the logger."""
    logging.getLogger().set_vault(vault)

  def set_log_level(self, level):
    """Set the log level

    Arguments:
      level: A string specifying the desired log level. It **must** be one of the ``logging`` *Python* module standard levels (``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``).

    Raises:
      ``ValueError``: When the given ``level`` is not a valid level name.
    """
    logging.getLogger().setLevel(level)

  def add_file_handler(self, logdir, workflow, session):
    """Adds a file handler to the logger.

    Arguments:
      logdir: A string defining the log directory in which all logs will be stored.
      workflow: A string specifying workflow's name.
      session: A unique string defining the workflow execution session.
    """

    log_fname = f"{workflow}_{session}.log"
    log_fname = os.path.join(logdir, log_fname)
    self.handlers[session] = logging.FileHandler(log_fname)
    self.handlers[session].setFormatter(
        coloredlogs.ColoredFormatter(fmt=self.file_fmt,
                                     datefmt=self.datefmt,
                                     level_styles=self.f_level_styles,
                                     field_styles=self.f_field_styles))
    logging.getLogger().addHandler(self.handlers[session])

  def remove_file_handler(self, session):
    """Removes the file handler associated with the specified session.

    Arguments:
      session: A unique string specifying a workflow session.
    """
    logging.getLogger().removeHandler(self.handlers[session])

  @staticmethod
  def print_logfile(logdir, workflow, session):
    """Print to *stdout* the log file content for the specified workflow session.

    Arguments:
      logdir: A string defining the log directory in which all logs will be stored.
      workflow: A string specifying the workflow name.
      session: A unique string defining the workflow execution session to retrieve the log for
    """
    log_fname = f"{workflow}_{session}.log"
    log_fname = os.path.join(logdir, log_fname)
    with open(log_fname, "r", encoding="utf-8") as log:
      print(log.read())
