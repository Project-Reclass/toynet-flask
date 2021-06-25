from typing import Any

class UtilError(Exception):
    """Base class for Exceptions produced by utility functions"""

class TypeCheckError(UtilError):
    """Base class for Exceptions produced by utility functions

    Attributes
        message:    str -- explanation of the error
    """

    def __init__(self, input: Any, message: str):
        self.input: Any = input
        self.message: str = message

class XMLParseError(Exception):
    """Exception raised for errors parsing a network configuration from XML file

    Attributes
        message:    str -- explanation of the error
        filename:   str -- file being parsed when error occured
    """

    def __init__(self, msg: str, filename: str):
        self.message = msg + ' (File: ' + filename + ')'
