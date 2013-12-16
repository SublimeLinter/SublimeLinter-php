#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Ryan Hileman and Aparajita Fishman
# Copyright (c) 2013 Ryan Hileman and Aparajita Fishman
#
# License: MIT
#

"""This module exports the PHP plugin class."""

from SublimeLinter.lint import Linter


class PHP(Linter):

    """Provides an interface to php -l."""

    syntax = ('php', 'html')
    cmd = 'php -l -n -d display_errors=On -d log_errors=Off'
    regex = r'^Parse error:\s*(?P<type>parse|syntax) error,?\s*(?P<message>.+?)?\s+in - on line (?P<line>\d+)'
    selectors = {
        'html': 'source.php.embedded.block.html'
    }

    def split_match(self, match):
        """Return the components of the error."""
        match, line, col, error, warning, message, near = super().split_match(match)

        # message might be empty, we have to supply a value
        if match and match.group('type') == 'parse' and not message:
            message = 'parse error'

        return match, line, col, error, warning, message, near
