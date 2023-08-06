"""Module that contains the function to start the RPC server"""
import os
import stat
import zerorpc

from babelnet import api


def listen():
    """starts the RPC server"""
    s = zerorpc.Server(api, heartbeat=40, pool_size=16)
    print("Exposing API")
    s.bind("tcp://*:1234")
    if os.path.exists('/babelnet_ipc'):
        s.bind("ipc:///babelnet_ipc/socket")
        os.chmod("/babelnet_ipc/socket", stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print("server listening")
    s.run()
    print("Shouldn't see this")
