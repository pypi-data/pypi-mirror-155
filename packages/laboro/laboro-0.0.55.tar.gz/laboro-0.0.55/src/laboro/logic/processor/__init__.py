import re
from laboro.logic.parser import Parser


class Processor:
  @staticmethod
  def process(context, statement):
    word_ptn = re.compile(r"\$store\$\w+")
    store_ptn = re.compile(r"^\$store\$")
    vars = re.findall(word_ptn, statement)
    values = [str(context.get(re.sub(store_ptn, "", var))) for var in vars]
    for var, value in zip(vars, values):
      var_ptn = re.compile(var.replace("$", r"\$"))
      statement = re.sub(var_ptn, value, statement)
    if context.store.step_item is not None:
      pattern = re.compile(r"\$step_item\$")
      statement = re.sub(pattern, str(context.store.step_item), statement)
    if context.store.action_item is not None:
      pattern = re.compile(r"\$action_item\$")
      statement = re.sub(pattern, str(context.store.action_item), statement)
    if context.store.method_item is not None:
      pattern = re.compile(r"\$method_item\$")
      statement = re.sub(pattern, str(context.store.method_item), statement)
    return Parser().eval(statement)

  @staticmethod
  def process_arg(context, value):
    store_ptn = re.compile(r"^\$store\$")
    if re.match(store_ptn, str(value)) is not None:
      value = context.get(re.sub(store_ptn, "", value))
    if context.store.step_item is not None:
      pattern = re.compile(r"\$step_item\$")
      value = re.sub(pattern, str(context.store.step_item), value)
    if context.store.action_item is not None:
      pattern = re.compile(r"\$action_item\$")
      value = re.sub(pattern, str(context.store.action_item), value)
    if context.store.method_item is not None:
      pattern = re.compile(r"\$method_item\$")
      value = re.sub(pattern, str(context.store.method_item), value)
    return Parser().literal_eval(value)
