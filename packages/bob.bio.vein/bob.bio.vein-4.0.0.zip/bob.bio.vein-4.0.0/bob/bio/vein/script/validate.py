#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


"""Utilities for command-line option validation"""


import glob
import logging
import os

import schema

logger = logging.getLogger(__name__)


def setup_logger(name, level):
    """Sets up and checks a verbosity level respects min and max boundaries


    Parameters:

      name (str): The name of the logger to setup

      v (int): A value indicating the verbosity that must be set


    Returns:

      logging.Logger: A standard Python logger that can be used to log messages


    Raises:

      schema.SchemaError: If the verbosity level exceeds the maximum allowed of 4

    """

    import bob.extension.log

    logger = bob.extension.log.setup(name)

    if not (0 <= level < 4):
        raise schema.SchemaError(
            "there can be only up to 3 -v's in a command-line"
        )

    # Sets-up logging
    bob.extension.log.set_verbosity_level(logger, level)

    return logger


def make_dir(p):
    """Checks if a path exists, if it doesn't, creates it


    Parameters:

      p (str): The path to check


    Returns

      bool: ``True``, always

    """

    if not os.path.exists(p):
        logger.info("Creating directory `%s'...", p)
        os.makedirs(p)

    return True


def check_path_does_not_exist(p):
    """Checks if a path exists, if it does, raises an exception


    Parameters:

      p (str): The path to check


    Returns:

      bool: ``True``, always


    Raises:

      schema.SchemaError: if the path exists

    """

    if os.path.exists(p):
        raise schema.SchemaError("path to {} exists".format(p))

    return True


def check_path_exists(p):
    """Checks if a path exists, if it doesn't, raises an exception


    Parameters:

      p (str): The path to check


    Returns:

      bool: ``True``, always


    Raises:

      schema.SchemaError: if the path doesn't exist

    """

    if not os.path.exists(p):
        raise schema.SchemaError("path to {} does not exist".format(p))

    return True


def check_model_does_not_exist(p):
    """Checks if the path to any potential model file does not exist


    Parameters:

      p (str): The path to check


    Returns:

      bool: ``True``, always


    Raises:

      schema.SchemaError: if the path exists

    """

    files = glob.glob(p + ".*")
    if files:
        raise schema.SchemaError("{} already exists".format(files))

    return True


def open_multipage_pdf_file(s):
    """Returns an opened matplotlib multi-page file


    Parameters:

      p (str): The path to the file to open


    Returns:

      matplotlib.backends.backend_pdf.PdfPages: with the handle to the multipage
      PDF file


    Raises:

      schema.SchemaError: if the path exists

    """
    from matplotlib.backends.backend_pdf import PdfPages

    return PdfPages(s)
