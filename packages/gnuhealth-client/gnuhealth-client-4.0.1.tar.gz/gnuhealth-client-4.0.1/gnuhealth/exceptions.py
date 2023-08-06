# This file is part of GNU Health.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from .jsonrpc import Fault

GNUHealthServerError = Fault


class GNUHealthServerUnavailable(Exception):
    pass


class GNUHealthError(Exception):

    def __init__(self, faultCode):
        self.faultCode = faultCode
