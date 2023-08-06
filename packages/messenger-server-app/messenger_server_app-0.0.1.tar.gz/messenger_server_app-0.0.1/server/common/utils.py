import imp
import json
import sys
import argparse
from common.decorators import log
from common.config import (USER_TEST, ENCODING, MAX_PACKAGE_LENGTH,
                           DEFAULT_IP_ADDRESS, DEFAULT_PORT)


@log
def create_parser(logger, default_port=DEFAULT_PORT, default_address=DEFAULT_IP_ADDRESS):
    parser = argparse.ArgumentParser()
    parser_group = parser.add_argument_group(title='Parameters')

    parser_group.add_argument('-n', '--name',
                              default='', help='TCP port')
    parser_group.add_argument('-s', '--password', default='', nargs='?')
    parser_group.add_argument('--no_gui', action='store_true')

    if sys.argv[0] == 'server.py':
        parser_group.add_argument('-a', '--addr',
                                  default=default_address, help='IP address')
        parser_group.add_argument('-p', '--port', type=int,
                                  default=default_port, help='TCP port')
    elif sys.argv[0] == 'client.py':
        parser_group.add_argument(
            'addr', default=default_address, nargs='?')
        parser_group.add_argument(
            'port', default=default_port, type=int, nargs='?')
    else:
        print('create_parser() improper use')
        sys.exit(1)

    namespace = parser.parse_args()
    listen_address = namespace.addr
    listen_port = namespace.port
    name = namespace.name
    password = namespace.password
    gui_flag = namespace.no_gui

    if not 1023 < listen_port < 65536:
        logger.critical(
            'The port must be specified in the range from 1024 to 65535')
        sys.exit(1)

    return listen_address, listen_port, name, password, gui_flag


@log
def send_message(opened_socket, message):
    json_message = json.dumps(message)
    response = json_message.encode(ENCODING)
    opened_socket.send(response)


@log
def get_message(opened_socket):
    response = opened_socket.recv(MAX_PACKAGE_LENGTH)
    if isinstance(response, bytes):
        json_response = response.decode(ENCODING)
        response_dict = json.loads(json_response)
        if isinstance(response_dict, dict):
            return response_dict
        raise ValueError
    raise ValueError


if __name__ == '__main__':
    parser = create_parser()
    argv = parser.parse_args()
    print(argv.addr, argv.port)
