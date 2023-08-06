import logging
from ast import literal_eval
from asteval import Interpreter


class Parser:
  @staticmethod
  def eval(expression):
    try:
      return Interpreter().eval(expression)
    except SyntaxError as err:
      logging.critical(f"Invalid syntax for expression: {expression}")
      raise err

  @staticmethod
  def literal_eval(expression):
    try:
      return literal_eval(expression)
    except (ValueError, SyntaxError):
      return expression
