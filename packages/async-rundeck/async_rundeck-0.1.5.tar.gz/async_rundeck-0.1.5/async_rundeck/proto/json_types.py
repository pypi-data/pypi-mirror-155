import json
from typing import TypeVar, NewType, NewType

T = TypeVar("T")

Number = float
String = str
Boolean = bool
Integer = int
Object = dict
File = NewType("File", bytes)

__all__ = ["Number", "String", "Boolean", "Integer", "Object", "File"]
