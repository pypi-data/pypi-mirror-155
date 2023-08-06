import string
import random
import logging
from laboro.module import Module

CHAR_LIST = string.ascii_uppercase + string.hexdigits


class SubDemo(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a demonstrator module that validate **Laboro** modules loading and class instantiation mechanisms.

  It also allow global testing on features common to any **Laboro** modules.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.
  """

  def __init__(self, context, args):
    super().__init__(filepath=__file__, context=context, args=args)

  def _get_list(self, size):
    return ["".join(random.choices(CHAR_LIST, k=int(1 + random.random() * 10))) for d in range(size)]

  @Module.laboro_method
  def get_random_list(self, size):
    """Generate a list of the specified size.

    Arguments:
      size: An integer value
    Returns:
      list: A list of random strings
    """
    logging.info(f"Generating a {size} items random data list")
    return self._get_list(size)

  @Module.laboro_method
  def get_random_dict(self, size):
    """Generate a dictionary of the specified size.

    Arguments:
      size: An integer value
    Returns:
      dict: A dictionary with random strings as keys and values
    """
    logging.info(f"Generating a {size} items random data dictionary")
    keys = self._get_list(size)
    values = self._get_list(size)
    return dict(zip(keys, values))
