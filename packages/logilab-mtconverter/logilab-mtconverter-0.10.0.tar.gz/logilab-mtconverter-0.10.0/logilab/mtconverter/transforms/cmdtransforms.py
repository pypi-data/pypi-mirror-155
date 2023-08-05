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
import os
from tempfile import mkstemp
import subprocess
from typing import Optional, List, Tuple, Any

from logilab.mtconverter import MissingBinary
from logilab.mtconverter.transform import Transform
from logilab.mtconverter import TransformData

bin_search_path: List[str] = [
    path for path in os.environ["PATH"].split(os.pathsep) if os.path.isdir(path)
]


def bin_search(binary: Optional[str]) -> str:
    """search the bin_search_path for a given binary returning its fullname or
    raises MissingBinary"""
    mode = os.R_OK | os.X_OK
    for path in bin_search_path:
        assert binary is not None
        pathbin = os.path.join(path, binary)
        if os.access(pathbin, mode) == 1:
            return pathbin
            break
    raise MissingBinary(
        'Unable to find binary "%s" in %s' % (binary, os.pathsep.join(bin_search_path))
    )


class POpenTransform(Transform):
    """abstract class for external command based transform

    The external command may read from stdin but must write to stdout
    If use_stdin is False, a temporary file will be used as input for
    the command
    """

    cmdname: Optional[str] = None
    cmdargs: str = ""
    use_stdin: bool = True
    input_encoding: Optional[str] = None
    # output_encoding = 'utf-8'

    def __init__(
        self,
        name: str = None,
        binary: str = None,
        cmdargs: str = None,
        use_stdin: bool = None,
        **kwargs: Any,
    ) -> None:
        if name is not None:
            self.name = name
        if binary is not None:
            self.binary = bin_search(binary)
        else:
            self.binary = bin_search(self.cmdname)
        if cmdargs is not None:
            self.cmdargs = cmdargs
        if use_stdin is not None:
            self.use_stdin = use_stdin

    def _command_line(self, trdata: TransformData) -> str:
        return "%s %s" % (self.binary, self.cmdargs)

    def _convert(self, trdata: TransformData) -> bytes:
        command = self._command_line(trdata)
        data: Optional[bytes] = trdata.encode(self.input_encoding)
        if not self.use_stdin:
            tmpfile, tmpname = mkstemp(text=False)  # create tmp
            assert data is not None
            os.write(tmpfile, data)  # write data to tmp using a file descriptor
            os.close(tmpfile)  # close it so the other process can read it
            command = command % {"infile": tmpname}  # apply tmp name to command
            data = None
        cmd = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True,
        )
        out, _ = cmd.communicate(data)
        if not self.use_stdin:
            # remove tmp file
            os.unlink(tmpname)
        return out.strip()


class pdf_to_text(POpenTransform):
    name: str = "pdf_to_text"
    inputs: Tuple[str, ...] = ("application/pdf",)
    output: str = "text/plain"
    output_encoding: str = "utf-8"

    cmdname: str = "pdftotext"
    cmdargs: str = "%(infile)s -enc UTF-8 -"
    use_stdin: bool = False


class lynx_dump(POpenTransform):
    name: str = "lynx_dump"
    inputs: Tuple[str, ...] = ("text/html", "text/xhtml")
    output: str = "text/plain"

    cmdname: str = "lynx"
    cmdargs: str = "-dump -stdin"
    use_stdin: bool = True

    def _command_line(self, trdata: TransformData) -> str:
        encoding = trdata.encoding
        if encoding == "ascii":
            encoding = "iso-8859-1"  # lynx doesn't know ascii !
        return "%s %s -assume_charset=%s -display_charset=%s" % (
            self.binary,
            self.cmdargs,
            encoding,
            encoding,
        )


transform_classes = [pdf_to_text]  # , lynx_dump]
