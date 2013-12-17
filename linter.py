#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Ryan Hileman, Aparajita Fishman and Anthony Pidden
# Copyright (c) 2013 Ryan Hileman, Aparajita Fishman and Anthony Pidden
#
# License: MIT
#

"""This module exports the PHP plugin class."""

from SublimeLinter.lint import Linter


class PHP(Linter):

    """Provides an interface to php -l."""

    syntax = ('php', 'html', 'html 5')
    cmd = 'php -l -n -d display_errors=On -d log_errors=Off'
    regex = (
        r'^Parse (?P<error>error):\s*(?P<type>parse|syntax) error,?\s*'
        r'(?P<message>.+?((?:\')(?P<near>[^\']+)(?:\'.+))) in - on line (?P<line>\d+)$'
    )
