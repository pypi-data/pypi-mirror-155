import argparse
import os
import platform
import socket
import sys
from typing import Set, Optional

from .constants import *

_localhost = None


def get_local_ip_address() -> str:
    global _localhost

    if _localhost is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            address = s.getsockname()[0]
            s.close()
            _localhost = address
        except:
            _localhost = 'localhost'
    return _localhost


def is_win() -> bool:
    return platform.system() == 'Windows'


def print_config(tcp: int, ipc: str):
    conf = []
    if tcp:
        conf.append(f'RPC_URL: "tcp://127.0.0.1:{tcp}"')
    if ipc:
        conf.append(f'RPC_URL: "ipc://{os.path.join(ipc, "socket")}"')
    print("To use BabelNet in RPC mode, add",
          "this line" if (len(conf) == 1) else "one of these lines",
          "in your babelnet_conf.yml file")
    for c in conf:
        print(c)


def mode_parser(mode: str) -> Optional[Set[str]]:
    if mode == MODE_ALL:
        return {MODE_TCP, MODE_IPC}
    elif mode in [MODE_TCP, MODE_IPC]:
        return {mode}
    else:
        return None


def check_bn(bn_path):
    if 'BABELNET_SKIP_CHECK' in os.environ:
        return True
    if not os.path.isdir(bn_path):
        raise FileNotFoundError
    elif not (os.path.exists(os.path.join(bn_path, "dict"))
              and os.path.exists(os.path.join(bn_path, "gloss"))
              and os.path.exists(os.path.join(bn_path, "lexicon"))):
        raise ValueError


def stop_server(client, msg: str = None) -> bool:
    from docker.errors import NotFound

    try:
        container = client.containers.get(DOCKER_NAME)
        if msg: print(msg)
        container.remove(force=True)
        return True
    except NotFound:
        return False


def start_server_interactive(print_only=None):
    if print_only is None:
        print_only = 'BABELNET_PRINT_CMD' in os.environ
    not_win = not is_win()

    while True:
        bn_path = input("BabelNet indices path: ")
        try:
            check_bn(bn_path)
            break
        except FileNotFoundError:
            print("Invalid path", bn_path)
        except ValueError:
            print(bn_path, "does not contain BabelNet indices")

    doc_port = input(f"Port for documentation ([{DEFAULT_DOC_PORT}], -1 to ignore): ")
    if doc_port != "-1":
        doc_port = int(doc_port) if doc_port else DEFAULT_DOC_PORT
    else:
        doc_port = None

    if not_win:
        while True:
            mode = input(f"RPC mode ([{MODE_TCP}]/{MODE_IPC}/{MODE_ALL}): ")
            if not mode:
                mode = MODE_TCP
            modes = mode_parser(mode.lower())
            if modes:
                break
            else:
                print("Invalid mode", mode)
    else:
        modes = mode_parser(MODE_TCP)

    if MODE_TCP in modes:
        tcp_port = input(f"Port for TCP mode ([{DEFAULT_TCP_PORT}]): ")
        tcp_port = int(tcp_port) if tcp_port else DEFAULT_TCP_PORT
    else:
        tcp_port = None

    if MODE_IPC in modes:
        ipc_path = ''
        while not ipc_path:
            ipc_path = input("IPC directory: ")
    else:
        ipc_path = None

    if print_only:
        print()
    start_server(bn_path, doc_port, tcp_port, ipc_path, print_only)


