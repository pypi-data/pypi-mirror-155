# copyright 2006-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-mtconverter.
#
# logilab-mtconverter is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-mtconverter is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-mtconverter. If not, see <http://www.gnu.org/licenses/>.
"""base transformation objects"""

from typing import Sequence, Optional
from typing import Any
from logilab.mtconverter import TransformData
from typing import Tuple

__docformat__: str = "restructuredtext en"


class Transform:
    """a transform is converting some content in a acceptable MIME type
    into another MIME type
    """

    name: Optional[str] = None
    inputs: Sequence[str] = []
    output: Optional[str] = None
    input_encoding: Optional[str] = None
    output_encoding: Optional[str] = None

    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)
        if not getattr(self, "name", None):
            self.name: str = self.__class__.__name__

    def convert(self, trdata: TransformData) -> TransformData:
        """convert the given data structure into transform output's mime type

        :param trdata: `TransformData`
        :rtype: `TransformData`
        """
        # this is not true when transform accept wildcard
        # assert trdata.mimetype in self.inputs
        assert self.output is not None
        trdata.data = self._convert(trdata)
        trdata.mimetype = self.output
        if self.output_encoding:
            trdata.encoding = self.output_encoding
        return trdata

    def _convert(self, trdata: TransformData) -> Any:
        raise NotImplementedError


class TransformsChain(list):
    """A chain of transforms used to transform data"""

    inputs: Tuple[str, ...] = ("application/octet-stream",)
    output: str = "application/octet-stream"
    name: Optional[str] = None

    def __init__(self, name: str = None, *args: Any) -> None:
        list.__init__(self, *args)
        if name is not None:
            self.name = name
        if args:
            self._update()

    def convert(self, trdata: TransformData) -> TransformData:
        for transform in self:
            trdata = transform.convert(trdata)
        return trdata

    def __setitem__(self, key, value) -> None:  # type: ignore[no-untyped-def] # use Protocol?
        list.__setitem__(self, key, value)
        self._update()

    def append(self, value) -> None:  # type: ignore[no-untyped-def] # FIXME: is value a Transform?
        list.append(self, value)
        self._update()

    def insert(self, *args) -> None:  # type: ignore[no-untyped-def] # FIXME: function still used?
        list.insert(*args)
        self._update()

    def remove(self, *args) -> None:  # type: ignore[no-untyped-def] # FIXME: function still used?
        list.remove(*args)
        self._update()

    def pop(self, *args) -> None:  # type: ignore[no-untyped-def] # FIXME: function still used?
        list.pop(*args)
        self._update()

    def _update(self) -> None:
        self.inputs = self[0].inputs
        self.output = self[-1].output
        for i in range(len(self)):
            if hasattr(self[-i - 1], "output_encoding"):
                self.output_encoding = self[-i - 1].output_encoding
                break
        else:
            try:
                del self.output_encoding
            except Exception:
                pass
