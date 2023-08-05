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
import unittest

from logilab.common.testlib import TestCase

import locale
from io import BytesIO
from logilab.mtconverter import (
    xml_escape,
    html_unescape,
    guess_encoding,
    DEFAULT_ENCODING,
    guess_mimetype_and_encoding,
    TransformData,
)

SPECIAL_CHARS = {
    "\f": "\n",
    "\b": " ",
    "\n": "\n",
    "\r": "\r",
    "\r\n": "\r\n",
    "\t": "\t",
    "\v": "\n",
}


class HtmlEscapeTC(TestCase):
    def test_escape(self):
        for data, expected in [
            ("toto", "toto"),
            ("r&d", "r&amp;d"),
            ("23<12 && 3>2", "23&lt;12 &amp;&amp; 3&gt;2"),
            ('d"h"', "d&quot;h&quot;"),
            ("h'", "h&#39;"),
        ]:
            yield self.assertEqual, xml_escape(data), expected

    def test_escape_special_chars(self):
        for car, trcar in SPECIAL_CHARS.items():
            yield self.assertEqual, xml_escape(car), trcar
        for carnum in range(32):
            car = chr(carnum)
            if car in SPECIAL_CHARS:
                continue
            yield self.assertEqual, xml_escape(car), " "
        yield self.assertEqual, xml_escape("é"), "é"

    def test_escape_special_chars_unicode(self):
        for car, trcar in SPECIAL_CHARS.items():
            yield self.assertEqual, xml_escape(car), trcar
        for carnum in range(32):
            car = chr(carnum)
            if car in SPECIAL_CHARS:
                continue
            yield self.assertEqual, xml_escape(car), " "

    def test_html_unescape(self):
        for data, expected in [
            ("toto", "toto"),
            ("r&amp;d", "r&d"),
            ("23&lt;12 &amp;&amp; 3&gt;2", "23<12 && 3>2"),
            ("d&quot;h&quot;", 'd"h"'),
            ("h&#39;", "h'"),
            ("x &equiv; y", "x \u2261 y"),
        ]:
            yield self.assertEqual, html_unescape(data), expected


class GuessEncodingTC(TestCase):
    def test_emacs_style_declaration(self):
        data = b"""# -*- coding: latin1 -*-"""
        self.assertEqual(guess_encoding(data), "latin1")

    def test_emacs_style_declaration_stringIO(self):
        data = b"""# -*- coding: latin1 -*-"""
        self.assertEqual(guess_encoding(BytesIO(data)), "latin1")

    def test_xml_style_declaration(self):
        data = b"""<?xml version="1.0" encoding="latin1"?>
        <root/>"""
        self.assertEqual(guess_encoding(data), "latin1")

    def test_html_style_declaration(self):
        data = b"""\
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:erudi="http://www.logilab.fr/" xml:lang="fr" \
lang="fr">
<head>
<base href="http://intranet.logilab.fr/jpl/" />\
<meta http-equiv="content-type" content="text/html; charset=latin1"/>
</head>
<body><p>hello world</p>
</body>
</html>"""
        self.assertEqual(guess_encoding(data), "latin1")

    def test_bad_detection(self):
        data = b'''class SchemaViewer(object):
    """return an ureport layout for some part of a schema"""
    def __init__(self, req=None, encoding=None):
'''
        # ascii detected by chardet
        try:
            import chardet  # noqa

            self.assertEqual(guess_encoding(data), "ascii")
        except ImportError:
            self.assertEqual(guess_encoding(data), DEFAULT_ENCODING)


class GuessMimetymeAndEncodingTC(TestCase):
    def test_base(self):
        format, encoding = guess_mimetype_and_encoding(filename="foo.txt", data=b"xxx")
        self.assertEqual(format, "text/plain")
        self.assertEqual(encoding, locale.getpreferredencoding())

    def test_set_mime_and_encoding_gz_file(self):
        format, encoding = guess_mimetype_and_encoding(
            filename="foo.txt.gz", data=b"xxx"
        )
        self.assertEqual(format, "text/plain")
        self.assertEqual(encoding, "gzip")
        format, encoding = guess_mimetype_and_encoding(
            filename="foo.txt.gz", data=b"xxx", format="application/gzip"
        )
        self.assertEqual(format, "text/plain")
        self.assertEqual(encoding, "gzip")
        format, encoding = guess_mimetype_and_encoding(filename="foo.gz", data=b"xxx")
        self.assertEqual(format, "application/gzip")
        self.assertEqual(encoding, None)

    def test_set_mime_and_encoding_bz2_file(self):
        format, encoding = guess_mimetype_and_encoding(
            filename="foo.txt.bz2", data=b"xxx"
        )
        self.assertEqual(format, "text/plain")
        self.assertEqual(encoding, "bzip2")
        format, encoding = guess_mimetype_and_encoding(
            filename="foo.txt.bz2", data=b"xxx", format="application/bzip2"
        )
        self.assertEqual(format, "text/plain")
        self.assertEqual(encoding, "bzip2")
        format, encoding = guess_mimetype_and_encoding(filename="foo.bz2", data=b"xxx")
        self.assertEqual(format, "application/bzip2")
        self.assertEqual(encoding, None)

    def test_set_mime_and_encoding_unknwon_ext(self):
        format, encoding = guess_mimetype_and_encoding(filename="foo.789", data=b"xxx")
        self.assertEqual(format, "application/octet-stream")
        self.assertEqual(encoding, None)


class TransformDataTC(TestCase):
    def test_autodetect_encoding_if_necessary(self):
        data = TransformData(
            b"""<?xml version="1.0" encoding="latin1"?>
        <root/>""",
            "text/xml",
        )
        self.assertEqual(data.encoding, "latin1")


if __name__ == "__main__":
    unittest.main()
