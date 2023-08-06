import sys
import logging
import argparse
from laboro.context import Context
from laboro.workflow import Workflow
from laboro.logger.manager import Manager as LogMgr
from laboro.vault import Vault


def run(workflow, context):
  try:
    with Workflow(name=workflow, context=context) as wkf:
      wkf.run()
  except Exception:
    pass


def main(workflows):
  context = Context(logger=LogMgr(Vault()))
  logging.getLogger().log_section("LABORO", "Bootstrapping")
  for workflow in workflows:
    logging.getLogger().vault.clear()
    run(workflow, context=context)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Run Laboro workflow",
                                   prog="laboro")
  parser.add_argument("-r", "--run",
                      metavar="workflow",
                      nargs="+",
                      required=True,
                      help="Run the specified workflows sequentially")
  args = parser.parse_args()
  if not args.run:
    parser.print_help()
    sys.exit(1)
  main(args.run)