def start_server(bn_path: str, doc_port: int = None, tcp_port: int = None, ipc_path: str = None, print_only=False,
                 no_update=False):
    if ipc_path is not None:
        ipc_path = os.path.realpath(ipc_path)

    if print_only:
        cmd = f'docker run -d --name {DOCKER_NAME} '
        if doc_port is not None:
            cmd += f'-p {doc_port}:8000 '
        if tcp_port is not None:
            cmd += f'-p {tcp_port}:1234 '
        if ipc_path is not None:
            cmd += f'-v "{ipc_path}:/babelnet_ipc" '

        cmd += f'-v "{os.path.realpath(bn_path)}:/root/babelnet" {DOCKER_IMAGE}'
        print("To start the RPC server, run the following command:")
        print(cmd)
    else:
        from docker.errors import ImageNotFound, APIError
        import docker

        try:
            client = docker.from_env()
        except:
            print("Error while connecting to docker", file=sys.stderr)
            sys.exit(1)

        if no_update:
            try:
                client.images.get(DOCKER_IMAGE)
            except ImageNotFound:
                print("Warning: Image not found locally.", file=sys.stderr)
                print("Pulling docker image...")
                client.images.pull(DOCKER_IMAGE)
        else:
            try:
                print("Pulling docker image...")
                client.images.pull(DOCKER_IMAGE)
            except APIError:
                print("Error while pulling image, using the local one")
                try:
                    print("Puling local image...")
                    client.images.get(DOCKER_IMAGE)
                except ImageNotFound as e:
                    print("Error while pulling image", file=sys.stderr)
                    print(f"Error: {e}", file=sys.stderr)
                    sys.exit(1)

        stop_server(client, "Removing old server...")

        ports = {}
        volumes = [f"{os.path.realpath(bn_path)}:/root/babelnet"]

        if doc_port is not None:
            ports[8000] = doc_port
        if tcp_port is not None:
            ports[1234] = tcp_port
        if ipc_path is not None:
            os.makedirs(ipc_path, exist_ok=True)
            volumes.append(f"{ipc_path}:/babelnet_ipc")

        print("Starting server...")
        client.containers.run(DOCKER_IMAGE, ports=ports, volumes=volumes, name=DOCKER_NAME,
                              detach=True, auto_remove=False)
        print("Server started")

    if doc_port is not None:
        host = "localhost" if print_only else get_local_ip_address()
        print()
        print("BabelNet Python API documentation",
              "will be" if print_only else "is",
              f"available at http://{host}:{doc_port}")
    print()
    print_config(tcp_port, ipc_path)


def main(prog=None):
    if prog is None:
        prog = os.path.basename(sys.argv[0])
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd == 'start':
        interactive = len(sys.argv) == 2
        if interactive:
            start_server_interactive()
        else:
            not_win = not is_win()
            parser = argparse.ArgumentParser(prog=f"{prog} start", description='Starts the BabelNet RPC server')
            parser.add_argument('--bn', required=True, metavar='<path>', help='BabelNet indices path')
            parser.add_argument('--doc', metavar='<port>', type=int, default=DEFAULT_DOC_PORT,
                                help=f'port for documentation (default {DEFAULT_DOC_PORT})')
            parser.add_argument('--no-doc', action='store_true', help='Disable the documentation port')
            mode_args = {'default': MODE_TCP}
            if not_win:
                mode_args['choices'] = [MODE_TCP, MODE_IPC, MODE_ALL]
                mode_args['help'] = f'RPC mode (default {MODE_TCP})'
            else:
                mode_args['choices'] = [MODE_TCP]
                mode_args['help'] = argparse.SUPPRESS
            parser.add_argument('-m', '--mode', **mode_args)
            parser.add_argument('--tcp', metavar='<port>', default=DEFAULT_TCP_PORT, type=int,
                                help=f'port for TPC mode (default {DEFAULT_TCP_PORT})')
            if not_win:
                parser.add_argument('--ipc', metavar='<path>', help='IPC directory')
            parser.add_argument("--print", action='store_true', help='Print the command instead of executing it')
            parser.add_argument("--no-update", action='store_true', default=False,
                                help='Disables the pull of the docker image')

            args = parser.parse_args(sys.argv[2:])
            modes = mode_parser(args.mode)
            if MODE_IPC in modes and args.ipc is None:
                parser.error(f"--ipc required with mode '{args.mode}'.")

            try:
                check_bn(args.bn)
            except FileNotFoundError:
                parser.error(f"Invalid BabelNet path: {args.bn}")
            except ValueError:
                parser.error(f"{args.bn} does not contain BabelNet indices.")

            start_server(args.bn, None if args.no_doc else args.doc, args.tcp if MODE_TCP in modes else None,
                         args.ipc if MODE_IPC in modes else None, args.print, args.no_update)
    elif cmd == 'stop':
        import docker

        parser = argparse.ArgumentParser(prog=f"{prog} stop", description='Stops the BabelNet RPC server')
        parser.parse_args(sys.argv[2:])

        client = docker.from_env()
        if stop_server(client, "Stopping server..."):
            print("Server stopped")
        else:
            print("No running server")
    else:
        print(f'''usage: {prog} <command> [<args>]

Controls the BabelNet RCP server in Docker 

commands:
  start             start the server
  stop              stop the server
    ''')
