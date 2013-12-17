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

import re
from SublimeLinter.lint import Linter


class PHP(Linter):

    """Provides an interface to php -l."""

    syntax = ('php', 'html', 'html 5')
    cmd = 'php -l -n -d display_errors=On -d log_errors=Off'
    regex = (
        r'^Parse (?P<error>error):\s*(?P<type>parse|syntax) error,?\s*'
        r'(?P<message>.+?) in - on line (?P<line>\d+)$'
    )

    def split_match(self, match):
        """Return the components of the error."""
        match, line, col, error, warning, message, near = super().split_match(match)

        # Find 'near' to better mark the location of the error
        m = re.search(r"unexpected '(?P<near>.+)'", message)
        if m:
            near = m.group('near')

        return match, line, col, error, warning, message, near
