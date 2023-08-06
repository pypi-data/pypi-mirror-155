# SPDX-FileCopyrightText: 2020 Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

import logging as log
import statsd  # type: ignore
import threading
from typing import Optional

STATSD_PREFIX = ""


class StatsdWrapper(threading.local):
    """
    Wrapper around the statsd library that handles our use cases:

    1. Configurable namespace/prefix per service + context
    2. Proper type hints
    """

    context: Optional[str] = None

    def _build_metric_name(self, name: str) -> str:
        return ".".join([STATSD_PREFIX, self.context or "all", name])

    def get_timer(self, name: str) -> statsd.Timer:
        return statsd.Timer(self._build_metric_name(name))

    def get_counter(self, name: str) -> statsd.Counter:
        return statsd.Counter(self._build_metric_name(name))


STATSD = StatsdWrapper()


class Base:
    """
    Base class for other "minty" classes.

    This base class provides a lazy-loaded "self.logger" and access to the
    global "statsd" object.
    """

    _logger: log.Logger

    @property
    def logger(self) -> log.Logger:
        """Return this object's logger instance, create one if necessary

        :return: A logger object for this instance
        :rtype: logging.Logger
        """
        try:
            self._logger
        except AttributeError:
            self._logger = log.getLogger(self.__class__.__name__)

        return self._logger

    @property
    def statsd(self) -> StatsdWrapper:
        """Return the global statsd instance (wrapper)"""
        return STATSD
