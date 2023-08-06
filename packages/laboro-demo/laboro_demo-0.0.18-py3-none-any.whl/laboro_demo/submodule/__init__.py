import string
import random
import logging
from laboro.module import Module


class SubDemo(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a demonstrator module that validate **Laboro** modules loading and class instantiation mechanisms.

  It also allow global testing on features common to any **Laboro** modules.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.
  """
  def __init__(self, context, args):
    super().__init__(filepath=__file__, context=context, args=args)

  @Module.laboro_method
  def get_random_list(self, num):
    logging.info("Generating random data list")
    return ["".join(random.choices(string.ascii_uppercase, k=9)) for d in range(num)]
