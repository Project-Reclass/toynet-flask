# This file is part of Toynet-Flask.
#
# Toynet-Flask is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Toynet-Flask is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toynet-Flask.  If not, see <https://www.gnu.org/licenses/>.

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
