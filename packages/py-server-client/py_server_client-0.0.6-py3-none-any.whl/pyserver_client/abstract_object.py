"""
Copyright (c) 2022 Plugin Andrey (9keepa@gmail.com)
Licensed under the MIT License
"""
from abc import ABCMeta, abstractmethod


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


class AbstractShell(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass


