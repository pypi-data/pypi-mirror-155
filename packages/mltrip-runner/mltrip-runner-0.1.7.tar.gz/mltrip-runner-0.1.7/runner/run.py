import argparse
import logging
import time
import os
import socket
import sys
import getpass
from pathlib import Path


from runner import factory
from runner.load import load


def set_logging(metadata):
    filename = metadata['log_path']
    level = metadata['log_level']
    filemode = 'a'
    datefmt = '%Y-%m-%dT%H:%M:%S'
    fmt = '%(asctime)s.%(msecs)03d%(tz)s|' \
          '%(hostname)s|%(ip)s|%(user)s|%(process)d|' \
          '%(levelname)s|%(filename)s|%(lineno)d|%(message)s'
    fmt = fmt.replace('%(hostname)s', socket.gethostname())
    fmt = fmt.replace('%(ip)s', socket.gethostbyname(socket.gethostname()))
    fmt = fmt.replace('%(user)s', getpass.getuser())
    fmt = fmt.replace('%(tz)s', time.strftime('%z'))
    # Workaround
    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    logging.basicConfig(filename=filename, filemode=filemode, format=fmt,
                        datefmt=datefmt, level=level)
    logging.info('Logging initialized')
    logging.info(f'hostname: {socket.getfqdn()}')
    logging.info(f'ip: {socket.gethostbyname(socket.getfqdn())}')
    logging.info(f'user: {getpass.getuser()}')
    logging.info(f'pid: {os.getpid()}')
    logging.info(f'python: {sys.executable}')
    logging.info(f'script: {__file__}')
    logging.info(f'working directory: {os.getcwd()}')
    logging.info(f'input path: {metadata["input_path"]}')
    logging.info(f'log path: {metadata["log_path"]}')
    logging.info(f'log level: {metadata["log_level"]}')


def initialize(data, fct):
    if isinstance(data, dict):
        for k, v in data.items():
            if k != 'class':
                data[k] = initialize(v, fct)
        try:
            data = fct(data)
        except factory.FactoryValueError as e:
            logging.debug(e)
        except factory.FactoryKeyError as e:
            logging.debug(e)
        except factory.FactoryClassError as e:
            logging.debug(e)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            data[i] = initialize(v, fct)
    elif isinstance(data, str) and data.startswith('/'):
        p = Path(data[1:]).resolve()
        d = load(p)
        data = initialize(d['data'], fct)
    return data


def parse_input():
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='input path')
    parser.add_argument('-l', '--log_path', help='log file path',
                        default=argparse.SUPPRESS)
    parser.add_argument('-v', '--log_level', default=argparse.SUPPRESS,
                        choices=['CRITICAL', 'FATAL', 'ERROR', 'WARNING',
                                 'WARN', 'INFO', 'DEBUG', 'NOTSET'])
    a = vars(parser.parse_known_args()[0])  # arguments
    # Get input
    p = Path(a['input_path']).resolve()
    i = load(p)
    # Update input metadata by arguments
    i.setdefault('data', {})
    i.setdefault('metadata', {})
    i['metadata'].update(a)
    i['metadata'].setdefault('log_path', p.with_suffix('.log'))
    i['metadata'].setdefault('log_level', 'INFO')
    return i


def main():
    i = parse_input()
    set_logging(i['metadata'])
    logging.info(f'input: {i}')
    action = initialize(i['data'], factory.Factory())
    action()


if __name__ == '__main__':
    main()
