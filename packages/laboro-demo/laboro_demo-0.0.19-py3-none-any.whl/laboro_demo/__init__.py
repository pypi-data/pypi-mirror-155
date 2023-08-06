import logging
from laboro.module import Module


class Demo(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a demonstrator module that validate **Laboro** modules loading and class instantiation mechanisms.

  It also allow global testing on features common to any **Laboro** modules.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.
  """
  def __init__(self, context, args):
    super().__init__(filepath=__file__, context=context, args=args)

  def _is_a_demo(self):
    """Display a message according to the ``is_demo`` arguments given at init time.
    """
    is_demo = "is not"
    if self.get_arg_value("is_demo"):
      is_demo = "is"
    logging.info(f"This instance of the {self.__class__.__name__} is named {self.get_arg_value('name')} and {is_demo} a demonstration module.")

  def _display_list(self):
    """Display the content of the ``demo_list`` argument if  the ``list_only`` argument was set to *True* at init time.
    """
    if "list_only" in self.args:
      logging.info("The given list items are:")
      for item in self.get_arg_value("demo_list"):
        logging.info(f"  - {item}")

  def _display_dict(self):
    """Display the content of the ``demo_dict`` argument if the ``dict_only`` argument was set to *True* at init time.
    """
    if "dict_only" in self.args:
      logging.info("The given dict items key and values are:")
      for key, value in self.get_arg_value("demo_dict").items():
        logging.info(f"  - {key}: {value}")

  def _display_password(self):
    """Display the **redacted** content of the ``password`` argument given at init time.
    """
    logging.info(f"The following password should be redacted: {self.get_arg_value('password')}")

  @Module.laboro_method
  def self_test(self):
    """Run all the private methods.
    """
    self._is_a_demo()
    self._display_list()
    self._display_dict()
    self._display_password()

  @Module.laboro_method
  def show_argument(self, argument):
    """Log the specified ``argument``.

    Arguments:
      ``argument``: A string value specifying one of the argument given to ``__init__``.

    Raises:
      ``laboro.error.LaboroError``: Whenever the ``argument`` value is not a valid argument name.
    """
    arg_value = self.get_arg_value_as_string(argument)
    logging.info(f"This arg was given at init time: {argument}: {arg_value}")

  @Module.laboro_method
  def get_value_from_dict(self, key):
    if "dict_only" in self.args and key in self.get_arg_value("demo_dict"):
      return self.get_arg_value("demo_dict")[key]

  @Module.laboro_method
  def show_list(self, arg_list):
    for item in arg_list:
      logging.info(f"- {item}")

  @Module.laboro_method
  def show_dict(self, arg_dict):
    for key, value in arg_dict.items():
      logging.info(f"- {key}: {value}")

  @Module.laboro_method
  def show_dict_value(self, arg_dict, key):
    logging.info(f"{key}: {arg_dict[key]}")

  @Module.laboro_method
  def show_value(self, value):
    logging.info(f"This is the given value: {value}")
