# -*- coding: utf-8 -*-
"""
    ext
    ~~~~~~~~~
    Borrowed very liberally from flask.ext

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""


def setup():
    from ..exthook import ExtensionImporter  # pylint: disable=import-outside-toplevel,cyclic-import

    importer = ExtensionImporter(["datarobot_%s"], __name__)
    importer.install()


setup()
del setup
