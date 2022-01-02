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
from .error import TypeCheckError


def inputTypeCheck(inputParam: Any, paramName: str, expectedType: type):
    if type(inputParam) != expectedType:
        raise TypeCheckError(
            inputParam,
            paramName + ' should be ' + str(expectedType) + ' but is: ' + str(type(inputParam))
        )
