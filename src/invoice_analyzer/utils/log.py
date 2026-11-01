from __future__ import annotations

import copy
import os
import sys
from pathlib import Path
from typing import Optional

import loguru

LOGGER_CONSOLE_PREFIX_SIZE = 11

SUMMARY_LOG_FILEPATH = Path(os.getcwd()) / 'summary.log'
EXCEPTION_LOG_FILEPATH = Path(os.getcwd()) / 'exception.log'


def get_logger(console: Optional[bool] = None,
               filepath: Optional[Path] = None,
               level: Optional[str] = None) -> loguru.Logger:

    if console is None and filepath is None:
        raise ValueError('expected console or filepath to be not None')

    base_logger = loguru.logger
    base_logger.remove()
    logger = copy.deepcopy(base_logger)

    console_format = "<level>{message}</level>"
    file_format = '{time:YYYY-MM-DD HH:mm:ss} | <level>{level: <8}</level> | {message}'

    if level:
        if console:
            logger.add(sys.stdout, level=level, diagnose=False, format=console_format)
        if filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            logger.add(filepath, level=level, diagnose=False, format=file_format)
    else:
        if console:
            logger.add(sys.stdout, diagnose=False, format=console_format)
        if filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            logger.add(filepath, diagnose=False, format=file_format)

    return logger


def info(
    msg: str,
    console: bool = True,
    filepath: Optional[Path] = SUMMARY_LOG_FILEPATH
):
    get_logger(console, filepath).info(msg)


def error(
    msg: str,
    console: bool = True,
    filepath: Optional[Path] = SUMMARY_LOG_FILEPATH
):
    get_logger(console, filepath).error(msg)


def debug(
    msg: str,
    console: bool = 'DEBUG' in os.environ,
    filepath: Path = SUMMARY_LOG_FILEPATH
):
    get_logger(console, filepath).debug(msg)


def warning(
    msg: str,
    console: bool = True,
    filepath: Path = SUMMARY_LOG_FILEPATH
):
    get_logger(console, filepath).warning(msg)


def success(
    msg: str,
    console: bool = True,
    filepath: Path = SUMMARY_LOG_FILEPATH
):
    get_logger(console, filepath).success(msg)


def exception(
    msg: str,
    console: bool = False,
    filepath: Path = EXCEPTION_LOG_FILEPATH
):
    get_logger(console, filepath).exception(msg)


def print_dash():
    terminal_size = os.get_terminal_size()
    info('-' * terminal_size.columns)
