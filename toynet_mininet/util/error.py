from typing import Any

class UtilError(Exception):
    '''Base class for Exceptions produced by utility functions'''

class TypeCheckError(UtilError):
    '''Base class for Exceptions produced by utility functions

    Attributes
        message:    str -- explanation of the error
    '''

    def __init__(self, input: Any, message: str):
        self.input: Any = input
        self.message: str = message

class XMLParseError(Exception):
    '''Exception raised for errors parsing a network configuration file

    Attributes
        message:    str -- explanation of the error
    '''

    def __init__(self, msg: str):
        self.message = msg

class XMLFileParseError(XMLParseError):
    '''Exception raised for errors parsing a network configuration from XML file

    Attributes
        message:    str -- explanation of the error
        filename:   str -- file being parsed when error occured
    '''

    def __init__(self, msg: str, filename: str):
        self.message = msg + ' (File: ' + filename + ')'

class XMLStringParseError(XMLParseError):
    '''Exception raised for errors parsing a netowrk configuration from a string representing an XML configuration

    Attributes
        message:    str -- explanation of the error
        content:    str -- XML content being parsed when error occured
    '''

    def __init__(self, msg: str, content: str):
        self.message = msg + ' (Contents: ' + content + ')'
