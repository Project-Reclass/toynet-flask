from typing import Any
from .error import TypeCheckError


def inputTypeCheck(inputParam: Any, paramName: str, expectedType: type):
    if type(inputParam) != expectedType:
        raise TypeCheckError(
            inputParam,
            paramName + ' should be ' + str(expectedType) + ' but is: ' + str(type(inputParam))
        )
