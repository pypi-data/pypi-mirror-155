import yaml
import logging
import builtins
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from laboro.error import LaboroError


class Validator:
  """The ``laboro.validator.Validator`` object purpose is to validate `json` object against `jsonschema` specification given as `YAML` files.

  This object is instantiated by some **Laboro** core components and is **not intended to be used directly**.
  """

  def _load_file(self, filepath):
    try:
      with open(filepath, mode="r", encoding="utf-8") as schema:
        return yaml.load(schema, Loader=yaml.FullLoader)
    except FileNotFoundError as err:
      msg = {"type": "FileNotFoundError",
             "message": f"Schema file not found: {filepath}"}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}") from err
    except(yaml.scanner.ScannerError,
           yaml.constructor.ConstructorError) as err:
      msg = {"type": "InvalidYamlError",
             "message": f"YAML file is invalid: {filepath}"}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}") from err

  def validate_instance(self, schema, instance):
    """Validate the given instance against the given schema.

    Arguments:
    ``schema``: A file path to a *YAML* representation of a `jsonschema` representing the schema against which the ``instance`` should be validated.

    ``instance``: A file path to a *YAML* representation of a `json` representing the instance to validate.

    Raises:
      ``laboro.error.Error``: Whenever the schema or the instance file can't be loaded or are not valid *YAML* files. Error is also raised when the given ``schema`` is not a valid `jsonschema` or when ``instance`` can not validate against the given ``schema`.
    """
    try:
      schema_yml = self._load_file(schema)
      instance_yml = self._load_file(instance)
      validate(instance=instance_yml, schema=schema_yml)
      return instance_yml
    except ValidationError as err:
      err_msg = str(err).split("\n")[0]
      msg = {"type": "InvalidInstanceError",
             "message": f"Instance is invalid: {err_msg}"}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}") from err
    except SchemaError as err:
      msg = {"type": "InvalidSchemaError",
             "message": f"Schema is invalid: {err}"}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}") from err

  def validate_data(self, schema, data):
    """Validate the specified `data` dict against the `YAML` representation of a `jsonschema`.

    Arguments:
      schema: A file path to a *YAML* representation of a `jsonschema`
      schema: A dict representing the instance to validate.

    Raises:
      ``laboro.error.Error``: Whenever the schema file can't be loaded or is not valid *YAML* files. Error is also raised when the given ``schema`` is not a valid `jsonschema` or when ``data`` can not validate against the given ``schema`.
    """
    try:
      schema_yml = self._load_file(schema)
      validate(instance=data, schema=schema_yml)
    except ValidationError as err:
      err_msg = str(err).split("\n")[0]
      msg = f"[InvalidDataError] {err_msg}"
      logging.critical(msg)
      raise LaboroError(msg) from err

  def validate_method_args(self, method, args):
    """Validate the method arguments against the method specification.

    Arguments:
      method: A string representation of a `jsonschema` describing the method specification.
      args: A dict representing the method argument and their values.

    Raises:
      ``laboro.error.LaboroError``: When the given ``args`` does not validate against the specification.
    """
    try:
      validate(instance=args, schema=method)
      if isinstance(args, dict):
        if self._validate_required(args, method):
          for arg, value in args.items():
            if arg in [arg["name"] for arg in method["args"]]:
              self._validate_type(arg, value, method)
              self._validate_implied(arg, args, method)
              self._validate_excluded(arg, args, method)
            else:
              msg = {"type": "UnknownArgError",
                     "message": f"Unknown argument: {arg}"}
              logging.critical(f"[{msg['type']}] {msg['message']}")
              raise LaboroError(f"[{msg['type']}] {msg['message']}")
          return True
        msg = "[MissingRequiredArgError] Missing required argument."
        logging.critical(msg)
        raise LaboroError(msg)
      msg = f"[ModuleArgError]: Expected a dict as args, received {type(args)}"
      logging.critical(msg)
      raise LaboroError(msg)
    except ValidationError as err:
      err_msg = str(err).split("\n")[0]
      msg = f"[InvalidSpecError] {err_msg}"
      logging.critical(msg)
      raise LaboroError(msg) from err

  def validate_obj_args(self, specification, args):
    """Validate the instantiation arguments against the object specification.

    Arguments:
      specification: A file path to a *YAML* representation of a `jsonschema` representing the schema against which the ``args`` should be validated.
      args: A dict representing the object instantiation argument and their values.

    Raises:
      ``laboro.error.LaboroError``: When the given ``args`` does not validate against the specification.
    """
    try:
      specification_yml = self._load_file(specification)
      validate(instance=args, schema=specification_yml)
      if isinstance(args, dict):
        if self._validate_required(args, specification_yml):
          for arg, value in args.items():
            if arg in [arg["name"] for arg in specification_yml["args"]]:
              self._validate_type(arg, value, specification_yml)
              self._validate_implied(arg, args, specification_yml)
              self._validate_excluded(arg, args, specification_yml)
            else:
              msg = {"type": "UnknownArgError",
                     "message": f"Unknown argument: {arg}"}
              logging.critical(f"[{msg['type']}] {msg['message']}")
              raise LaboroError(f"[{msg['type']}] {msg['message']}")
          return True
        msg = "[MissingRequiredArgError] Missing required argument."
        logging.critical(msg)
        raise LaboroError(msg)
      msg = f"[ModuleArgError]: Expected a dict as args, received {type(args)}"
      logging.critical(msg)
      raise LaboroError(msg)
    except ValidationError as err:
      err_msg = str(err).split("\n")[0]
      msg = f"[InvalidSpecError] {err_msg}"
      logging.critical(msg)
      raise LaboroError(msg) from err

  def _validate_required(self, arguments, specification):
    required = sorted([arg["name"] for arg in list(filter(lambda arg: arg["required"], specification["args"]))])
    return sorted([arg for arg in arguments if arg in required]) == required

  def _validate_type(self, arg, value, specification):
    arg_type = [aarg["type"] for aarg in specification["args"] if aarg["name"] == arg][0]
    if arg_type != "any":
      try:
        arg_type = getattr(builtins, arg_type)
        if not isinstance(value, arg_type):
          msg = {"type": "BadArgTypeError",
                 "message": f"Expected type {arg_type} / received {type(value)} for {arg}."}
          logging.critical(f"[{msg['type']}] {msg['message']}")
          raise LaboroError(f"[{msg['type']}] {msg['message']}")
      except AttributeError as err:
        msg = {"type": "UnknownTypeError",
               "message": f"Unknown type '{arg_type}' for argument {arg}."}
        logging.critical(f"[{msg['type']}] {msg['message']}")
        raise LaboroError(f"[{msg['type']}] {msg['message']}") from err

  def _validate_implied(self, arg, arguments, specification):
    try:
      implied = sorted([aarg["implied"] for aarg in list(filter(lambda arg: arg["implied"], specification["args"])) if aarg["name"] == arg])[0]
    except IndexError:
      implied = list()
    if sorted([iarg for iarg in arguments if iarg in implied]) != implied:
      msg = {"type": "MissingImpliedArgError",
             "message": f"All args of {implied} are required by {arg}."}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}")

  def _validate_excluded(self, arg, arguments, specification):
    try:
      excluded = sorted([aarg["excluded"] for aarg in list(filter(lambda arg: arg["excluded"], specification["args"])) if aarg["name"] == arg])[0]
    except IndexError:
      excluded = list()
    if len([earg for earg in arguments if earg in excluded]) > 0:
      msg = {"type": "ExcludedArgError",
             "message": f"None of {' or '.join(excluded)} can be used alongside {arg}."}
      logging.critical(f"[{msg['type']}] {msg['message']}")
      raise LaboroError(f"[{msg['type']}] {msg['message']}")
