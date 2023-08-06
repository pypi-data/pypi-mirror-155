# This file is part of the python-structures library.
# Copyright (c) 2022 Piotr Żarczyński

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
A small package for creating and manipulating structs similar to those in C/C++
"""

from __future__ import annotations

__author__ = "Piotr Żarczyński"

__version__ = "0.1.1"

import typing
import types

from typing import ClassVar, Any, Type


class _Struct:
    def __getattribute__(self, attrib) -> ClassVar[Any]:
        _attrib = super().__getattribute__(attrib)
        if isinstance(_attrib, type):
            raise NotImplementedError("Struct attribute hasn't been initialized yet")
        else:
            return _attrib


def struct(_cls: Type[_T]) -> Type[_T]:
    fields = vars(_cls)["__annotations__"]
    _struct = types.new_class(_cls.__name__, (_Struct, _cls))
    for field, val in fields.items():
        setattr(_struct, field, eval(val))
    return _struct