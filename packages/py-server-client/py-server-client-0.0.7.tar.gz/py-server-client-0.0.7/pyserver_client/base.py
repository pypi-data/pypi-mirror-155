"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from abc import ABCMeta, abstractmethod
from jinja2 import Template
import os
import re

DEFAULT_TEMPLATE = """
{% set runcmd = Self.color.WHITE + '[ Run command ] ' + Self.color.COMMAND + Self.command + " " + Self.color.END %}
{% set stdout = Self.color.OKGREEN + '[ STDOUT ]' + Self.color.END %}
{% set stderr = Self.color.RED + '[ STDERR ]' + Self.color.END %}
{% set result = Self.color.OKCYAN + '[ Result ] ' + Self.color.COMMAND + Self.result.command + Self.color.END + Self.color.OKGREEN + " return_code " + Self.result.return_code|string + Self.color.END %}
{{runcmd}}
{% if stdout_rows %}{{stdout}}{{'-' * (Self.terminal_columns - stdout|length)}}\n{% endif %}
{% for line in stdout_rows -%}{{line}}{% endfor %}
{% if stderr_rows %}{{stderr}}{{'-' * (Self.terminal_columns - stderr|length)}}\n{% endif %}
{% for line in stderr_rows -%}{{line}}{% endfor %}
{{result}}
""".strip()

class BaseExecuteResult:

    @abstractmethod
    def __init__(self, stdin, stdout, stderr, return_code: int, command: str):
        pass

    @abstractmethod
    def __bool__(self):
        pass


class AbstractResponse(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def return_code(self) -> int:
        pass

    @abstractmethod
    def __bool__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def pprint(self):
        pass


class AbstractCommandExecutor(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _execute(self, command: str):
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class ExecuteResult(BaseExecuteResult):

    def __init__(self, stdin, stdout, stderr, return_code: int, command: str):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self._return_code = return_code
        self.command = command

    @property
    def return_code(self):
        return self._return_code

    def __bool__(self):
        return self._return_code == 0

class ResultPresentation:
    class color:
        """https://habr.com/ru/company/macloud/blog/558316/
        """
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        END = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        RED = '\033[31m'
        WHITE = '\033[37m'
        COMMAND = '\033[2;34m'

    def __init__(self, result: ExecuteResult):
        self.result = result
        self.stdout_rows = [x for x in self.result.stdout]
        self.stderr_rows = [x for x in self.result.stderr]
        self.command = self.result.command

        self.rows = []
        self.rows.extend(self.stdout_rows)
        self.rows.extend(self.stderr_rows)

        # terminal
        self.terminal_columns = 120
        self.terminal_lines = 10
        try:
            self.ts = os.get_terminal_size()
            self.terminal_columns = self.ts.columns
            self.terminal_lines = self.ts.lines
        except OSError:
            pass

    def __str__(self):
        jinja_template = Template(DEFAULT_TEMPLATE, trim_blocks=True)
        string = jinja_template.render(Self=self,
                                       stdout_rows=self.stdout_rows,
                                       stderr_rows=self.stderr_rows)
        string = re.sub(r"\n{1,}", "\n", string)
        return string
