import sys
import logging
import argparse
from laboro.context import Context
from laboro.config.manager import Manager as CfgMgr
from laboro.workflow import Workflow
from laboro.logger.manager import Manager as LogMgr
from laboro.vault import Vault


def run(context, cfg_mgr):
  try:
    with Workflow(context=context, **cfg_mgr.workflow_config) as wkf:
      wkf.run()
  except Exception:
    pass


def main(workflows):
  cfg_mgr = CfgMgr(main_config="/etc/laboro/laboro.yml")
  context = Context(logger=LogMgr(Vault()), config_mgr=cfg_mgr)
  logging.getLogger().log_section("LABORO", "Bootstrapping")
  for workflow_cfg in workflows:
    logging.getLogger().vault.clear()
    cfg_mgr.workflow_config = workflow_cfg
    run(context=context, cfg_mgr=cfg_mgr)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Run Laboro workflow",
                                   prog="laboro")
  parser.add_argument("-w", "--workflow",
                      metavar="workflows",
                      nargs="+",
                      required=True,
                      help="Run the specified workflows sequentially")
  args = parser.parse_args()
  if not args.workflow:
    parser.print_help()
    sys.exit(1)
  main(args.workflow)
