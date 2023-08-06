"""This module contains the implementation of the rpc api. It uses rpc in order to perform queries"""
import functools
import inspect
import threading

import zerorpc
from zerorpc import Client

from babelnet.apis.abstract_api import AbstractAPI
from babelnet.conf import _config

_TIMEOUT: int = 60
_HEARTBEAT: int = 40

_th_local = threading.local()

def _init_client():
    """Function that initializes a rpc client and returns it."""
    c: Client = zerorpc.Client(
        heartbeat=_HEARTBEAT, timeout=_TIMEOUT, passive_heartbeat=False
    )
    c.connect(_config.RPC_URL)
    return c


class RPCApi(AbstractAPI):
    """The RPC api."""

    def __init__(self):
        """init method"""
        methods = inspect.getmembers(
            AbstractAPI,
            lambda x: inspect.isfunction(x)
            # and x.__dict__.get("__isabstractmethod__", False),
        )

        def wrap(mn, *args, **kwargs):
            try:
                c = _th_local.c
            except AttributeError:
                c = _init_client()
                _th_local.c = c
            fn = getattr(c, mn)
            dict_args = dict(args=args, kwargs=kwargs)
            return fn(dict_args)

        for method_name, method in methods:
            func = functools.partial(wrap, method_name)
            self.__dict__[method_name] = func
