"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
import os
import sys
from io import IOBase
from paramiko import SSHClient, AutoAddPolicy
from .tool import log
from configparser import ConfigParser, ExtendedInterpolation
from typing import Union, Type
from .base import AbstractCommandExecutor, ExecuteResult


def is_posix():
    try:
        import posix
        return True
    except Exception:
        return False


logger = log(__name__)


class BaseSCError(Exception):
    """BaseServerClientError"""
    pass


class ExecuteCommandError(BaseSCError):
    pass


class RemoteShell(AbstractCommandExecutor):

    def __init__(self, server: str, user: str, port=22, password=None, exec_result=None):
        self.exec_result: Union[Type[ExecuteResult]] = exec_result
        self.server = server
        self.port = port
        self.user = user
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())  # no known_hosts error
        if is_posix():
            client.load_system_host_keys()
        client.connect(self.server, username=self.user, port=self.port, password=password)
        self.client = client

    def _execute(self, command:str):
        stdin, stdout, stderr = self.client.exec_command(command)
        return (stdin, stdout, stderr)

    def get_sftp(self):
        return self._get_sftp()

    def _get_sftp(self):
        return self.client.open_sftp()

    def get_file(self, remotepath, localpath):

        def progress(count, total, status=f' File {self.server}:{remotepath} download.'):
            bar_len = 60
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
            sys.stdout.flush()

        sftp = self._get_sftp()
        sftp.get(remotepath, os.path.join(localpath), callback=progress)
        logger.info(f"File {localpath} is downloaded from {self.server}:{remotepath}")

    def put_file(self, localpath: Union[str, IOBase], remotepath ):

        def progress(count, total, status=f' File {localpath} upload.'):
            bar_len = 60
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
            sys.stdout.flush()
        sftp = self._get_sftp()

        if isinstance(localpath, IOBase):
            file_object: IOBase = localpath
            sftp.putfo(file_object, remotepath)
        else:
            sftp.put(localpath, remotepath, callback=progress)
        logger.info(f"File {localpath} is uploaded into {self.server}:{remotepath}")

    def exec_command(self, command: str):
        stdin, stdout, stderr = self._execute(command)
        return_code = stdout.channel.recv_exit_status()
        return self.exec_result(stdin, stdout, stderr, return_code, command)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class RemoteServer:

    def __init__(self, server:str, user:str, port:int=22, exec_result=None, password=None,
                 pkey=None, verbose=False):
        self.verbose = verbose
        self.exec_result: Union[Type[ExecuteResult]] = exec_result
        self._shell = RemoteShell(server, user, port=port, password=password, exec_result=exec_result)
        if self.verbose:
            logger.info(f"Ok connected to server {server}:{port}")

    def monitor_server(self):
        """https://github.com/afaqurk/linux-dash"""
        pass

    def free(self):
        return self.shell("free -h")

    def shell(self, command: str):
        exec_result = self._shell.exec_command(command)
        return exec_result

    def struct_shell(self, command: str):
        exec_result = self._shell.exec_command(command)
        if not exec_result:
            raise ExecuteCommandError(
                f"Command {command} completed with error. return_code {exec_result.return_code}")
        return exec_result

    def command(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def cmd(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def execute_command(self, *args, **kwargs):
        return self.shell(*args, **kwargs)

    def put_file(self, local_path, remote_path):
        self._shell.put_file(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self._shell.get_file(remote_path, local_path)

    def get_sftp(self):
        return self._shell.get_sftp()

    def mkdir(self, path, parents=False):
        if parents:
            return self._shell.exec_command(f"mkdir -p {path}")
        else:
            return self._shell.exec_command(f"mkdir {path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connect()

    def close_connect(self):
        self._shell.client.close()
        if self.verbose:
            logger.info(f"Connect closed the server {self._shell.server}:{self._shell.port}")


class Config:

    class Field:
        def __init__(self, dictionary: dict):
            for k, v in dictionary.items():
                setattr(self, k, v)

    def __init__(self, *args, **kwargs):
        pass

    def read(self, path):
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(path)

        my_config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
        for key in my_config_parser_dict:
            val = my_config_parser_dict[key]
            fields = Config.Field(val)
            setattr(self, key, fields)
